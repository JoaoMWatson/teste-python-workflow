import json
import logging

import requests
from dotenv import dotenv_values

logger = logging.getLogger('root')
config = dotenv_values("../../.env")

LEANIX_API_TOKEN = config["LEANIX_API_TOKEN"]
LEANIX_SUBDOMAIN = config["LEANIX_SUBDOMAIN"]
LEANIX_GRAPHQL_URL = (
    f"https://{LEANIX_SUBDOMAIN}.leanix.net/services/pathfinder/v1/graphql"
)
LEANIX_OAUTH2_URL = (
    f"https://{LEANIX_SUBDOMAIN}.leanix.net/services/mtm/v1/oauth2/token"
)


def _obtain_access_token() -> str:
    """Obtains a LeanIX Access token using the Technical User generated
    API secret.

    Returns:
        str: The LeanIX Access Token
    """
    if not LEANIX_API_TOKEN:
        logging.error("LeanIX key not configured")
        raise Exception("A valid token is required")

    response = requests.post(
        LEANIX_OAUTH2_URL,
        auth=("apitoken", LEANIX_API_TOKEN),
        data={"grant_type": "client_credentials"},
    )

    response.raise_for_status()
    response_payload = response.json()

    logging.info("OATH2 retrieved")
    return response_payload["access_token"]


def check_application_exists_by_name(application_name) -> bool:
    """Executes a query against the LeanIX GraphQL API and prints
    the output.
    """
    access_token = _obtain_access_token()
    graphql_query = """{
        allFactSheets(filter: {displayName: "%s"}) {
        edges {
            node {
                id
                name
                displayName
                createdAt
                updatedAt
                }
            }
        }
    }
    """ % (application_name)

    data = {"query": graphql_query}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(
        url=LEANIX_GRAPHQL_URL,
        headers={"Authorization": headers},
        data=json.dumps(data),
    )

    response.raise_for_status()

    response_payload = response.json()

    if response_payload["data"]["allFactSheets"]["edges"]:
        logging.info(
            f"Application check in LeanIX catalog. Application name: {application_name}"
        )
        return True

    logging.warning(
        f"Application does not exists in LeanIX. Application name: {application_name}"
    )
    return False

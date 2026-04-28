import json
import logging

import requests
from dotenv import dotenv_values


logger = logging.getLogger('root')
config = dotenv_values("../../.env")

CONFLUENT_ENDPOINT = config["CONFLUENT_ENDPOINT"]
CONFLUENT_API_KEY = config["CONFLUENT_API_KEY"]

headers = {
            "content-type": "application/json",
            "Authorization": f"Basic {CONFLUENT_API_KEY}",
        }

def check_service_account_exists(
    application_name: str,
) -> bool:
    """Check if service-account exists within given name

    arguments:
    application_name -- Name for the application returned from forms
    """
    try:
        url = f"{CONFLUENT_ENDPOINT}/iam/v2/service-accounts?display_name={application_name}"
        
        response = requests.get(url, headers=headers)
        response_payload = response.json()

        if response_payload["data"]:
            logging.warning(
                "Service account already exists, please check and try later"
            )
            return True

        return False

    except requests.ConnectionError as e:
        logging.error("Fail connect to confluent api")
        print(f"Connection Error, {e.__traceback__}")
    except json.JSONDecodeError as e:
        print(f"Decode error, {e.__traceback__}")


def create_service_account(display_name: str, description: str) -> str:
    """Create service account using confluent api endpoint

    Args:
        display_name (str): Name that shows on confluent platform for service accounts.
            Format: sa-<domínio|jornada>-<nome-aplicação>-<env>
        description (str): Short description that shows on confluent platform for service account.
            Format: app: <nome-aplicacao> | domain: <dominio> | owner: <time/owner>

    Returns:
        str: Service account id. Format: 'sa-xpto123'
    """

    try:
        url = f"{CONFLUENT_ENDPOINT}/iam/v2/service-accounts"

        payload = {"display_name": display_name, "description": description}

        response = requests.post(url=url, data=json.dumps(payload), headers=headers)

        response.raise_for_status()
        response_payload = response.json()["metadata"]["resource_name"]

        service_account_id = response_payload[38:]
        logging.info("Service account created:", service_account_id)

        return service_account_id

    except requests.ConnectionError as e:
        logging.error("Connection error")
        print(f"Connection Error, {e.__traceback__}")


def create_api_key(
    service_account: str, resource: str, display_name: str, description: str, env: str
):
    """Create an api key using confluent api endpoint

    Args:
        service_account (str): Service account id created previously
        resource (str): Resource that uses the api key, schema-registry, broker or cluster
        display_name (str): Name that shows on confluent platform for service accounts.
            Format: sa-<domínio|jornada>-<nome-aplicação>-<env>
        description (str): Short description that shows on confluent platform for service account.
            Format: app: <nome-aplicacao> | domain: <dominio> | owner: <time/owner>
        env (str): Environment on Confluent cloud

    Returns:
        Tuple: Object contain information about api key
    """
    try:
        url = f"{CONFLUENT_ENDPOINT}/iam/v2/api-keys"

        payload = {
            "spec": {
                "display_name": display_name,
                "description": description,
                "owner": {"id": service_account},
                "resource": {"id": resource, "environment": env},
            }
        }

        response = requests.post(url=url, data=json.dumps(payload), headers=headers)

        response.raise_for_status()
        response_payload = response.json()

        logging.info("Api key created:", response_payload["id"])

        return response_payload

    except requests.ConnectionError as e:
        logging.error("Connection error")
        print(f"Connection Error, {e.__traceback__}")
    except json.JSONDecodeError as e:
        print(f"Decode error, {e.__traceback__}")


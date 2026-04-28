from integration.confluent_integration import check_service_account_exists, create_api_key, create_service_account
from integration.leanix_integration import check_application_exists_by_name
from utils.get_environment_info import get_environment_info
from utils.validate_input import validate_input

import json

import logging

logger = logging.getLogger('root')


def send_api_key_sa(
    application_name: str, domain: str, squad: str, env: str
):
    """Return the confirmation and info about the service account and schema-registry

    Args:
        application_name (str): Application name registered inside leanix
        domain (str): Domain name
        squad (str): Squad responsible for the application
        env (str): Environment which user has requested the service-account

    Returns:
        Dict: Object contains service-account key and schema-registry key
    """
    try:
        if not check_application_exists_by_name(application_name):
            assert ValueError(f"Application does not exists in LeanIX. Application name: {application_name}")
            return None

        service_account_display_name = f"sa-{domain}-{application_name}-{env}"
        validate_input(service_account_display_name, [6, 64])

        if check_service_account_exists(service_account_display_name):
            return None

        description = f"app: {application_name} | domain: {domain} | owner: {squad}"
        environment_resources = get_environment_info(env)

        
        sr_display_name = f"sr-{domain}-{application_name}-{env}"
        validate_input(sr_display_name, [6, 64])

    
        api_display_name = f"apiKey-{domain}-{application_name}-{env}"
        validate_input(api_display_name, [6, 70])

        service_account_id = create_service_account(
            service_account_display_name, description
        )

        sr_api_key = create_api_key(
            service_account=service_account_id,
            resource=environment_resources["schema_registry_cluster"],
            env=environment_resources["broker"],
            display_name=sr_display_name,
            description=description,
        )

        api_key = create_api_key(
            service_account=service_account_id,
            resource=environment_resources["cluster"],
            env=environment_resources["broker"],
            display_name=api_display_name,
            description=description,
        )

        response_payload = {
            "schema-registry": {
                "key": sr_api_key["id"],
                "secret": sr_api_key["spec"]["secret"],
            },
            "confluent-kafka": {
                "key": api_key["id"],
                "secret": api_key["spec"]["secret"],
            },
        }

        return json.dumps(response_payload)

    except ValueError as e:
        logging.error(e)
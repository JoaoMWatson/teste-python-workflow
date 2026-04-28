import logging

from dotenv import dotenv_values

config = dotenv_values(".env.environments")
logger = logging.getLogger('root')


def get_environment_info(environment: str):
    environment_resources = {
        "cluster": "",
        "schema_registry_cluster": "",
        "broker": "",
    }

    if environment == "dev" or environment == "develop":
        environment_resources["cluster"] = config["DEV_CLUSTER"]
        environment_resources["schema_registry_cluster"] = config["DEV_SR_CLUSTER"]
        environment_resources["broker"] = config["DEV_BROKER"]

    if environment == "homolog" or environment == "homol":
        environment_resources["cluster"] = config["HML_CLUSTER"]
        environment_resources["schema_registry_cluster"] = config["HML_SR_CLUSTER"]
        environment_resources["broker"] = config["HML_BROKER"]

    if environment == "prod" or environment == "production":
        environment_resources["cluster"] = config["PROD_CLUSTER"]
        environment_resources["schema_registry_cluster"] = config["PROD_SR_CLUSTER"]
        environment_resources["broker"] = config["PROD_BROKER"]

    return environment_resources
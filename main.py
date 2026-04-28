# from src.service.service_account_service import send_api_key_sa

import json
import sys
import log


def main(payload):
    service = payload["service"]

    # if service == "create-service-account":
    #     response = send_api_key_sa(payload["application_name"], payload["domain"],
    #                     payload["squad"], payload["env"])
    # if service == "create-acl":
    #     pass
    # if service == "list-acl":
    #     pass
    response_payload = {
            "schema-registry": {
                "key": "SDOIFJSDIO123",
                "secret": "SAIUDAOISJisjdfis340434==0055teste",
            },
            "confluent-kafka": {
                "key": "SDOIFJSDIO123TESTE2",
                "secret": "SAIUDAOISJisjdfis340434==0055testeTESTE32",
            },
        }
    print(response_payload)
    

if __name__ == "__main__":
    logger = log.setup_custom_logger('root')
    logger.debug('main message')
    import submodule
    
    event_data = json.loads(sys.stdin.read())
    
    main(event_data["client_payload"])

import logging

logger = logging.getLogger('root')

def validate_input(input_string: str, desired_length_range: tuple) -> bool:

    is_valid_length = (
        desired_length_range[0] <= len(input_string) <= desired_length_range[1]
    )

    if is_valid_length:
        return True

    logging.error("String not valid, null or pass max length", input_string)
    raise ValueError("String not valid, please check and try again", input_string)

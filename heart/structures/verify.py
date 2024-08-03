from utils.apiMessages import LocalApiCode, error_message


def verify_json(
    json,
    requiredParameters=None,
    optionalParameters=None,
    errorCode=LocalApiCode.invalidJson,
):
    if requiredParameters is None:
        requiredParameters = []
    if optionalParameters is None:
        optionalParameters = []

    requiredParameters = set(requiredParameters)
    if not isinstance(json, dict):
        return [error_message(errorCode)]

    if requiredParameters - set(json):
        return [error_message(errorCode)]

    if set(json) - (requiredParameters | set(optionalParameters)):
        return [error_message(errorCode)]

    return []

from utils.apiMessages import errorMessage, LocalApiCode


def verifyJson(json, requiredParameters=None, optionalParameters=None, errorCode=LocalApiCode.invalidJson):
    if requiredParameters is None:
        requiredParameters = []
    if optionalParameters is None:
        optionalParameters = []

    requiredParameters = set(requiredParameters)
    if not isinstance(json, dict):
        return [errorMessage(errorCode)]
    
    if requiredParameters - set(json):
        return [errorMessage(errorCode)]

    if set(json) - (requiredParameters | set(optionalParameters)):
        return [errorMessage(errorCode)]
    
    return []

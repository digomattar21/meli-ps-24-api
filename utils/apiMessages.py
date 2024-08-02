

def errorMessage(code, message=None, language="portuguese"):
    return {
        "code": code,
        "message": message or localApiMessage[language][code],
    }


class LocalApiCode:
    notFound = "notFound"
    invalidJWT = "invalidJWT"
    unknownRoute = "unknownRoute"
    unauthorized = "unauthorized"
    invalidJson = "invalidJson"
    invalidUser = "invalidUser"
    invalidSpot = "invalidSpot"
    existingUser = "existingUser"
    emptyRequest = "emptyRequest"
    invalidImages = "invalidImages"
    internalError = "internalError"
    invalidSecret = "invalidSecret"
    invalidCamera = "invalidCamera"
    invalidComment = "invalidComment"
    invalidLocation = "invalidLocation"
    invalidPassword = "invalidPassword"
    unauthenticated = "unauthenticated"
    invalidParameters = "invalidParameters"
    invalidVerification = "invalidVerification"
    invalidCommentOwner = "invalidCommentOwner"
    invalidCameraPassword = "invalidCameraPassword"
    invalidAddress = "invalidAddress"


localApiMessage = {
    "english": {
        LocalApiCode.invalidAddress: "Invalid Address Format",
        LocalApiCode.invalidJWT: "Token is not legit.",
        LocalApiCode.invalidUser: "User does not exist.",
        LocalApiCode.invalidSpot: "Spot does not exist.",
        LocalApiCode.unknownRoute: "Route does not exist.",
        LocalApiCode.invalidCamera: "Camera does not exist.",
        LocalApiCode.invalidImages: "Invalid list of images.",
        LocalApiCode.invalidJson: "Json recived is invalid.",
        LocalApiCode.invalidParameters: "Invalid Parameters.",
        LocalApiCode.invalidComment: "Comment does not exist.",
        LocalApiCode.existingUser: "User is already registered.",
        LocalApiCode.invalidPassword: "Password does not match.",
        LocalApiCode.invalidVerification: "User is not verified.",
        LocalApiCode.unauthorized: "User doesn't have permission",
        LocalApiCode.invalidLocation: "Spot location is invalid.",
        LocalApiCode.unauthenticated: "User is not authenticated.",
        LocalApiCode.invalidSecret: "Secret does not match server.",
        LocalApiCode.invalidCameraPassword: "Password does not match.",
        LocalApiCode.internalError: "Internal error occured, contact us.",
        LocalApiCode.emptyRequest: "Request does not contain any content.",
        LocalApiCode.invalidCommentOwner: "You do not have permission to alter this comment.",
    },
    "portuguese": {
        LocalApiCode.invalidAddress: "Endereco não esta formatado corretamente",
        LocalApiCode.invalidJWT: "Token não é válido.",
        LocalApiCode.invalidUser: "Usuário não existe.",
        LocalApiCode.invalidSpot: "Spot não existe.",
        LocalApiCode.unknownRoute: "Rota não existe.",
        LocalApiCode.invalidCamera: "Câmera não existe.",
        LocalApiCode.invalidImages: "Fotos invalidas.",
        LocalApiCode.invalidJson: "Json recebido é inválido.",
        LocalApiCode.invalidParameters: "Parâmetros inválidos.",
        LocalApiCode.invalidComment: "Comentário não existe.",
        LocalApiCode.existingUser: "Usuário já está registrado.",
        LocalApiCode.invalidPassword: "Senha não confere.",
        LocalApiCode.unauthenticated: "Usuário não está autenticado.",
        LocalApiCode.unauthorized: "Usuário não tem permissão.",
        LocalApiCode.invalidLocation: "Localização do spot é inválida.",
        LocalApiCode.invalidSecret: "Segredo não confere com o servidor.",
        LocalApiCode.invalidCameraPassword: "Senha não confere.",
        LocalApiCode.emptyRequest: "Requisição não contém nenhum conteúdo.",
        LocalApiCode.internalError: "Erro interno de servidor, contate-nos.",
        LocalApiCode.invalidVerification: "Token de verificação não confere.",
        LocalApiCode.invalidCommentOwner: "Você não tem permissão para alterar esse comentário.",
    },
}

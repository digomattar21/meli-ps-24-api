def error_message(code, message=None, language="portuguese"):
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
    invalidCategory = "invalidCategory"
    invalidSubcategory = "invalidSubcategory"
    invalidSeverity = "invalidSeverity"
    ticketNotFound = "ticketNotFound"
    categoryNotFound = "categoryNotFound"
    duplicateCategoryName = "duplicateCategoryName"
    invalidParentCategory = "invalidParentCategory"
    invalidCategoryName = "invalidCategoryName"
    invalidTitle = "invalidTitle"
    invalidDescription = "invalidDescription"
    isNotSubcategory = "isNotSubcategory"
    existingUser = "existingUser"
    emptyRequest = "emptyRequest"
    internalError = "internalError"
    invalidSecret = "invalidSecret"
    unauthenticated = "unauthenticated"
    invalidParameters = "invalidParameters"


localApiMessage = {
    "english": {
        LocalApiCode.invalidJWT: "Token is not legit.",
        LocalApiCode.invalidUser: "User does not exist.",
        LocalApiCode.unknownRoute: "Route does not exist.",
        LocalApiCode.invalidJson: "Json recived is invalid.",
        LocalApiCode.invalidParameters: "Invalid Parameters.",
        LocalApiCode.existingUser: "User is already registered.",
        LocalApiCode.unauthorized: "User doesn't have permission",
        LocalApiCode.unauthenticated: "User is not authenticated.",
        LocalApiCode.invalidSecret: "Secret does not match server.",
        LocalApiCode.internalError: "Internal error occured, contact us.",
        LocalApiCode.emptyRequest: "Request does not contain any content.",
        LocalApiCode.ticketNotFound: "Ticket not found.",
        LocalApiCode.categoryNotFound: "Category not found.",
        LocalApiCode.invalidParentCategory: (
            "Parent category with this id does not exist."
        ),
        LocalApiCode.invalidCategoryName: "Category name must be a string.",
        LocalApiCode.invalidTitle: "Title must be a string.",
        LocalApiCode.invalidDescription: "Description must be a string.",
        LocalApiCode.isNotSubcategory: (
            "Subcategory id provided is not a subcategory of the category "
            "or it doesn't exist."
        ),
        LocalApiCode.duplicateCategoryName: "Category with this name already exists",
        LocalApiCode.invalidCategory: "Category id does not match existing category.",
        LocalApiCode.isNotSubcategory: (
            "Subcategory id provided is not a subcategory "
            "of the category or it doesn't exist."
        ),
        LocalApiCode.invalidSeverity: (
            "Severity level does not match existing severity levels "
            "and it cannot equal 1."
        ),
    },
    "portuguese": {
        LocalApiCode.invalidJWT: "Token não é válido.",
        LocalApiCode.invalidUser: "Usuário não existe.",
        LocalApiCode.unknownRoute: "Rota não existe.",
        LocalApiCode.invalidJson: "Json recebido é inválido.",
        LocalApiCode.invalidParameters: "Parâmetros inválidos.",
        LocalApiCode.existingUser: "Usuário já está registrado.",
        LocalApiCode.unauthenticated: "Usuário não está autenticado.",
        LocalApiCode.unauthorized: "Usuário não tem permissão.",
        LocalApiCode.invalidSecret: "Segredo não confere com o servidor.",
        LocalApiCode.emptyRequest: "Requisição não contém nenhum conteúdo.",
        LocalApiCode.internalError: "Erro interno de servidor, contate-nos.",
        LocalApiCode.invalidCategory: "Id da categoria nao existe.",
        LocalApiCode.invalidParentCategory: "Categoria parente com esse id nao existe.",
        LocalApiCode.duplicateCategoryName: "Categoria com esse nome ja existe.",
        LocalApiCode.invalidCategoryName: "Nome da categoria deve ser uma string.",
        LocalApiCode.invalidTitle: "Titulo deve ser uma string.",
        LocalApiCode.invalidDescription: "Descricao deve ser uma string.",
        LocalApiCode.categoryNotFound: "Categoria nao encontrada.",
        LocalApiCode.isNotSubcategory: (
            "Id de subcategoria nao é uma subcategoria do id de categoria fornecido "
            "ou a subcategoria não existe."
        ),
        LocalApiCode.ticketNotFound: "Ticket nao encontrado.",
        LocalApiCode.invalidSubcategory: "Id da subcategoria nao existe.",
        LocalApiCode.invalidSeverity: (
            "Level de seriedade nao corresponde a dados existentes " "e nao pode ser 1."
        ),
    },
}

from controllers.public.category import CategoryController
from controllers.public.healthcheck import HealthCheckController
from controllers.public.ticket import TicketController
from heart.server.route import Route

routes = [
    Route("/ticket", TicketController, methods=["GET", "POST"]),
    Route(
        "/ticket/<int:ticket_id>", TicketController, methods=["GET", "PATCH", "DELETE"]
    ),
    Route("/category", CategoryController, methods=["GET", "POST"]),
    Route(
        "/category/<int:category_id>",
        CategoryController,
        methods=["GET", "PATCH", "DELETE"],
    ),
    Route("/healthcheck", HealthCheckController, methods=["GET"]),
]

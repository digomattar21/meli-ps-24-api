from heart.server.route import Route
from controllers.public.ticket import TicketController
from controllers.public.healthcheck import HealthCheckController

routes = [
    Route("/ticket", TicketController),
    Route("/healthcheck", HealthCheckController),
]
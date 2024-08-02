from flask import Flask
from routes.public import routes as publicRoutes
from utils.apiMessages import errorMessage, LocalApiCode


def _notFound(error):
    return {"errors": [errorMessage(LocalApiCode.unknownRoute)]}, 404

app = Flask(__name__)

for route in publicRoutes:
    app.add_url_rule(rule=route.path, view_func=route.handler.as_view(route.name))
app.register_error_handler(404, _notFound)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

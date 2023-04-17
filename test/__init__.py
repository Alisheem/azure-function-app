import azure.functions as func
from flask import Flask

app = Flask(__name__)


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route("/hello")
def index():
    return "hi"

# if __name__== '__main__':
#     app.run()

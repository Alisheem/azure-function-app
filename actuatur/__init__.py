import azure.functions as func
from flask import Flask
from pyctuator.pyctuator import Pyctuator
import datetime

with open("git.properties", "r") as f:
    properties = {}
    for line in f:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        key, value = line.split("=", 1)
        properties[key] = value


branch_name = properties["git.branch"]
commit_time = properties["git.commit.time"]

build_info = {
    "branch": branch_name,
    "commit_time": commit_time,
    "build_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

app = Flask(__name__)

pyctuator = Pyctuator(app,"monitor",
                      app_url="http://localhost:7071",
                      pyctuator_endpoint_url="http://localhost:7071/actuator",
                      registration_url="",
                      additional_app_info=dict(
    build_info=build_info,
  ))

# pyctuator.set_build_info(name=get_conf("app.name"),
#                          version=get_conf("app.version"))


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

# if __name__== '__main__':
#     app.run()

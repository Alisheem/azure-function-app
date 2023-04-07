import azure.functions as func
from flask import Flask
from pyctuator.pyctuator import Pyctuator
import git
import datetime

repo = git.Repo(search_parent_directories=True)
branch = repo.active_branch.name
commit = repo.head.commit
commit_time = datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')


build_info = {
    "git_branch": branch,
    "commit_time": commit_time,
    "build_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

app = Flask(__name__)

pyctuator = Pyctuator(app,"monitor",
                      app_url="http://localhost:7071",
                      pyctuator_endpoint_url="http://localhost:7071/actuator",
                      registration_url="",
                      additional_app_info=dict(
    build_info=build_info
  ))


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route("/hello")
def index():
    return "hi"

if __name__== '__main__':
    app.run()

import azure.functions as func
from flask import Flask
from pyctuator.pyctuator import Pyctuator
# import git
# import datetime
import os

os.system("sudo apt install git-all")

app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
git_commit_hash = open(os.path.join(app_root, '.git', 'refs', 'heads', 'master')).read().strip()
# git_repository_url = open(os.path.join(app_root, '.git', 'config')).read().split('[remote "origin"]')[1].split('url = ')[1].split('\n')[0].strip()
# repo = git.Repo(search_parent_directories=True)
# branch = repo.active_branch.name
# commit = repo.head.commit
# commit_time = datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')

build_info = {
    "commit_hash":git_commit_hash
    # "git_branch": branch,
    # "commit_time": commit_time,
    # "build_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

# activeProfiles="dev"

app = Flask(__name__)

# os.environ['activeProfiles'] = 'dev'


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

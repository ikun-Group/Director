import logging.handlers
from flask import Flask, Response, request
from datetime import datetime
import json
from director_resource import directorResource
from flask_cors import CORS

application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(application)

@application.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "CC project",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@application.route("/directors/<guid>", methods=["GET"])
def get_director_by_guid(guid):

    result = directorResource.get_by_key(guid)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@application.route("/directors", methods=["GET"])
def get_all_director():

    result = directorResource.get_all()

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)


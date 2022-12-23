import logging.handlers
from flask import Flask, Response, request
from datetime import datetime
import json
from director_resource import DirectorResource
from flask_cors import CORS
import copy
from rest_utils import RESTContext


app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)

@app.get("/api/health")
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


@app.route("/api/directors", methods=["GET", "POST"])
def directors():
    request_inputs = RESTContext(request, directors)
    if request_inputs.method == "GET":
        result = DirectorResource.get_all(limit=request_inputs.limit, offset=request_inputs.offset)
        result = request_inputs.add_pagination(result)
        if result:
            res = json.dumps(result)
            status_code = 200
        else:
            res = "Not found"
            status_code = 404
    elif request.method == "POST":
        director_profile = request.get_json()
        try:
            ret = DirectorResource.create_director(**director_profile)
            if ret:
                res = 'Director created!'
                status_code = 201
            else:
                res = 'Failed to create director'
                status_code = 422
        except Exception as e:
            res = 'Error: {}'.format(str(e))
            status_code = 422
    else:
        res = 'Not implemented'
        status_code = 501
    return Response(f"{status_code} - {res}", status=status_code, mimetype="application/json")


@app.route("/api/directors/<guid>", methods=["GET", "PUT", "DELETE"])
def director_by_id(guid):
    if request.method == "GET":
        result = DirectorResource.get_by_template('*', {'guid': guid}, limit=None, offset=None)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("Not found", status=404, content_type="text/plain")
    elif request.method == "PUT":
        director_profile = request.get_json()
        if len(director_profile) != 7:
            rsp = Response('input length not right', status=400, content_type="text/plain")
        else:
            try:
                result = DirectorResource.update_director(guid, **director_profile)
                if result:
                    rsp = Response('Update successful', status=200, content_type="application.json")
                else:
                    rsp = Response("Update failed", status=404, content_type="text/plain")
            except Exception as e:
                rsp = Response('Error: {}'.format(str(e)), status=404, content_type="text/plain")
    elif request.method == "DELETE":
        try:
            result = DirectorResource.delete_director(guid)
            if result:
                rsp = Response('Delete successful', status=200, content_type="application.json")
            else:
                rsp = Response("Delete failed", status=404, content_type="text/plain")
        except Exception as e:
            rsp = Response('Error: {}'.format(str(e)), status=404, content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    return rsp


@app.route("/api/directors/<guid>/<value>", methods=["GET"])
def get_value_by_id(guid, value):
    result = DirectorResource.get_by_template([value], {'guid': guid})
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


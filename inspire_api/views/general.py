import datetime
import json

from flask import Blueprint, Response, current_app, g, request
from inspire_api.dependencies import postgres

general_bp = Blueprint('general', __name__)


@general_bp.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_wsgi_list(),
        "commit": current_app.config["COMMIT"]
    }), mimetype='application/json', status=200)


@general_bp.route("/health/cascade/<str_depth>")
def cascade_health(str_depth):  # pragma: no cover
    depth = int(str_depth)

    if (depth < 0) or (depth > int(current_app.config.get("MAX_HEALTH_CASCADE"))):
        current_app.logger.info(depth)
        current_app.logger.error("Cascade depth {} out of allowed range (0 - {})".format(
            depth, current_app.config.get("MAX_HEALTH_CASCADE")))
        return Response(response=json.dumps({
            "app": current_app.config.get("APP_NAME"),
            "cascade_depth": str_depth,
            "status": "ERROR",
            "timestamp": str(datetime.datetime.now())
        }), mimetype='application/json', status=500)
    dbs = []
    services = []
    overall_status = 200  # if we encounter a failure at any point then this will be set to != 200
    if current_app.config.get("DEPENDENCIES") is not None:
        for dependency, value in current_app.config.get("DEPENDENCIES").items():
            if "postgres" in value:
                # postgres db url - try calling current timestamp routine
                db = dict()
                db["name"] = dependency
                try:
                    db_timestamp = postgres.get_current_timestamp()
                    # trim microseconds to 3 to match java
                    db["current_timestamp"] = db_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
                    db["status"] = "OK"
                except Exception as e:
                    message = "Error during health cascade on request to database: {}; full error: {}."
                    current_app.logger.error(message.format(dependency, e))
                    overall_status = 500
                    db["status"] = "BAD"
                finally:
                    dbs.append(db)
            else:
                if depth > 0:
                    # As there is an inconsistant approach to url variables we need to check to see if we have a
                    # trailing '/' and add one if not
                    if value[-1] != '/':
                        value = value + '/'

                    # Setup our service entry
                    service = {
                        "name": dependency,
                        "type": "http"
                    }
                    try:
                        resp = g.requests.get(value + 'health/cascade/' + str(depth - 1))  # Try and request the health
                    except ConnectionAbortedError as e:  # More specific logging statement for abortion error
                        message = "Connection Aborted during health cascade on attempt to connect to {}; " + \
                                  "full error: {}"
                        current_app.logger.error(message.format(dependency, e))
                        service["status"] = "UNKNOWN"
                        overall_status = 500
                        service["status_code"] = None
                        service["content_type"] = None
                        service["content"] = None
                    except Exception as e:  # Generic catch-all exception
                        message = "Unknown error occured during health cascade on request to {}; full error: {}"
                        current_app.logger.error(message.format(dependency, e))
                        service["status"] = "UNKNOWN"
                        overall_status = 500
                        service["status_code"] = None
                        service["content_type"] = None
                        service["content"] = None
                    else:   # Everything worked
                        service["status_code"] = resp.status_code
                        service["content_type"] = resp.headers["content-type"]
                        service["content"] = resp.json()
                        if resp.status_code == 200:  # Happy route, happy service, happy status_code.
                            service["status"] = "OK"
                        elif resp.status_code == 500:  # Something went wrong
                            service["status"] = "BAD"
                            overall_status = 500
                        else:   # Who knows what happened.
                            service["status"] = "UNKNOWN"
                            overall_status = 500
                    finally:
                        services.append(service)
    response_json = {
        "cascade_depth": depth,
        "server_timestamp": str(datetime.datetime.now()),
        "app": current_app.config.get("APP_NAME"),
        "status": "UNKNOWN",
        "headers": request.headers.to_wsgi_list(),
        "commit": current_app.config.get("COMMIT"),
        "db": dbs,
        "services": services
    }
    if overall_status == 500:
        response_json['status'] = "BAD"
    else:
        response_json['status'] = "OK"
    return Response(response=json.dumps(response_json), mimetype='application/json', status=overall_status)

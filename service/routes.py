"""
Controller for routes
"""
from flask import jsonify, url_for, abort
from service import app
from service.common import status

C = {}


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Returns information abut the service"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")

    counters= [dict(name=count[0], counter=count[1]) for count in C.items()]

    return jsonify(counters)


############################################################
# Create counters
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter"""
    app.logger.info("Request to Create counter: %s...", name)

    if name in C:
        return abort(
                status.HTTP_409_CONFLICT,
                f"Counter {name} already exists")

    C[name] = 0

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter"""
    app.logger.info("Request to Read counter: %s...", name)

    if name not in C:
        return abort(
            status.HTTP_404_NOT_FOUND,
            f"Counter {name} does not exist")

    counter = C[name]
    return jsonify(name=name, counter=counter)


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Updates a counter"""
    app.logger.info("Request to Update counter: %s...", name)

    if name not in C:
        return abort(
            status.HTTP_404_NOT_FOUND,
            f"Counter {name} does not exist")

    C[name] += 1

    counter = C[name]
    return jsonify(name=name, counter=counter)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Deletes a counter"""
    app.logger.info("Request to Delete counter: %s...", name)

    if name in C:
        C.pop(name)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# Utility for testing
############################################################
def reset_counters():
    """Removes all counters while testing"""
    global C  # pylint: disable=global-statement
    if app.testing:
        C = {}

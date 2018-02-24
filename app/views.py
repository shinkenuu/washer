from flask import abort, jsonify

from app import app
from app.models import Server


@app.route('/<server_name>', methods=['GET'])
def vote(server_name):
    server = Server.query.filter_by(name=server_name).first()

    if not server:
        abort(404)

    credential_to_vote = server.next_to_vote

    response = {
        'credential_that_voted': dict(credential_to_vote)
    }

    return jsonify(response), 200

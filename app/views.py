from flask import jsonify

from app import app
from app.models import Server


@app.route('/<server_name>', methods=['GET'])
def vote(server_name):
    server = Server.query.filter_by(name=server_name).first()

    if not server:
        return jsonify(error='server name not found'), 404

    credential_to_vote = server.next_to_vote

    return jsonify(credential_to_vote.__dict__)

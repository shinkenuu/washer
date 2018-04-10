from flask import abort, jsonify

from app import app
from app.models import Server
from app.services import crawl


@app.route('/<server_name>', methods=['GET'])
def vote(server_name):
    server = Server.query.filter_by(name=server_name).first()

    if server is None:
        abort(404)

    crawl_results = crawl(server=server)

    return jsonify(crawl_results), 500 if crawl_results.get('errors', False) else 200

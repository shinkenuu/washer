from app import app
from models import Credential


@app.route('/')
def home():
    next_to_vote = min(Credential.objects(able_to_vote=True).all(),
                       key=lambda credential: credential.last_vote_datetime)


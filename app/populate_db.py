from app.database import db_session
from app.models import CrawlForm, CrawlSpot, Credential, Server


SERVER = Server(name='mapledestiny')


LOGIN_CRAWL_SPOT = CrawlSpot(
    order_of_crawling=0,
    url='http://mapledestiny.net/login/',
    server=SERVER
)


VOTE_CRAWL_SPOT = CrawlSpot(
    order_of_crawling=1,
    url='http://mapledestiny.net/vote/',
    server=SERVER
)


LOGIN_CRAWL_FORM = CrawlForm(
    xpath='//form[@class="form-signin"]',
    data={"username": "__credential__.username", "password": "__credential__.password"},
    click_data={"type": "submit"},
    spot=LOGIN_CRAWL_SPOT
)


VOTE_CRAWL_FORM_0 = CrawlForm(
    number=0,
    click_data={"value": "Vote on Gtop100 (4k NX)"} ,
    spot=VOTE_CRAWL_SPOT
)


VOTE_CRAWL_FORM_1 = CrawlForm(
    number=1,
    click_data={"value": "Vote on UltimatePS (2k NX)"},
    spot=VOTE_CRAWL_SPOT
)

CREDENTIALS = [
    Credential(username='8balls', password='ehnoiscarai', server=SERVER),
    Credential(username='8balls2', password='ehnoiscarai', server=SERVER),
    Credential(username='8balls3', password='ehnoiscarai', server=SERVER),
    Credential(username='8balls4', password='ehnoiscarai', server=SERVER),
    Credential(username='Matrim', password='5hadow', server=SERVER),
    Credential(username='Vincent_', password='5hadow', server=SERVER),
]


def populate_db():
    db_session.add_all(
        [SERVER] +
        [LOGIN_CRAWL_SPOT, VOTE_CRAWL_SPOT] +
        [LOGIN_CRAWL_FORM, VOTE_CRAWL_FORM_0, VOTE_CRAWL_FORM_1] +
        CREDENTIALS
    )

    db_session.flush()

import mock
import pytest

from crawlers.exceptions import LoginFailed, UnableToVote
from tests.crawlers import create_spider_response as _create_spider_response


def create_spider_response(html_filename, url=None):
    return _create_spider_response(spider_name='destiny', html_filename=html_filename, url=url)


@pytest.fixture
def destiny_spider_fixture():
    from crawlers.spiders.destiny import DestinySpider

    mocked_json_data = {
        'servers': [
            {
                'name': 'destiny',
                'base_url': 'http://www.site.net',
                'credentials': [
                    {
                        'username': 'username_entered',
                        'password': 'password_entered',
                        'able_to_vote': True,
                        'last_vote_datetime': '2017-03-01 00:01:02',
                    },
                    {
                        'username': 'username_just_voted',
                        'password': 'password_just_voted',
                        'able_to_vote': True,
                        'last_vote_datetime': '2018-05-31 19:31:02',
                    }
                ]
            }
        ]
    }

    with mock.patch.object(DestinySpider, 'read_dict_from_json', return_value=mocked_json_data) as _:
        return DestinySpider()


def test_login_form_request(destiny_spider_fixture):
    login_form_request = destiny_spider_fixture.login(create_spider_response('login.html'))

    expected_body = b'csrfmiddlewaretoken=aEYzKfMkUg8jLFCDr5LcpjAzxclaRx5C' + \
        b'&username=' + bytes(destiny_spider_fixture.credential.username, 'utf-8') + \
        b'&password=' + bytes(destiny_spider_fixture.credential.password, 'utf-8')

    assert login_form_request.body == expected_body


def test_login_callback_detects_failed_login(destiny_spider_fixture):

    # Test when not logged in

    try:
        destiny_spider_fixture.login_callback(create_spider_response('home.html'))
        assert False
    except LoginFailed:
        assert True

    # Test when logged in

    destiny_spider_fixture.login_callback(create_spider_response('home_logged.html'))


def test_vote_without_available_site(destiny_spider_fixture):
    vote_disabled_response = create_spider_response('vote_disabled.html')

    try:
        for _ in destiny_spider_fixture.vote(vote_disabled_response):
            pass
        assert False
    except UnableToVote:
        assert True


def test_vote_with_some_available_site(destiny_spider_fixture):
    vote_one_disabled_response = create_spider_response('vote_one_disabled.html')

    vote_form_requests = [form_request for form_request
                          in destiny_spider_fixture.vote(vote_one_disabled_response)]

    vote_site_names_left = ['Gtop100']

    for vote_form_request in vote_form_requests:

        for vote_site_name in vote_site_names_left:

            if vote_site_name in str(vote_form_request.body):
                vote_site_names_left.pop(vote_site_names_left.index(vote_site_name))
                break

    assert len(vote_site_names_left) == 0


def test_vote_on_all_available_site(destiny_spider_fixture):
    vote_response = create_spider_response('vote.html')

    vote_form_requests = [form_request for form_request
                          in destiny_spider_fixture.vote(vote_response)]

    vote_site_names_left = ['UltimatePS', 'Gtop100']

    for vote_form_request in vote_form_requests:

        for vote_site_name in vote_site_names_left:

            if vote_site_name in str(vote_form_request.body):
                vote_site_names_left.pop(vote_site_names_left.index(vote_site_name))
                break

    assert len(vote_site_names_left) == 0

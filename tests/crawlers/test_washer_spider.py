from datetime import timedelta
import json
import mock
import pytest
from shutil import copyfile

from crawlers.spiders import WasherSpider

from tests.test_schemas import WASHER_DICT

SCHEMA_JSON_FILEPATH = './tests/schema_example.json'
TMP_SCHEMA_JSON_FILEPATH = '/tmp/schema_example.json'


class FakeWasherSpider(WasherSpider):
    name = 'fake'


@pytest.fixture
def washer_spider_fixture():
    copyfile(SCHEMA_JSON_FILEPATH, TMP_SCHEMA_JSON_FILEPATH)
    return FakeWasherSpider(json_schema_filepath=TMP_SCHEMA_JSON_FILEPATH)


@mock.patch.object(WasherSpider, 'read_dict_from_json')
def test_washer_initialization(mocked_washer_read_from_dict, washer_spider_fixture):

    washer_schema_dict = WASHER_DICT.copy()
    fake_spider_server = washer_schema_dict['servers'][0]
    fake_spider_server['name'] = washer_spider_fixture.name

    latest_to_vote_credential = fake_spider_server['credentials'][0].copy()
    last_vote_datetime = latest_to_vote_credential['last_vote_datetime']
    last_vote_datetime -= timedelta(days=1)
    fake_spider_server['credentials'].append(latest_to_vote_credential)

    mocked_washer_read_from_dict.return_value = washer_schema_dict
    washer_spider = FakeWasherSpider()

    assert washer_spider.schema.to_dict() == washer_schema_dict
    assert washer_spider.server.to_dict() == washer_schema_dict['servers'][0]
    assert washer_spider.credential.to_dict() == latest_to_vote_credential


def test_credential_selection():
    # test next_credential_to_vote
    pass


def test_recording_of_data(washer_spider_fixture):
    expected_file_dict_content = washer_spider_fixture.schema.to_dict()
    washer_spider_fixture.write_dict_to_json(expected_file_dict_content)

    with open(washer_spider_fixture.json_schema_filepath, 'r') as json_file:
        assert json.load(json_file) == expected_file_dict_content
        assert json_file.read() != json.dumps(expected_file_dict_content)  # test for pprint

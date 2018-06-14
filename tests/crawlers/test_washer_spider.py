import pytest
from shutil import copyfile

from crawlers.spiders import WasherSpider

SCHEMA_JSON_FILEPATH = './tests/schema_example.json'
TMP_SCHEMA_JSON_FILEPATH = '/tmp/schema_example.json'


@pytest.fixture
def washer_spider_fixture():
    class FakeWasherSpider(WasherSpider):
        name = 'fake'

    copyfile(SCHEMA_JSON_FILEPATH, TMP_SCHEMA_JSON_FILEPATH)

    return FakeWasherSpider(json_schema_filepath=TMP_SCHEMA_JSON_FILEPATH)


def test_washer_initialization():
    pass


def test_recording_of_data():
    pass

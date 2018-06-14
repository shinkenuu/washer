from datetime import datetime
import pytest

from schemas import CredentialSchema, ServerSchema, Schema, WasherSchema

CREDENTIAL_SCHEMA = CredentialSchema(**{
    'username': 'name',
    'password': 'secret',
    'able_to_vote': True,
    'last_vote_datetime': '2018-02-13 14:54:03'
})

SERVER_SCHEMA = ServerSchema(**{
    'name': 'site',
    'base_url': 'www.site.com',
    'credentials': [
        {
            'username': 'name',
            'password': 'secret',
            'able_to_vote': True,
            'last_vote_datetime': '2018-02-13 14:54:03'
        }
    ]
})

WASHER_SCHEMA = WasherSchema(**{
    'servers': [
        {
            'name': 'site',
            'base_url': 'www.site.com',
            'credentials': [
                {
                    'username': 'name',
                    'password': 'secret',
                    'able_to_vote': True,
                    'last_vote_datetime': '2018-02-13 14:54:03'
                }
            ]
        }
    ]
})


@pytest.fixture
def schema_fixture():
    class FakeSchema(Schema):
        fields = ['key1', 'key2', 'key3']

    return FakeSchema(
        key1='value1',
        key2='value2',
        key3=FakeSchema(key1='value3_1', key2='value3_2', key3='value3_3')
    )


def test_initialization(schema_fixture):
    assert schema_fixture.key1 == 'value1'
    assert schema_fixture.key2 == 'value2'

    assert schema_fixture.key3.key1 == 'value3_1'
    assert schema_fixture.key3.key2 == 'value3_2'
    assert schema_fixture.key3.key3 == 'value3_3'


def test_formatting(schema_fixture):
    expected_dict = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': {
            'key1': 'value3_1',
            'key2': 'value3_2',
            'key3': 'value3_3',
        },
    }

    assert dict(schema_fixture) == expected_dict


def test_credential_schema():
    for key, value in dict(CREDENTIAL_SCHEMA).items():
        assert CREDENTIAL_SCHEMA.__getattribute__(key) == value


def test_server_schema():
    for key, value in dict(SERVER_SCHEMA).items():
        assert SERVER_SCHEMA.__getattribute__(key) == value


def test_washer_schema():
    for key, value in dict(WASHER_SCHEMA).items():
        assert WASHER_SCHEMA.__getattribute__(key) == value

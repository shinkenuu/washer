from datetime import datetime
import pytest

from schemas import CredentialSchema, ServerSchema, Schema, WasherSchema

CREDENTIAL_DICT = {
    'username': 'name',
    'password': 'secret',
    'able_to_vote': True,
    'last_vote_datetime': '2018-02-13 14:54:03'
}

SERVER_DICT = {
    'name': 'site',
    'base_url': 'www.site.com',
    'credentials': [
        CREDENTIAL_DICT
    ]
}

WASHER_DICT = {
    'servers': [
        SERVER_DICT
    ]
}

CREDENTIAL_SCHEMA = CredentialSchema(**CREDENTIAL_DICT)
SERVER_SCHEMA = ServerSchema(**SERVER_DICT)
WASHER_SCHEMA = WasherSchema(**WASHER_DICT)


def test_credential_schema():
    assert CREDENTIAL_SCHEMA.to_dict() == CREDENTIAL_DICT


def test_server_schema():
    assert SERVER_SCHEMA.to_dict() == SERVER_DICT


def test_washer_schema():
    assert WASHER_SCHEMA.to_dict() == WASHER_DICT

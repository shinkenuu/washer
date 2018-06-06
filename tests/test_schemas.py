import pytest

from schemas import Schema


@pytest.fixture
def schema_fixture():
    class FakeSchema(Schema):
        attributes = ['key1', 'key2', 'key3']

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

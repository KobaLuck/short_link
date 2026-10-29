import pytest
from yacut.models import URLMap

@pytest.mark.parametrize('payload', [[], 'text', 3, True, {'url': None},
    {'url': []}, {'url': ''}, {'url': 'x' * 2049},
    {'url': 'https://example.com', 'custom_id': 3},
    {'url': 'https://example.com', 'custom_id': False},
    {'url': 'https://example.com', 'custom_id': 'abc\n'}])
def test_invalid_payload_returns_400_without_writing(client, payload):
    response = client.post('/api/id/', json=payload)
    assert response.status_code == 400
    assert 'message' in response.json
    assert URLMap.query.count() == 0

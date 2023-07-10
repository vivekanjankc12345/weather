import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_weather(client):
    response = client.get('/weather/San Francisco')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['city'] == 'San Francisco'
    assert 'temperature' in data
    assert 'weather' in data


def test_get_weather_city_not_found(client):
    response = client.get('/weather/Unknown City')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'City not found'


def test_add_weather(client):
    data = {
        'city': 'Chicago',
        'temperature': 18,
        'weather': 'Cloudy'
    }
    response = client.post('/weather', json=data)
    assert response.status_code == 201
    assert response.data == b''


def test_update_weather(client):
    data = {
        'temperature': 22,
        'weather': 'Sunny'
    }
    response = client.put('/weather/New York', json=data)
    assert response.status_code == 200
    assert response.data == b''


def test_update_weather_city_not_found(client):
    data = {
        'temperature': 22,
        'weather': 'Sunny'
    }
    response = client.put('/weather/Unknown City', json=data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'City not found'


def test_delete_weather(client):
    response = client.delete('/weather/Seattle')
    assert response.status_code == 204
    assert response.data == b''


def test_delete_weather_city_not_found(client):
    response = client.delete('/weather/Unknown City')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'City not found'

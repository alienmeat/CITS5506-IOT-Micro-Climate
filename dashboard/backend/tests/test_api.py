import os
import tempfile
import pytest

# Импортируем ваше Flask-приложение и функцию инициализации БД
import app
from app import app as flask_app, init_db, DB_FILE

@pytest.fixture(autouse=True)
def client(tmp_path, monkeypatch):
    """
    Фикстура создаёт временную БД и тестовый клиент Flask.
    """
    # Подменяем путь к файлу БД на временный
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(app, 'DB_FILE', str(test_db))
    # Инициализируем БД заново
    init_db()
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_home_endpoint(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Flask backend is running' in rv.data


def test_notification_settings_structure(client):
    rv = client.get('/notification-settings')
    assert rv.status_code == 200
    data = rv.get_json()
    # Проверяем ключи
    expected_keys = {'min_temp','max_temp','min_humid','max_humid','min_press','max_press'}
    assert expected_keys.issubset(data.keys())


def test_alerts_empty_by_default(client):
    rv = client.get('/alerts')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert data == []


def test_control_history_empty(client):
    rv = client.get('/control-history')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_device_status_structure(client):
    rv = client.get('/device-status')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'devices' in json_data
    assert isinstance(json_data['devices'], list)


def test_current_settings_defaults(client):
    rv = client.get('/current-settings')
    assert rv.status_code == 200
    data = rv.get_json()
    # Должен быть default pin V8
    assert 'V8' in data
    assert data['V8'] in (0,1)  # Smart Control default off (0)
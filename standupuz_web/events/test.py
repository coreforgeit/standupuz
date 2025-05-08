# test_events_api.py

import requests

BASE_URL = "http://localhost:8000/api/event/"


def test_list_events():
    """Проверяем, что список возвращается корректно"""
    resp = requests.get(BASE_URL)
    assert resp.status_code == 200, f"Ожидали 200, получили {resp.status_code}"
    data = resp.json()
    assert "cards" in data, "В ответе нет ключа 'cards'"
    assert isinstance(data["cards"], list), "'cards' не список"


def test_event_detail_existing():
    """Проверяем detail для существующего события"""
    # Сначала берём какой-нибудь существующий event_id из списка
    list_resp = requests.get(BASE_URL)
    cards = list_resp.json().get("cards", [])
    if not cards:
        print("Нет событий для теста detail — пропускаем")
        return
    event_id = cards[0]["event_id"]

    detail_resp = requests.get(f"{BASE_URL}{event_id}/")
    assert detail_resp.status_code == 200, f"Ожидали 200 для event_id={event_id}, получили {detail_resp.status_code}"
    ev = detail_resp.json()
    # Проверяем минимум один ключ из структуры
    expected_keys = {
        "event_id", "photo_path", "places",
        "date_str", "time_str", "day_str",
        "place", "min_amount", "description", "tg_link"
    }
    assert expected_keys.issubset(ev.keys()), f"В ответе detail не все поля: {expected_keys - set(ev.keys())}"


def test_event_detail_not_found():
    """Проверяем 404 для несуществующего события"""
    invalid_id = 999999
    resp = requests.get(f"{BASE_URL}{invalid_id}/")
    assert resp.status_code == 404, f"Ожидали 404, получили {resp.status_code}"
    data = resp.json()
    assert data.get("detail") == "Event not found.", "Неверное сообщение об ошибке"


if __name__ == "__main__":
    test_list_events()
    test_event_detail_existing()
    test_event_detail_not_found()
    print("✅ Все тесты пройдены")

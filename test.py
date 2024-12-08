import requests
import pytest

url = 'http://127.0.0.1:5000/get_form'

def setup_module():
    pass

def teardown_module():
    pass

# Проверяем запрос со всеми полями
def test_all_fields():
    r = requests.post(url, data='user_name=Nikita')
    assert r.text == 'Data 1'

# Проверяем запрос с частью полей
def test_part_fields():
    r = requests.post(url, data='id=ABC123')
    assert r.text == 'Data 2'

# Проверяем запрос на дату в формате DD.MM.YYYY
def test_date_ddmmyyyy():
    r = requests.post(url, data='birth_date=06.04.2004')
    assert r.text == 'Data 2'

# Проверяем запрос на дату в формате YYYY-MM-DD
def test_date_yyyymmdd():
    r = requests.post(url, data='birth_date=2004-04-06')
    assert r.text == 'Data 2'

# Проверяем запрос на телефон
def test_phone():
    r = requests.post(url, data='telephone=+7 925 293 46 98')
    assert r.text == 'Data 2'

# Проверяем запрос на email
def test_email():
    r = requests.post(url, data='mail=shcnik@yandex.ru')
    assert r.text == 'Data 2'

# Проверяем запрос на несколько полей
def test_multiple_fields():
    r = requests.post(url, data='mail=shcnik@yandex.ru&id=ABC123')
    assert r.text == 'Data 2'

# Проверяем случай отсутствия формы
def test_no_form():
    r = requests.post(url, data='user_name=Nikita&birth_date=06.04.2004&telephone=+7 925 293 46 98&mail=shcnik@yandex.ru')
    assert r.json() == {'user_name': 'text', 'birth_date': 'date', 'telephone': 'phone', 'mail': 'email'}

# Проверяем случай, когда подходят 2 формы
def test_multiple_hits():
    r = requests.post(url, data='surname=Scherbakov&given_name=Nikita')
    assert r.text == 'Data 3'

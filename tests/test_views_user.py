import pytest
from django.urls import reverse
from django.test import Client
from users.models import User


@pytest.mark.django_db
def test_register_user_view():
    """ Проверяет успешную регистрацию нового пользователя """
    client = Client()
    register_url = reverse("users:reg")

    response = client.post(register_url, {
        "username": "new_user",
        "password1": "TestPassword123",
        "password2": "TestPassword123"
    })

    assert response.status_code == 302  # Редирект на логин
    assert User.objects.filter(username="new_user").exists()


@pytest.mark.django_db
def test_register_user_existing_username():
    """ Проверяет ошибку при регистрации с уже существующим именем """
    client = Client()
    User.objects.create_user(username="existing_user", password="TestPassword123")
    register_url = reverse("users:reg")

    response = client.post(register_url, {
        "username": "existing_user",
        "password1": "TestPassword123",
        "password2": "TestPassword123"
    })

    assert response.status_code == 200  # Остаёмся на той же странице
    assert "Пользователь с таким именем уже существует" in response.content.decode()


@pytest.mark.django_db
def test_register_user_invalid_password():
    """ Проверяет ошибку при регистрации с некорректным паролем """
    client = Client()
    register_url = reverse("users:reg")

    response = client.post(register_url, {
        "username": "new_user",
        "password1": "123",  # Слишком короткий пароль
        "password2": "123"
    })

    assert response.status_code == 200
    assert "Введённый пароль слишком короткий" in response.content.decode()


@pytest.mark.django_db
def test_register_user_empty_form():
    """ Проверяет ошибку при отправке пустой формы регистрации """
    client = Client()
    register_url = reverse("users:reg")

    response = client.post(register_url, {})

    assert response.status_code == 200
    assert "Обязательное поле" in response.content.decode()


@pytest.mark.django_db
def test_login_user_view():
    """ Проверяет успешный вход пользователя в систему """
    client = Client()
    user = User.objects.create_user(username="test_user", password="TestPassword123")
    login_url = reverse("users:log")

    response = client.post(login_url, {
        "username": "test_user",
        "password": "TestPassword123"
    })

    assert response.status_code == 302  # редирект после входа
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_login_invalid_credentials():
    """ Проверяет ошибку входа с неправильными данными """
    client = Client()
    User.objects.create_user(username="test_user", password="TestPassword123")
    login_url = reverse("users:log")

    response = client.post(login_url, {
        "username": "test_user",
        "password": "WrongPassword"
    })

    assert response.status_code == 200
    assert "Пожалуйста, введите правильные имя пользователя и пароль" in response.content.decode()


@pytest.mark.django_db
def test_login_non_existent_user():
    """ Проверяет ошибку входа несуществующего пользователя """
    client = Client()
    login_url = reverse("users:log")

    response = client.post(login_url, {
        "username": "non_existent",
        "password": "SomePassword"
    })

    assert response.status_code == 200
    assert "Пожалуйста, введите правильные имя пользователя и пароль" in response.content.decode()


@pytest.mark.django_db
def test_login_empty_form():
    """ Проверяет ошибку при входе с пустой формой """
    client = Client()
    login_url = reverse("users:log")

    response = client.post(login_url, {})

    assert response.status_code == 200
    assert "Обязательное поле" in response.content.decode()

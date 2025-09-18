import pytest
from referee.forms import CreateRoomForm
from users.forms import RegisterUserForm


@pytest.mark.django_db
def test_create_room_form_valid():
    """ CreateRoomForm принимает корректные данные """
    form = CreateRoomForm(data={"name": "Комната 1"})
    assert form.is_valid()


@pytest.mark.django_db
def test_create_room_form_invalid():
    """ CreateRoomForm не проходит валидацию без имени """
    form = CreateRoomForm(data={})  # Нет name
    assert not form.is_valid()
    assert "name" in form.errors  # Ошибка в name


@pytest.mark.django_db
def test_register_user_form_valid():
    """ Форма регистрации принимает корректные данные """
    form = RegisterUserForm(data={
        "username": "testuser",
        "password1": "TestPass123!",
        "password2": "TestPass123!"
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_register_user_form_password_mismatch():
    """ Пароли не совпадают """
    form = RegisterUserForm(data={
        "username": "testuser",
        "password1": "TestPass123!",
        "password2": "AnotherPass!"
    })
    assert not form.is_valid()
    assert "password2" in form.errors

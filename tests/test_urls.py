import pytest
from django.urls import reverse, resolve
from referee.views import *
from users.views import RegUser, Login


@pytest.mark.parametrize("url_name, kwargs", [
    ("referee:home", None),
    ("referee:create_room", None),
    ("referee:my_rooms", None),
    ("referee:join_room", None),
])
@pytest.mark.django_db
def test_public_urls(client, url_name, kwargs, user):
    """доступность страниц"""
    client.force_login(user)  # логинимся
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("url_name, view_class, kwargs", [
    ("referee:home", Home, None),
    ("referee:create_room", CreateRoom, None),
    ("referee:my_rooms", MyRooms, None),
    ("referee:join_room", JoinRoom, None),
    ("users:reg", RegUser, None),
    ("users:log", Login, None),
])
def test_url_resolves_to_correct_view(url_name, view_class, kwargs):
    """ соответствия URL и View"""
    url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)
    resolved_view = resolve(url).func.view_class
    assert resolved_view == view_class

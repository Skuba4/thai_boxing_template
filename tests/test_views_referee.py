import json
import pytest
import uuid
from django.urls import reverse
from django.test import Client
from referee.models import RoomJudges, Room, Notes, Fight
from users.models import User


@pytest.mark.django_db
def test_home_view(client: Client):
    """проверяет, что главная страница доступна"""
    response = client.get(reverse("referee:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_judge_view(client, user, room):
    """проверяет добавление судьи в комнату"""
    client.force_login(user)
    add_judge_url = reverse("referee:add_judge", kwargs={"uuid_room": room.uuid_room})

    # проверяем, что нельзя добавить самого себя как судью
    response = client.post(add_judge_url, json.dumps({"username": user.username}), content_type="application/json")
    assert response.status_code == 400
    assert "Вы не можете добавить себя как судью." in response.json()["error"]

    # создаём второго пользователя и добавляем его как судью
    judge_user = User.objects.create_user(username="judge_user", password="testpassword")
    response = client.post(add_judge_url, json.dumps({"username": judge_user.username}),
                           content_type="application/json")
    assert response.status_code == 200
    assert RoomJudges.objects.filter(room=room, user=judge_user).exists()

    # проверяем, что нельзя добавить одного и того же судью дважды
    response = client.post(add_judge_url, json.dumps({"username": judge_user.username}),
                           content_type="application/json")
    assert response.status_code == 400
    assert "Этот судья уже добавлен" in response.json()["error"]

    # отправляем некорректные данные
    response = client.post(add_judge_url, "not a json", content_type="application/json")
    assert response.status_code == 400
    assert "Ошибка чтения JSON" in response.json()["error"]


@pytest.mark.django_db
def test_delete_judge_view(client, user, room, judge):
    """проверяет удаление судьи из комнаты"""
    client.force_login(user)
    delete_judge_url = reverse("referee:delete_judge", kwargs={"uuid_room": room.uuid_room, "judge_id": judge.user.id})

    # удаляем судью
    response = client.post(delete_judge_url)
    assert response.status_code == 200
    assert not RoomJudges.objects.filter(room=room, user=judge.user).exists()

    # проверяем, что нельзя удалить несуществующего судью
    response = client.post(delete_judge_url)
    assert response.status_code == 404
    assert "Судья не найден" in response.json()["error"]


@pytest.mark.django_db
def test_active_judge_view(client, user, room):
    """проверяет активацию и деактивацию судьи"""
    client.force_login(user)
    judge_user = User.objects.create_user(username="judge_user", password="testpassword")
    judge = RoomJudges.objects.create(room=room, user=judge_user, is_active=False)
    active_judge_url = reverse("referee:active_judge", kwargs={"uuid_room": room.uuid_room, "judge_id": judge_user.id})

    # активируем судью
    response = client.post(active_judge_url)
    judge.refresh_from_db()
    assert response.status_code == 200
    assert judge.is_active is True

    # деактивируем судью
    response = client.post(active_judge_url)
    judge.refresh_from_db()
    assert response.status_code == 200
    assert judge.is_active is False


@pytest.mark.django_db
def test_create_room_view(user):
    """проверяет создание новой комнаты"""
    client = Client()
    client.force_login(user)
    create_room_url = reverse("referee:create_room")

    response = client.post(create_room_url, {"name": "New Room"})
    assert response.status_code == 302  # перенаправление после успешного создания
    assert Room.objects.filter(name="New Room", boss=user).exists()


@pytest.mark.django_db
def test_my_rooms_view(user, room):
    """проверяет, что пользователь видит только свои комнаты"""
    client = Client()
    client.force_login(user)
    my_rooms_url = reverse("referee:my_rooms")

    response = client.get(my_rooms_url)
    assert response.status_code == 200
    assert "Test Room" in response.content.decode()


@pytest.mark.django_db
def test_delete_room_view(user, room):
    """проверяет удаление комнаты"""
    client = Client()
    client.force_login(user)
    delete_room_url = reverse("referee:delete_room", kwargs={"uuid_room": room.uuid_room})

    response = client.post(delete_room_url)
    assert response.status_code == 200
    assert not Room.objects.filter(uuid_room=room.uuid_room).exists()


@pytest.mark.django_db
def test_join_room_view(user, room):
    """проверяет успешное подключение к комнате"""
    client = Client()
    client.force_login(user)
    join_room_url = reverse("referee:join_room")

    response = client.post(join_room_url, {"uuid_room": room.uuid_room})
    assert response.status_code == 302  # перенаправление на страницу комнаты


@pytest.mark.django_db
def test_join_non_existent_room_view(user):
    """проверяет ошибку при попытке войти в несуществующую комнату"""
    client = Client()
    client.force_login(user)
    join_room_url = reverse("referee:join_room")
    fake_uuid = str(uuid.uuid4())

    response = client.post(join_room_url, {"uuid_room": fake_uuid})
    assert response.status_code == 200
    assert "Комната не найдена" in response.context["error"]


@pytest.mark.django_db
def test_detail_room_view(user, room, fight, judge):
    """проверяет отображение страницы комнаты"""
    client = Client()
    client.force_login(user)
    detail_room_url = reverse("referee:detail_room", kwargs={"uuid_room": room.uuid_room})

    response = client.get(detail_room_url)
    assert response.status_code == 200
    assert "ЛИНК:" in response.content.decode()


@pytest.mark.django_db
def test_create_fight_view(client, user, room):
    """проверяет создание нового боя"""
    client.force_login(user)
    create_fight_url = reverse("referee:create_fight", kwargs={"uuid_room": room.uuid_room})

    # создаём первый бой (должно сработать)
    response = client.post(create_fight_url, {
        "number_fight": 1,
        "fighter_1": "Fighter A",
        "fighter_2": "Fighter B",
    })
    assert response.status_code == 200
    assert Fight.objects.filter(room=room, number_fight=1).exists()

    # пытаемся создать бой с уже занятым номером (должно вернуть ошибку)
    response = client.post(create_fight_url, {
        "number_fight": 1,
        "fighter_1": "Fighter X",
        "fighter_2": "Fighter Y",
    })
    assert response.status_code == 400
    assert "Номер боя занят" in response.json()["error"]


@pytest.mark.django_db
def test_edit_fight_view(client, user, fight):
    """проверяет редактирование существующего боя"""
    client.force_login(user)
    edit_fight_url = reverse("referee:edit_fight", kwargs={"uuid_fight": fight.uuid})

    # обновляем информацию о бое
    response = client.post(edit_fight_url, {
        "number_fight": 2,
        "fighter_1": "Updated Fighter A",
        "fighter_2": "Updated Fighter B",
    })
    assert response.status_code == 200

    # проверяем, что данные обновились
    fight.refresh_from_db()
    assert fight.number_fight == 2
    assert fight.fighter_1 == "Updated Fighter A"
    assert fight.fighter_2 == "Updated Fighter B"


@pytest.mark.django_db
def test_delete_fight_view(client, user, fight):
    """проверяет удаление боя"""
    client.force_login(user)
    delete_fight_url = reverse("referee:delete_fight", kwargs={"uuid_fight": fight.uuid})

    # удаляем бой (должно сработать)
    response = client.post(delete_fight_url)
    assert response.status_code == 200
    assert not Fight.objects.filter(uuid=fight.uuid).exists()

    # пытаемся удалить несуществующий бой (должно вернуть 404)
    response = client.post(delete_fight_url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_winner_fight_view(client, user, fight):
    """проверяет назначение победителя боя"""
    client.force_login(user)
    winner_fight_url = reverse("referee:winner_fight", kwargs={"uuid_fight": fight.uuid})

    # назначаем победителя "fighter_1"
    response = client.post(winner_fight_url, json.dumps({"winner": "fighter_1"}), content_type="application/json")
    assert response.status_code == 200
    fight.refresh_from_db()
    assert fight.winner == "fighter_1"

    # меняем победителя на "fighter_2"
    response = client.post(winner_fight_url, json.dumps({"winner": "fighter_2"}), content_type="application/json")
    assert response.status_code == 200
    fight.refresh_from_db()
    assert fight.winner == "fighter_2"


@pytest.mark.django_db
def test_create_note_view(client, user, fight, judge):
    """проверяет создание записки по бою"""
    client.force_login(user)
    judge.is_active = True
    judge.save()
    create_note_url = reverse("referee:create_note")

    # создаём записку (должно сработать)
    response = client.post(create_note_url, json.dumps({
        "fight_id": str(fight.uuid),
        "round": 1,
        "red_remark": "Good strike",
        "blue_remark": "Defense improved",
        "winner": "red"
    }), content_type="application/json")
    assert response.status_code == 200
    assert Notes.objects.filter(fight=fight, round_number=1).exists()

    # отправляем некорректные данные (должно вернуть 400)
    response = client.post(create_note_url, "not a json", content_type="application/json")
    assert response.status_code == 400
    assert "Ошибка обработки JSON" in response.json()["error"]


@pytest.mark.django_db
def test_fight_notes_view(client, user, note):
    """проверяет получение записок для конкретного боя"""
    client.force_login(user)
    fight_notes_url = reverse("referee:fight_notes",
                              kwargs={"fight_uuid": note.fight.uuid, "round_number": note.round_number})

    # получаем записки (должно вернуть успех)
    response = client.get(fight_notes_url)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(response.json()["notes"]) == 1
    assert response.json()["notes"][0]["red_remark"] == "C1"
    assert response.json()["notes"][0]["blue_remark"] == "C1 C1"

    # запрашиваем записки для несуществующего раунда (должно вернуть ошибку)
    invalid_fight_notes_url = reverse("referee:fight_notes", kwargs={"fight_uuid": note.fight.uuid, "round_number": 99})
    response = client.get(invalid_fight_notes_url)
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Нет записок для этого раунда." in response.json()["message"]

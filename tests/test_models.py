import pytest
from referee.models import Room, RoomJudges, Fight, Notes
from users.models import User


@pytest.mark.django_db
def test_create_user(user):
    assert User.objects.count() == 1
    assert user.username == "test_user"


@pytest.mark.django_db
def test_create_room(room):
    assert Room.objects.count() == 1
    assert room.name == "Test Room"
    assert room.boss.username == "test_user"


@pytest.mark.django_db
def test_create_judge(judge, room):
    assert RoomJudges.objects.count() == 1
    assert judge.room == room
    assert judge.is_active is True


@pytest.mark.django_db
def test_create_fight(fight, room):
    assert Fight.objects.count() == 1
    assert fight.room == room
    assert fight.number_fight == 1
    assert fight.fighter_1 == "Fighter A"
    assert fight.fighter_2 == "Fighter B"


@pytest.mark.django_db
def test_create_note(note, fight, judge):
    assert Notes.objects.count() == 1
    assert note.fight == fight
    assert note.judge == "Judge 1"
    assert note.round_number == 1
    assert note.winner == "red"

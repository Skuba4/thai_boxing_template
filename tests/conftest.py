import pytest
from users.models import User
from referee.models import Room, RoomJudges, Fight, Notes


@pytest.fixture
def user():
    return User.objects.create_user(username="test_user", password="testpassword")


@pytest.fixture
def room(user):
    return Room.objects.create(name="Test Room", boss=user)


@pytest.fixture
def judge(user, room):
    return RoomJudges.objects.create(room=room, user=user, is_active=True)


@pytest.fixture
def fight(room):
    return Fight.objects.create(
        room=room,
        number_fight=1,
        fighter_1="Fighter A",
        fighter_2="Fighter B"
    )


@pytest.fixture
def note(fight):
    return Notes.objects.create(
        fight=fight,
        judge="Judge 1",
        round_number=1,
        red_fighter=fight.fighter_1,
        blue_fighter=fight.fighter_2,
        red_remark="C1",
        blue_remark="C1 C1",
        winner="red"
    )

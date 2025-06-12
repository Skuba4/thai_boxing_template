from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Fight, Room, RoomJudges


class JsonResponseMixin:
    """Генерация JSON-ответов"""

    def render_json_response(self, success, status=200, **kwargs):
        return JsonResponse({'success': success, **kwargs}, status=status)


class RoomMixin:
    """Получение объекта комнаты"""

    def get_room(self, uuid_room):
        return get_object_or_404(Room, uuid_room=uuid_room)


class FightMixin:
    """Получение объекта Fight по UUID"""

    def get_fight(self, uuid_fight):
        return get_object_or_404(Fight, uuid=uuid_fight)


class JudgeMixin(RoomMixin):
    """Работа с судьями"""

    def get_judge(self, uuid_room, judge_id):
        room = self.get_room(uuid_room)
        return get_object_or_404(RoomJudges, room=room, user_id=judge_id)


class RoomContextMixin:
    """Создаёт контекст с боями и статусом пользователя"""

    def get_room_context(self, room):
        return {
            'fights': Fight.objects.filter(room=room),
            'is_boss': self.request.user == room.boss,
            'is_active_judge': RoomJudges.objects.filter(room=room, user=self.request.user, is_active=True).exists(),
        }


class FightDataMixin:
    """Создаёт контекст с записками боёв"""

    def get_fight_notes(self, fight, user):
        notes = fight.notes.filter(judge=user).values_list('round_number', flat=True)
        return {
            "fight": fight,
            "round_1": 1 in notes,
            "round_2": 2 in notes,
            "round_3": 3 in notes,
        }

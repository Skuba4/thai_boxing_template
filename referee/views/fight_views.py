import json

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404

from referee.models import Fight, Notes
from ..mixins import FightMixin, RoomContextMixin, JsonResponseMixin, RoomMixin

__all__ = ['CreateFight', 'EditFight', 'DeleteFight', 'WinnerFight', 'CreateNote', 'FightNotes']


class CreateFight(LoginRequiredMixin, RoomMixin, RoomContextMixin, JsonResponseMixin, View):
    def post(self, request, uuid_room):
        room = self.get_room(uuid_room)

        try:
            Fight.objects.create(
                room=room,
                number_fight=request.POST['number_fight'],
                fighter_1=request.POST['fighter_1'],
                fighter_2=request.POST['fighter_2']
            )
        except IntegrityError:
            return self.render_json_response(False, error="Номер боя занят", status=400)

        fights_html = render_to_string('referee/includes/fights_list.html', self.get_room_context(room),
                                       request=request)
        return self.render_json_response(True, fights_html=fights_html)


class EditFight(LoginRequiredMixin, FightMixin, RoomContextMixin, JsonResponseMixin, View):
    def post(self, request, uuid_fight):
        fight = self.get_fight(uuid_fight)

        try:
            fight.number_fight = request.POST['number_fight']
            fight.fighter_1 = request.POST['fighter_1']
            fight.fighter_2 = request.POST['fighter_2']
            fight.full_clean()
            fight.save()
        except ValidationError as V:
            return self.render_json_response(False, error=str(V), status=400)
        except IntegrityError:
            return self.render_json_response(False, error="Номер боя занят", status=400)

        fights_html = render_to_string('referee/includes/fights_list.html', self.get_room_context(fight.room),
                                       request=request)
        return self.render_json_response(True, fights_html=fights_html)


class DeleteFight(LoginRequiredMixin, FightMixin, RoomContextMixin, JsonResponseMixin, View):
    def post(self, request, uuid_fight):
        fight = self.get_fight(uuid_fight)

        if fight.room.boss != request.user:
            return self.render_json_response(False, error="Ты не главный судья!", status=403)

        fight.delete()

        fights_html = render_to_string('referee/includes/fights_list.html', self.get_room_context(fight.room),
                                       request=request)
        return self.render_json_response(True, fights_html=fights_html)


class WinnerFight(LoginRequiredMixin, FightMixin, RoomContextMixin, JsonResponseMixin, View):
    def post(self, request, uuid_fight):
        fight = self.get_fight(uuid_fight)

        try:
            fight.winner = json.loads(request.body).get('winner')
            fight.full_clean()
            fight.save()
        except ValidationError as V:
            return self.render_json_response(False, error=str(V), status=400)

        fights_html = render_to_string('referee/includes/fights_list.html', self.get_room_context(fight.room),
                                       request=request)
        return self.render_json_response(True, fights_html=fights_html)


class CreateNote(LoginRequiredMixin, JsonResponseMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            fight = get_object_or_404(Fight, uuid=data.get("fight_id"))
            judge = request.user

            if not fight.room.judges.filter(id=judge.id).exists():
                return self.render_json_response(False, error="Ты не судья!", status=403)

            Notes.objects.create(
                fight=fight,
                judge=judge.username,
                red_fighter=fight.fighter_1,
                blue_fighter=fight.fighter_2,
                round_number=int(data.get("round")),
                red_remark=data.get("red_remark", ""),
                blue_remark=data.get("blue_remark", ""),
                winner=data.get("winner"),
            )
            return self.render_json_response(True)

        except json.JSONDecodeError:
            return self.render_json_response(False, error="Ошибка обработки JSON", status=400)
        except Exception as e:
            return self.render_json_response(False, error=str(e), status=500)


class FightNotes(LoginRequiredMixin, View):
    def get(self, request, fight_uuid, round_number):
        notes_queryset = Notes.objects.filter(fight=get_object_or_404(Fight, uuid=fight_uuid),
                                              round_number=round_number)
        if not notes_queryset.exists():
            return JsonResponse({"success": False, "message": "Нет записок для этого раунда."})

        # list comprehension
        notes_list = [
            {
                "date": note.data.strftime("%Y-%m-%d") if note.data else "",
                "judge": note.judge,
                "round_number": note.round_number,
                "red_fighter": note.red_fighter,
                "blue_fighter": note.blue_fighter,
                "red_remark": note.red_remark,
                "blue_remark": note.blue_remark,
                "winner": note.get_winner_display(),
            }
            for note in notes_queryset
        ]

        return JsonResponse({"success": True, "notes": notes_list})

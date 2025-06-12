import json
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404

from referee.mixins import JudgeMixin, JsonResponseMixin, RoomMixin
from referee.models import Room, RoomJudges
from users.models import User

__all__ = ['AddJudge', 'DeleteJudge', 'ActiveJudge']


class AddJudge(LoginRequiredMixin, RoomMixin, JsonResponseMixin, View):
    def post(self, request, uuid_room):
        room = self.get_room(uuid_room)

        try:
            username = json.loads(request.body).get('username')
        except json.JSONDecodeError:
            return self.render_json_response(False, error="Ошибка чтения JSON", status=400)

        user_to_add = User.objects.filter(username=username).first()
        if not user_to_add:
            return self.render_json_response(False, error="Пользователь не найден", status=404)

        if RoomJudges.objects.filter(room=room, user=user_to_add).exists():
            return self.render_json_response(False, error="Этот судья уже добавлен", status=400)

        if user_to_add == request.user:
            return self.render_json_response(False, error="Вы не можете добавить себя как судью.", status=400)
        RoomJudges.objects.create(room=room, user=user_to_add)

        judges_html = render_to_string('referee/includes/judges_list.html',
                                       {'judges': RoomJudges.objects.filter(room=room)}, request=request)
        return self.render_json_response(True, judges_html=judges_html)


class DeleteJudge(LoginRequiredMixin, JudgeMixin, JsonResponseMixin, View):
    def post(self, request, uuid_room, judge_id):
        try:
            judge = self.get_judge(uuid_room, judge_id)
            judge.delete()
            judges_html = render_to_string(
                'referee/includes/judges_list.html',
                {'judges': RoomJudges.objects.filter(room=judge.room)},
                request=request
            )
            return self.render_json_response(True, judges_html=judges_html)
        except (RoomJudges.DoesNotExist, Http404):
            return self.render_json_response(False, error="Судья не найден", status=404)
        except Exception as e:
            return self.render_json_response(False, error=f"Ошибка удаления судьи: {str(e)}", status=500)


class ActiveJudge(LoginRequiredMixin, View):
    def post(self, request, uuid_room, judge_id):
        room = get_object_or_404(Room, uuid_room=uuid_room)
        judge = get_object_or_404(RoomJudges, room=room, user_id=judge_id)

        if not judge.is_active:
            active_judges_count = RoomJudges.objects.filter(room=room, is_active=True).count()
            if active_judges_count >= 3:
                return JsonResponse({'success': False, 'error': 'Можно выбрать не более 3 активных судей.'})
            judge.is_active = True
        else:
            judge.is_active = False
        judge.save()

        judges_html = render_to_string('referee/includes/judges_list.html',
                                       {'judges': RoomJudges.objects.filter(room=room)}, request=request)

        return JsonResponse({'success': True, 'judges_html': judges_html})

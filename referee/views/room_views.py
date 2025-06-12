from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from referee.forms import CreateRoomForm
from referee.mixins import RoomMixin, FightDataMixin
from referee.models import Room, RoomJudges, Fight

__all__ = ['CreateRoom', 'MyRooms', 'DeleteRoom', 'JoinRoom', 'DetailRoom']


class CreateRoom(LoginRequiredMixin, CreateView):
    model = Room
    template_name = 'referee/create_room.html'
    form_class = CreateRoomForm

    def form_valid(self, form):
        '''form.instance(объект Room), .boss(обратились к полю главного судьи), self.request.user(и присвоили текущего пользователя)'''
        form.instance.boss = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('referee:detail_room', kwargs={'uuid_room': self.object.uuid_room})


class MyRooms(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'referee/my_rooms.html'
    context_object_name = 'object'

    def get_queryset(self):
        '''Кастомный список (по умолчанию Room.objects.all())'''
        return Room.objects.filter(boss=self.request.user)


class DeleteRoom(LoginRequiredMixin, View):
    def post(self, request, uuid_room):
        get_object_or_404(Room, uuid_room=uuid_room, boss=request.user).delete()

        rooms_html = render_to_string('referee/includes/room_list.html',
                                      {'object': Room.objects.filter(boss=request.user)}, request=request)

        return JsonResponse({'success': True, 'rooms_html': rooms_html})


class JoinRoom(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'referee/join_room.html')

    def post(self, request):
        uuid_room = request.POST.get('uuid_room')

        try:
            Room.objects.get(uuid_room=uuid_room)
            return redirect('referee:detail_room', uuid_room=uuid_room)
        except Room.DoesNotExist:
            return render(request, 'referee/join_room.html', {'error': 'Комната не найдена'})


class DetailRoom(LoginRequiredMixin, RoomMixin, FightDataMixin, View):
    def get(self, request, uuid_room):
        room = self.get_room(uuid_room)

        fights = Fight.objects.filter(room=room)
        fights_data = [self.get_fight_notes(fight, request.user) for fight in fights]

        context = {
            "object": room,
            "uuid": room.uuid_room,
            "is_boss": request.user == room.boss,
            "is_active_judge": RoomJudges.objects.filter(room=room, user=request.user, is_active=True).exists(),
            "judges": RoomJudges.objects.filter(room=room),
            "fights": fights,
            "fights_data": fights_data,
        }

        return render(request, "referee/detail_room.html", context)

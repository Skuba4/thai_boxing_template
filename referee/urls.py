from django.urls import path
from .views import *

app_name = 'referee'

urlpatterns = [
    # base
    path('', Home.as_view(), name='home'),
    # room_views
    path('crate_room/', CreateRoom.as_view(), name='create_room'),
    path('my_rooms/', MyRooms.as_view(), name='my_rooms'),
    path('delete_room/<uuid:uuid_room>/', DeleteRoom.as_view(), name='delete_room'),
    path('join_room/', JoinRoom.as_view(), name='join_room'),
    path('room/<uuid:uuid_room>/', DetailRoom.as_view(), name='detail_room'),
    # fight_views
    path('create_fight/<uuid:uuid_room>/', CreateFight.as_view(), name='create_fight'),
    path('delete_fight/<uuid:uuid_fight>/', DeleteFight.as_view(), name='delete_fight'),
    path('edit/<uuid:uuid_fight>/', EditFight.as_view(), name='edit_fight'),
    path('set_winner/<uuid:uuid_fight>/', WinnerFight.as_view(), name='winner_fight'),
    path('create_note/', CreateNote.as_view(), name='create_note'),
    path("notes/<uuid:fight_uuid>/<int:round_number>/", FightNotes.as_view(), name="fight_notes"),
    # judge_views
    path('add_judge/<uuid:uuid_room>/', AddJudge.as_view(), name='add_judge'),
    path('delete_judge/<uuid:uuid_room>/<int:judge_id>/', DeleteJudge.as_view(), name='delete_judge'),
    path('active_judge/<uuid:uuid_room>/<int:judge_id>/', ActiveJudge.as_view(), name='active_judge'),
]

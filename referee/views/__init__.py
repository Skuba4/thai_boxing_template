from . import room_views, fight_views, judge_views, base

from .room_views import *
from .fight_views import *
from .judge_views import *
from .base import *

__all__ = (
        base.__all__ +
        room_views.__all__ +
        fight_views.__all__ +
        judge_views.__all__
)

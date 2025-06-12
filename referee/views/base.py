from django.views.generic import TemplateView

__all__ = ['Home']


class Home(TemplateView):
    template_name = 'referee/home.html'

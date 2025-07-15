from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeViews(TemplateView):
    template_name = 'core/index.html' # Archivo html que se muestra
    contexto = {
        'title': 'Hands Unmuted',
        'bootcamp': 'Inteligencia Artificial Explorador',
        'author': 'Sara Herrera & Julian Polanco',
        'version': '1.0.0'
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)

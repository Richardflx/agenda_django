from django.shortcuts import render, HttpResponse
from .models import Evento

# Create your views here.
def evento(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(f'Descrição do evento: {evento.descricao if evento.descricao else "Sem descrição"}')

def lista_eventos(request):
    evento = Evento.objects.all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Evento

# Create your views here.
def evento(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(f'Descrição do evento: {evento.descricao if evento.descricao else "Sem descrição"}')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("/")
        else:
            messages.error(request, 'Usuário ou Senha inválido')
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo_evento')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local_evento = request.POST.get('local_evento')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local_evento = local_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                             data_evento=data_evento,
            #                                             descricao=descricao,
            #                                             local_evento=local_evento)
        else:
            Evento.objects.create(titulo=titulo,
                                    data_evento=data_evento,
                                    descricao=descricao,
                                    local_evento=local_evento,
                                    usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')
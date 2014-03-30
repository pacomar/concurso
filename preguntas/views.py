from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from preguntas.models import *
from preguntas.forms import *
import datetime
from random import randint

def inicio(request):
	ctx = {}
	return render(request, 'inicio.html', ctx)

def comienza(request):
	if request.method=='POST':
		formulario=ComienzaForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			con = Concurso.objects.create(nombre=nom)
			return HttpResponseRedirect('/pregunta/'+str(con.id))
	else:
		formulario = ComienzaForm()
	ctx = {'formulario':formulario}
	return render(request, 'comienza.html', ctx)

@staff_member_required
def nueva_pregunta(request):
	if request.method=='POST':
		formulario=PreguntaForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return redirect('/nueva')
	else:
		formulario = PreguntaForm()
	ctx = {'formulario':formulario}
	return render(request, 'nueva.html', ctx)

def siguiente_pregunta(request, id_concurso):
	con = get_object_or_404(Concurso, id = id_concurso)
	if not con.terminado:
		if len(con.preguntas.all()) < 5:
			pres = Pregunta.objects.filter(dificultad='1').exclude(id__in=con.preguntas.all())
		elif len(con.preguntas.all()) < 10:
			pres = Pregunta.objects.filter(dificultad='2').exclude(id__in=con.preguntas.all())
		elif len(con.preguntas.all()) < 15:
			pres = Pregunta.objects.filter(dificultad='3').exclude(id__in=con.preguntas.all())
		elif len(con.preguntas.all()) < 19:
			pres = Pregunta.objects.filter(dificultad='4').exclude(id__in=con.preguntas.all())
		else:
			return redirect('/termina/'+str(con.id))
		if not pres:
			return redirect('/termina/'+str(con.id))
		pregunta = pres[randint(0,len(pres)-1)]
		con.preguntas.add(pregunta)
		con.save()
		ctx = {'pregunta':pregunta, 'concurso':con}
		return render(request, 'pregunta.html', ctx)
	else:
		return redirect('/')

def ranking(request):
	cons = Concurso.objects.order_by('-puntuacion', 'duracion')
	dias = []
	for c in cons:
		dias.append(c.hora_fin.date())
	dias = set(dias)
	cons = Concurso.objects.order_by('-puntuacion', 'duracion')[:30]
	ctx = {'resultados':cons, 'dias':dias}
	return render(request, 'ranking.html', ctx)

def ranking_dia(request, dia, mes, ano):
	cons = Concurso.objects.order_by('-puntuacion', 'duracion')[:30]
	dias = []
	for c in cons:
		dias.append(c.hora_fin.date())
	dias = set(dias)
	cons = Concurso.objects.filter(hora_fin__day=int(dia), hora_fin__month=int(mes), hora_fin__year=int(ano)).order_by('-puntuacion', 'duracion')[:30]
	ctx = {'resultados':cons, 'dias':dias}
	return render(request, 'ranking.html', ctx)

def responde(request, id_concurso, pregunta_id, pregunta_res):
	con = get_object_or_404(Concurso, id=id_concurso)
	pre = get_object_or_404(Pregunta, id=pregunta_id)
	if pregunta_res == pre.correcta:
		con.puntuacion = con.puntuacion + 1
		con.save()
	return redirect('/pregunta/'+str(con.id))

def terminar(request, id_concurso):
	con = get_object_or_404(Concurso, id=id_concurso)
	if not con.terminado:
		con.terminado = True
		tmp = con.hora_fin - con.hora_inicio
		con.duracion = tmp.seconds / 60.0
		con.save()
	ctx = {'concurso':con}
	return render(request, 'fin.html', ctx)
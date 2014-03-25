from django.db import models

PREGUNTAS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)
DIFICULTADES = (
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
)

class Pregunta(models.Model):
	pregunta = models.CharField(max_length=200)
	res1 = models.CharField(max_length=200)
	res2 = models.CharField(max_length=200)
	res3 = models.CharField(max_length=200)
	res4 = models.CharField(max_length=200)
	correcta = models.CharField(max_length=200, choices=PREGUNTAS)
	dificultad = models.CharField(max_length=200, choices=DIFICULTADES)

	def __unicode__(self):
		return self.pregunta+" "+self.dificultad

class Concurso(models.Model):
	comodin = models.BooleanField(default=True)
	puntuacion = models.IntegerField(default=0)
	preguntas = models.ManyToManyField('Pregunta', blank=True, null=True)
	nombre = models.CharField(max_length=200)
	hora_inicio = models.DateTimeField(auto_now_add=True)
	hora_fin = models.DateTimeField(auto_now=True)
	terminado = models.BooleanField(default=False)
	duracion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

	def __unicode__(self):
		return self.nombre+" "+str(self.puntuacion)
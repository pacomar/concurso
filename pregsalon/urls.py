from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'preguntas.views.inicio', name='home'),
	url(r'^comienza/$', 'preguntas.views.comienza', name='home'),
	url(r'^pregunta/(?P<id_concurso>\d+)$','preguntas.views.siguiente_pregunta'),
	url(r'^responde/(?P<id_concurso>\d+)/(?P<pregunta_id>\d+)/(?P<pregunta_res>\d+)/$','preguntas.views.responde'),
	url(r'^termina/(?P<id_concurso>\d+)$','preguntas.views.terminar'),
	url(r'^ranking/$','preguntas.views.ranking'),
	url(r'^nueva/$', 'preguntas.views.nueva_pregunta'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	)
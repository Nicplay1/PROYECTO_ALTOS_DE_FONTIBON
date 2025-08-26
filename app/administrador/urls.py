from django.urls import path
from . import views
urlpatterns = [
path("gestionar/", views.gestionar_usuarios, name="gestionar_usuarios"),
path("reservas/gestionar/", views.gestionar_reservas, name="gestionar_reservas"),
path("noticias/", views.listar_noticias, name="listar_noticias"),
path("noticias/editar/<int:id_noticia>/", views.editar_noticia, name="editar_noticia"),
path("noticias/eliminar/<int:id_noticia>/", views.eliminar_noticia, name="eliminar_noticia"),
]
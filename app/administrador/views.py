from django.shortcuts import render, redirect, get_object_or_404
from usuario.models import *
from usuario.decorators import login_requerido
from django.contrib import messages
from .forms import *

# Create your views here.
@login_requerido
def gestionar_usuarios(request):
    usuarios = Usuario.objects.select_related("id_rol").all()

    if request.method == "POST":
        usuario_id = request.POST.get("usuario_id")
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        form = CambiarRolForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Rol de {usuario.nombres} actualizado correctamente.")
            return redirect("gestionar_usuarios")
    else:
        form = CambiarRolForm()

    return render(request, "administrador/gestionar_usuarios.html", {
        "usuarios": usuarios,
        "form": form,
        "roles": Rol.objects.all()
    })

@login_requerido
def gestionar_reservas(request):
    reservas = Reserva.objects.select_related("cod_usuario", "cod_zona").all()

    if request.method == "POST":
        reserva_id = request.POST.get("reserva_id")
        reserva = get_object_or_404(Reserva, pk=reserva_id)
        form = EditarReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f"Reserva {reserva.id_reserva} actualizada correctamente.")
            return redirect("gestionar_reservas")
    else:
        form = EditarReservaForm()

    return render(request, "administrador/gestionar_reservas.html", {
        "reservas": reservas,
        "form": form
    })



@login_requerido
def listar_noticias(request):
    noticias = Noticias.objects.all().order_by("-fecha_publicacion")

    if request.method == "POST":
        form = NoticiasForm(request.POST)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.cod_usuario = request.usuario  # 👈 usar el decorador, no request.user
            noticia.save()
            messages.success(request, "Noticia creada exitosamente.")
            return redirect("listar_noticias")
    else:
        form = NoticiasForm()

    return render(request, "administrador/noticias/listar.html", {
        "noticias": noticias,
        "form": form,
    })

# EDITAR
@login_requerido
def editar_noticia(request, id_noticia):
    noticia = get_object_or_404(Noticias, id_noticia=id_noticia)

    if request.method == "POST":
        form = NoticiasForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            messages.success(request, "Noticia actualizada correctamente ✏️")
            return redirect("listar_noticias")
    else:
        form = NoticiasForm(instance=noticia)

    return render(request, "administrador/noticias/editar.html", {
        "form": form,
        "noticia": noticia
    })

# ELIMINAR
@login_requerido
def eliminar_noticia(request, id_noticia):
    noticia = get_object_or_404(Noticias, id_noticia=id_noticia)
    noticia.delete()
    messages.success(request, "Noticia eliminada 🗑️")
    return redirect("listar_noticias")
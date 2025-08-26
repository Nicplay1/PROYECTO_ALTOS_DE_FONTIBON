from django.shortcuts import render, redirect,get_object_or_404
from usuario.models import *
from usuario.decorators import login_requerido
from .forms import *
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
@login_requerido
def detalle_residente(request):
    """
    Si el residente ya tiene detalle → mostrar últimas 2 noticias.
    Si no → mostrar formulario para registrar detalles.
    """
    usuario = request.usuario
    detalle = DetalleResidente.objects.filter(cod_usuario=usuario).first()

    # Si ya tiene detalle → mostrar las noticias
    if detalle:
        noticias = Noticias.objects.all().order_by("-fecha_publicacion")[:2]  # 🔥 Solo las 2 últimas
        return render(request, "residente/detalles_residente/noticias.html", {
            "usuario": usuario,
            "detalle": detalle,
            "noticias": noticias,
        })

    # Si no tiene → permitir registrar
    if request.method == "POST":
        form = DetalleResidenteForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.cod_usuario = usuario
            detalle.save()
            messages.success(request, "Detalles de residente registrados correctamente.")
            return redirect("detalle_residente")  # redirige para ahora sí ver noticias
    else:
        form = DetalleResidenteForm()

    return render(
        request,
        "residente/detalles_residente/registrar_detalle_residente.html",
        {"form": form}
    )



@login_requerido
def listar_zonas(request):
    zonas = ZonaComun.objects.all()
    return render(request, "residente/zonas_comunes/listar_zonas.html", {"zonas": zonas})

# Crear reserva
@login_requerido
def crear_reserva(request, id_zona):
    zona = get_object_or_404(ZonaComun, pk=id_zona)

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_uso = form.cleaned_data['fecha_uso']

            # Validar SOLO si la zona es 6, 12 o 13
            if zona.id_zona in [6, 12, 13] and Reserva.objects.filter(cod_zona=zona, fecha_uso=fecha_uso).exists():
                messages.error(request, "Ya existe una reserva para esta fecha en la zona seleccionada.")
            else:
                reserva = form.save(commit=False)
                reserva.cod_usuario = request.usuario   # 👈 usamos el usuario de tu decorador
                reserva.cod_zona = zona
                reserva.estado = "En espera"
                reserva.forma_pago = "Efectivo"
                reserva.save()
                messages.success(request, "Reserva creada correctamente.")
                return redirect("mis_reservas")
        else:
            print("ERRORES:", form.errors)
            messages.error(request, "Error al crear la reserva. Revisa los datos.")
    else:
        form = ReservaForm()

    return render(request, "residente/zonas_comunes/crear_reserva.html", {
        "form": form,
        "zona": zona
    })


@login_requerido
def fechas_ocupadas(request, id_zona):
    zona = get_object_or_404(ZonaComun, pk=id_zona)

    # Solo marcar "ocupado" si la zona pertenece a los ids 6, 12 o 13
    if zona.id_zona in [6, 12, 13]:
        reservas = Reserva.objects.filter(cod_zona=zona).values_list("fecha_uso", flat=True)
    else:
        reservas = []  # las demás zonas siempre aparecen libres

    return JsonResponse({"fechas": list(reservas)})

# Detalle de la reserva
@login_requerido
def mis_reservas(request):
    usuario = request.usuario
    reservas = Reserva.objects.filter(cod_usuario=usuario).select_related("cod_zona")
    return render(request, "residente/zonas_comunes/detalle_reserva.html", {"reservas": reservas})

@login_requerido
def eliminar_reserva(request, id_reserva):
    # Traemos la reserva (siempre debe existir)
    reserva = get_object_or_404(Reserva, pk=id_reserva)

    # Validación: si es residente, solo puede eliminar sus propias reservas
    if request.usuario.id_rol.id_rol == 2 and reserva.cod_usuario != request.usuario:
        messages.error(request, "No puedes eliminar esta reserva.")
        return redirect("mis_reservas")

    if request.method == "POST":
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")

        # Redirección dependiendo del rol
        if request.usuario.id_rol.id_rol == 3:  # Administrador
            return redirect("gestionar_reservas")
        elif request.usuario.id_rol.id_rol == 2:  # Residente
            return redirect("mis_reservas")

    messages.error(request, "No se pudo eliminar la reserva.")

    # Redirección segura por rol
    if request.usuario.id_rol.id_rol == 3:
        return redirect("gestionar_reservas")
    else:
        return redirect("mis_reservas")




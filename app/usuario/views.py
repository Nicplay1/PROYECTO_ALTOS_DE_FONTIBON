from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import*
from .forms import*
from .decorators import login_requerido
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            numero_documento = form.cleaned_data['numero_documento']
            if Usuario.objects.filter(numero_documento=numero_documento).exists():
                messages.error(request, "El documento ya está registrado.")
            else:
                usuario = form.save(commit=False)
                usuario.contraseña = make_password(form.cleaned_data['contraseña'])
                usuario.save()
                messages.success(request, "Usuario registrado exitosamente. Ahora puede iniciar sesión.")
                return redirect("login")
        else:
            messages.error(request, "Error en el registro. Verifique los datos.")
    else:
        form = RegisterForm()
    return render(request, "usuario/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_documento = form.cleaned_data['numero_documento']
            contraseña = form.cleaned_data['contraseña']

            try:
                usuario = Usuario.objects.get(numero_documento=numero_documento)
                if check_password(contraseña, usuario.contraseña):
                    request.session['usuario_id'] = usuario.id_usuario
                    request.session['rol_id'] = usuario.id_rol_id
                    messages.success(request, f"Bienvenido {usuario.nombres} {usuario.apellidos}!")

                    # Redirección según rol
                    if usuario.id_rol_id == 1:
                        return redirect("index")
                    elif usuario.id_rol_id == 2:
                        return redirect("detalle_residente")
                    elif usuario.id_rol_id == 3:
                        return redirect("gestionar_usuarios")
                    elif usuario.id_rol_id == 4:
                        return redirect("vigilante_home")
                    elif usuario.id_rol_id == 5:
                        return redirect("asistente_home")
                else:
                    messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                messages.error(request, "Documento no registrado.")
    else:
        form = LoginForm()
    return render(request, "usuario/login.html", {"form": form})

def logout_view(request):
    # Elimina todas las variables de sesión
    request.session.flush()
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")





@login_requerido
def perfil_usuario(request):
    usuario = request.usuario
    residente = get_object_or_404(DetalleResidente, cod_usuario=usuario)

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('perfil_usuario')
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, 'usuario/perfil.html', {
        'usuario': usuario,
        'residente': residente,
        'form': form
    })


@login_requerido
def cambiar_contrasena(request):
    if request.method == 'POST':
        nueva = request.POST.get('nueva_contraseña')
        confirmar = request.POST.get('confirmar_contraseña')

        if nueva and nueva == confirmar:
            user = request.usuario

            # 🔑 Encripta la contraseña siempre
            user.contraseña = make_password(nueva)
            user.save()

            messages.success(request, "Contraseña actualizada correctamente.")
        else:
            messages.error(request, "Las contraseñas no coinciden.")

    return redirect('perfil_usuario')

def index(request):
    return render(request, 'usuario/index.html')

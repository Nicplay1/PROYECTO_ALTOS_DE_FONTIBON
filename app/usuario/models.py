from django.db import models


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Rol'

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_documento = models.CharField(
        max_length=20,
        choices=[('CC', 'CC'), ('CE', 'CE'), ('TI', 'TI'), ('Pasaporte', 'Pasaporte')]
    )
    numero_documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=13)
    celular = models.CharField(max_length=13)
    estado = models.CharField(max_length=10, default='Activo')
    contraseña = models.CharField(max_length=250, null=True, blank=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='ID_rol', default=1)

    class Meta:
        managed = False
        db_table = 'Usuario'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class ZonaComun(models.Model):
    id_zona = models.AutoField(primary_key=True)
    nombre_zona = models.CharField(max_length=20)
    capacidad = models.IntegerField()
    tipo_pago = models.CharField(
        max_length=20,
        choices=[('Por hora', 'Por hora'), ('Franja horaria', 'Franja horaria'), ('Evento', 'Evento')]
    )
    estado = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'Zona_comun'

    def __str__(self):
        return self.nombre_zona


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=15,
        choices=[('Rechazada', 'Rechazada'), ('Aprobada', 'Aprobada'), ('En espera', 'En espera')],
        default='En espera'
    )
    
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateField()
    observacion = models.CharField(max_length=255, null=True, blank=True)
    forma_pago = models.CharField(
    max_length=20,
    choices=[('Transferencia', 'Transferencia'), ('Efectivo', 'Efectivo')],
    null=True, blank=True   # 👈 agrega esto
)
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')
    cod_zona = models.ForeignKey(ZonaComun, on_delete=models.CASCADE, db_column='cod_zona')

    class Meta:
        managed = False
        db_table = 'Reserva'

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.cod_usuario}"


class DetalleResidente(models.Model):
    id_detalle_residente = models.AutoField(primary_key=True)
    propietario = models.BooleanField(default=True)
    apartamento = models.IntegerField()
    torre = models.IntegerField()
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')

    class Meta:
        managed = False
        db_table = 'Detalle_residente'

    def __str__(self):
        return f"Residente {self.cod_usuario} - Torre {self.torre}, Apto {self.apartamento}"
    
    
class Noticias(models.Model):
    id_noticia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()  # ahora es TextField
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    cod_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='cod_usuario'
    )

    class Meta:
        managed = False   # porque la tabla ya existe en la BD
        db_table = 'Noticias'

    def __str__(self):
        return f"Noticia {self.id_noticia}: {self.descripcion[:30]}..."

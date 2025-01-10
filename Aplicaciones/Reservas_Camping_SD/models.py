from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    celular = models.CharField(max_length=15)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)


class Campista(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

class Reserva(models.Model):
    TIPO_ALOJAMIENTO = [
        ('Tienda', 'Tienda'),
        ('Cabaña', 'Cabaña'),
        ('Caravana', 'Caravana'),
    ]

    ESTADO_RESERVA = [
        ('Confirmada', 'Confirmada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    campista = models.ForeignKey(Campista, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con Usuario
    tipo_alojamiento = models.CharField(max_length=50, choices=TIPO_ALOJAMIENTO)
    numero_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=50, choices=ESTADO_RESERVA)
    observaciones = models.TextField(blank=True, null=True)
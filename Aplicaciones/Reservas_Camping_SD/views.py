from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Usuario, Campista, Reserva

# Función para manejar el inicio de sesión de los usuarios
def iniciar_sesion(request):
    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        usuario = request.POST.get('usuario')  # Obtiene el nombre de usuario del formulario
        contrasena = request.POST.get('contrasena')  # Obtiene la contraseña del formulario

        try:
            # Intenta buscar un usuario que coincida con las credenciales proporcionadas
            usuario_obj = Usuario.objects.get(usuario=usuario, contrasena=contrasena)
            request.session['usuario'] = usuario_obj.usuario  # Guarda el usuario en la sesión
            return redirect('/campistas/')  # Redirige a la lista de campistas
        except Usuario.DoesNotExist:
            # Si no se encuentra el usuario, muestra un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')  # Renderiza la página de inicio de sesión

# Función para cerrar la sesión del usuario
def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('/')  # Redirige a la página de inicio

# Función para mostrar la página de inicio
def pagina_inicio(request):
    if 'usuario' not in request.session:  # Verifica si el usuario no ha iniciado sesión
        return redirect('/')  # Redirige a la página de inicio de sesión
    return render(request, 'inicio.html')  # Renderiza la página de inicio

# Función para registrar un nuevo usuario
def registro_usuario(request):
    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        nombre = request.POST.get('nombre')  # Obtiene el nombre del formulario
        apellido = request.POST.get('apellido')  # Obtiene el apellido del formulario
        cedula = request.POST.get('cedula')  # Obtiene la cédula del formulario
        celular = request.POST.get('celular')  # Obtiene el celular del formulario
        usuario = request.POST.get('usuario')  # Obtiene el usuario del formulario
        contrasena = request.POST.get('contrasena')  # Obtiene la contraseña del formulario

        # Verifica si el usuario ya existe en la base de datos
        if Usuario.objects.filter(usuario=usuario).exists():
            messages.error(request, 'El usuario ya existe.')  # Muestra un mensaje de error
            return redirect('/registro/')
        # Verifica si la cédula ya está registrada
        if Usuario.objects.filter(cedula=cedula).exists():
            messages.error(request, 'La cédula ya está registrada.')  # Muestra un mensaje de error
            return redirect('/registro/')

        # Crea un nuevo usuario con los datos proporcionados
        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            celular=celular,
            usuario=usuario,
            contrasena=contrasena
        )
        messages.success(request, 'Usuario registrado exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/')  # Redirige a la página de inicio

    return render(request, 'registro.html')  # Renderiza la página de registro





#--------------------------------------------------------------------------------------------------------
# Función para listar campistas
def lista_campistas(request):
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_actual = Usuario.objects.get(usuario=request.session['usuario'])
    campistas = Campista.objects.filter(usuario=usuario_actual)
    total_campistas = campistas.count()

    return render(request, 'lista_campistas.html', {
        'campistas': campistas,
        'total_campistas': total_campistas,
    })

# Función para crear un nuevo campista
def crear_campista(request):
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_actual = Usuario.objects.get(usuario=request.session['usuario'])

    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        correo_electronico = request.POST.get('correo_electronico')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        if Campista.objects.filter(correo_electronico=correo_electronico, usuario=usuario_actual).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('/campistas/crear/')

        Campista.objects.create(
            nombre_completo=nombre_completo,
            correo_electronico=correo_electronico,
            telefono=telefono,
            direccion=direccion,
            usuario=usuario_actual
        )
        messages.success(request, 'Campista creado exitosamente.')
        return redirect('/campistas/')

    return render(request, 'crear_campista.html')

def editar_campista(request, id):
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_actual = Usuario.objects.get(usuario=request.session['usuario'])
    campista = Campista.objects.filter(id=id, usuario=usuario_actual).first()

    if not campista:
        messages.error(request, 'Campista no encontrado o no tiene permiso para editarlo.')
        return redirect('/campistas/')

    if request.method == 'POST':
        campista.nombre_completo = request.POST.get('nombre_completo')
        campista.correo_electronico = request.POST.get('correo_electronico')
        campista.telefono = request.POST.get('telefono')
        campista.direccion = request.POST.get('direccion')
        campista.save()
        messages.success(request, 'Campista actualizado exitosamente.')
        return redirect('/campistas/')

    return render(request, 'editar_campista.html', {'campista': campista})


# Función para eliminar un campista
def eliminar_campista(request, id):
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_actual = Usuario.objects.get(usuario=request.session['usuario'])
    campista = Campista.objects.filter(id=id, usuario=usuario_actual).first()

    if not campista:
        messages.error(request, 'Campista no encontrado o no tiene permiso para eliminarlo.')
        return redirect('/campistas/')

    if Reserva.objects.filter(campista=campista).exists():
        messages.error(request, 'No se puede eliminar el campista porque tiene reservas asociadas.')
        return redirect('/campistas/')

    campista.delete()
    messages.success(request, 'Campista eliminado exitosamente.')
    return redirect('/campistas/')

























# Función para listar reservas
def lista_reservas(request):
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_actual = request.session['usuario']
    reservas = Reserva.objects.filter(usuario__usuario=usuario_actual)  # Filtra las reservas por usuario
    total_campistas = Campista.objects.filter(reserva__usuario__usuario=usuario_actual).distinct().count()  # Filtra campistas relacionados con las reservas del usuario
    total_reservas = reservas.count()  # Cuenta las reservas del usuario actual

    return render(request, 'lista_reservas.html', {
        'reservas': reservas,
        'total_campistas': total_campistas,
        'total_reservas': total_reservas,
    })


# Función para crear una nueva reserva
def crear_reserva(request):
    if 'usuario' not in request.session:
        return redirect('/')

    # Obtiene el usuario actual
    usuario_actual = Usuario.objects.get(usuario=request.session['usuario'])

    # Filtra los campistas relacionados directamente con el usuario actual
    campistas = Campista.objects.filter(usuario=usuario_actual)  # Ajusta esto según tus modelos

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        campista_id = request.POST.get('campista')
        tipo_alojamiento = request.POST.get('tipo_alojamiento')
        numero_personas = request.POST.get('numero_personas')
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones')

        campista = Campista.objects.filter(id=campista_id, usuario=usuario_actual).first()
        if not campista:
            messages.error(request, 'Campista no encontrado o no pertenece a este usuario.')
            return redirect('/reservas/crear/')

        Reserva.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            campista=campista,
            tipo_alojamiento=tipo_alojamiento,
            numero_personas=numero_personas,
            estado=estado,
            observaciones=observaciones,
            usuario=usuario_actual  # Asocia la reserva al usuario actual
        )
        messages.success(request, 'Reserva creada exitosamente.')
        return redirect('/reservas/')

    return render(request, 'crear_reserva.html', {'campistas': campistas})


# Función para editar una reserva existente
def editar_reserva(request, id):
    reserva = Reserva.objects.filter(id=id, usuario__usuario=request.session['usuario']).first()  # Filtra por usuario actual
    if not reserva:
        messages.error(request, 'Reserva no encontrada o no tiene permiso para editarla.')
        return redirect('/reservas/')

    campistas = Campista.objects.all()
    if request.method == 'POST':
        reserva.fecha_inicio = request.POST.get('fecha_inicio')
        reserva.fecha_fin = request.POST.get('fecha_fin')
        campista_id = request.POST.get('campista')
        reserva.campista = Campista.objects.filter(id=campista_id).first()
        reserva.tipo_alojamiento = request.POST.get('tipo_alojamiento')
        reserva.numero_personas = request.POST.get('numero_personas')
        reserva.estado = request.POST.get('estado')
        reserva.observaciones = request.POST.get('observaciones')
        reserva.save()

        messages.success(request, 'Reserva actualizada exitosamente.')
        return redirect('/reservas/')

    # Formatea las fechas para que sean compatibles con el atributo value del input tipo date
    reserva.fecha_inicio = reserva.fecha_inicio.strftime('%Y-%m-%d')
    reserva.fecha_fin = reserva.fecha_fin.strftime('%Y-%m-%d')

    return render(request, 'editar_reserva.html', {'reserva': reserva, 'campistas': campistas})


# Función para eliminar una reserva existente
def eliminar_reserva(request, id):
    reserva = Reserva.objects.filter(id=id, usuario__usuario=request.session['usuario']).first()
    if not reserva:
        messages.error(request, 'Reserva no encontrada o no tiene permiso para eliminarla.')
        return redirect('/reservas/')

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('/reservas/')

    messages.error(request, 'Acción no permitida.')
    return redirect('/reservas/')

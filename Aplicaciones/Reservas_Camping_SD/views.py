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
    campistas = Campista.objects.annotate(
        tiene_reservas=Count('reserva')  # Anota si cada campista tiene reservas
    )
    total_campistas = Campista.objects.count()  # Cuenta el total de campistas
    total_reservas = Reserva.objects.count()  # Cuenta el total de reservas

    # Renderiza la página de lista de campistas con los datos
    return render(request, 'lista_campistas.html', {
        'campistas': campistas,
        'total_campistas': total_campistas,
        'total_reservas': total_reservas,
    })
#----------------------------------------------------------------------------------------------------------







# Función para crear un nuevo campista
def crear_campista(request):
    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        nombre_completo = request.POST.get('nombre_completo')  # Obtiene el nombre completo
        correo_electronico = request.POST.get('correo_electronico')  # Obtiene el correo electrónico
        telefono = request.POST.get('telefono')  # Obtiene el teléfono
        direccion = request.POST.get('direccion')  # Obtiene la dirección

        # Verifica si el correo ya está registrado
        if Campista.objects.filter(correo_electronico=correo_electronico).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('/campistas/crear/')

        # Crea un nuevo campista
        Campista.objects.create(
            nombre_completo=nombre_completo,
            correo_electronico=correo_electronico,
            telefono=telefono,
            direccion=direccion
        )
        messages.success(request, 'Campista creado exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/campistas/')  # Redirige a la lista de campistas
    return render(request, 'crear_campista.html')  # Renderiza la página para crear campistas

# ---------------------------Función para editar un campista existente----------------------------------
def editar_campista(request, id):
    try:
        campista = Campista.objects.get(id=id)  # Busca el campista por su ID
    except Campista.DoesNotExist:
        messages.error(request, 'El campista no existe.')  # Muestra un mensaje de error
        return redirect('/campistas/')

    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        campista.nombre_completo = request.POST.get('nombre_completo')  # Actualiza el nombre completo
        campista.correo_electronico = request.POST.get('correo_electronico')  # Actualiza el correo
        campista.telefono = request.POST.get('telefono')  # Actualiza el teléfono
        campista.direccion = request.POST.get('direccion')  # Actualiza la dirección
        campista.save()  # Guarda los cambios
        messages.success(request, 'Campista actualizado exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/campistas/')  # Redirige a la lista de campistas
    return render(request, 'editar_campista.html', {'campista': campista})  # Renderiza la página de edición



# --------------Función para eliminar un campista
def eliminar_campista(request, id):
    try:
        campista = Campista.objects.get(id=id)  # Busca el campista por su ID
    except Campista.DoesNotExist:
        messages.error(request, 'El campista no existe.')  # Muestra un mensaje de error
        return redirect('/campistas/')

    # Verifica si el campista tiene reservas asociadas
    if Reserva.objects.filter(campista=campista).exists():
        messages.error(request, 'No se puede eliminar el campista porque tiene reservas asociadas.')
        return redirect('/campistas/')

    campista.delete()  # Elimina el campista
    messages.success(request, 'Campista eliminado exitosamente.')  # Muestra un mensaje de éxito
    return redirect('/campistas/')  # Redirige a la lista de campistas

# Función para listar reservas
def lista_reservas(request):
    reservas = Reserva.objects.all()  # Obtiene todas las reservas
    total_campistas = Campista.objects.count()  # Cuenta el total de campistas
    total_reservas = Reserva.objects.count()  # Cuenta el total de reservas

    # Renderiza la página de lista de reservas con los datos
    return render(request, 'lista_reservas.html', {
        'reservas': reservas,
        'total_campistas': total_campistas,
        'total_reservas': total_reservas,
    })

# Función para crear una nueva reserva
def crear_reserva(request):
    campistas = Campista.objects.all()  # Obtiene todos los campistas para mostrar en el formulario
    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        fecha_inicio = request.POST.get('fecha_inicio')  # Obtiene la fecha de inicio
        fecha_fin = request.POST.get('fecha_fin')  # Obtiene la fecha de fin
        campista_id = request.POST.get('campista')  # Obtiene el ID del campista
        tipo_alojamiento = request.POST.get('tipo_alojamiento')  # Obtiene el tipo de alojamiento
        numero_personas = request.POST.get('numero_personas')  # Obtiene el número de personas
        estado = request.POST.get('estado')  # Obtiene el estado
        observaciones = request.POST.get('observaciones')  # Obtiene las observaciones

        # Busca el campista asociado a la reserva
        campista = Campista.objects.filter(id=campista_id).first()
        if not campista:  # Si no se encuentra el campista, muestra un mensaje de error
            messages.error(request, 'Campista no encontrado.')
            return redirect('/reservas/crear/')

        # Crea una nueva reserva
        Reserva.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            campista=campista,
            tipo_alojamiento=tipo_alojamiento,
            numero_personas=numero_personas,
            estado=estado,
            observaciones=observaciones
        )
        messages.success(request, 'Reserva creada exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/reservas/')  # Redirige a la lista de reservas
    return render(request, 'crear_reserva.html', {'campistas': campistas})  # Renderiza la página para crear reservas

# Función para editar una reserva existente
def editar_reserva(request, id):
    reserva = Reserva.objects.filter(id=id).first()  # Busca la reserva por su ID
    if not reserva:  # Si no se encuentra la reserva, muestra un mensaje de error
        messages.error(request, 'Reserva no encontrada.')
        return redirect('/reservas/')

    campistas = Campista.objects.all()  # Obtiene todos los campistas para el formulario
    if request.method == 'POST':  # Verifica si el formulario se envió mediante POST
        reserva.fecha_inicio = request.POST.get('fecha_inicio')  # Actualiza la fecha de inicio
        reserva.fecha_fin = request.POST.get('fecha_fin')  # Actualiza la fecha de fin
        campista_id = request.POST.get('campista')  # Obtiene el ID del campista actualizado
        reserva.campista = Campista.objects.filter(id=campista_id).first()  # Actualiza el campista asociado
        reserva.tipo_alojamiento = request.POST.get('tipo_alojamiento')  # Actualiza el tipo de alojamiento
        reserva.numero_personas = request.POST.get('numero_personas')  # Actualiza el número de personas
        reserva.estado = request.POST.get('estado')  # Actualiza el estado
        reserva.observaciones = request.POST.get('observaciones')  # Actualiza las observaciones
        reserva.save()  # Guarda los cambios
        messages.success(request, 'Reserva actualizada exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/reservas/')  # Redirige a la lista de reservas

    # Formatea las fechas para mostrarlas en el campo de tipo "date"
    reserva.fecha_inicio = reserva.fecha_inicio.strftime('%Y-%m-%d')
    reserva.fecha_fin = reserva.fecha_fin.strftime('%Y-%m-%d')

    return render(request, 'editar_reserva.html', {'reserva': reserva, 'campistas': campistas})  # Renderiza la página de edición

# Función para eliminar una reserva existente
def eliminar_reserva(request, id):
    reserva = Reserva.objects.filter(id=id).first()  # Busca la reserva por su ID
    if not reserva:  # Si no se encuentra la reserva, muestra un mensaje de error
        messages.error(request, 'Reserva no encontrada.')
        return redirect('/reservas/')

    if request.method == 'POST':  # Si se confirmó la eliminación
        reserva.delete()  # Elimina la reserva
        messages.success(request, 'Reserva eliminada exitosamente.')  # Muestra un mensaje de éxito
        return redirect('/reservas/')  # Redirige a la lista de reservas

    messages.error(request, 'Acción no permitida.')  # Si no es POST, muestra un mensaje de error
    return redirect('/reservas/')  # Redirige a la lista de reservas

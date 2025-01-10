from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la página de inicio de sesión
    path('', views.iniciar_sesion),  # Cuando la URL esté vacía, se redirige a la vista iniciar_sesion

    # Ruta para cerrar sesión
    path('cerrar_sesion/', views.cerrar_sesion),  # Cierra la sesión del usuario y redirige

    # Ruta para la página de inicio
    path('inicio/', views.pagina_inicio),  # Página principal después de iniciar sesión

    # Ruta para el registro de nuevos usuarios
    path('registro/', views.registro_usuario),  # Permite registrar nuevos usuarios

    # Campistas
    path('campistas/', views.lista_campistas),  # Lista de todos los campistas
    path('campistas/crear/', views.crear_campista),  # Formulario para crear un nuevo campista
    path('campistas/editar/<int:id>/', views.editar_campista),  # Editar un campista existente, identificado por su ID
    path('campistas/eliminar/<int:id>/', views.eliminar_campista),  # Eliminar un campista existente por su ID

    # Reservas
    path('reservas/', views.lista_reservas),  # Lista de todas las reservas
    path('reservas/crear/', views.crear_reserva),  # Formulario para crear una nueva reserva
    path('reservas/editar/<int:id>/', views.editar_reserva),  # Editar una reserva existente, identificada por su ID
    path('reservas/eliminar/<int:id>/', views.eliminar_reserva),  # Eliminar una reserva existente por su ID
]
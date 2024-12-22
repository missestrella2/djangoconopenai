from django.urls import path
from . import views

urlpatterns = [
    # Ingredientes Principales
    path('ingredientes/', views.lista_ingredientes_principal, name='lista_ingredientes_principal'),
    path('ingredientes/agregar/', views.agregar_ingrediente_principal, name='agregar_ingrediente_principal'),
    path('ingredientes/<int:pk>/', views.detalle_ingrediente_principal, name='detalle_ingrediente_principal'),
    path('ingredientes/<int:pk>/editar/', views.editar_ingrediente_principal, name='editar_ingrediente_principal'),
    path('ingredientes/<int:pk>/eliminar/', views.eliminar_ingrediente_principal, name='eliminar_ingrediente_principal'),

    # Ingredientes de Recetas
    path('recetas/<int:receta_id>/ingredientes/', views.lista_ingredientes_receta, name='lista_ingredientes_receta'),
    path('recetas/<int:receta_id>/ingredientes/agregar/', views.agregar_ingrediente_receta, name='agregar_ingrediente_receta'),
    path('recetas/ingredientes/<int:pk>/', views.detalle_ingrediente_receta, name='detalle_ingrediente_receta'),
    path('recetas/ingredientes/<int:pk>/editar/', views.editar_ingrediente_receta, name='editar_ingrediente_receta'),
    path('recetas/ingredientes/<int:pk>/eliminar/', views.eliminar_ingrediente_receta, name='eliminar_ingrediente_receta'),

    # Recetas
    path('recetas/', views.lista_recetas, name='lista_recetas'),
    path('recetas/agregar/', views.agregar_receta, name='agregar_receta'),
    path('recetas/<int:pk>/', views.detalle_receta, name='detalle_receta'),
    path('recetas/<int:pk>/editar/', views.editar_receta, name='editar_receta'),
    path('recetas/<int:pk>/eliminar/', views.eliminar_receta, name='eliminar_receta'),
    

    # Caterings
    path('caterings/', views.lista_caterings, name='lista_caterings'),
    path('caterings/agregar/', views.agregar_catering, name='agregar_catering'),
    path('caterings/<int:pk>/', views.ver_catering, name='ver_catering'),
    path('caterings/<int:pk>/editar/', views.editar_catering, name='editar_catering'),
    path('caterings/<int:pk>/eliminar/', views.eliminar_catering, name='eliminar_catering'),
    path('caterings/<int:pk>/finalizar/', views.finalizar_catering, name='finalizar_catering'),
    
    # Home y Cálculos
    path('calculos/', views.home_calculos, name='home_calculos'),
    path('', views.home, name='home'),
]

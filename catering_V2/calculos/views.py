from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Receta, RecetaIngrediente, Ingrediente, Catering, CateringReceta
from .forms import IngredienteForm, RecetaForm, CateringForm, RecetaIngredienteForm, CateringRecetaForm
from decimal import Decimal


def calcular_lista_compras(catering_id):
    catering = get_object_or_404(Catering, pk=catering_id)
    lista_compras = {}
    cantidad_personas_catering = Decimal(catering.cantidad_personas)
    cantidad_porciones_totales = 0

    for catering_receta in catering.recetas.all():
        receta = catering_receta.receta
        porciones_necesarias = Decimal(catering_receta.porciones)
        cantidad_porciones_totales += porciones_necesarias
        porciones_receta = Decimal(receta.porciones)

        for ingrediente_receta in RecetaIngrediente.objects.filter(receta=receta):
            ingrediente = ingrediente_receta.ingrediente
            cantidad_por_receta = Decimal(ingrediente_receta.cantidad_necesaria)
            precio_unitario = Decimal(ingrediente.precio)
            cantidad_unidad = Decimal(ingrediente.cantidad)

            cantidad_ajustada = (cantidad_por_receta / porciones_receta) * porciones_necesarias

            if ingrediente.nombre in lista_compras:
                lista_compras[ingrediente.nombre]['cantidad'] += cantidad_ajustada
            else:
                lista_compras[ingrediente.nombre] = {
                    'cantidad': cantidad_ajustada,
                    'unidad': ingrediente.unidad,
                    'precio_unitario': precio_unitario,
                    'cantidad_unidad': cantidad_unidad,
                }

    costo_total = Decimal(0)
    for ingrediente in lista_compras.values():
        ingrediente['costo_total'] = (ingrediente['cantidad'] * ingrediente['precio_unitario']) / ingrediente['cantidad_unidad']
        costo_total += ingrediente['costo_total']

    costo_por_persona = costo_total / cantidad_personas_catering if cantidad_personas_catering > 0 else Decimal(0)
    porciones_por_persona = cantidad_porciones_totales / cantidad_personas_catering if cantidad_personas_catering > 0 else Decimal(0)

    return lista_compras, costo_total, costo_por_persona, cantidad_porciones_totales, porciones_por_persona


def finalizar_catering(request, pk):
    catering = get_object_or_404(Catering, pk=pk)
    lista_compras, costo_total, costo_por_persona, cantidad_porciones_totales, porciones_por_persona = calcular_lista_compras(pk)

    return render(request, 'calculos/finalizar_catering.html', {
        'catering': catering,
        'lista_compras': lista_compras,
        'costo_total': costo_total,
        'costo_por_persona': costo_por_persona,
        'cantidad_personas': catering.cantidad_personas,
        'cantidad_porciones_totales': cantidad_porciones_totales,
        'porciones_por_persona': porciones_por_persona,
    })


# Vista para el home principal
def home(request):
    return render(request, 'home.html')

# Vista para el home de cálculos
def home_calculos(request):
    return render(request, 'calculos/home_calculos.html')

# Gestionar ingredientes principales
def agregar_ingrediente_principal(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ingredientes_principal')
    else:
        form = IngredienteForm()
    return render(request, 'calculos/agregar_ingrediente_principal.html', {'form': form})

def lista_ingredientes_principal(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'calculos/lista_ingredientes_principal.html', {'ingredientes': ingredientes})

def detalle_ingrediente_principal(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    return render(request, 'calculos/detalle_ingrediente_principal.html', {'ingrediente': ingrediente})

def editar_ingrediente_principal(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            return redirect('lista_ingredientes_principal')
    else:
        form = IngredienteForm(instance=ingrediente)
    return render(request, 'calculos/editar_ingrediente_principal.html', {'form': form, 'ingrediente': ingrediente})

def eliminar_ingrediente_principal(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    # Verificar si el ingrediente está en alguna receta
    if RecetaIngrediente.objects.filter(ingrediente=ingrediente).exists():
        return render(request, 'calculos/error.html', {
            'mensaje': f"No se puede eliminar el ingrediente '{ingrediente.nombre}' porque está asociado a una o más recetas."
        })
    # Proceder con la eliminación
    if request.method == 'POST':
        ingrediente.delete()
        return redirect('lista_ingredientes_principal')
    return render(request, 'calculos/eliminar_ingrediente_principal.html', {'ingrediente': ingrediente})

# Gestionar recetas
def agregar_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            return redirect('editar_receta', pk=receta.pk)
    else:
        form = RecetaForm()
    return render(request, 'calculos/agregar_receta.html', {'form': form})

def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'calculos/lista_recetas.html', {'recetas': recetas})

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    ingredientes = RecetaIngrediente.objects.filter(receta=receta)
    return render(request, 'calculos/detalle_receta.html', {'receta': receta, 'ingredientes': ingredientes})

def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    ingredientes = RecetaIngrediente.objects.filter(receta=receta)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm(instance=receta)
        ingrediente_form = RecetaIngredienteForm()

    return render(request, 'calculos/editar_receta.html', {
        'form': form,
        'receta': receta,
        'ingredientes': ingredientes,
        'ingrediente_form': ingrediente_form,
    })

def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    # Verificar si la receta está en algún catering
    if CateringReceta.objects.filter(receta=receta).exists():
        return render(request, 'calculos/error.html', {
            'mensaje': f"No se puede eliminar la receta '{receta.nombre}' porque está asociada a uno o más caterings."
        })
    # Proceder con la eliminación
    if request.method == 'POST':
        receta.delete()
        return redirect('lista_recetas')
    return render(request, 'calculos/eliminar_receta.html', {'receta': receta})


# Gestionar ingredientes en recetas
def agregar_ingrediente_receta(request, receta_id):
    receta = get_object_or_404(Receta, pk=receta_id)
    if request.method == 'POST':
        form = RecetaIngredienteForm(request.POST)
        if form.is_valid():
            ingrediente_receta = form.save(commit=False)
            ingrediente_receta.receta = receta
            ingrediente_receta.save()
            return redirect('lista_ingredientes_receta', receta_id=receta.id)
    else:
        form = RecetaIngredienteForm()
    return render(request, 'calculos/agregar_ingrediente_receta.html', {'form': form, 'receta': receta})

def lista_ingredientes_receta(request, receta_id):
    receta = get_object_or_404(Receta, pk=receta_id)
    ingredientes = RecetaIngrediente.objects.filter(receta=receta)
    return render(request, 'calculos/lista_ingredientes_receta.html', {
        'receta': receta,
        'receta_id': receta.id,  # Asegurarse de pasar el ID
        'ingredientes': ingredientes,
    })

def detalle_ingrediente_receta(request, pk):
    ingrediente_receta = get_object_or_404(RecetaIngrediente, pk=pk)
    return render(request, 'calculos/detalle_ingrediente_receta.html', {'ingrediente_receta': ingrediente_receta})

def editar_ingrediente_receta(request, pk):
    ingrediente_receta = get_object_or_404(RecetaIngrediente, pk=pk)
    if request.method == 'POST':
        form = RecetaIngredienteForm(request.POST, instance=ingrediente_receta)
        if form.is_valid():
            form.save()
            return redirect('lista_ingredientes_receta', receta_id=ingrediente_receta.receta.id)
    else:
        form = RecetaIngredienteForm(instance=ingrediente_receta)
    return render(request, 'calculos/editar_ingrediente_receta.html', {
        'form': form,
        'ingrediente_receta': ingrediente_receta,
    })

def eliminar_ingrediente_receta(request, pk):
    ingrediente_receta = get_object_or_404(RecetaIngrediente, pk=pk)
    receta_id = ingrediente_receta.receta.id
    if request.method == 'POST':
        ingrediente_receta.delete()
        return redirect('lista_ingredientes_receta', receta_id=receta_id)
    return render(request, 'calculos/eliminar_ingrediente_receta.html', {
        'ingrediente_receta': ingrediente_receta,
    })

# Gestionar catering
def agregar_catering(request):
    if request.method == 'POST':
        form = CateringForm(request.POST)
        if form.is_valid():
            catering = form.save()
            return redirect('editar_catering', pk=catering.pk)
    else:
        form = CateringForm()
    return render(request, 'calculos/agregar_catering.html', {'form': form})

def editar_catering(request, pk):
    catering = get_object_or_404(Catering, pk=pk)
    recetas = CateringReceta.objects.filter(catering=catering)
    if request.method == 'POST':
        form = CateringRecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.catering = catering
            receta.save()
            return redirect('editar_catering', pk=catering.pk)
    else:
        form = CateringRecetaForm()
    return render(request, 'calculos/editar_catering.html', {
        'catering': catering,
        'recetas': recetas,
        'form': form,
    })

def eliminar_catering(request, pk):
    catering = get_object_or_404(Catering, pk=pk)
    if request.method == 'POST':
        catering.delete()
        return redirect('lista_caterings')
    return render(request, 'calculos/eliminar_catering.html', {'catering': catering})

def ver_catering(request, pk):
    catering = get_object_or_404(Catering, pk=pk)
    recetas = CateringReceta.objects.filter(catering=catering)
    return render(request, 'calculos/ver_catering.html', {
        'catering': catering,
        'recetas': recetas,
    })

def lista_caterings(request):
    caterings = Catering.objects.all()
    return render(request, 'calculos/lista_caterings.html', {'caterings': caterings})




# AJAX para agregar ingredientes a recetas
def agregar_ingrediente_ajax(request):
    if request.method == 'POST':
        form = RecetaIngredienteForm(request.POST)
        if form.is_valid():
            ingrediente_receta = form.save()
            receta = ingrediente_receta.receta
            ingredientes = RecetaIngrediente.objects.filter(receta=receta)
            html = render_to_string('calculos/ingredientes_lista.html', {'ingredientes': ingredientes})
            return JsonResponse({'html': html})
    return JsonResponse({'error': 'Formulario inválido'}, status=400)

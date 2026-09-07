from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Contacto
from .forms import ContactoForm

def index(request):
    query = request.GET.get('q', '')
    if query:
        contactos = Contacto.objects.filter(
            Q(nombre__icontains=query) | Q(telefono__icontains=query) | Q(email__icontains=query)
        )
    else:
        contactos = Contacto.objects.all()

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactoForm()

    return render(request, 'agenda/index.html', {
        'contactos': contactos,
        'form': form,
        'query': query,
    })

def editar(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactoForm(instance=contacto)

    contactos = Contacto.objects.all()
    return render(request, 'agenda/index.html', {
        'contactos': contactos,
        'form': form,
        'editando': True,
        'contacto_id': id,
    })

def eliminar(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        contacto.delete()
        return redirect('index')

    return render(request, 'agenda/eliminar.html', {'contacto': contacto})

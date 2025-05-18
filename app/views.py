from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {
        'next_url': '/quantidade/',
    })

def quantidade(request):
    return render(request, 'quantidade.html', {
        'previous_url': '/',
        'next_url': '/formulario/',
    })

def formulario(request):
    return render(request, 'formulario.html', {
        'previous_url': '/quantidade/',
        'next_url': '/pagamento/',
    })

def pagamento(request):
    return render(request, 'pagamento.html', {
        'previous_url': '/formulario/',
        'next_url': '/bilhete/',
    })

def bilhete(request):
    return render(request, 'bilhete.html', {
        'previous_url': '/pagamento/',
        'next_url': '/',
    })
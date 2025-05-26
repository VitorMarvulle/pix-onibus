from django.shortcuts import render
import mercadopago, base64, qrcode
from io import BytesIO

def home(request):
    return render(request, 'home.html', {
        'next_url': '/quantidade/',
        'empresas': '/empresa/login',
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
    sdk = mercadopago.SDK("TEST-6337997335997184-040119-fce8a6dd49cf5dcc02d0ef2414c85283-1489971308")

    payment_data = {
        "transaction_amount": 10.00,
        "description": "Pagamento de passagem",
        "payment_method_id": "pix",
        "payer": {
            "email": "comprador@email.com",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "identification": {
                "type": "CPF",
                "number": "12345678909"
            },
            "address": {
                "zip_code": "06233200",
                "street_name": "Av. das Nações Unidas",
                "street_number": "3003",
                "neighborhood": "Bonfim",
                "city": "Osasco",
                "federal_unit": "SP"
            }
        }
    }
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    pix_payload = payment["point_of_interaction"]["transaction_data"]["qr_code"]

    qr = qrcode.make(pix_payload)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'pagamento.html', {
        'previous_url': '/formulario/',
        'next_url': '/bilhete/',
        'qrcode_base64': img_base64,
    })

def bilhete(request):
    return render(request, 'bilhete.html', {
        'previous_url': '/pagamento/',
        'next_url': '/',
    })
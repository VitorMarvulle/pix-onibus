from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
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
        'quantidade': request.GET.get('quantidade', 1),
    })

@csrf_protect
def formulario(request):
    quantidade = request.POST.get('quantidade', 1)
    return render(request, 'formulario.html', {
        'previous_url': '/quantidade/',
        'next_url': '/pagamento/',
        'quantidade': quantidade
    })

@csrf_protect
def pagamento(request):
    quantidade = int(request.POST.get('quantidade', 1))
    valor_unitario = 5.25
    valor_total = quantidade * valor_unitario

    sdk = mercadopago.SDK("APP_USR-6337997335997184-040119-bbb1fa4293760c754506a6679ed8f799-1489971308")

    payment_data = {
        "transaction_amount": float(valor_total),
        "description": f"Pagamento de {quantidade} passagem{'ns' if quantidade > 1 else ''}",
        "payment_method_id": "pix",
        "payer": {
            "email": "passageiro@onipix.com",
            "phone": {
                "area_code": "11",
                "number": "999999999"
            }
        }
    }
    payment_response = sdk.payment().create(payment_data)
    print("DEBUG - Payment Response:", payment_response)  # Debug print

    if "response" not in payment_response:
        raise ValueError("Invalid payment response")

    payment = payment_response["response"]
    
    payment = payment_response["response"]
    payment_status = payment["status"]
    pix_payload = payment["point_of_interaction"]["transaction_data"]["qr_code"]

    qr = qrcode.make(pix_payload)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

     #status = False
     #if payment_status == "approved":
        #status = True
        #Liberar próxima página (bilhete.html)
        
    return render(request, 'pagamento.html', {
        'previous_url': '/formulario/',
        'next_url': '/bilhete/',
        'qrcode_base64': img_base64,
        'quantidade': quantidade,
        'valor_total': valor_total,
        'valor_unitario': valor_unitario,
        'pix_copiacola': pix_payload
        #'status': pago
    })

def bilhete(request):
    return render(request, 'bilhete.html', {
        'previous_url': '/pagamento/',
        'next_url': '/',
    })
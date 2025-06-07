import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
import mercadopago, base64, qrcode
from io import BytesIO

from app_empresa.models import Passagem, gerarCodigoPassagem

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
    payment = payment_response["response"]
    
    payment_id = payment["id"]
    payment_status = payment["status"]
    status = False

    pix_payload = payment["point_of_interaction"]["transaction_data"]["qr_code"]
    qr = qrcode.make(pix_payload)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    if payment_status == "approved":
        status = True
        return redirect('bilhete')
    request.session['payment_id'] = payment_id
        
    return render(request, 'pagamento.html', {
        'previous_url': '/formulario/',
        'qrcode_base64': img_base64,
        'quantidade': quantidade,
        'valor_total': valor_total,
        'valor_unitario': valor_unitario,
        'pix_copiacola': pix_payload,
        'payment_id': payment_id,
        'status': status
    })

def check_payment_status(request):
    payment_id = request.session.get('payment_id')
    if not payment_id:
        return JsonResponse({'error': 'Payment ID not found'})
    
    sdk = mercadopago.SDK("APP_USR-6337997335997184-040119-bbb1fa4293760c754506a6679ed8f799-1489971308")
    payment = sdk.payment().get(payment_id)
    
    if payment["response"]["status"] == "approved":
        return JsonResponse({'status': 'approved', 'redirect_url': '/bilhete/'})
    
    return JsonResponse({'status': payment["response"]["status"]})

def bilhete(request):
    ticket_number = gerarCodigoPassagem()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=3,
    )
    qr.add_data(ticket_number)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img_qr.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()
    current_datetime = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")

    # passagem = Passagem.objects.create(
    #     idPassagem=ticket_number,
    #     valor=Decimal('5.25'),
    #     dataCriacao=current_datetime,
    #     usosDisponiveis=quantidade,
    #     usuarioId = 2
    # )

    return render(request, 'bilhete.html', {
        'qr_code': qr_image,
        'date': current_datetime,
        'price': '5,25',
        'ticket_number': ticket_number,
    })
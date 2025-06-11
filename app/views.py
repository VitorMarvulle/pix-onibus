from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.conf import settings 
import mercadopago, base64, qrcode
from io import BytesIO

from app.models import Usuario
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
    telefone = request.POST.get('telefone')
    request.session['quantidade'] = quantidade
    request.session['telefone'] = telefone

    telefone_cleaned = ''.join(filter(str.isdigit, str(telefone)))
    if len(telefone_cleaned) == 11:
        area_code = telefone_cleaned[:2]
        number = telefone_cleaned[2:]
    else:
        area_code = area_code
        number = number

    valor_unitario = 0.01
    valor_total = quantidade * valor_unitario

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

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
    
    quantidade = request.session.get('quantidade')
    telefone = request.session.get('telefone')
        
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    payment = sdk.payment().get(payment_id)
    
    if payment["response"]["status"] == "approved":
        try:
            telefone_cleaned = ''.join(filter(str.isdigit, str(telefone)))
            if not telefone_cleaned:
                raise ValueError("Invalid phone number format")
                
            telefone_int = int(telefone_cleaned)
            
            usuario, created = Usuario.objects.get_or_create(
                idTelUsuario=telefone_int
            )
            passagem = Passagem.objects.create(
                usuario=usuario,
                valor=Decimal('5.25'),
                usosDisponiveis=quantidade
            )
            request.session['passagem_id'] = passagem.idPassagem
            
            print(f"Created ticket for phone: {telefone_int}, quantidade: {quantidade}")
            
            return JsonResponse({
                'status': 'approved',
                'redirect_url': '/bilhete/'
            })
            
        except Exception as e:
            print(f"Error creating ticket: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Erro ao criar bilhete'
            })
            
    return JsonResponse({'status': payment["response"]["status"]})

def bilhete(request):
    try:
        passagem_id = request.session.get('passagem_id')
        passagem = Passagem.objects.get(idPassagem=passagem_id)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=3,
        )
        qr.add_data(passagem.idPassagem)
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        qr_image = base64.b64encode(buffer.getvalue()).decode()

        return render(request, 'bilhete.html', {
            'qr_code': qr_image,
            'date': passagem.dataCriacao,
            'price': passagem.valor,
            'ticket_number': passagem.idPassagem,
            'quantidade': passagem.usosDisponiveis
        })
    
    except Exception as e:
        print(f"Error displaying ticket: {str(e)}")
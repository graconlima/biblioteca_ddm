from rest_framework import viewsets, permissions 
from .models import Autor, Livro 
from .serializers import AutorSerializer, LivroSerializer 


class AutorViewSet(viewsets.ModelViewSet): 
    queryset = Autor.objects.all() 
    serializer_class = AutorSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class LivroViewSet(viewsets.ModelViewSet): 
    queryset = Livro.objects.all() 
    serializer_class = LivroSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

#Registro token
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Dispositivo


@csrf_exempt
def registrar_token_firebase(request):

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Metodo invalido"},
            status=405
        )

    dados = json.loads(request.body)

    token = dados.get("token")
    usuario = dados.get("usuario")

    dispositivo, criado = Dispositivo.objects.update_or_create(
        usuario=usuario,
        defaults={
            "token": token
        }
    )

    return JsonResponse({
        "mensagem": "Token registrado"
    })


# conexao firebase
from firebase_admin import messaging

@csrf_exempt
def notificar_firebase(request):

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Metodo invalido"},
            status=405
        )

    dados = json.loads(request.body)

    usuario = dados.get("usuario")

    titulo = dados.get("titulo")

    corpo = dados.get("body")

    dispositivo = Dispositivo.objects.get(
        usuario=usuario
    )

    mensagem = messaging.Message(

        notification=messaging.Notification(
            title=titulo,
            body=corpo
        ),

        data={
            "dado_extra": "123"
        },

        token=dispositivo.token
    )

    resposta = messaging.send(mensagem)

    return JsonResponse({
        "mensagem": "Notificacao enviada",
        "resposta_firebase": resposta
    })
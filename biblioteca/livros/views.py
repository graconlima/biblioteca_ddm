from rest_framework import viewsets, permissions 
from .models import Autor, Livro, Dispositivo
from .serializers import AutorSerializer, LivroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from firebase_admin import messaging

class AutorViewSet(viewsets.ModelViewSet): 
    queryset = Autor.objects.all() 
    serializer_class = AutorSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class LivroViewSet(viewsets.ModelViewSet): 
    queryset = Livro.objects.all() 
    serializer_class = LivroSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

class FirebaseNotificationViewSet(viewsets.GenericViewSet):
    """
    Gerenciamento de recursos do Firebase Cloud Messaging.
    """
    queryset = Dispositivo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    # URL gerada: POST /api/firebase/tokens/
    @action(detail=False, methods=['post'], url_path='tokens')
    def registro_token(self, request):
        """
        Cria ou atualiza um recurso de token de dispositivo.
        """
        dados = request.data
        token = dados.get("token")
        usuario = dados.get("usuario")

        if not token or not usuario:
            return Response({"erro": "Campos 'token' e 'usuario' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        dispositivo, criado = Dispositivo.objects.update_or_create(
            usuario=usuario,
            defaults={"token": token}
        )
        return Response({"mensagem": "Token registrado com sucesso."}, status=status.HTTP_200_OK)

    # URL gerada: POST /api/firebase/notificacoes/
    @action(detail=False, methods=['post'], url_path='notificacoes')
    def notificacao(self, request):
        """
        Envia uma nova mensagem/notificação para o recurso de dispositivo especificado.
        """
        dados = request.data
        usuario = dados.get("usuario")
        titulo = dados.get("titulo")
        corpo = dados.get("body")

        if not usuario or not titulo or not corpo:
            return Response({"erro": "Campos 'usuario', 'titulo' e 'body' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dispositivo = Dispositivo.objects.get(usuario=usuario)
        except Dispositivo.DoesNotExist:
            return Response({"erro": "Usuario nao possui dispositivo registrado"}, status=status.HTTP_404_NOT_FOUND)

        mensagem = messaging.Message(
            notification=messaging.Notification(
                title=titulo,
                body=corpo
            ),
            data={"dado_extra": "123"},
            token=dispositivo.token
        )

        resposta = messaging.send(mensagem)
        return Response({
            "mensagem": "Notificacao enviada",
            "resposta_firebase": resposta
        }, status=status.HTTP_200_OK)

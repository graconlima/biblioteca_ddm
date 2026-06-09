from rest_framework import viewsets, permissions 
from .models import Autor, Livro, Dispositivo
from .serializers import AutorSerializer, LivroSerializer, TokenFirebaseSerializer, NotificacaoFirebaseSerializer
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

    def get_serializer_class(self):
        """
        Retorna o serializer correto baseado na rota para o Swagger mapear sem erros.
        """
        if getattr(self, 'swagger_fake_view', False):
            return TokenFirebaseSerializer  # Evita quebras genéricas do swagger na inicialização
            
        if self.action == 'registro_token':
            return TokenFirebaseSerializer
        if self.action == 'notificacao':
            return NotificacaoFirebaseSerializer
        return None

    @action(detail=False, methods=['post'], url_path='tokens')
    def registro_token(self, request):
        """
        Cria ou atualiza um recurso de token de dispositivo.
        """
        # Utiliza o serializer para validar os dados recebidos
        serializer = TokenFirebaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dados = serializer.validated_data
        token = dados.get("token")
        usuario = dados.get("usuario")

        dispositivo, criado = Dispositivo.objects.update_or_create(
            usuario=usuario,
            defaults={"token": token}
        )
        return Response({"mensagem": "Token registrado com sucesso."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='notificacoes')
    def notificacao(self, request):
        """
        Envia uma nova mensagem/notificação para o recurso de dispositivo especificado.
        """
        # Utiliza o serializer para validar os dados recebidos
        serializer = NotificacaoFirebaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dados = serializer.validated_data
        usuario = dados.get("usuario")
        titulo = dados.get("titulo")
        corpo = dados.get("body")

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

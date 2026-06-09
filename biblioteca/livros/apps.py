import os
from django.apps import AppConfig
from django.conf import settings
import firebase_admin
from firebase_admin import credentials

class LivrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livros'

    def ready(self):
        # Evita inicializar duas vezes durante o recarregamento automático do Django
        if not firebase_admin._apps:
            # Constrói o caminho para o arquivo JSON de credenciais
            caminho_credenciais = os.path.join(settings.BASE_DIR, 'biblioteca', 'firebase', 'firebase-service-account.json')
            
            try:
                cred = credentials.Certificate(caminho_credenciais)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK inicializado com sucesso!")
            except Exception as e:
                print(f"Erro ao inicializar o Firebase: {e}")

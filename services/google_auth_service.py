import datetime
from typing import Dict, Optional
import json
from pathlib import Path
import sys
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

# Adiciona o diretório raiz ao path para importar o firebase_config
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from firebase.firebase_config import (
    add_document,
    update_document,
    query_documents,
    get_document
)

class GoogleAuthService:
    """
    Serviço para autenticação usando Google Sign-In.
    """
    
    COLLECTION_NAME = "users"
    CLIENT_SECRETS_FILE = "client_secrets.json"
    
    @staticmethod
    def get_google_flow():
        """
        Cria e retorna um objeto Flow para autenticação Google.
        
        Returns:
            Flow: Objeto de fluxo de autenticação Google
        """
        # Configurar o fluxo OAuth2
        flow = Flow.from_client_secrets_file(
            GoogleAuthService.CLIENT_SECRETS_FILE,
            scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
            ],
            redirect_uri=os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8501')
        )
        return flow
    
    @staticmethod
    def verify_google_token(token: str) -> Optional[Dict]:
        """
        Verifica um token do Google e retorna as informações do usuário.
        
        Args:
            token: Token JWT do Google
            
        Returns:
            Dict com informações do usuário ou None se token inválido
        """
        try:
            # Verificar o token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                os.getenv('GOOGLE_CLIENT_ID')
            )
            
            # Verificar se o token expirou
            if idinfo['exp'] < datetime.datetime.now().timestamp():
                print("Token expirado")
                return None
                
            return {
                'email': idinfo['email'],
                'name': idinfo.get('name', ''),
                'picture': idinfo.get('picture', ''),
                'google_id': idinfo['sub']
            }
            
        except Exception as e:
            print(f"Erro ao verificar token: {e}")
            return None
    
    @staticmethod
    def get_or_create_user(google_user: Dict) -> Optional[Dict]:
        """
        Obtém um usuário existente ou cria um novo baseado nas informações do Google.
        
        Args:
            google_user: Dicionário com informações do usuário do Google
            
        Returns:
            Dict com informações do usuário ou None se houver erro
        """
        # Buscar usuário existente pelo email
        existing_users = query_documents(
            GoogleAuthService.COLLECTION_NAME,
            field="email",
            operator="==",
            value=google_user['email']
        )
        
        if existing_users:
            user = existing_users[0]
            # Atualizar informações do Google se necessário
            if user.get('google_id') != google_user['google_id']:
                update_document(
                    GoogleAuthService.COLLECTION_NAME,
                    user['id'],
                    {
                        'google_id': google_user['google_id'],
                        'picture': google_user['picture'],
                        'updated_at': datetime.datetime.now().isoformat()
                    }
                )
            return user
        
        # Criar novo usuário
        user_data = {
            'email': google_user['email'],
            'name': google_user['name'],
            'picture': google_user['picture'],
            'google_id': google_user['google_id'],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat(),
            'last_login': datetime.datetime.now().isoformat(),
            'preferences': json.dumps({
                'currency': 'BRL',
                'theme': 'light',
                'date_format': 'DD/MM/YYYY',
                'language': 'pt-BR',
                'notifications_enabled': True
            })
        }
        
        user_id = add_document(GoogleAuthService.COLLECTION_NAME, user_data)
        
        if user_id:
            user_data['id'] = user_id
            return user_data
            
        return None
    
    @staticmethod
    def update_last_login(user_id: str) -> bool:
        """
        Atualiza a data do último login do usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se atualização bem sucedida, False caso contrário
        """
        return update_document(
            GoogleAuthService.COLLECTION_NAME,
            user_id,
            {'last_login': datetime.datetime.now().isoformat()}
        ) 
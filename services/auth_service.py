import datetime
from typing import Dict, List, Optional
import uuid
import hashlib
import os
from pathlib import Path
import sys
import json

# Adiciona o diretório raiz ao path para importar o firebase_config
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from firebase.firebase_config import (
    add_document,
    update_document,
    delete_document,
    query_documents,
    get_document
)

class AuthService:
    """
    Serviço para autenticação e gerenciamento de usuários.
    """
    
    COLLECTION_NAME = "users"
    
    @staticmethod
    def register_user(
        email: str,
        password: str,
        name: str,
        profile_image: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Registra um novo usuário no sistema.
        
        Args:
            email: Email do usuário (deve ser único)
            password: Senha do usuário
            name: Nome completo do usuário
            profile_image: URL da imagem de perfil (opcional)
            
        Returns:
            Dicionário com os dados do usuário criado, incluindo ID, ou None se houver erro
        """
        # Verificar se o email já está em uso
        existing_users = query_documents(
            AuthService.COLLECTION_NAME, 
            field="email", 
            operator="==", 
            value=email
        )
        
        if existing_users:
            print(f"Email já está em uso: {email}")
            return None
        
        # Gerar salt aleatório para a senha
        salt = os.urandom(32).hex()
        
        # Hash da senha com salt
        hashed_password = AuthService._hash_password(password, salt)
        
        # Preparar dados do usuário
        user_data = {
            "email": email,
            "password_hash": hashed_password,
            "password_salt": salt,
            "name": name,
            "profile_image": profile_image or "",
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "last_login": None,
            "preferences": json.dumps({
                "currency": "BRL",
                "theme": "light",
                "date_format": "DD/MM/YYYY",
                "language": "pt-BR",
                "notifications_enabled": True
            })
        }
        
        # Adicionar usuário ao Firestore
        user_id = add_document(AuthService.COLLECTION_NAME, user_data)
        
        if user_id:
            # Retornar dados do usuário sem informações sensíveis
            return {
                "id": user_id,
                "email": email,
                "name": name,
                "profile_image": profile_image or "",
                "created_at": user_data["created_at"]
            }
        
        return None
    
    @staticmethod
    def login(email: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário com email e senha.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Dicionário com os dados do usuário (sem informações sensíveis) ou None se autenticação falhar
        """
        # Buscar usuário pelo email
        users = query_documents(
            AuthService.COLLECTION_NAME, 
            field="email", 
            operator="==", 
            value=email
        )
        
        if not users:
            print(f"Usuário não encontrado: {email}")
            return None
        
        user = users[0]
        user_id = user["id"]
        
        # Verificar a senha
        hashed_password = AuthService._hash_password(password, user["password_salt"])
        
        if hashed_password != user["password_hash"]:
            print("Senha incorreta")
            return None
        
        # Atualizar data do último login
        update_document(
            AuthService.COLLECTION_NAME,
            user_id,
            {"last_login": datetime.datetime.now().isoformat()}
        )
        
        # Retornar dados do usuário sem informações sensíveis
        return {
            "id": user_id,
            "email": user["email"],
            "name": user["name"],
            "profile_image": user.get("profile_image", ""),
            "created_at": user["created_at"],
            "preferences": json.loads(user.get("preferences", "{}"))
        }
    
    @staticmethod
    def get_user(user_id: str) -> Optional[Dict]:
        """
        Obtém os dados de um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com os dados do usuário (sem informações sensíveis) ou None se não encontrado
        """
        user = get_document(AuthService.COLLECTION_NAME, user_id)
        
        if not user:
            return None
        
        # Retornar dados do usuário sem informações sensíveis
        return {
            "id": user_id,
            "email": user["email"],
            "name": user["name"],
            "profile_image": user.get("profile_image", ""),
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
            "last_login": user.get("last_login"),
            "preferences": json.loads(user.get("preferences", "{}"))
        }
    
    @staticmethod
    def update_user_profile(
        user_id: str,
        name: Optional[str] = None,
        profile_image: Optional[str] = None,
        preferences: Optional[Dict] = None
    ) -> bool:
        """
        Atualiza o perfil de um usuário.
        
        Args:
            user_id: ID do usuário
            name: Novo nome (opcional)
            profile_image: Nova URL de imagem de perfil (opcional)
            preferences: Novas preferências do usuário (opcional)
            
        Returns:
            True se a atualização for bem-sucedida, False caso contrário
        """
        # Verificar se o usuário existe
        user = get_document(AuthService.COLLECTION_NAME, user_id)
        
        if not user:
            print(f"Usuário não encontrado: {user_id}")
            return False
        
        # Preparar dados para atualização
        update_data = {"updated_at": datetime.datetime.now().isoformat()}
        
        if name is not None:
            update_data["name"] = name
            
        if profile_image is not None:
            update_data["profile_image"] = profile_image
            
        if preferences is not None:
            # Obter preferências atuais
            current_preferences = json.loads(user.get("preferences", "{}"))
            # Mesclar com as novas preferências
            current_preferences.update(preferences)
            # Salvar preferências atualizadas
            update_data["preferences"] = json.dumps(current_preferences)
        
        # Atualizar usuário no Firestore
        return update_document(AuthService.COLLECTION_NAME, user_id, update_data)
    
    @staticmethod
    def change_password(user_id: str, current_password: str, new_password: str) -> bool:
        """
        Altera a senha de um usuário.
        
        Args:
            user_id: ID do usuário
            current_password: Senha atual
            new_password: Nova senha
            
        Returns:
            True se a alteração for bem-sucedida, False caso contrário
        """
        # Verificar se o usuário existe
        user = get_document(AuthService.COLLECTION_NAME, user_id)
        
        if not user:
            print(f"Usuário não encontrado: {user_id}")
            return False
        
        # Verificar a senha atual
        hashed_current_password = AuthService._hash_password(
            current_password, 
            user["password_salt"]
        )
        
        if hashed_current_password != user["password_hash"]:
            print("Senha atual incorreta")
            return False
        
        # Gerar novo salt e hash para a nova senha
        new_salt = os.urandom(32).hex()
        hashed_new_password = AuthService._hash_password(new_password, new_salt)
        
        # Atualizar senha no Firestore
        update_data = {
            "password_hash": hashed_new_password,
            "password_salt": new_salt,
            "updated_at": datetime.datetime.now().isoformat()
        }
        
        return update_document(AuthService.COLLECTION_NAME, user_id, update_data)
    
    @staticmethod
    def delete_user(user_id: str, password: str) -> bool:
        """
        Exclui um usuário do sistema.
        
        Args:
            user_id: ID do usuário
            password: Senha do usuário para confirmar a exclusão
            
        Returns:
            True se a exclusão for bem-sucedida, False caso contrário
        """
        # Verificar se o usuário existe
        user = get_document(AuthService.COLLECTION_NAME, user_id)
        
        if not user:
            print(f"Usuário não encontrado: {user_id}")
            return False
        
        # Verificar a senha
        hashed_password = AuthService._hash_password(password, user["password_salt"])
        
        if hashed_password != user["password_hash"]:
            print("Senha incorreta para exclusão")
            return False
        
        # Excluir usuário do Firestore
        return delete_document(AuthService.COLLECTION_NAME, user_id)
    
    @staticmethod
    def list_users(limit: Optional[int] = None) -> List[Dict]:
        """
        Lista todos os usuários do sistema (apenas para administradores).
        
        Args:
            limit: Número máximo de usuários a retornar (opcional)
            
        Returns:
            Lista de usuários (sem informações sensíveis)
        """
        # Obter todos os usuários
        users = query_documents(AuthService.COLLECTION_NAME)
        
        # Aplicar limite se especificado
        if limit and limit > 0:
            users = users[:limit]
        
        # Remover informações sensíveis
        result = []
        for user in users:
            user_id = user["id"]
            result.append({
                "id": user_id,
                "email": user["email"],
                "name": user["name"],
                "profile_image": user.get("profile_image", ""),
                "created_at": user["created_at"],
                "last_login": user.get("last_login")
            })
        
        return result
    
    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """
        Gera um hash seguro para a senha.
        
        Args:
            password: Senha em texto plano
            salt: Salt para adicionar à senha
            
        Returns:
            Hash da senha com salt
        """
        # Concatenar senha e salt
        password_salt = password + salt
        
        # Usar SHA-256 para o hash
        return hashlib.sha256(password_salt.encode()).hexdigest()
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """
        Verifica a validade de um token de autenticação.
        
        Args:
            token: Token de autenticação
            
        Returns:
            Dados do usuário associado ao token ou None se token inválido
        """
        # Simples implementação de exemplo
        # Em uma aplicação real, use JWT ou similar
        try:
            # Simular verificação de token
            # Formato simulado: "user_id:timestamp:hash"
            parts = token.split(":")
            if len(parts) != 3:
                return None
            
            user_id = parts[0]
            timestamp = parts[1]
            
            # Verificar se o token expirou (exemplo: 24 horas)
            current_time = datetime.datetime.now().timestamp()
            token_time = float(timestamp)
            
            if current_time - token_time > 24 * 60 * 60:  # 24 horas em segundos
                print("Token expirado")
                return None
            
            # Buscar o usuário
            return AuthService.get_user(user_id)
        
        except Exception as e:
            print(f"Erro ao verificar token: {e}")
            return None
    
    @staticmethod
    def generate_token(user_id: str) -> str:
        """
        Gera um token de autenticação para um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Token de autenticação
        """
        # Simples implementação de exemplo
        # Em uma aplicação real, use JWT ou similar
        timestamp = datetime.datetime.now().timestamp()
        data = f"{user_id}:{timestamp}"
        hash_value = hashlib.sha256(data.encode()).hexdigest()
        
        return f"{user_id}:{timestamp}:{hash_value}" 
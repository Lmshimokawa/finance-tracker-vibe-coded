import datetime
from typing import Dict, List, Optional
import uuid
from pathlib import Path
import sys

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

class CategoryService:
    """
    Serviço para gerenciamento de categorias de transações financeiras.
    """
    
    COLLECTION_NAME = "categories"
    
    @staticmethod
    def add_category(
        name: str,
        category_type: str,  # 'income' ou 'expense'
        color: str,
        icon: str,
        user_id: str,
        description: Optional[str] = None,
        is_default: bool = False
    ) -> Optional[str]:
        """
        Adiciona uma nova categoria.
        
        Args:
            name: Nome da categoria
            category_type: Tipo da categoria ('income' ou 'expense')
            color: Código de cor em hexadecimal (ex: "#FF5733")
            icon: Nome do ícone
            user_id: ID do usuário proprietário da categoria
            description: Descrição da categoria (opcional)
            is_default: Indica se é uma categoria padrão do sistema
            
        Returns:
            ID da categoria adicionada ou None se houver erro
        """
        # Verificar se já existe uma categoria com o mesmo nome e tipo para o usuário
        existing_categories = query_documents(
            CategoryService.COLLECTION_NAME,
            field="user_id",
            operator="==",
            value=user_id
        )
        
        for category in existing_categories:
            if (category.get("name") == name and 
                category.get("type") == category_type):
                print(f"Categoria já existe: {name} ({category_type})")
                return None
        
        # Preparar dados da categoria
        category_data = {
            "name": name,
            "type": category_type,
            "color": color,
            "icon": icon,
            "user_id": user_id,
            "description": description or "",
            "is_default": is_default,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }
        
        # Adicionar categoria ao Firestore
        return add_document(CategoryService.COLLECTION_NAME, category_data)
    
    @staticmethod
    def get_category(category_id: str) -> Optional[Dict]:
        """
        Obtém uma categoria pelo ID.
        
        Args:
            category_id: ID da categoria
            
        Returns:
            Dados da categoria ou None se não encontrada
        """
        return get_document(CategoryService.COLLECTION_NAME, category_id)
    
    @staticmethod
    def update_category(
        category_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """
        Atualiza uma categoria existente.
        
        Args:
            category_id: ID da categoria a ser atualizada
            name: Novo nome (opcional)
            color: Nova cor (opcional)
            icon: Novo ícone (opcional)
            description: Nova descrição (opcional)
            
        Returns:
            True se a atualização for bem-sucedida, False caso contrário
        """
        # Verificar se a categoria existe
        category = get_document(CategoryService.COLLECTION_NAME, category_id)
        
        if not category:
            print(f"Categoria não encontrada: {category_id}")
            return False
        
        # Verificar se é uma categoria padrão
        if category.get("is_default", False):
            print("Não é possível atualizar uma categoria padrão")
            return False
        
        # Preparar dados para atualização
        update_data = {"updated_at": datetime.datetime.now().isoformat()}
        
        if name is not None:
            update_data["name"] = name
            
        if color is not None:
            update_data["color"] = color
            
        if icon is not None:
            update_data["icon"] = icon
            
        if description is not None:
            update_data["description"] = description
        
        # Atualizar categoria no Firestore
        return update_document(CategoryService.COLLECTION_NAME, category_id, update_data)
    
    @staticmethod
    def delete_category(category_id: str) -> bool:
        """
        Exclui uma categoria pelo ID.
        
        Args:
            category_id: ID da categoria a ser excluída
            
        Returns:
            True se a exclusão for bem-sucedida, False caso contrário
        """
        # Verificar se a categoria existe
        category = get_document(CategoryService.COLLECTION_NAME, category_id)
        
        if not category:
            print(f"Categoria não encontrada: {category_id}")
            return False
        
        # Verificar se é uma categoria padrão
        if category.get("is_default", False):
            print("Não é possível excluir uma categoria padrão")
            return False
        
        # Excluir categoria no Firestore
        return delete_document(CategoryService.COLLECTION_NAME, category_id)
    
    @staticmethod
    def list_categories(
        user_id: str,
        category_type: Optional[str] = None,
        include_default: bool = True
    ) -> List[Dict]:
        """
        Lista categorias com base em filtros especificados.
        
        Args:
            user_id: ID do usuário proprietário das categorias
            category_type: Tipo de categoria para filtrar ('income' ou 'expense') (opcional)
            include_default: Indica se deve incluir categorias padrão do sistema
            
        Returns:
            Lista de categorias que correspondem aos critérios de filtro
        """
        # Consulta para obter categorias do usuário
        user_categories = query_documents(
            CategoryService.COLLECTION_NAME,
            field="user_id",
            operator="==",
            value=user_id
        )
        
        # Consulta para obter categorias padrão se necessário
        default_categories = []
        if include_default:
            default_categories = query_documents(
                CategoryService.COLLECTION_NAME,
                field="is_default",
                operator="==",
                value=True
            )
        
        # Combinar resultados
        all_categories = user_categories + default_categories
        
        # Remover possíveis duplicatas (por ID)
        seen_ids = set()
        unique_categories = []
        
        for category in all_categories:
            if category["id"] not in seen_ids:
                seen_ids.add(category["id"])
                unique_categories.append(category)
        
        # Aplicar filtro por tipo se especificado
        if category_type:
            filtered_categories = [
                c for c in unique_categories
                if c.get("type") == category_type
            ]
        else:
            filtered_categories = unique_categories
        
        # Ordenar por nome
        filtered_categories.sort(key=lambda x: x.get("name", ""))
        
        return filtered_categories
    
    @staticmethod
    def create_default_categories(user_id: str) -> List[str]:
        """
        Cria categorias padrão para um novo usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de IDs das categorias criadas
        """
        # Lista de categorias padrão para despesas
        default_expense_categories = [
            {
                "name": "Alimentação",
                "type": "expense",
                "color": "#FF5733",
                "icon": "restaurant",
                "description": "Gastos com alimentação, restaurantes, delivery",
                "is_default": False
            },
            {
                "name": "Moradia",
                "type": "expense",
                "color": "#33A8FF",
                "icon": "home",
                "description": "Aluguel, condomínio, IPTU, manutenção",
                "is_default": False
            },
            {
                "name": "Transporte",
                "type": "expense",
                "color": "#33FF57",
                "icon": "directions_car",
                "description": "Combustível, transporte público, manutenção de veículos",
                "is_default": False
            },
            {
                "name": "Saúde",
                "type": "expense",
                "color": "#C133FF",
                "icon": "medical_services",
                "description": "Plano de saúde, medicamentos, consultas",
                "is_default": False
            },
            {
                "name": "Educação",
                "type": "expense",
                "color": "#FFBD33",
                "icon": "school",
                "description": "Mensalidades, cursos, livros",
                "is_default": False
            },
            {
                "name": "Lazer",
                "type": "expense",
                "color": "#33FFF6",
                "icon": "sports_esports",
                "description": "Entretenimento, viagens, hobbies",
                "is_default": False
            },
            {
                "name": "Vestuário",
                "type": "expense",
                "color": "#FF33A8",
                "icon": "checkroom",
                "description": "Roupas, calçados, acessórios",
                "is_default": False
            }
        ]
        
        # Lista de categorias padrão para receitas
        default_income_categories = [
            {
                "name": "Salário",
                "type": "income",
                "color": "#3358FF",
                "icon": "payments",
                "description": "Salário mensal, bônus, comissões",
                "is_default": False
            },
            {
                "name": "Freelance",
                "type": "income",
                "color": "#33FF85",
                "icon": "work",
                "description": "Trabalhos autônomos e serviços prestados",
                "is_default": False
            },
            {
                "name": "Investimentos",
                "type": "income",
                "color": "#FFBD33",
                "icon": "trending_up",
                "description": "Rendimentos de aplicações financeiras",
                "is_default": False
            },
            {
                "name": "Presentes",
                "type": "income",
                "color": "#FF5733",
                "icon": "card_giftcard",
                "description": "Presentes em dinheiro",
                "is_default": False
            }
        ]
        
        # Combinar todas as categorias padrão
        all_default_categories = default_expense_categories + default_income_categories
        
        # Criar cada categoria e coletar os IDs
        created_ids = []
        
        for category_data in all_default_categories:
            # Adicionar o user_id
            category_data["user_id"] = user_id
            
            # Criar a categoria
            category_id = CategoryService.add_category(
                name=category_data["name"],
                category_type=category_data["type"],
                color=category_data["color"],
                icon=category_data["icon"],
                user_id=user_id,
                description=category_data["description"],
                is_default=category_data["is_default"]
            )
            
            if category_id:
                created_ids.append(category_id)
        
        return created_ids 
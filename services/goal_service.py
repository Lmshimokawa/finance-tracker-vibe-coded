import datetime
from typing import Dict, List, Optional, Union
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

class GoalService:
    """
    Serviço para gerenciamento de metas financeiras.
    """
    
    COLLECTION_NAME = "goals"
    
    @staticmethod
    def add_goal(
        name: str,
        target_amount: float,
        current_amount: float,
        deadline: Union[datetime.date, str],
        user_id: str,
        category: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,  # 'high', 'medium', 'low'
        icon: Optional[str] = None,
        color: Optional[str] = None
    ) -> Optional[str]:
        """
        Adiciona uma nova meta financeira.
        
        Args:
            name: Nome da meta
            target_amount: Valor alvo a ser alcançado
            current_amount: Valor atual já economizado
            deadline: Data limite para atingir a meta
            user_id: ID do usuário proprietário da meta
            category: Categoria da meta (opcional)
            description: Descrição detalhada da meta (opcional)
            priority: Prioridade da meta (opcional)
            icon: Ícone para representar a meta (opcional)
            color: Cor associada à meta (opcional)
            
        Returns:
            ID da meta adicionada ou None se houver erro
        """
        # Converte a data para string ISO se for um objeto date
        if isinstance(deadline, datetime.date):
            deadline_str = deadline.isoformat()
        else:
            deadline_str = str(deadline)
        
        # Preparar dados da meta
        goal_data = {
            "name": name,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "deadline": deadline_str,
            "user_id": user_id,
            "category": category or "Outro",
            "description": description or "",
            "priority": priority or "medium",
            "icon": icon or "flag",
            "color": color or "#3358FF",
            "progress_percentage": (current_amount / target_amount * 100) if target_amount > 0 else 0,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "completed": current_amount >= target_amount,
            "completed_at": datetime.datetime.now().isoformat() if current_amount >= target_amount else None
        }
        
        # Adicionar meta ao Firestore
        return add_document(GoalService.COLLECTION_NAME, goal_data)
    
    @staticmethod
    def get_goal(goal_id: str) -> Optional[Dict]:
        """
        Obtém uma meta pelo ID.
        
        Args:
            goal_id: ID da meta
            
        Returns:
            Dados da meta ou None se não encontrada
        """
        return get_document(GoalService.COLLECTION_NAME, goal_id)
    
    @staticmethod
    def update_goal(
        goal_id: str,
        name: Optional[str] = None,
        target_amount: Optional[float] = None,
        current_amount: Optional[float] = None,
        deadline: Optional[Union[datetime.date, str]] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None
    ) -> bool:
        """
        Atualiza uma meta existente.
        
        Args:
            goal_id: ID da meta a ser atualizada
            name: Novo nome (opcional)
            target_amount: Novo valor alvo (opcional)
            current_amount: Novo valor atual (opcional)
            deadline: Nova data limite (opcional)
            category: Nova categoria (opcional)
            description: Nova descrição (opcional)
            priority: Nova prioridade (opcional)
            icon: Novo ícone (opcional)
            color: Nova cor (opcional)
            
        Returns:
            True se a atualização for bem-sucedida, False caso contrário
        """
        # Verificar se a meta existe
        goal = get_document(GoalService.COLLECTION_NAME, goal_id)
        
        if not goal:
            print(f"Meta não encontrada: {goal_id}")
            return False
        
        # Preparar dados para atualização
        update_data = {"updated_at": datetime.datetime.now().isoformat()}
        
        if name is not None:
            update_data["name"] = name
            
        if target_amount is not None:
            update_data["target_amount"] = target_amount
            
        if current_amount is not None:
            update_data["current_amount"] = current_amount
            
        if deadline is not None:
            # Converte a data para string ISO se for um objeto date
            if isinstance(deadline, datetime.date):
                update_data["deadline"] = deadline.isoformat()
            else:
                update_data["deadline"] = str(deadline)
                
        if category is not None:
            update_data["category"] = category
            
        if description is not None:
            update_data["description"] = description
            
        if priority is not None:
            update_data["priority"] = priority
            
        if icon is not None:
            update_data["icon"] = icon
            
        if color is not None:
            update_data["color"] = color
        
        # Calcular progresso se target_amount ou current_amount mudaram
        if "target_amount" in update_data or "current_amount" in update_data:
            # Obter valores atualizados para cálculo
            target = update_data.get("target_amount", goal.get("target_amount", 0))
            current = update_data.get("current_amount", goal.get("current_amount", 0))
            
            # Calcular progresso percentual
            if target > 0:
                update_data["progress_percentage"] = (current / target * 100)
            else:
                update_data["progress_percentage"] = 0
                
            # Verificar se a meta foi concluída
            if current >= target:
                update_data["completed"] = True
                if not goal.get("completed", False):  # Se ainda não estava marcada como concluída
                    update_data["completed_at"] = datetime.datetime.now().isoformat()
            else:
                update_data["completed"] = False
                update_data["completed_at"] = None
        
        # Atualizar meta no Firestore
        return update_document(GoalService.COLLECTION_NAME, goal_id, update_data)
    
    @staticmethod
    def delete_goal(goal_id: str) -> bool:
        """
        Exclui uma meta pelo ID.
        
        Args:
            goal_id: ID da meta a ser excluída
            
        Returns:
            True se a exclusão for bem-sucedida, False caso contrário
        """
        return delete_document(GoalService.COLLECTION_NAME, goal_id)
    
    @staticmethod
    def list_goals(
        user_id: str,
        include_completed: bool = False,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict]:
        """
        Lista metas com base em filtros especificados.
        
        Args:
            user_id: ID do usuário proprietário das metas
            include_completed: Indica se deve incluir metas já concluídas
            category: Categoria para filtrar (opcional)
            priority: Prioridade para filtrar (opcional)
            
        Returns:
            Lista de metas que correspondem aos critérios de filtro
        """
        # Consulta para obter metas do usuário
        goals = query_documents(
            GoalService.COLLECTION_NAME,
            field="user_id",
            operator="==",
            value=user_id
        )
        
        # Aplicar filtros adicionais
        filtered_goals = goals
        
        # Filtrar por status de conclusão
        if not include_completed:
            filtered_goals = [
                g for g in filtered_goals
                if not g.get("completed", False)
            ]
            
        # Filtrar por categoria
        if category:
            filtered_goals = [
                g for g in filtered_goals
                if g.get("category") == category
            ]
            
        # Filtrar por prioridade
        if priority:
            filtered_goals = [
                g for g in filtered_goals
                if g.get("priority") == priority
            ]
        
        # Ordenar por deadline (mais próximos primeiro) e depois por progresso
        filtered_goals.sort(key=lambda x: (x.get("deadline", ""), 100 - x.get("progress_percentage", 0)))
        
        return filtered_goals
    
    @staticmethod
    def update_goal_progress(
        goal_id: str, 
        amount_to_add: float
    ) -> bool:
        """
        Adiciona um valor ao progresso atual da meta.
        
        Args:
            goal_id: ID da meta
            amount_to_add: Valor a ser adicionado ao progresso atual
            
        Returns:
            True se a atualização for bem-sucedida, False caso contrário
        """
        # Verificar se a meta existe
        goal = get_document(GoalService.COLLECTION_NAME, goal_id)
        
        if not goal:
            print(f"Meta não encontrada: {goal_id}")
            return False
        
        # Calcular novo valor atual
        current_amount = goal.get("current_amount", 0) + amount_to_add
        
        # Atualizar a meta com o novo valor
        return GoalService.update_goal(
            goal_id=goal_id,
            current_amount=current_amount
        )
    
    @staticmethod
    def get_goals_summary(user_id: str) -> Dict:
        """
        Obtém um resumo das metas de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com resumo das metas
        """
        # Obter todas as metas do usuário
        all_goals = GoalService.list_goals(user_id, include_completed=True)
        
        # Separar metas concluídas e pendentes
        completed_goals = [g for g in all_goals if g.get("completed", False)]
        pending_goals = [g for g in all_goals if not g.get("completed", False)]
        
        # Calcular total alvo e atual para metas pendentes
        total_target = sum(g.get("target_amount", 0) for g in pending_goals)
        total_current = sum(g.get("current_amount", 0) for g in pending_goals)
        
        # Calcular progresso geral
        overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
        
        # Encontrar metas próximas do prazo (menos de 30 dias)
        today = datetime.date.today()
        approaching_deadline = []
        
        for goal in pending_goals:
            deadline_str = goal.get("deadline", "")
            if deadline_str:
                try:
                    deadline = datetime.date.fromisoformat(deadline_str)
                    days_remaining = (deadline - today).days
                    
                    if 0 <= days_remaining <= 30:
                        # Adicionar dias restantes à meta
                        goal_with_days = goal.copy()
                        goal_with_days["days_remaining"] = days_remaining
                        approaching_deadline.append(goal_with_days)
                except ValueError:
                    pass  # Ignorar se a data não for válida
        
        # Ordenar por dias restantes (menos dias primeiro)
        approaching_deadline.sort(key=lambda x: x.get("days_remaining", 0))
        
        # Preparar resumo
        summary = {
            "total_goals": len(all_goals),
            "completed_goals": len(completed_goals),
            "pending_goals": len(pending_goals),
            "total_target_amount": total_target,
            "total_current_amount": total_current,
            "overall_progress": overall_progress,
            "approaching_deadline": approaching_deadline[:5]  # Limitar a 5 metas
        }
        
        return summary 
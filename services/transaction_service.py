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

class TransactionService:
    """
    Serviço para gerenciar transações financeiras utilizando Firebase.
    """
    
    COLLECTION_NAME = "transactions"
    
    @staticmethod
    def add_transaction(
        description: str,
        transaction_type: str,
        category: str,
        amount: float,
        date: Union[datetime.date, str],
        user_id: str,
        notes: Optional[str] = None,
        payment_method: Optional[str] = None
    ) -> Optional[str]:
        """
        Adiciona uma nova transação ao banco de dados.
        
        Args:
            description: Descrição da transação
            transaction_type: Tipo de transação ('income' ou 'expense')
            category: Categoria da transação
            amount: Valor da transação
            date: Data da transação (pode ser um objeto date ou string no formato YYYY-MM-DD)
            user_id: ID do usuário proprietário da transação
            notes: Observações adicionais (opcional)
            payment_method: Método de pagamento (opcional)
            
        Returns:
            ID da transação adicionada ou None se houver erro
        """
        # Converte a data para string ISO se for um objeto date
        if isinstance(date, datetime.date):
            date_str = date.isoformat()
        else:
            date_str = str(date)
            
        # Prepara os dados da transação
        transaction_data = {
            "description": description,
            "type": transaction_type,
            "category": category,
            "amount": amount,
            "date": date_str,
            "user_id": user_id,
            "notes": notes or "",
            "payment_method": payment_method or "",
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }
        
        # Adiciona a transação ao Firestore
        return add_document(TransactionService.COLLECTION_NAME, transaction_data)
    
    @staticmethod
    def get_transaction(transaction_id: str) -> Optional[Dict]:
        """
        Obtém uma transação pelo ID.
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Dados da transação ou None se não encontrada
        """
        return get_document(TransactionService.COLLECTION_NAME, transaction_id)
    
    @staticmethod
    def update_transaction(
        transaction_id: str,
        description: Optional[str] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        amount: Optional[float] = None,
        date: Optional[Union[datetime.date, str]] = None,
        notes: Optional[str] = None,
        payment_method: Optional[str] = None
    ) -> bool:
        """
        Atualiza uma transação existente.
        
        Args:
            transaction_id: ID da transação a ser atualizada
            description: Nova descrição (opcional)
            transaction_type: Novo tipo (opcional)
            category: Nova categoria (opcional)
            amount: Novo valor (opcional)
            date: Nova data (opcional)
            notes: Novas observações (opcional)
            payment_method: Novo método de pagamento (opcional)
            
        Returns:
            True se a atualização for bem-sucedida, False caso contrário
        """
        # Prepara os dados para atualização
        update_data = {}
        
        if description is not None:
            update_data["description"] = description
            
        if transaction_type is not None:
            update_data["type"] = transaction_type
            
        if category is not None:
            update_data["category"] = category
            
        if amount is not None:
            update_data["amount"] = amount
            
        if date is not None:
            # Converte a data para string ISO se for um objeto date
            if isinstance(date, datetime.date):
                update_data["date"] = date.isoformat()
            else:
                update_data["date"] = str(date)
                
        if notes is not None:
            update_data["notes"] = notes
            
        if payment_method is not None:
            update_data["payment_method"] = payment_method
            
        # Adiciona timestamp de atualização
        update_data["updated_at"] = datetime.datetime.now().isoformat()
        
        # Atualiza a transação no Firestore
        return update_document(TransactionService.COLLECTION_NAME, transaction_id, update_data)
    
    @staticmethod
    def delete_transaction(transaction_id: str) -> bool:
        """
        Exclui uma transação pelo ID.
        
        Args:
            transaction_id: ID da transação a ser excluída
            
        Returns:
            True se a exclusão for bem-sucedida, False caso contrário
        """
        return delete_document(TransactionService.COLLECTION_NAME, transaction_id)
    
    @staticmethod
    def list_transactions(
        user_id: str,
        start_date: Optional[Union[datetime.date, str]] = None,
        end_date: Optional[Union[datetime.date, str]] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Lista transações com base em filtros especificados.
        
        Args:
            user_id: ID do usuário proprietário das transações
            start_date: Data inicial para filtragem (opcional)
            end_date: Data final para filtragem (opcional)
            transaction_type: Tipo de transação para filtrar (opcional)
            category: Categoria para filtrar (opcional)
            limit: Número máximo de resultados (opcional)
            
        Returns:
            Lista de transações que correspondem aos critérios de filtro
        """
        # Consulta base para obter todas as transações do usuário
        transactions = query_documents(
            TransactionService.COLLECTION_NAME, 
            field="user_id", 
            operator="==", 
            value=user_id
        )
        
        # Aplicar filtros adicionais na lista de resultados
        filtered_transactions = transactions
        
        # Filtro por tipo de transação
        if transaction_type:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.get("type") == transaction_type
            ]
            
        # Filtro por categoria
        if category:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.get("category") == category
            ]
            
        # Filtro por data inicial
        if start_date:
            # Converte para string se for objeto date
            if isinstance(start_date, datetime.date):
                start_date_str = start_date.isoformat()
            else:
                start_date_str = str(start_date)
                
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.get("date") >= start_date_str
            ]
            
        # Filtro por data final
        if end_date:
            # Converte para string se for objeto date
            if isinstance(end_date, datetime.date):
                end_date_str = end_date.isoformat()
            else:
                end_date_str = str(end_date)
                
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.get("date") <= end_date_str
            ]
        
        # Ordenar transações por data (mais recentes primeiro)
        filtered_transactions.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # Aplicar limite se especificado
        if limit and limit > 0:
            filtered_transactions = filtered_transactions[:limit]
        
        return filtered_transactions
    
    @staticmethod
    def get_summary(
        user_id: str,
        start_date: Optional[Union[datetime.date, str]] = None,
        end_date: Optional[Union[datetime.date, str]] = None
    ) -> Dict:
        """
        Calcula resumo financeiro (receitas, despesas, saldo) para um período.
        
        Args:
            user_id: ID do usuário
            start_date: Data inicial para cálculo (opcional)
            end_date: Data final para cálculo (opcional)
            
        Returns:
            Dicionário com os totais de receitas, despesas e saldo
        """
        # Obter transações no período
        transactions = TransactionService.list_transactions(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calcular totais
        total_income = sum(
            t.get("amount", 0) 
            for t in transactions 
            if t.get("type") == "income"
        )
        
        total_expenses = sum(
            t.get("amount", 0) 
            for t in transactions 
            if t.get("type") == "expense"
        )
        
        balance = total_income - total_expenses
        
        # Calcular economia (% da receita que não foi gasta)
        savings_percentage = 0
        if total_income > 0:
            savings_percentage = ((total_income - total_expenses) / total_income) * 100
            # Garantir que não seja negativo
            savings_percentage = max(0, savings_percentage)
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "savings_percentage": savings_percentage
        }
    
    @staticmethod
    def get_category_summary(
        user_id: str,
        transaction_type: str,
        start_date: Optional[Union[datetime.date, str]] = None,
        end_date: Optional[Union[datetime.date, str]] = None
    ) -> List[Dict]:
        """
        Calcula o total por categoria para um determinado tipo de transação.
        
        Args:
            user_id: ID do usuário
            transaction_type: Tipo de transação ('income' ou 'expense')
            start_date: Data inicial para cálculo (opcional)
            end_date: Data final para cálculo (opcional)
            
        Returns:
            Lista de dicionários com categoria e total
        """
        # Obter transações do tipo especificado no período
        transactions = TransactionService.list_transactions(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type
        )
        
        # Dicionário para armazenar o total por categoria
        category_totals = {}
        
        # Calcular o total para cada categoria
        for transaction in transactions:
            category = transaction.get("category", "Outros")
            amount = transaction.get("amount", 0)
            
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        # Converter para lista de dicionários
        result = [
            {"category": category, "amount": amount}
            for category, amount in category_totals.items()
        ]
        
        # Ordenar por valor (maior para menor)
        result.sort(key=lambda x: x["amount"], reverse=True)
        
        return result
    
    @staticmethod
    def get_monthly_summary(
        user_id: str,
        months: int = 6
    ) -> List[Dict]:
        """
        Calcula o resumo financeiro mensal para os últimos meses.
        
        Args:
            user_id: ID do usuário
            months: Número de meses para calcular (padrão: 6)
            
        Returns:
            Lista de dicionários com resumo mensal
        """
        # Data atual
        today = datetime.date.today()
        
        # Lista para armazenar os resumos mensais
        monthly_summaries = []
        
        # Calcular para cada mês
        for i in range(months):
            # Calcular o primeiro dia do mês
            month = today.month - i
            year = today.year
            
            # Ajustar o ano se o mês for negativo
            while month <= 0:
                month += 12
                year -= 1
                
            # Primeiro e último dia do mês
            first_day = datetime.date(year, month, 1)
            
            # Calcular o último dia do mês
            if month == 12:
                last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
            else:
                last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
            
            # Obter resumo para o mês
            summary = TransactionService.get_summary(
                user_id=user_id,
                start_date=first_day,
                end_date=last_day
            )
            
            # Adicionar informações do mês ao resumo
            month_name = first_day.strftime("%B")  # Nome do mês
            month_year = first_day.strftime("%m/%Y")  # Mês/Ano
            
            monthly_summary = {
                "month": month_name,
                "month_year": month_year,
                "income": summary["total_income"],
                "expenses": summary["total_expenses"],
                "balance": summary["balance"],
                "savings_percentage": summary["savings_percentage"]
            }
            
            monthly_summaries.append(monthly_summary)
        
        # Ordenar por data (mais antigo para mais recente)
        monthly_summaries.reverse()
        
        return monthly_summaries 
import datetime
from typing import Dict, List, Optional, Tuple, Union
import calendar
from dateutil.relativedelta import relativedelta
import locale

# Configuração da localização para pt_BR
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except:
        # Fallback para o locale padrão
        pass

def format_date(date: Union[datetime.date, str], format_str: str = "%d/%m/%Y") -> str:
    """
    Formata uma data para string no formato especificado.
    
    Args:
        date: Objeto date ou string no formato ISO (YYYY-MM-DD)
        format_str: String de formato (padrão: DD/MM/YYYY)
        
    Returns:
        Data formatada como string
    """
    if isinstance(date, str):
        try:
            date = datetime.date.fromisoformat(date)
        except ValueError:
            return date  # Retorna a string original se não puder converter
    
    return date.strftime(format_str)

def parse_date(date_str: str, format_str: str = "%d/%m/%Y") -> Optional[datetime.date]:
    """
    Converte uma string de data para um objeto date.
    
    Args:
        date_str: String de data no formato especificado
        format_str: Formato da string de data (padrão: DD/MM/YYYY)
        
    Returns:
        Objeto date ou None se a conversão falhar
    """
    try:
        return datetime.datetime.strptime(date_str, format_str).date()
    except ValueError:
        try:
            # Tenta formato ISO como fallback
            return datetime.date.fromisoformat(date_str)
        except ValueError:
            return None

def get_today() -> datetime.date:
    """
    Retorna a data atual.
    
    Returns:
        Data atual como objeto date
    """
    return datetime.date.today()

def get_first_day_of_month(date: Optional[datetime.date] = None) -> datetime.date:
    """
    Retorna o primeiro dia do mês para a data especificada.
    
    Args:
        date: Data de referência (padrão: data atual)
        
    Returns:
        Primeiro dia do mês como objeto date
    """
    if date is None:
        date = get_today()
    
    return datetime.date(date.year, date.month, 1)

def get_last_day_of_month(date: Optional[datetime.date] = None) -> datetime.date:
    """
    Retorna o último dia do mês para a data especificada.
    
    Args:
        date: Data de referência (padrão: data atual)
        
    Returns:
        Último dia do mês como objeto date
    """
    if date is None:
        date = get_today()
    
    # Obter o último dia do mês
    last_day = calendar.monthrange(date.year, date.month)[1]
    return datetime.date(date.year, date.month, last_day)

def get_date_range(period: str) -> Tuple[datetime.date, datetime.date]:
    """
    Retorna o intervalo de datas para um período específico.
    
    Args:
        period: Período desejado ('today', 'this_week', 'this_month', 'last_month', 
                'this_quarter', 'this_year', 'last_30_days', 'last_90_days', 'custom')
        
    Returns:
        Tupla com data inicial e data final do período
    """
    today = get_today()
    
    if period == "today":
        return today, today
    
    elif period == "this_week":
        # Segunda-feira da semana atual
        start_date = today - datetime.timedelta(days=today.weekday())
        # Domingo da semana atual
        end_date = start_date + datetime.timedelta(days=6)
        return start_date, end_date
    
    elif period == "this_month":
        start_date = get_first_day_of_month(today)
        end_date = get_last_day_of_month(today)
        return start_date, end_date
    
    elif period == "last_month":
        # Último dia do mês anterior
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        start_date = get_first_day_of_month(last_month)
        end_date = get_last_day_of_month(last_month)
        return start_date, end_date
    
    elif period == "this_quarter":
        # Determinar o trimestre atual
        quarter = (today.month - 1) // 3 + 1
        start_month = (quarter - 1) * 3 + 1
        start_date = datetime.date(today.year, start_month, 1)
        # Último dia do último mês do trimestre
        if quarter < 4:
            end_month = quarter * 3
            end_date = datetime.date(today.year, end_month, 1)
            end_date = get_last_day_of_month(end_date)
        else:
            end_date = datetime.date(today.year, 12, 31)
        return start_date, end_date
    
    elif period == "this_year":
        start_date = datetime.date(today.year, 1, 1)
        end_date = datetime.date(today.year, 12, 31)
        return start_date, end_date
    
    elif period == "last_30_days":
        start_date = today - datetime.timedelta(days=29)
        return start_date, today
    
    elif period == "last_90_days":
        start_date = today - datetime.timedelta(days=89)
        return start_date, today
    
    # Período padrão (últimos 30 dias)
    start_date = today - datetime.timedelta(days=29)
    return start_date, today

def get_month_name(month: int, abbreviated: bool = False) -> str:
    """
    Retorna o nome do mês em português.
    
    Args:
        month: Número do mês (1-12)
        abbreviated: Se True, retorna o nome abreviado
        
    Returns:
        Nome do mês em português
    """
    if not 1 <= month <= 12:
        return ""
    
    # Usar um objeto date para obter o nome do mês
    date = datetime.date(2000, month, 1)
    
    if abbreviated:
        return date.strftime("%b").capitalize()
    else:
        return date.strftime("%B").capitalize()

def get_weekday_name(weekday: int, abbreviated: bool = False) -> str:
    """
    Retorna o nome do dia da semana em português.
    
    Args:
        weekday: Número do dia da semana (0-6, onde 0 é segunda-feira)
        abbreviated: Se True, retorna o nome abreviado
        
    Returns:
        Nome do dia da semana em português
    """
    if not 0 <= weekday <= 6:
        return ""
    
    # Usar um objeto date para obter o nome do dia da semana
    # 2000-01-03 foi uma segunda-feira
    date = datetime.date(2000, 1, 3 + weekday)
    
    if abbreviated:
        return date.strftime("%a").capitalize()
    else:
        return date.strftime("%A").capitalize()

def get_relative_date(days: int) -> datetime.date:
    """
    Retorna uma data relativa à data atual.
    
    Args:
        days: Número de dias a adicionar ou subtrair (negativo)
        
    Returns:
        Data relativa como objeto date
    """
    return get_today() + datetime.timedelta(days=days)

def get_relative_month(months: int) -> datetime.date:
    """
    Retorna uma data relativa à data atual em termos de meses.
    
    Args:
        months: Número de meses a adicionar ou subtrair (negativo)
        
    Returns:
        Data relativa como objeto date
    """
    return get_today() + relativedelta(months=months)

def get_date_diff(date1: Union[datetime.date, str], date2: Union[datetime.date, str]) -> int:
    """
    Calcula a diferença em dias entre duas datas.
    
    Args:
        date1: Primeira data (objeto date ou string ISO)
        date2: Segunda data (objeto date ou string ISO)
        
    Returns:
        Diferença em dias (inteiro positivo)
    """
    # Converter strings para objetos date se necessário
    if isinstance(date1, str):
        date1 = parse_date(date1) or get_today()
    
    if isinstance(date2, str):
        date2 = parse_date(date2) or get_today()
    
    # Calcular a diferença em dias
    delta = date2 - date1
    return abs(delta.days)

def get_months_between(start_date: Union[datetime.date, str], end_date: Union[datetime.date, str]) -> List[Tuple[datetime.date, datetime.date]]:
    """
    Retorna uma lista de tuplas com o primeiro e último dia de cada mês entre as datas especificadas.
    
    Args:
        start_date: Data inicial (objeto date ou string ISO)
        end_date: Data final (objeto date ou string ISO)
        
    Returns:
        Lista de tuplas (primeiro_dia, último_dia) para cada mês
    """
    # Converter strings para objetos date se necessário
    if isinstance(start_date, str):
        start_date = parse_date(start_date) or get_today()
    
    if isinstance(end_date, str):
        end_date = parse_date(end_date) or get_today()
    
    # Garantir que start_date seja anterior a end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Inicializar com o primeiro dia do mês da data de início
    current_date = get_first_day_of_month(start_date)
    result = []
    
    # Iterar pelos meses até a data final
    while current_date <= end_date:
        first_day = current_date
        last_day = get_last_day_of_month(current_date)
        
        # Ajustar o intervalo para as datas de início e fim
        if first_day < start_date:
            first_day = start_date
        
        if last_day > end_date:
            last_day = end_date
        
        result.append((first_day, last_day))
        
        # Avançar para o próximo mês
        current_date = (current_date + relativedelta(months=1)).replace(day=1)
    
    return result

def format_period(period: str) -> str:
    """
    Formata um período para exibição.
    
    Args:
        period: Código do período ('today', 'this_week', etc.)
        
    Returns:
        Descrição do período formatada
    """
    today = get_today()
    
    if period == "today":
        return f"Hoje ({format_date(today)})"
    
    elif period == "this_week":
        start_date, end_date = get_date_range("this_week")
        return f"Esta Semana ({format_date(start_date)} - {format_date(end_date)})"
    
    elif period == "this_month":
        month_name = get_month_name(today.month)
        return f"{month_name}/{today.year}"
    
    elif period == "last_month":
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        month_name = get_month_name(last_month.month)
        return f"{month_name}/{last_month.year}"
    
    elif period == "this_quarter":
        quarter = (today.month - 1) // 3 + 1
        return f"{quarter}º Trimestre/{today.year}"
    
    elif period == "this_year":
        return f"Ano de {today.year}"
    
    elif period == "last_30_days":
        start_date, end_date = get_date_range("last_30_days")
        return f"Últimos 30 dias ({format_date(start_date)} - {format_date(end_date)})"
    
    elif period == "last_90_days":
        start_date, end_date = get_date_range("last_90_days")
        return f"Últimos 90 dias ({format_date(start_date)} - {format_date(end_date)})"
    
    elif period == "custom":
        return "Período Personalizado"
    
    return "Período Desconhecido"

def get_period_options() -> List[Dict[str, str]]:
    """
    Retorna uma lista de opções de período para seleção em UI.
    
    Returns:
        Lista de dicionários com código e descrição de cada período
    """
    periods = [
        {"value": "today", "label": "Hoje"},
        {"value": "this_week", "label": "Esta Semana"},
        {"value": "this_month", "label": "Este Mês"},
        {"value": "last_month", "label": "Mês Passado"},
        {"value": "this_quarter", "label": "Este Trimestre"},
        {"value": "this_year", "label": "Este Ano"},
        {"value": "last_30_days", "label": "Últimos 30 dias"},
        {"value": "last_90_days", "label": "Últimos 90 dias"},
        {"value": "custom", "label": "Personalizado"}
    ]
    
    return periods 
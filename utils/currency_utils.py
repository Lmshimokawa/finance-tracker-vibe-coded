from typing import Dict, List, Optional, Union
import locale
from decimal import Decimal, ROUND_HALF_UP

# Configuração da localização para pt_BR
try:
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_MONETARY, 'Portuguese_Brazil')
    except:
        # Fallback para o locale padrão
        pass

def format_currency(
    value: Union[float, int, Decimal], 
    currency_code: str = "BRL", 
    show_symbol: bool = True,
    decimal_places: int = 2
) -> str:
    """
    Formata um valor monetário de acordo com o código da moeda.
    
    Args:
        value: Valor a ser formatado
        currency_code: Código ISO da moeda (padrão: BRL)
        show_symbol: Se True, inclui o símbolo da moeda
        decimal_places: Número de casas decimais
        
    Returns:
        Valor formatado como string
    """
    # Converter para Decimal para garantir precisão
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    
    # Arredondar para o número especificado de casas decimais
    value = value.quantize(Decimal('0.' + '0' * decimal_places), rounding=ROUND_HALF_UP)
    
    # Formatar de acordo com a moeda
    if currency_code == "BRL":
        # Formatação para Real brasileiro
        formatted = format_brl(value, show_symbol, decimal_places)
    elif currency_code == "USD":
        # Formatação para Dólar americano
        formatted = format_usd(value, show_symbol, decimal_places)
    elif currency_code == "EUR":
        # Formatação para Euro
        formatted = format_eur(value, show_symbol, decimal_places)
    else:
        # Formatação genérica
        formatted = format_generic(value, currency_code, show_symbol, decimal_places)
    
    return formatted

def format_brl(value: Decimal, show_symbol: bool = True, decimal_places: int = 2) -> str:
    """
    Formata um valor em Real brasileiro (BRL).
    
    Args:
        value: Valor a ser formatado
        show_symbol: Se True, inclui o símbolo da moeda
        decimal_places: Número de casas decimais
        
    Returns:
        Valor formatado como string
    """
    # Definir o formato das casas decimais
    decimal_format = f",.{decimal_places}f"
    
    # Formatação com separador de milhares e casas decimais
    formatted_value = f"{value:{decimal_format}}"
    
    # Substituir separadores para o padrão brasileiro
    formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Adicionar símbolo se necessário
    if show_symbol:
        return f"R$ {formatted_value}"
    
    return formatted_value

def format_usd(value: Decimal, show_symbol: bool = True, decimal_places: int = 2) -> str:
    """
    Formata um valor em Dólar americano (USD).
    
    Args:
        value: Valor a ser formatado
        show_symbol: Se True, inclui o símbolo da moeda
        decimal_places: Número de casas decimais
        
    Returns:
        Valor formatado como string
    """
    # Definir o formato das casas decimais
    decimal_format = f",.{decimal_places}f"
    
    # Formatação com separador de milhares e casas decimais
    formatted_value = f"{value:{decimal_format}}"
    
    # Adicionar símbolo se necessário
    if show_symbol:
        return f"$ {formatted_value}"
    
    return formatted_value

def format_eur(value: Decimal, show_symbol: bool = True, decimal_places: int = 2) -> str:
    """
    Formata um valor em Euro (EUR).
    
    Args:
        value: Valor a ser formatado
        show_symbol: Se True, inclui o símbolo da moeda
        decimal_places: Número de casas decimais
        
    Returns:
        Valor formatado como string
    """
    # Definir o formato das casas decimais
    decimal_format = f",.{decimal_places}f"
    
    # Formatação com separador de milhares e casas decimais
    formatted_value = f"{value:{decimal_format}}"
    
    # Substituir separadores para o padrão europeu
    formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Adicionar símbolo se necessário
    if show_symbol:
        return f"€ {formatted_value}"
    
    return formatted_value

def format_generic(
    value: Decimal, 
    currency_code: str, 
    show_symbol: bool = True, 
    decimal_places: int = 2
) -> str:
    """
    Formata um valor com um código de moeda genérico.
    
    Args:
        value: Valor a ser formatado
        currency_code: Código ISO da moeda
        show_symbol: Se True, inclui o código da moeda
        decimal_places: Número de casas decimais
        
    Returns:
        Valor formatado como string
    """
    # Definir o formato das casas decimais
    decimal_format = f",.{decimal_places}f"
    
    # Formatação com separador de milhares e casas decimais
    formatted_value = f"{value:{decimal_format}}"
    
    # Adicionar código da moeda se necessário
    if show_symbol:
        return f"{currency_code} {formatted_value}"
    
    return formatted_value

def parse_currency(value_str: str, currency_code: str = "BRL") -> Optional[Decimal]:
    """
    Converte uma string formatada como moeda para um valor Decimal.
    
    Args:
        value_str: String com o valor formatado
        currency_code: Código ISO da moeda (padrão: BRL)
        
    Returns:
        Valor como Decimal ou None se a conversão falhar
    """
    try:
        # Remover símbolo da moeda e espaços
        value_str = value_str.replace("R$", "").replace("$", "").replace("€", "").strip()
        
        if currency_code in ["BRL", "EUR"]:
            # Para moedas que usam vírgula como separador decimal
            value_str = value_str.replace(".", "").replace(",", ".")
        
        # Converter para Decimal
        return Decimal(value_str)
    
    except (ValueError, decimal.InvalidOperation):
        return None

def calculate_percentage(value: Union[float, int, Decimal], total: Union[float, int, Decimal]) -> float:
    """
    Calcula a porcentagem de um valor em relação a um total.
    
    Args:
        value: Valor parcial
        total: Valor total
        
    Returns:
        Porcentagem como float
    """
    if total == 0:
        return 0.0
    
    # Converter para float para cálculo
    value_float = float(value)
    total_float = float(total)
    
    return (value_float / total_float) * 100

def format_percentage(value: Union[float, int, Decimal], decimal_places: int = 1) -> str:
    """
    Formata um valor como porcentagem.
    
    Args:
        value: Valor a ser formatado
        decimal_places: Número de casas decimais
        
    Returns:
        Porcentagem formatada como string
    """
    # Arredondar para o número especificado de casas decimais
    if isinstance(value, Decimal):
        value = value.quantize(Decimal('0.' + '0' * decimal_places), rounding=ROUND_HALF_UP)
    else:
        value = round(float(value), decimal_places)
    
    # Definir o formato das casas decimais
    decimal_format = f",.{decimal_places}f"
    
    # Formatação
    formatted_value = f"{value:{decimal_format}}"
    
    # Para formato brasileiro, substituir ponto por vírgula
    if locale.getlocale(locale.LC_MONETARY)[0] in ['pt_BR', 'Portuguese_Brazil']:
        formatted_value = formatted_value.replace(".", ",")
    
    return f"{formatted_value}%"

def get_currency_options() -> List[Dict[str, str]]:
    """
    Retorna uma lista de opções de moeda para seleção em UI.
    
    Returns:
        Lista de dicionários com código e descrição de cada moeda
    """
    currencies = [
        {"value": "BRL", "label": "Real Brasileiro (R$)"},
        {"value": "USD", "label": "Dólar Americano ($)"},
        {"value": "EUR", "label": "Euro (€)"},
        {"value": "GBP", "label": "Libra Esterlina (£)"},
        {"value": "JPY", "label": "Iene Japonês (¥)"},
        {"value": "CAD", "label": "Dólar Canadense (C$)"},
        {"value": "AUD", "label": "Dólar Australiano (A$)"},
        {"value": "CHF", "label": "Franco Suíço (Fr)"},
        {"value": "CNY", "label": "Yuan Chinês (¥)"},
        {"value": "ARS", "label": "Peso Argentino ($)"}
    ]
    
    return currencies 
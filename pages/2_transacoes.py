import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importações futuras dos serviços
# from services.transaction_service import get_transactions, save_transaction, delete_transaction
# from services.category_service import get_categories
# from services.auth_service import check_authentication

# Configuração da página
st.set_page_config(
    page_title="Transações | Finance Tracker",
    page_icon="💸",
    layout="wide",
)

# CSS personalizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        color: #4F46E5;
        margin-bottom: 1rem;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .income {
        color: #22c55e;
        font-weight: bold;
    }
    .expense {
        color: #ef4444;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título da página
st.markdown('<h1 class="main-header">Gerenciar Transações</h1>', unsafe_allow_html=True)

# Tabs para alternar entre registro e lista
tab1, tab2 = st.tabs(["Registrar Transação", "Listar Transações"])

# Tab de Registro de Transação
with tab1:
    st.markdown("### Nova Transação")
    
    with st.form(key="transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            descricao = st.text_input("Descrição", placeholder="Ex: Mercado, Salário, etc.")
            
            tipo = st.selectbox(
                "Tipo",
                options=["Despesa", "Receita"],
                index=0
            )
            
            categorias = [
                "Alimentação", "Moradia", "Transporte", "Lazer", 
                "Saúde", "Educação", "Trabalho", "Investimentos", "Outros"
            ]
            categoria = st.selectbox("Categoria", options=categorias)
            
        with col2:
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            data = st.date_input("Data", value=datetime.date.today())
            observacao = st.text_area("Observação (opcional)", height=95)
        
        submitted = st.form_submit_button("Salvar Transação")
        
        if submitted:
            st.success(f"Transação {tipo} de R$ {valor:.2f} registrada com sucesso!")
            # Aqui entra a lógica para salvar no Firebase
            # save_transaction(user_id, descricao, valor, data, tipo, categoria, observacao)

# Tab de Listagem de Transações
with tab2:
    st.markdown("### Transações Registradas")
    
    # Filtros
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    
    with col1:
        data_inicial = st.date_input(
            "Data Inicial",
            value=datetime.date.today().replace(day=1),  # Primeiro dia do mês
            key="data_inicial"
        )
    
    with col2:
        data_final = st.date_input(
            "Data Final",
            value=datetime.date.today(),
            key="data_final"
        )
    
    with col3:
        filtro_tipo = st.selectbox(
            "Tipo",
            options=["Todos", "Despesa", "Receita"],
            index=0,
            key="filtro_tipo"
        )
    
    with col4:
        categorias_filtro = ["Todos"] + [
            "Alimentação", "Moradia", "Transporte", "Lazer", 
            "Saúde", "Educação", "Trabalho", "Investimentos", "Outros"
        ]
        filtro_categoria = st.selectbox("Categoria", options=categorias_filtro, index=0)
    
    st.markdown("---")
    
    # Dados de exemplo para a tabela de transações
    dados_exemplo = {
        'id': ['1', '2', '3', '4', '5', '6', '7', '8'],
        'descricao': ['Supermercado', 'Aluguel', 'Salário', 'Restaurante', 'Cinema', 'Farmácia', 'Freelance', 'Gasolina'],
        'valor': [250.00, 1200.00, 5000.00, 75.50, 45.00, 120.00, 800.00, 180.00],
        'data': [
            datetime.date(2023, 3, 1),
            datetime.date(2023, 3, 5),
            datetime.date(2023, 3, 5),
            datetime.date(2023, 3, 10),
            datetime.date(2023, 3, 12),
            datetime.date(2023, 3, 15),
            datetime.date(2023, 3, 20),
            datetime.date(2023, 3, 25),
        ],
        'tipo': ['Despesa', 'Despesa', 'Receita', 'Despesa', 'Despesa', 'Despesa', 'Receita', 'Despesa'],
        'categoria': ['Alimentação', 'Moradia', 'Trabalho', 'Alimentação', 'Lazer', 'Saúde', 'Trabalho', 'Transporte']
    }
    
    df = pd.DataFrame(dados_exemplo)
    
    # Aplicando filtros
    if filtro_tipo != "Todos":
        df = df[df['tipo'] == filtro_tipo]
    
    if filtro_categoria != "Todos":
        df = df[df['categoria'] == filtro_categoria]
    
    df = df[(df['data'] >= data_inicial) & (df['data'] <= data_final)]
    
    # Tabela de transações
    st.dataframe(
        df,
        column_config={
            "id": None,  # Esconde a coluna ID
            "descricao": "Descrição",
            "valor": st.column_config.NumberColumn(
                "Valor (R$)",
                format="R$ %.2f",
            ),
            "data": st.column_config.DateColumn(
                "Data",
                format="DD/MM/YYYY",
            ),
            "tipo": "Tipo",
            "categoria": "Categoria",
            "ações": st.column_config.Column(
                "Ações",
                width="small",
            )
        },
        hide_index=True,
        use_container_width=True,
    )
    
    # Resumo
    receitas = df[df['tipo'] == 'Receita']['valor'].sum()
    despesas = df[df['tipo'] == 'Despesa']['valor'].sum()
    saldo = receitas - despesas
    
    st.markdown("---")
    st.markdown("### Resumo do período")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<h3 class='income'>Receitas: R$ {receitas:.2f}</h3>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<h3 class='expense'>Despesas: R$ {despesas:.2f}</h3>", unsafe_allow_html=True)
    
    with col3:
        if saldo >= 0:
            st.markdown(f"<h3 class='income'>Saldo: R$ {saldo:.2f}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 class='expense'>Saldo: R$ {saldo:.2f}</h3>", unsafe_allow_html=True)
    
    # Opções de exportação
    st.markdown("### Exportar dados")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exportar para CSV", use_container_width=True):
            st.success("Arquivo CSV gerado com sucesso!")
            # Logic para download do CSV
    
    with col2:
        if st.button("Exportar para Excel", use_container_width=True):
            st.success("Arquivo Excel gerado com sucesso!")
            # Logic para download do Excel 
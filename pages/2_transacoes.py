import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para importações futuras
sys.path.append(str(Path(__file__).parent.parent))

# Configuração da página
st.set_page_config(
    page_title="Transações | Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .transaction-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .income-indicator {
        color: #4caf50;
        font-weight: 600;
    }
    
    .expense-indicator {
        color: #f44336;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>Gerenciar Transações</h1>", unsafe_allow_html=True)

# Abas para registrar e listar transações
tab1, tab2 = st.tabs(["Registrar Transação", "Listar Transações"])

with tab1:
    # Formulário para registrar transação
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input("Descrição", placeholder="Ex: Supermercado, Salário")
            transaction_type = st.selectbox(
                "Tipo",
                ["Receita", "Despesa"]
            )
            category = st.selectbox(
                "Categoria",
                ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Salário", "Investimentos", "Outros"]
            )
        
        with col2:
            value = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            date = st.date_input("Data", datetime.datetime.now())
            notes = st.text_area("Observações (opcional)", placeholder="Detalhes adicionais sobre a transação")
        
        submit_button = st.form_submit_button("Registrar Transação", use_container_width=True)
        
        if submit_button:
            # Em uma aplicação real, salvaríamos no banco de dados
            st.success(f"Transação registrada com sucesso: {description} - R$ {value:.2f}")

with tab2:
    # Filtros para buscar transações
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input("Data inicial", datetime.datetime.now() - datetime.timedelta(days=30))
    
    with col2:
        end_date = st.date_input("Data final", datetime.datetime.now())
    
    with col3:
        filter_type = st.selectbox(
            "Tipo",
            ["Todos", "Receitas", "Despesas"],
            index=0
        )
    
    filter_category = st.multiselect(
        "Categorias",
        ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Salário", "Investimentos", "Outros"],
        default=[]
    )
    
    # Dados de exemplo para transações
    transactions_data = {
        'id': list(range(1, 11)),
        'data': pd.date_range(end=datetime.datetime.now(), periods=10).tolist(),
        'descricao': [
            'Supermercado', 'Aluguel', 'Salário', 'Academia', 'Farmácia',
            'Restaurante', 'Combustível', 'Internet', 'Curso Online', 'Investimento'
        ],
        'categoria': [
            'Alimentação', 'Moradia', 'Salário', 'Saúde', 'Saúde',
            'Alimentação', 'Transporte', 'Moradia', 'Educação', 'Investimentos'
        ],
        'tipo': [
            'Despesa', 'Despesa', 'Receita', 'Despesa', 'Despesa',
            'Despesa', 'Despesa', 'Despesa', 'Despesa', 'Receita'
        ],
        'valor': [
            320.50, 1200.00, 5000.00, 120.00, 85.75,
            65.90, 200.00, 120.00, 150.00, 750.00
        ]
    }
    
    df_transactions = pd.DataFrame(transactions_data)
    
    # Aplicar filtros
    mask = (df_transactions['data'] >= pd.Timestamp(start_date)) & \
           (df_transactions['data'] <= pd.Timestamp(end_date))
    
    if filter_type != "Todos":
        tipo_filtro = "Receita" if filter_type == "Receitas" else "Despesa"
        mask = mask & (df_transactions['tipo'] == tipo_filtro)
    
    if filter_category:
        mask = mask & (df_transactions['categoria'].isin(filter_category))
    
    filtered_df = df_transactions[mask]
    
    # Exibir resultados filtrados
    if not filtered_df.empty:
        st.write(f"**{len(filtered_df)} transações encontradas**")
        
        # Formatar a exibição da tabela
        filtered_df['data'] = filtered_df['data'].dt.strftime('%d/%m/%Y')
        
        # Colorir os valores de acordo com o tipo
        def color_valor(val):
            color = 'green' if val[0] == 'Receita' else 'red'
            valor = val[1]
            return f'color: {color}'
        
        # Reordenar e renomear colunas
        columns_to_display = ['data', 'descricao', 'categoria', 'tipo', 'valor']
        display_names = {'data': 'Data', 'descricao': 'Descrição', 'categoria': 'Categoria', 'tipo': 'Tipo', 'valor': 'Valor (R$)'}
        
        styled_df = filtered_df[columns_to_display].rename(columns=display_names)
        
        # Exibir a tabela
        st.dataframe(
            styled_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Resumo
        total_receitas = filtered_df[filtered_df['tipo'] == 'Receita']['valor'].sum()
        total_despesas = filtered_df[filtered_df['tipo'] == 'Despesa']['valor'].sum()
        saldo = total_receitas - total_despesas
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Receitas", f"R$ {total_receitas:.2f}")
        
        with col2:
            st.metric("Total de Despesas", f"R$ {total_despesas:.2f}")
        
        with col3:
            st.metric("Saldo", f"R$ {saldo:.2f}", delta=f"R$ {saldo:.2f}")
        
        # Opções para exportar
        st.subheader("Exportar dados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Exportar para CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name=f"transacoes_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                label="Exportar para Excel",
                data=filtered_df.to_csv(index=False).encode('utf-8'),  # Em uma app real, usaríamos BytesIO para Excel
                file_name=f"transacoes_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Nenhuma transação encontrada com os filtros aplicados.")
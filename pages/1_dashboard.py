import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para importações futuras
sys.path.append(str(Path(__file__).parent.parent))

# Configuração da página
st.set_page_config(
    page_title="Dashboard | Finance Tracker",
    page_icon="📊",
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
    
    .metric-card {
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-revenue {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    
    .metric-expense {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    
    .metric-balance {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    
    .metric-saving {
        background-color: #fff8e1;
        border-left: 5px solid #ffc107;
    }
    
    .metric-label {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .goal-container {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .goal-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>Dashboard Financeiro</h1>", unsafe_allow_html=True)

# Seletor de período
col_period, col_refresh = st.columns([4, 1])
with col_period:
    period = st.selectbox(
        "Selecione o período:",
        ["Último mês", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Todos os tempos"]
    )
with col_refresh:
    st.button("🔄 Atualizar", use_container_width=True)

# Resumo financeiro
st.subheader("Resumo Financeiro")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card metric-revenue'>
        <div class='metric-label'>Receitas</div>
        <div class='metric-value'>R$ 5.750,00</div>
        <div>+12% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card metric-expense'>
        <div class='metric-label'>Despesas</div>
        <div class='metric-value'>R$ 3.280,00</div>
        <div>-5% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card metric-balance'>
        <div class='metric-label'>Saldo</div>
        <div class='metric-value'>R$ 2.470,00</div>
        <div>+35% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card metric-saving'>
        <div class='metric-label'>Economia</div>
        <div class='metric-value'>43%</div>
        <div>+8% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

# Dados de exemplo para visualizações
despesas_categorias = {
    'Moradia': 1200,
    'Alimentação': 850,
    'Transporte': 350,
    'Lazer': 280,
    'Saúde': 400,
    'Educação': 200
}

# Visualização de dados
st.subheader("Análise de Gastos e Receitas")
col1, col2 = st.columns(2)

with col1:
    # Gráfico de despesas por categoria
    st.markdown("<div class='chart-title'>Despesas por Categoria</div>", unsafe_allow_html=True)
    fig = px.pie(
        values=list(despesas_categorias.values()),
        names=list(despesas_categorias.keys()),
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Transações por categoria
    st.markdown("<div class='chart-title'>Transações por Categoria</div>", unsafe_allow_html=True)
    
    df_transacoes = pd.DataFrame({
        'Categoria': list(despesas_categorias.keys()),
        'Valor': list(despesas_categorias.values())
    })
    
    fig = px.bar(
        df_transacoes,
        x='Categoria',
        y='Valor',
        color='Categoria',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# Timeline de evolução financeira
st.subheader("Evolução Financeira")

# Dados de exemplo para a linha do tempo
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
receitas = [4200, 4500, 4800, 5100, 5400, 5750]
despesas = [3500, 3400, 3450, 3200, 3300, 3280]
saldos = [r - d for r, d in zip(receitas, despesas)]

df_timeline = pd.DataFrame({
    'Mês': meses,
    'Receitas': receitas,
    'Despesas': despesas,
    'Saldo': saldos
})

fig = px.line(
    df_timeline, 
    x='Mês', 
    y=['Receitas', 'Despesas', 'Saldo'],
    markers=True,
    color_discrete_sequence=['#2196f3', '#f44336', '#4caf50']
)

fig.update_layout(
    xaxis_title='',
    yaxis_title='Valor (R$)',
    legend_title='',
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# Metas financeiras
st.subheader("Metas Financeiras")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='goal-title'>Fundo de Emergência</div>", unsafe_allow_html=True)
    meta_emergencia = 10000
    atual_emergencia = 4500
    porcentagem_emergencia = int((atual_emergencia / meta_emergencia) * 100)
    st.progress(porcentagem_emergencia / 100)
    st.caption(f"R$ {atual_emergencia:.2f} de R$ {meta_emergencia:.2f} ({porcentagem_emergencia}%)")

with col2:
    st.markdown("<div class='goal-title'>Férias</div>", unsafe_allow_html=True)
    meta_ferias = 5000
    atual_ferias = 3200
    porcentagem_ferias = int((atual_ferias / meta_ferias) * 100)
    st.progress(porcentagem_ferias / 100)
    st.caption(f"R$ {atual_ferias:.2f} de R$ {meta_ferias:.2f} ({porcentagem_ferias}%)")
import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importações futuras dos serviços
# from services.transaction_service import get_transactions_by_user
# from services.auth_service import check_authentication

# Configuração da página
st.set_page_config(
    page_title="Dashboard | Finance Tracker",
    page_icon="📊",
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
    </style>
""", unsafe_allow_html=True)

# Título da página
st.markdown('<h1 class="main-header">Dashboard Financeiro</h1>', unsafe_allow_html=True)

# Seletor de período
col1, col2 = st.columns([1, 3])
with col1:
    periodo = st.selectbox(
        "Selecione o período:",
        ["Último mês", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Período personalizado"]
    )

if periodo == "Período personalizado":
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data inicial", datetime.date.today() - datetime.timedelta(days=30))
    with col2:
        data_fim = st.date_input("Data final", datetime.date.today())

# Resumo financeiro
st.markdown("### Resumo Financeiro")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Receitas", "R$ 5.000,00", "+10%")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Despesas", "R$ 3.750,00", "-5%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Saldo", "R$ 1.250,00", "+25%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Economia", "25%", "+5%")
    st.markdown('</div>', unsafe_allow_html=True)

# Dados de exemplo para os gráficos
df_exemplo = pd.DataFrame({
    'categoria': ['Alimentação', 'Moradia', 'Transporte', 'Lazer', 'Saúde', 'Educação', 'Outros'],
    'valor': [800, 1200, 500, 300, 400, 350, 200]
})

receitas_exemplo = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=6, freq='M'),
    'valor': [4800, 4900, 5000, 5100, 5000, 5200]
})

despesas_exemplo = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=6, freq='M'),
    'valor': [3600, 3800, 3700, 3900, 3750, 3850]
})

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Despesas por Categoria")
    fig_pie = px.pie(df_exemplo, values='valor', names='categoria', hole=0.4,
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("### Transações por Categoria")
    fig_bar = px.bar(df_exemplo, x='categoria', y='valor', color='categoria',
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_bar.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_bar, use_container_width=True)

# Linha do tempo
st.markdown("### Evolução Financeira")
df_timeline = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=6, freq='M'),
    'Receitas': [4800, 4900, 5000, 5100, 5000, 5200],
    'Despesas': [3600, 3800, 3700, 3900, 3750, 3850],
    'Saldo': [1200, 1100, 1300, 1200, 1250, 1350]
})

df_timeline_melted = pd.melt(df_timeline, id_vars=['data'], value_vars=['Receitas', 'Despesas', 'Saldo'],
                           var_name='Tipo', value_name='Valor')

fig_line = px.line(df_timeline_melted, x='data', y='Valor', color='Tipo', markers=True,
                 color_discrete_map={'Receitas': '#22c55e', 'Despesas': '#ef4444', 'Saldo': '#3b82f6'})
fig_line.update_layout(margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_line, use_container_width=True)

# Metas e objetivos
st.markdown("### Metas Financeiras")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fundo de Emergência")
    meta_emergencia = 10000
    atual_emergencia = 6500
    progresso_emergencia = int((atual_emergencia / meta_emergencia) * 100)
    
    st.progress(progresso_emergencia / 100)
    st.markdown(f"<p>R$ {atual_emergencia:.2f} de R$ {meta_emergencia:.2f} ({progresso_emergencia}%)</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Viagem de Férias")
    meta_ferias = 5000
    atual_ferias = 2000
    progresso_ferias = int((atual_ferias / meta_ferias) * 100)
    
    st.progress(progresso_ferias / 100)
    st.markdown(f"<p>R$ {atual_ferias:.2f} de R$ {meta_ferias:.2f} ({progresso_ferias}%)</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) 
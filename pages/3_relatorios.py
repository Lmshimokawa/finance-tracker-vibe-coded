import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importações futuras dos serviços
# from services.transaction_service import get_transactions_by_period
# from services.auth_service import check_authentication

# Configuração da página
st.set_page_config(
    page_title="Relatórios | Finance Tracker",
    page_icon="📈",
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
    .report-section {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título da página
st.markdown('<h1 class="main-header">Relatórios Financeiros</h1>', unsafe_allow_html=True)

# Seletor de período e tipo de relatório
col1, col2 = st.columns(2)

with col1:
    periodo = st.selectbox(
        "Período de análise:",
        ["Último mês", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Período personalizado"],
        index=0
    )
    
    if periodo == "Período personalizado":
        data_inicio = st.date_input("Data inicial", 
                                   value=datetime.date.today().replace(day=1) - datetime.timedelta(days=30),
                                   key="relatorio_data_inicio")
        data_fim = st.date_input("Data final", 
                                value=datetime.date.today(),
                                key="relatorio_data_fim")

with col2:
    tipo_relatorio = st.selectbox(
        "Tipo de relatório:",
        ["Visão Geral", "Despesas", "Receitas", "Fluxo de Caixa", "Tendências"],
        index=0
    )

# Dados de exemplo para os gráficos
categorias_despesas = ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Outros"]
valores_despesas = [800, 1200, 500, 300, 400, 350, 200]

categorias_receitas = ["Salário", "Freelance", "Investimentos", "Outros"]
valores_receitas = [4000, 800, 150, 50]

df_timeline = pd.DataFrame({
    'data': pd.date_range(start='2023-01-01', periods=6, freq='M'),
    'Receitas': [4800, 4900, 5000, 5100, 5000, 5200],
    'Despesas': [3600, 3800, 3700, 3900, 3750, 3850],
    'Saldo': [1200, 1100, 1300, 1200, 1250, 1350]
})

# Relatório de Visão Geral
if tipo_relatorio == "Visão Geral":
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("## Resumo Financeiro")
    
    # Cards de resumo
    col1, col2, col3, col4 = st.columns(4)
    
    receitas_total = sum(valores_receitas)
    despesas_total = sum(valores_despesas)
    saldo = receitas_total - despesas_total
    economia = (saldo / receitas_total) * 100 if receitas_total > 0 else 0
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Receitas", f"R$ {receitas_total:.2f}", "+10%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Despesas", f"R$ {despesas_total:.2f}", "-5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Saldo", f"R$ {saldo:.2f}", "+25%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Economia", f"{economia:.1f}%", "+5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráficos
    st.markdown("## Composição Financeira")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Despesas por Categoria")
        fig_despesas = px.pie(
            names=categorias_despesas,
            values=valores_despesas,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_despesas.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_despesas, use_container_width=True)
    
    with col2:
        st.markdown("### Receitas por Categoria")
        fig_receitas = px.pie(
            names=categorias_receitas,
            values=valores_receitas,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig_receitas.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_receitas, use_container_width=True)
    
    # Evolução mensal
    st.markdown("## Evolução Mensal")
    
    df_timeline_melted = pd.melt(
        df_timeline, 
        id_vars=['data'], 
        value_vars=['Receitas', 'Despesas', 'Saldo'],
        var_name='Tipo', 
        value_name='Valor'
    )
    
    fig_timeline = px.line(
        df_timeline_melted, 
        x='data', 
        y='Valor', 
        color='Tipo', 
        markers=True,
        color_discrete_map={'Receitas': '#22c55e', 'Despesas': '#ef4444', 'Saldo': '#3b82f6'}
    )
    fig_timeline.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Relatório de Despesas
elif tipo_relatorio == "Despesas":
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("## Análise de Despesas")
    
    # Gráfico de barras
    st.markdown("### Despesas por Categoria")
    fig_bar = px.bar(
        x=categorias_despesas,
        y=valores_despesas,
        color=categorias_despesas,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_bar.update_layout(showlegend=False, xaxis_title="Categoria", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tendência de despesas
    st.markdown("### Tendência de Despesas")
    fig_line = px.line(
        df_timeline,
        x='data',
        y='Despesas',
        markers=True,
        color_discrete_sequence=['#ef4444']
    )
    fig_line.update_layout(xaxis_title="Mês", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Top despesas
    st.markdown("### Top 5 Maiores Despesas")
    
    # Criar dados de exemplo para o top 5
    top_despesas = pd.DataFrame({
        'Descrição': ['Aluguel', 'Supermercado', 'Financiamento', 'Escola', 'Internet'],
        'Valor': [1200, 800, 600, 400, 150],
        'Categoria': ['Moradia', 'Alimentação', 'Financiamentos', 'Educação', 'Serviços']
    })
    
    st.dataframe(
        top_despesas,
        column_config={
            "Descrição": st.column_config.TextColumn("Descrição"),
            "Valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
            "Categoria": st.column_config.TextColumn("Categoria"),
        },
        hide_index=True,
        use_container_width=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Relatório de Receitas
elif tipo_relatorio == "Receitas":
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("## Análise de Receitas")
    
    # Gráfico de barras
    st.markdown("### Receitas por Categoria")
    fig_bar = px.bar(
        x=categorias_receitas,
        y=valores_receitas,
        color=categorias_receitas,
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig_bar.update_layout(showlegend=False, xaxis_title="Categoria", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tendência de receitas
    st.markdown("### Tendência de Receitas")
    fig_line = px.line(
        df_timeline,
        x='data',
        y='Receitas',
        markers=True,
        color_discrete_sequence=['#22c55e']
    )
    fig_line.update_layout(xaxis_title="Mês", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Variação percentual
    st.markdown("### Variação Percentual de Receitas")
    
    # Calcular variação percentual
    df_timeline['Variacao'] = df_timeline['Receitas'].pct_change() * 100
    df_timeline['Variacao'].fillna(0, inplace=True)
    
    fig_var = go.Figure()
    fig_var.add_trace(go.Bar(
        x=df_timeline['data'],
        y=df_timeline['Variacao'],
        marker_color=['#22c55e' if x >= 0 else '#ef4444' for x in df_timeline['Variacao']]
    ))
    fig_var.update_layout(xaxis_title="Mês", yaxis_title="Variação (%)")
    st.plotly_chart(fig_var, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Relatório de Fluxo de Caixa
elif tipo_relatorio == "Fluxo de Caixa":
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("## Fluxo de Caixa")
    
    # Gráfico de barras empilhadas
    st.markdown("### Receitas vs Despesas")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_timeline['data'],
        y=df_timeline['Receitas'],
        name='Receitas',
        marker_color='#22c55e'
    ))
    fig.add_trace(go.Bar(
        x=df_timeline['data'],
        y=df_timeline['Despesas'],
        name='Despesas',
        marker_color='#ef4444'
    ))
    
    fig.update_layout(barmode='group', xaxis_title="Mês", yaxis_title="Valor (R$)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Evolução do saldo
    st.markdown("### Evolução do Saldo")
    
    fig_saldo = px.area(
        df_timeline,
        x='data',
        y='Saldo',
        color_discrete_sequence=['#3b82f6']
    )
    fig_saldo.update_layout(xaxis_title="Mês", yaxis_title="Saldo (R$)")
    st.plotly_chart(fig_saldo, use_container_width=True)
    
    # Tabela de fluxo de caixa
    st.markdown("### Tabela de Fluxo de Caixa")
    
    st.dataframe(
        df_timeline,
        column_config={
            "data": st.column_config.DateColumn("Mês", format="MMM/YYYY"),
            "Receitas": st.column_config.NumberColumn("Receitas", format="R$ %.2f"),
            "Despesas": st.column_config.NumberColumn("Despesas", format="R$ %.2f"),
            "Saldo": st.column_config.NumberColumn("Saldo", format="R$ %.2f"),
        },
        hide_index=True,
        use_container_width=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Relatório de Tendências
elif tipo_relatorio == "Tendências":
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("## Análise de Tendências")
    
    # Projeção para os próximos meses
    st.markdown("### Projeção para os Próximos Meses")
    
    # Dados de projeção
    meses_futuros = pd.date_range(start='2023-07-01', periods=3, freq='M')
    projecao = pd.DataFrame({
        'data': pd.concat([pd.Series(df_timeline['data']), pd.Series(meses_futuros)]),
        'Receitas': [4800, 4900, 5000, 5100, 5000, 5200, 5300, 5400, 5500],
        'Despesas': [3600, 3800, 3700, 3900, 3750, 3850, 3900, 3950, 4000],
    })
    
    projecao['Saldo'] = projecao['Receitas'] - projecao['Despesas']
    
    # Adicionar linha tracejada para separar dados reais de projeções
    fig = go.Figure()
    
    # Dados reais (6 primeiros meses)
    fig.add_trace(go.Scatter(
        x=projecao['data'][:6],
        y=projecao['Receitas'][:6],
        mode='lines+markers',
        name='Receitas (Atual)',
        line=dict(color='#22c55e', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=projecao['data'][:6],
        y=projecao['Despesas'][:6],
        mode='lines+markers',
        name='Despesas (Atual)',
        line=dict(color='#ef4444', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=projecao['data'][:6],
        y=projecao['Saldo'][:6],
        mode='lines+markers',
        name='Saldo (Atual)',
        line=dict(color='#3b82f6', width=3)
    ))
    
    # Projeções (3 últimos meses)
    fig.add_trace(go.Scatter(
        x=projecao['data'][5:],
        y=projecao['Receitas'][5:],
        mode='lines+markers',
        name='Receitas (Projeção)',
        line=dict(color='#22c55e', width=3, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=projecao['data'][5:],
        y=projecao['Despesas'][5:],
        mode='lines+markers',
        name='Despesas (Projeção)',
        line=dict(color='#ef4444', width=3, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=projecao['data'][5:],
        y=projecao['Saldo'][5:],
        mode='lines+markers',
        name='Saldo (Projeção)',
        line=dict(color='#3b82f6', width=3, dash='dash')
    ))
    
    # Linha vertical para separar dados reais de projeções
    fig.add_vline(x=projecao['data'][5], line_width=2, line_dash="dash", line_color="gray")
    fig.add_annotation(x=projecao['data'][5], y=projecao['Receitas'].max(),
                     text="Projeção", showarrow=True, arrowhead=1, ax=50)
    
    fig.update_layout(xaxis_title="Mês", yaxis_title="Valor (R$)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de tendência por categoria
    st.markdown("### Análise de Tendência por Categoria")
    
    # Dados de exemplo para tendência de categorias
    categoria_tendencia = pd.DataFrame({
        'Categoria': categorias_despesas,
        'Atual': valores_despesas,
        'Média Anterior': [750, 1150, 520, 320, 380, 320, 180],
        'Tendência': ['+6.7%', '+4.3%', '-3.8%', '-6.3%', '+5.3%', '+9.4%', '+11.1%']
    })
    
    st.dataframe(
        categoria_tendencia,
        column_config={
            "Categoria": st.column_config.TextColumn("Categoria"),
            "Atual": st.column_config.NumberColumn("Mês Atual (R$)", format="R$ %.2f"),
            "Média Anterior": st.column_config.NumberColumn("Média 3 Meses (R$)", format="R$ %.2f"),
            "Tendência": st.column_config.TextColumn("Tendência"),
        },
        hide_index=True,
        use_container_width=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Opções de exportação
st.markdown("---")
st.markdown("### Exportar Relatório")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Exportar como PDF", use_container_width=True):
        st.success("Relatório PDF gerado com sucesso!")
        # Logic para download do PDF

with col2:
    if st.button("Exportar como Excel", use_container_width=True):
        st.success("Relatório Excel gerado com sucesso!")
        # Logic para download do Excel

with col3:
    if st.button("Enviar por E-mail", use_container_width=True):
        st.success("Relatório enviado por e-mail com sucesso!")
        # Logic para envio por e-mail 
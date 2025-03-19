import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from pathlib import Path
import sys
import json

# Adiciona o diretório raiz ao path para importações
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from services.goal_service import GoalService
from utils.currency_utils import format_currency, format_percentage
from utils.date_utils import format_date, parse_date, get_today

# Configuração da página
st.set_page_config(
    page_title="Metas Financeiras | Finance Tracker",
    page_icon="🎯",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1E88E5;
    }
    
    .subheader {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        margin-top: 1rem;
        color: #0D47A1;
    }
    
    .card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f0f2f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .card-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #333;
    }
    
    .card-content {
        font-size: 1rem;
        color: #666;
    }
    
    .goal-progress {
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .goal-high {
        border-left: 4px solid #E53935;
    }
    
    .goal-medium {
        border-left: 4px solid #FB8C00;
    }
    
    .goal-low {
        border-left: 4px solid #43A047;
    }
    
    .goal-completed {
        border-left: 4px solid #757575;
        opacity: 0.8;
    }
    
    .goal-info {
        display: flex;
        justify-content: space-between;
    }
    
    .goal-date {
        font-size: 0.8rem;
        color: #757575;
    }
    
    .goal-amount {
        font-weight: 600;
    }
    
    .form-section {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    /* Estiliza gráfico de progresso */
    .progress-container {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 4px;
        margin: 8px 0;
    }
    
    .progress-bar {
        height: 10px;
        border-radius: 4px;
        text-align: right;
    }
    
    /* Cores para os estados de progresso */
    .progress-low {
        background-color: #ef5350;
    }
    
    .progress-medium {
        background-color: #ffb74d;
    }
    
    .progress-high {
        background-color: #66bb6a;
    }
    
    .progress-complete {
        background-color: #42a5f5;
    }
    
    /* Tamanho dos gráficos */
    .goal-chart {
        height: 300px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da página
st.markdown('<h1 class="main-header">Metas Financeiras 🎯</h1>', unsafe_allow_html=True)

# Usuário simulado (em uma aplicação real, seria obtido através da sessão)
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user123"

# Inicialização de variáveis de estado da sessão
if 'goals' not in st.session_state:
    st.session_state.goals = []
    
if 'show_completed' not in st.session_state:
    st.session_state.show_completed = False

# Funções auxiliares

def render_progress_bar(progress):
    """Renderiza uma barra de progresso com classes CSS."""
    if progress >= 100:
        css_class = "progress-complete"
    elif progress >= 70:
        css_class = "progress-high"
    elif progress >= 30:
        css_class = "progress-medium"
    else:
        css_class = "progress-low"
        
    html = f"""
    <div class="progress-container">
        <div class="progress-bar {css_class}" style="width:{min(100, progress)}%"></div>
    </div>
    <div style="text-align: right; font-size: 0.8rem;">{format_percentage(progress)}</div>
    """
    
    return html

def get_goal_css_class(priority, completed):
    """Retorna a classe CSS para um cartão de meta baseado na prioridade e status."""
    if completed:
        return "goal-completed"
    elif priority == "high":
        return "goal-high"
    elif priority == "medium":
        return "goal-medium"
    else:
        return "goal-low"

def get_days_remaining_text(deadline_str):
    """Calcula e formata o texto de dias restantes para o prazo."""
    try:
        deadline = datetime.date.fromisoformat(deadline_str)
        today = get_today()
        days = (deadline - today).days
        
        if days < 0:
            return "Prazo expirado"
        elif days == 0:
            return "Prazo é hoje!"
        elif days == 1:
            return "1 dia restante"
        else:
            return f"{days} dias restantes"
    except:
        return "Data inválida"

def load_goals():
    """Carrega as metas do usuário."""
    # Em uma implementação real, isso buscaria do banco de dados
    # Usando o GoalService que criamos
    goals = GoalService.list_goals(
        user_id=st.session_state.user_id,
        include_completed=st.session_state.show_completed
    )
    
    # Se o serviço real não estiver disponível, usamos dados de exemplo
    if not goals:
        # Dados de exemplo
        goals = [
            {
                "id": "goal1",
                "name": "Fundo de Emergência",
                "target_amount": 10000.0,
                "current_amount": 6500.0,
                "progress_percentage": 65.0,
                "deadline": "2023-12-31",
                "category": "Poupança",
                "description": "Acumular 6 meses de despesas para emergências",
                "priority": "high",
                "color": "#3358FF",
                "icon": "shield",
                "completed": False,
                "created_at": "2023-01-15T10:30:00",
                "user_id": "user123"
            },
            {
                "id": "goal2",
                "name": "Viagem para Europa",
                "target_amount": 15000.0,
                "current_amount": 3750.0,
                "progress_percentage": 25.0,
                "deadline": "2024-06-30",
                "category": "Lazer",
                "description": "Viagem para conhecer 5 países na Europa",
                "priority": "medium",
                "color": "#FF5733",
                "icon": "flight",
                "completed": False,
                "created_at": "2023-02-20T14:15:00",
                "user_id": "user123"
            },
            {
                "id": "goal3",
                "name": "Novo Notebook",
                "target_amount": 5000.0,
                "current_amount": 5000.0,
                "progress_percentage": 100.0,
                "deadline": "2023-08-31",
                "category": "Tecnologia",
                "description": "Comprar um novo notebook para trabalho",
                "priority": "low",
                "color": "#33FF57",
                "icon": "laptop",
                "completed": True,
                "completed_at": "2023-08-15T09:45:00",
                "created_at": "2023-04-10T08:20:00",
                "user_id": "user123"
            },
            {
                "id": "goal4",
                "name": "Entrada Apartamento",
                "target_amount": 80000.0,
                "current_amount": 24000.0,
                "progress_percentage": 30.0,
                "deadline": "2025-12-31",
                "category": "Moradia",
                "description": "Juntar dinheiro para entrada de um apartamento",
                "priority": "high",
                "color": "#C133FF",
                "icon": "home",
                "completed": False,
                "created_at": "2023-03-05T16:40:00",
                "user_id": "user123"
            }
        ]
    
    return goals

def add_goal(name, target_amount, current_amount, deadline, category, 
             description, priority, icon, color):
    """Adiciona uma nova meta."""
    # Converte string de data para objeto date
    deadline_date = parse_date(deadline)
    
    # Em uma implementação real, usaria o GoalService
    goal_id = GoalService.add_goal(
        name=name,
        target_amount=float(target_amount),
        current_amount=float(current_amount),
        deadline=deadline_date,
        user_id=st.session_state.user_id,
        category=category,
        description=description,
        priority=priority,
        icon=icon,
        color=color
    )
    
    if goal_id:
        st.success(f"Meta '{name}' adicionada com sucesso!")
    else:
        # Simulação de sucesso para demonstração
        st.success(f"Meta '{name}' adicionada com sucesso! (Simulação)")
    
    # Recarregar metas
    st.session_state.goals = load_goals()

def update_goal_progress(goal_id, amount_to_add):
    """Atualiza o progresso de uma meta."""
    # Em uma implementação real, usaria o GoalService
    success = GoalService.update_goal_progress(
        goal_id=goal_id,
        amount_to_add=float(amount_to_add)
    )
    
    if success:
        st.success(f"Progresso da meta atualizado com sucesso!")
    else:
        # Simulação de sucesso para demonstração
        st.success(f"Progresso da meta atualizado com sucesso! (Simulação)")
    
    # Recarregar metas
    st.session_state.goals = load_goals()

def delete_goal(goal_id):
    """Exclui uma meta."""
    # Em uma implementação real, usaria o GoalService
    success = GoalService.delete_goal(goal_id)
    
    if success:
        st.success(f"Meta excluída com sucesso!")
    else:
        # Simulação de sucesso para demonstração
        st.success(f"Meta excluída com sucesso! (Simulação)")
    
    # Recarregar metas
    st.session_state.goals = load_goals()

# Carregar metas
st.session_state.goals = load_goals()

# Criar abas
tab1, tab2 = st.tabs(["Minhas Metas", "Nova Meta"])

# Aba de visualização das metas
with tab1:
    # Opção para mostrar metas concluídas
    show_completed = st.checkbox(
        "Mostrar metas concluídas",
        value=st.session_state.show_completed
    )
    
    if show_completed != st.session_state.show_completed:
        st.session_state.show_completed = show_completed
        st.session_state.goals = load_goals()
    
    # Dividir a visualização em duas colunas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="subheader">Lista de Metas</h2>', unsafe_allow_html=True)
        
        # Verificar se há metas para exibir
        if not st.session_state.goals:
            st.info("Você ainda não possui metas definidas. Crie sua primeira meta na aba 'Nova Meta'!")
        else:
            # Agrupar metas por prioridade
            high_priority = [g for g in st.session_state.goals if g.get("priority") == "high" and not g.get("completed", False)]
            medium_priority = [g for g in st.session_state.goals if g.get("priority") == "medium" and not g.get("completed", False)]
            low_priority = [g for g in st.session_state.goals if g.get("priority") == "low" and not g.get("completed", False)]
            completed = [g for g in st.session_state.goals if g.get("completed", False)]
            
            # Exibir metas de alta prioridade
            if high_priority:
                st.markdown('<div class="card-header">Prioridade Alta</div>', unsafe_allow_html=True)
                for goal in high_priority:
                    with st.expander(f"{goal['name']} - {format_currency(goal['target_amount'])}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="goal-info">
                                <div>Progresso: <span class="goal-amount">{format_currency(goal['current_amount'])}</span> de <span class="goal-amount">{format_currency(goal['target_amount'])}</span></div>
                                <div class="goal-date">Prazo: {format_date(goal['deadline'])} ({get_days_remaining_text(goal['deadline'])})</div>
                            </div>
                            {render_progress_bar(goal['progress_percentage'])}
                            """, unsafe_allow_html=True)
                            
                            if goal.get('description'):
                                st.markdown(f"**Descrição:** {goal['description']}")
                        
                        with col2:
                            # Formulário para atualizar progresso
                            with st.form(key=f"update_form_{goal['id']}"):
                                amount = st.number_input("Adicionar valor", min_value=0.01, step=10.0, format="%.2f")
                                submitted = st.form_submit_button("Atualizar")
                                
                                if submitted:
                                    update_goal_progress(goal['id'], amount)
                            
                            # Botão para excluir meta
                            if st.button("Excluir Meta", key=f"delete_{goal['id']}"):
                                delete_goal(goal['id'])
            
            # Exibir metas de média prioridade
            if medium_priority:
                st.markdown('<div class="card-header">Prioridade Média</div>', unsafe_allow_html=True)
                for goal in medium_priority:
                    with st.expander(f"{goal['name']} - {format_currency(goal['target_amount'])}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="goal-info">
                                <div>Progresso: <span class="goal-amount">{format_currency(goal['current_amount'])}</span> de <span class="goal-amount">{format_currency(goal['target_amount'])}</span></div>
                                <div class="goal-date">Prazo: {format_date(goal['deadline'])} ({get_days_remaining_text(goal['deadline'])})</div>
                            </div>
                            {render_progress_bar(goal['progress_percentage'])}
                            """, unsafe_allow_html=True)
                            
                            if goal.get('description'):
                                st.markdown(f"**Descrição:** {goal['description']}")
                        
                        with col2:
                            # Formulário para atualizar progresso
                            with st.form(key=f"update_form_{goal['id']}"):
                                amount = st.number_input("Adicionar valor", min_value=0.01, step=10.0, format="%.2f")
                                submitted = st.form_submit_button("Atualizar")
                                
                                if submitted:
                                    update_goal_progress(goal['id'], amount)
                            
                            # Botão para excluir meta
                            if st.button("Excluir Meta", key=f"delete_{goal['id']}"):
                                delete_goal(goal['id'])
            
            # Exibir metas de baixa prioridade
            if low_priority:
                st.markdown('<div class="card-header">Prioridade Baixa</div>', unsafe_allow_html=True)
                for goal in low_priority:
                    with st.expander(f"{goal['name']} - {format_currency(goal['target_amount'])}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="goal-info">
                                <div>Progresso: <span class="goal-amount">{format_currency(goal['current_amount'])}</span> de <span class="goal-amount">{format_currency(goal['target_amount'])}</span></div>
                                <div class="goal-date">Prazo: {format_date(goal['deadline'])} ({get_days_remaining_text(goal['deadline'])})</div>
                            </div>
                            {render_progress_bar(goal['progress_percentage'])}
                            """, unsafe_allow_html=True)
                            
                            if goal.get('description'):
                                st.markdown(f"**Descrição:** {goal['description']}")
                        
                        with col2:
                            # Formulário para atualizar progresso
                            with st.form(key=f"update_form_{goal['id']}"):
                                amount = st.number_input("Adicionar valor", min_value=0.01, step=10.0, format="%.2f")
                                submitted = st.form_submit_button("Atualizar")
                                
                                if submitted:
                                    update_goal_progress(goal['id'], amount)
                            
                            # Botão para excluir meta
                            if st.button("Excluir Meta", key=f"delete_{goal['id']}"):
                                delete_goal(goal['id'])
            
            # Exibir metas concluídas
            if completed and show_completed:
                st.markdown('<div class="card-header">Metas Concluídas</div>', unsafe_allow_html=True)
                for goal in completed:
                    with st.expander(f"{goal['name']} - {format_currency(goal['target_amount'])} ✓"):
                        st.markdown(f"""
                        <div class="goal-info">
                            <div>Progresso: <span class="goal-amount">{format_currency(goal['current_amount'])}</span> de <span class="goal-amount">{format_currency(goal['target_amount'])}</span></div>
                            <div class="goal-date">Concluída em: {format_date(goal.get('completed_at', goal.get('updated_at', '')))}</div>
                        </div>
                        {render_progress_bar(goal['progress_percentage'])}
                        """, unsafe_allow_html=True)
                        
                        if goal.get('description'):
                            st.markdown(f"**Descrição:** {goal['description']}")
                        
                        # Botão para excluir meta
                        if st.button("Excluir Meta", key=f"delete_{goal['id']}"):
                            delete_goal(goal['id'])
    
    with col2:
        st.markdown('<h2 class="subheader">Resumo</h2>', unsafe_allow_html=True)
        
        # Calcular valores para resumo
        active_goals = [g for g in st.session_state.goals if not g.get("completed", False)]
        completed_goals = [g for g in st.session_state.goals if g.get("completed", False)]
        
        total_active = len(active_goals)
        total_completed = len(completed_goals)
        total_target = sum(g.get("target_amount", 0) for g in active_goals)
        total_current = sum(g.get("current_amount", 0) for g in active_goals)
        
        # Calcular progresso geral
        overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
        
        # Exibir cards de resumo
        st.markdown(f"""
        <div class="card">
            <div class="card-header">Metas Ativas</div>
            <div class="card-content">{total_active}</div>
        </div>
        <div class="card">
            <div class="card-header">Metas Concluídas</div>
            <div class="card-content">{total_completed}</div>
        </div>
        <div class="card">
            <div class="card-header">Valor Total a Atingir</div>
            <div class="card-content">{format_currency(total_target)}</div>
        </div>
        <div class="card">
            <div class="card-header">Valor Atual Acumulado</div>
            <div class="card-content">{format_currency(total_current)}</div>
        </div>
        <div class="card">
            <div class="card-header">Progresso Geral</div>
            <div class="card-content">
                {render_progress_bar(overall_progress)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico de distribuição das metas
        if active_goals:
            st.markdown('<div class="card-header">Distribuição das Metas</div>', unsafe_allow_html=True)
            
            # Preparar dados para o gráfico
            goal_data = []
            for goal in active_goals:
                goal_data.append({
                    "name": goal['name'],
                    "current": goal['current_amount'],
                    "remaining": goal['target_amount'] - goal['current_amount']
                })
            
            df_goals = pd.DataFrame(goal_data)
            
            # Criar gráfico de barras empilhadas
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_goals['name'],
                y=df_goals['current'],
                name='Valor Atual',
                marker_color='#4CAF50'
            ))
            
            fig.add_trace(go.Bar(
                x=df_goals['name'],
                y=df_goals['remaining'],
                name='Valor Restante',
                marker_color='#F44336'
            ))
            
            fig.update_layout(
                barmode='stack',
                title='Progresso por Meta',
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Metas por prioridade
            priority_counts = {
                "Alta": len([g for g in active_goals if g.get("priority") == "high"]),
                "Média": len([g for g in active_goals if g.get("priority") == "medium"]),
                "Baixa": len([g for g in active_goals if g.get("priority") == "low"])
            }
            
            # Dados para o gráfico de pizza
            df_priority = pd.DataFrame({
                "Prioridade": list(priority_counts.keys()),
                "Quantidade": list(priority_counts.values())
            })
            
            # Criar gráfico de pizza
            fig = px.pie(
                df_priority, 
                values='Quantidade', 
                names='Prioridade',
                color_discrete_sequence=['#F44336', '#FF9800', '#4CAF50'],
                title='Metas por Prioridade'
            )
            
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Aba para adicionar nova meta
with tab2:
    st.markdown('<h2 class="subheader">Criar Nova Meta Financeira</h2>', unsafe_allow_html=True)
    
    with st.form("new_goal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome da Meta*", placeholder="Ex: Fundo de Emergência")
            target_amount = st.number_input("Valor Total da Meta*", min_value=1.0, step=100.0, format="%.2f")
            current_amount = st.number_input("Valor Inicial*", min_value=0.0, step=100.0, format="%.2f")
            
            category = st.selectbox(
                "Categoria",
                options=["Poupança", "Investimento", "Moradia", "Transporte", "Tecnologia", "Lazer", "Educação", "Saúde", "Outro"],
                index=0
            )
        
        with col2:
            deadline = st.date_input(
                "Data Limite*",
                value=get_today() + datetime.timedelta(days=365)
            )
            
            priority = st.select_slider(
                "Prioridade",
                options=["low", "medium", "high"],
                value="medium",
                format_func=lambda x: {"low": "Baixa", "medium": "Média", "high": "Alta"}[x]
            )
            
            color = st.color_picker("Cor", "#3358FF")
            
            icon = st.selectbox(
                "Ícone",
                options=["flag", "shield", "home", "flight", "laptop", "school", "directions_car", "savings", "account_balance", "favorite", "beach_access", "healing"],
                index=0
            )
        
        description = st.text_area("Descrição", placeholder="Detalhes sobre sua meta financeira...")
        
        submitted = st.form_submit_button("Criar Meta")
        
        if submitted:
            if not name or target_amount <= 0:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Formatar a data para string
                deadline_str = deadline.isoformat()
                
                # Adicionar a meta
                add_goal(name, target_amount, current_amount, deadline_str,
                         category, description, priority, icon, color) 
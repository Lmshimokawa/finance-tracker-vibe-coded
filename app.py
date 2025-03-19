import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from firebase.firebase_config import initialize_firebase

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o Firebase
firebase_app = initialize_firebase()

# Configuração da página
st.set_page_config(
    page_title="Finance Tracker | Controle Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #0D47A1;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .feature-section {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1.5rem;
    }
    
    .feature-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.8rem;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #1E88E5;
    }
    
    .info-box {
        background-color: #e1f5fe;
        border-left: 5px solid #03a9f4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .custom-button {
        background-color: #1E88E5;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        text-decoration: none;
        font-weight: 500;
        display: inline-block;
    }
    
    .custom-button:hover {
        background-color: #0D47A1;
        color: white;
    }
    
    /* Estilos para visualização em dispositivos móveis */
    @media only screen and (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
        }
    }
    
    /* Estilização para a página inicial */
    .promo-section {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .promo-image {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Customização da sidebar */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Verificação de estado de login (em uma aplicação real, verificaria a sessão)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Se usuário não estiver logado, mostrar página de login
if not st.session_state.logged_in:
    # Cabeçalho principal
    st.markdown("<h1 class='main-header'>Finance Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Controle suas finanças com simplicidade e inteligência</h2>", unsafe_allow_html=True)
    
    # Layout em 2 colunas
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Informações sobre o app
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>🚀 Gerencie suas finanças pessoais</div>", unsafe_allow_html=True)
        st.markdown("""
        O Finance Tracker é uma aplicação moderna para controle financeiro pessoal 
        que ajuda você a:
        
        - Visualizar um resumo da sua saúde financeira em tempo real
        - Registrar e categorizar despesas e receitas
        - Analisar tendências através de relatórios detalhados
        - Definir e acompanhar metas financeiras
        - Tomar decisões financeiras mais conscientes
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Seção de recursos/diferenciais
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>✨ Recursos destacados</div>", unsafe_allow_html=True)
        
        feat_col1, feat_col2 = st.columns(2)
        
        with feat_col1:
            st.markdown("**📊 Dashboard intuitivo**")
            st.markdown("Visualize sua situação financeira com gráficos interativos e métricas claras.")
            
            st.markdown("**💸 Gerenciamento de Transações**")
            st.markdown("Registre despesas e receitas com detalhes, categorias e filtros avançados.")
        
        with feat_col2:
            st.markdown("**📈 Relatórios detalhados**")
            st.markdown("Analise tendências, compare períodos e exporte dados em diversos formatos.")
            
            st.markdown("**🎯 Metas financeiras**")
            st.markdown("Defina, acompanhe e alcance suas metas financeiras com facilidade.")
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Formulário de login
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>🔐 Entrar</div>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="seu@email.com")
            password = st.text_input("Senha", type="password", placeholder="••••••••")
            
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                # Em uma aplicação real, verificaria as credenciais no Firebase
                # Simulação de login bem-sucedido
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_id = "user123"  # ID de exemplo
                    st.session_state.user_name = "Usuário de Exemplo"
                    st.success("Login realizado com sucesso!")
                    st.rerun()  # Recarrega a página após o login
                else:
                    st.error("Por favor, preencha todos os campos.")
        
        # Opção de registro
        st.markdown("<div class='feature-header' style='margin-top: 1.5rem;'>🆕 Novo por aqui?</div>", unsafe_allow_html=True)
        
        with st.form("register_form"):
            new_name = st.text_input("Nome completo", placeholder="Seu Nome")
            new_email = st.text_input("Email", placeholder="seu@email.com")
            new_password = st.text_input("Senha", type="password", placeholder="••••••••")
            new_password_confirm = st.text_input("Confirmar senha", type="password", placeholder="••••••••")
            
            register_button = st.form_submit_button("Criar conta")
            
            if register_button:
                # Em uma aplicação real, registraria o usuário no Firebase
                if new_name and new_email and new_password and new_password_confirm:
                    if new_password == new_password_confirm:
                        st.success("Conta criada com sucesso! Faça login para continuar.")
                    else:
                        st.error("As senhas não coincidem.")
                else:
                    st.error("Por favor, preencha todos os campos.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; font-size: 0.8rem; color: #666;">
        Finance Tracker © 2023 | Desenvolvido com ❤️ usando Streamlit e Firebase
    </div>
    """, unsafe_allow_html=True)

# Se usuário estiver logado, exibir uma página inicial com boas-vindas
else:
    # Cabeçalho principal
    st.markdown("<h1 class='main-header'>Finance Tracker</h1>", unsafe_allow_html=True)
    
    # Mensagem de boas-vindas
    st.markdown(f"""
    <div class='info-box'>
        <h3>Bem-vindo(a), {st.session_state.get('user_name', 'Usuário')}!</h3>
        <p>Navegue usando o menu lateral para acessar todas as funcionalidades do aplicativo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visão geral dos recursos/páginas disponíveis
    st.markdown("<div class='feature-header'>Acesso rápido</div>", unsafe_allow_html=True)
    
    # Layout em 2x2 para os acessos rápidos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-icon'>📊</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>Dashboard</div>", unsafe_allow_html=True)
        st.markdown("Visualize sua situação financeira atual com métricas e gráficos interativos.")
        st.markdown("<a href='1_dashboard' target='_self' class='custom-button'>Acessar Dashboard</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-icon'>📈</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>Relatórios</div>", unsafe_allow_html=True)
        st.markdown("Gere relatórios personalizados e analise tendências de gastos e receitas.")
        st.markdown("<a href='3_relatorios' target='_self' class='custom-button'>Visualizar Relatórios</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-icon'>💰</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>Transações</div>", unsafe_allow_html=True)
        st.markdown("Registre e gerencie todas as suas transações financeiras com facilidade.")
        st.markdown("<a href='2_transacoes' target='_self' class='custom-button'>Gerenciar Transações</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='feature-section'>", unsafe_allow_html=True)
        st.markdown("<div class='feature-icon'>🎯</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-header'>Metas Financeiras</div>", unsafe_allow_html=True)
        st.markdown("Defina objetivos financeiros e acompanhe seu progresso ao longo do tempo.")
        st.markdown("<a href='5_metas' target='_self' class='custom-button'>Definir Metas</a>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Dicas financeiras (adicional)
    st.markdown("<div class='feature-header' style='margin-top: 1.5rem;'>💡 Dica do dia</div>", unsafe_allow_html=True)
    
    # Dicas aleatórias
    import random
    dicas = [
        "Considere separar 20% da sua renda para investimentos a longo prazo.",
        "Crie um fundo de emergência que cubra 6 meses de despesas básicas.",
        "Revise suas assinaturas mensais e elimine as que você não usa com frequência.",
        "Automatize suas economias com transferências programadas no dia do pagamento.",
        "Use a regra 50/30/20: 50% para necessidades, 30% para desejos e 20% para economias."
    ]
    
    st.info(random.choice(dicas))
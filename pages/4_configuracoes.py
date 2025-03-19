import streamlit as st
import yaml
from pathlib import Path
import sys
import datetime

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importações futuras dos serviços
# from services.category_service import get_categories, save_category, delete_category
# from services.auth_service import update_user_profile, get_user_profile
# from services.backup_service import export_data, import_data

# Configuração da página
st.set_page_config(
    page_title="Configurações | Finance Tracker",
    page_icon="⚙️",
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
    .config-section {
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título da página
st.markdown('<h1 class="main-header">Configurações</h1>', unsafe_allow_html=True)

# Tabs para organizar as configurações
tab1, tab2, tab3, tab4 = st.tabs(["Perfil", "Categorias", "Backup e Restauração", "Sobre"])

# Tab de Perfil
with tab1:
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Dados do Perfil")
    
    # Dados fictícios do perfil
    user_profile = {
        "nome": "Administrador",
        "email": "admin@example.com",
        "created_at": datetime.datetime(2023, 1, 1),
    }
    
    with st.form("perfil_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome", value=user_profile["nome"])
            email = st.text_input("E-mail", value=user_profile["email"], disabled=True)
            data_cadastro = st.text_input(
                "Data de Cadastro", 
                value=user_profile["created_at"].strftime("%d/%m/%Y"),
                disabled=True
            )
        
        with col2:
            st.markdown("##### Foto de Perfil")
            st.image("https://via.placeholder.com/150", width=150)
            foto_perfil = st.file_uploader("Alterar foto de perfil", type=["png", "jpg", "jpeg"])
        
        st.markdown("---")
        
        st.markdown("## Alterar Senha")
        
        col1, col2 = st.columns(2)
        
        with col1:
            senha_atual = st.text_input("Senha Atual", type="password")
        
        with col2:
            senha_nova = st.text_input("Nova Senha", type="password")
            senha_confirma = st.text_input("Confirmar Nova Senha", type="password")
        
        submitted = st.form_submit_button("Salvar Alterações")
        
        if submitted:
            if senha_nova and senha_nova != senha_confirma:
                st.error("As senhas não coincidem!")
            else:
                st.success("Perfil atualizado com sucesso!")
                # Aqui entraria a lógica para atualizar o perfil
                # update_user_profile(user_id, nome, email, senha_nova, foto_perfil)
    
    st.markdown("## Preferências")
    
    moeda = st.selectbox(
        "Moeda padrão",
        options=["R$ (Real Brasileiro)", "US$ (Dólar Americano)", "€ (Euro)", "£ (Libra Esterlina)"],
        index=0
    )
    
    formato_data = st.selectbox(
        "Formato de data",
        options=["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"],
        index=0
    )
    
    tema = st.selectbox(
        "Tema",
        options=["Claro", "Escuro", "Sistema"],
        index=0
    )
    
    if st.button("Salvar Preferências"):
        st.success("Preferências salvas com sucesso!")
        # Aqui entraria a lógica para salvar as preferências
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab de Categorias
with tab2:
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Gerenciar Categorias")
    
    # Categorias existentes
    categorias_despesas = ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Educação", "Outros"]
    categorias_receitas = ["Salário", "Freelance", "Investimentos", "Outros"]
    
    # Seleção do tipo de categoria
    tipo_categoria = st.selectbox(
        "Tipo de transação",
        options=["Despesa", "Receita"],
        index=0
    )
    
    # Formulário para adicionar categoria
    with st.expander("Adicionar Nova Categoria"):
        with st.form("nova_categoria"):
            nome_categoria = st.text_input("Nome da Categoria")
            
            cor_categoria = st.color_picker("Cor", "#4F46E5")
            
            icone_categoria = st.selectbox(
                "Ícone",
                options=["🍔", "🏠", "🚗", "🎮", "🏥", "📚", "💼", "💰", "📊", "🛒", "💳", "📱", "⚙️", "🔍", "📝"],
                index=0
            )
            
            submit_categoria = st.form_submit_button("Adicionar Categoria")
            
            if submit_categoria and nome_categoria:
                st.success(f"Categoria {nome_categoria} adicionada com sucesso!")
                # Lógica para adicionar categoria
                # save_category(user_id, nome_categoria, tipo_categoria, cor_categoria, icone_categoria)
    
    # Lista de categorias existentes
    st.markdown("### Categorias Existentes")
    
    if tipo_categoria == "Despesa":
        categorias = categorias_despesas
    else:
        categorias = categorias_receitas
    
    for i, categoria in enumerate(categorias):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{categoria}**")
        
        with col2:
            if st.button("Editar", key=f"edit_{i}"):
                # Lógica para editar categoria
                st.info(f"Editar categoria {categoria}")
        
        with col3:
            if st.button("Excluir", key=f"delete_{i}"):
                # Lógica para excluir categoria
                st.error(f"Categoria {categoria} excluída!")
        
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab de Backup e Restauração
with tab3:
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Backup e Restauração de Dados")
    
    st.info("Os backups são importantes para garantir a segurança dos seus dados financeiros. Recomendamos fazer backup regularmente.")
    
    # Backup
    st.markdown("### Exportar Dados")
    
    formato_backup = st.selectbox(
        "Formato de exportação",
        options=["JSON", "CSV", "Excel"],
        index=0
    )
    
    dados_backup = st.multiselect(
        "Dados a exportar",
        options=["Transações", "Categorias", "Configurações", "Todos"],
        default=["Todos"]
    )
    
    periodo_backup = st.selectbox(
        "Período",
        options=["Todo o histórico", "Último mês", "Últimos 3 meses", "Último ano", "Personalizado"],
        index=0
    )
    
    if periodo_backup == "Personalizado":
        col1, col2 = st.columns(2)
        with col1:
            data_inicio_backup = st.date_input("Data inicial", value=datetime.date.today() - datetime.timedelta(days=30))
        with col2:
            data_fim_backup = st.date_input("Data final", value=datetime.date.today())
    
    if st.button("Exportar Dados", type="primary"):
        st.success("Backup realizado com sucesso!")
        # Lógica para exportar dados
        # export_data(user_id, formato_backup, dados_backup, periodo_backup)
    
    # Restauração
    st.markdown("### Importar Dados")
    
    arquivo_importacao = st.file_uploader("Selecione o arquivo de backup", type=["json", "csv", "xlsx"])
    
    opcao_importacao = st.radio(
        "Opção de importação",
        options=["Substituir dados existentes", "Apenas adicionar novos registros"]
    )
    
    if arquivo_importacao is not None:
        if st.button("Importar Dados", type="primary"):
            st.success("Dados importados com sucesso!")
            # Lógica para importar dados
            # import_data(user_id, arquivo_importacao, opcao_importacao)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab Sobre
with tab4:
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Sobre o Finance Tracker")
    
    st.markdown("""
    #### Versão 0.1.0
    
    **Finance Tracker** é uma aplicação de controle financeiro pessoal desenvolvida com Python e Streamlit,
    focada em proporcionar uma experiência simples e eficiente para gerenciar suas finanças.
    
    ### Recursos
    
    - Dashboard interativo com visão geral das finanças
    - Registro e gerenciamento de transações
    - Categorização personalizada
    - Relatórios detalhados e gráficos
    - Backup e restauração de dados
    
    ### Tecnologias
    
    - **Frontend/Backend**: Streamlit
    - **Banco de Dados**: Firebase Firestore
    - **Visualizações**: Plotly, Pandas
    
    ### Contato e Suporte
    
    Para suporte ou mais informações, entre em contato através de:
    - Email: contato@financetracker.com
    - GitHub: [github.com/Lmshimokawa/finance-tracker-vibe-coded](https://github.com/Lmshimokawa/finance-tracker-vibe-coded)
    
    ---
    
    Desenvolvido como um projeto de aprendizado. Todos os direitos reservados.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True) 
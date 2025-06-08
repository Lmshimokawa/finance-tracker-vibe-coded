# Finance Tracker

Uma aplicação moderna e intuitiva para rastreamento e gerenciamento de finanças pessoais, construída com Python e Streamlit, integrada com Firebase.

## 🚀 Funcionalidades

- **Dashboard Financeiro**: Visualize resumos e gráficos da sua situação financeira
- **Gerenciamento de Transações**: Registre despesas e receitas com categorização
- **Relatórios Detalhados**: Analise seus gastos e tendências financeiras
- **Metas Financeiras**: Defina e acompanhe objetivos financeiros
- **Configurações Personalizáveis**: Adapte a aplicação às suas preferências

## 🔧 Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **Banco de Dados**: Firebase/Firestore
- **Visualização de Dados**: Plotly
- **Armazenamento de Credenciais**: Dotenv

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Firebase (para o banco de dados)
- Dependências listadas em `requirements.txt`

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/finance-tracker.git
cd finance-tracker
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Preencha as credenciais do Firebase e outras configurações

4. Inicialize o projeto Firebase e baixe o arquivo de credenciais:
   - Coloque o arquivo `serviceAccountKey.json` na pasta `firebase/`

## 🚀 Execução

Execute o aplicativo com o comando:
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`.

## 📂 Estrutura do Projeto

```
finance-tracker/
├── app.py                  # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Exemplo de configuração
├── firebase/               # Módulos relacionados ao Firebase
│   ├── __init__.py
│   ├── firebase_config.py  # Configuração de conexão com Firebase
│   └── serviceAccountKey.json (não versionado)
├── pages/                  # Páginas da aplicação
│   ├── 1_dashboard.py
│   ├── 2_transacoes.py
│   ├── 3_relatorios.py
│   ├── 4_configuracoes.py
│   └── 5_metas.py
├── services/               # Lógica de negócios
│   ├── __init__.py
│   ├── auth_service.py
│   ├── transaction_service.py
│   ├── category_service.py
│   └── goal_service.py
├── utils/                  # Funções utilitárias
│   ├── __init__.py
│   ├── date_utils.py
│   └── currency_utils.py
└── static/                 # Recursos estáticos (imagens, CSS, etc.)
```

## 📊 Principais Recursos

### Dashboard
- Resumo de finanças mensal e anual
- Gráficos de despesas por categoria
- Indicadores de economia e situação financeira

### Transações
- Registro detalhado de transações com data, categoria e notas
- Filtros e busca avançada
- Exportação de dados para Excel e CSV

### Relatórios
- Análise comparativa de períodos
- Tendências de gastos 
- Previsões financeiras

### Metas
- Definição de metas financeiras com prazo
- Acompanhamento de progresso
- Categorização de objetivos por prioridade

## 🔐 Autenticação e Segurança

A aplicação utiliza Firebase Authentication para gerenciar usuários e proteger dados. Cada usuário tem acesso apenas aos próprios dados financeiros.

## 🧪 Testes

Para executar testes:
```bash
pip install pytest
pytest tests/
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie sua branch de funcionalidade (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato através de [seu-email@exemplo.com]. 
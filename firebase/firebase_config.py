import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
load_dotenv()

# Verifica se já existe uma instância do Firebase inicializada
def initialize_firebase():
    """
    Inicializa a conexão com o Firebase se ainda não estiver inicializada.
    Retorna a instância do Firestore.
    """
    if not firebase_admin._apps:
        # Tenta carregar o arquivo de credenciais
        cred_path = Path(__file__).parent / "serviceAccountKey.json"
        
        # Se o arquivo de credenciais existir, usa-o
        if cred_path.exists():
            cred = credentials.Certificate(str(cred_path))
            firebase_admin.initialize_app(cred)
        # Se não existir, tenta usar as variáveis de ambiente
        else:
            # Configuração a partir de variáveis de ambiente
            firebase_config = {
                "apiKey": os.getenv("FIREBASE_API_KEY"),
                "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
                "projectId": os.getenv("FIREBASE_PROJECT_ID"),
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
                "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                "appId": os.getenv("FIREBASE_APP_ID"),
                "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
                "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
            }
            
            # Se alguma variável de ambiente necessária não estiver configurada
            if not all([firebase_config["apiKey"], firebase_config["projectId"]]):
                print("AVISO: Configuração do Firebase incompleta nas variáveis de ambiente.")
                return None
            
            # Inicializa o Firebase com as variáveis de ambiente
            try:
                firebase_admin.initialize_app()
            except ValueError as e:
                print(f"Erro ao inicializar Firebase: {e}")
                return None
    
    # Retorna a instância do Firestore
    return firestore.client()

# Função para obter uma referência ao Firestore
def get_firestore():
    """
    Retorna uma instância do cliente Firestore, inicializando o Firebase se necessário.
    """
    return initialize_firebase()

# Funções utilitárias para operações no Firestore

def get_collection(collection_name):
    """
    Retorna uma referência para a coleção especificada.
    
    Args:
        collection_name (str): Nome da coleção no Firestore.
        
    Returns:
        firestore.CollectionReference: Referência para a coleção.
    """
    db = get_firestore()
    if db:
        return db.collection(collection_name)
    return None

def add_document(collection_name, data):
    """
    Adiciona um documento a uma coleção.
    
    Args:
        collection_name (str): Nome da coleção.
        data (dict): Dados a serem adicionados.
        
    Returns:
        str: ID do documento adicionado ou None em caso de erro.
    """
    collection_ref = get_collection(collection_name)
    if collection_ref:
        try:
            doc_ref = collection_ref.add(data)[1]
            return doc_ref.id
        except Exception as e:
            print(f"Erro ao adicionar documento: {e}")
    return None

def get_document(collection_name, document_id):
    """
    Obtém um documento pelo ID.
    
    Args:
        collection_name (str): Nome da coleção.
        document_id (str): ID do documento.
        
    Returns:
        dict: Dados do documento ou None se não encontrado.
    """
    collection_ref = get_collection(collection_name)
    if collection_ref:
        try:
            doc = collection_ref.document(document_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"Erro ao obter documento: {e}")
    return None

def update_document(collection_name, document_id, data):
    """
    Atualiza um documento existente.
    
    Args:
        collection_name (str): Nome da coleção.
        document_id (str): ID do documento.
        data (dict): Dados a serem atualizados.
        
    Returns:
        bool: True se a atualização for bem-sucedida, False caso contrário.
    """
    collection_ref = get_collection(collection_name)
    if collection_ref:
        try:
            collection_ref.document(document_id).update(data)
            return True
        except Exception as e:
            print(f"Erro ao atualizar documento: {e}")
    return False

def delete_document(collection_name, document_id):
    """
    Exclui um documento pelo ID.
    
    Args:
        collection_name (str): Nome da coleção.
        document_id (str): ID do documento.
        
    Returns:
        bool: True se a exclusão for bem-sucedida, False caso contrário.
    """
    collection_ref = get_collection(collection_name)
    if collection_ref:
        try:
            collection_ref.document(document_id).delete()
            return True
        except Exception as e:
            print(f"Erro ao excluir documento: {e}")
    return False

def query_documents(collection_name, field=None, operator=None, value=None):
    """
    Consulta documentos em uma coleção com filtros opcionais.
    
    Args:
        collection_name (str): Nome da coleção.
        field (str, optional): Campo para filtrar.
        operator (str, optional): Operador para o filtro ('==', '>', '<', '>=', '<=', 'array_contains').
        value (any, optional): Valor para comparar.
        
    Returns:
        list: Lista de documentos que atendem aos critérios ou lista vazia se nenhum for encontrado.
    """
    collection_ref = get_collection(collection_name)
    if not collection_ref:
        return []
    
    try:
        # Se houver filtros, aplica-os
        if field and operator and value is not None:
            query = collection_ref.where(field, operator, value)
        else:
            query = collection_ref
            
        # Executa a consulta
        docs = query.stream()
        
        # Converte os documentos para dicionários
        result = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Adiciona o ID do documento aos dados
            result.append(data)
            
        return result
    except Exception as e:
        print(f"Erro ao consultar documentos: {e}")
        return []

# Para testes
if __name__ == "__main__":
    # Teste de conexão
    db = get_firestore()
    if db:
        print("Conexão com Firebase estabelecida com sucesso!")
    else:
        print("Falha ao conectar com o Firebase.") 
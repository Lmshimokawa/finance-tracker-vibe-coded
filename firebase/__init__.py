from firebase.firebase_config import (
    initialize_firebase,
    get_firestore,
    get_collection,
    add_document,
    get_document,
    update_document,
    delete_document,
    query_documents
)

# Exportar todas as funções disponíveis no pacote
__all__ = [
    'initialize_firebase',
    'get_firestore',
    'get_collection',
    'add_document',
    'get_document',
    'update_document',
    'delete_document',
    'query_documents'
] 
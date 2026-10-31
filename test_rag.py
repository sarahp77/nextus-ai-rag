from rag_service import index_document, search_knowledge

print("--- Indexing ---")
print(index_document())

print("--- Searching ---")
print(search_knowledge("How much is the Growth tier?"))

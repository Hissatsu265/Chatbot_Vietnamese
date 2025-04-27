from sentence_transformers import CrossEncoder
import numpy as np
from src.embedder import VietnameseEmbedder, load_faiss_index

def preprocess_question(question: str) -> str:
    from underthesea import text_normalize, word_tokenize

    question = text_normalize(question.strip())
    tokenized = word_tokenize(question, format="text")
    return tokenized

def cross_rerank(query: str, candidate_docs: list, top_k: int = 5):
 
    
    # reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L6-H384-v1')
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
    # reranker = CrossEncoder('microsoft/mpnet-base')

    pairs = [(query, doc) for doc in candidate_docs]
    scores = reranker.predict(pairs)
    print(scores)
    # Sắp xếp theo score giảm dần
    ranked_docs = [doc for _, doc in sorted(zip(scores, candidate_docs), key=lambda x: x[0], reverse=True)]
    print(ranked_docs)
    return ranked_docs[:top_k]
def retrieve_with_cross_reranker(query, k=10, k_final=5,vector_path: str = "embeddings/vector_store/faiss_index",):
    embedder = VietnameseEmbedder()
    index, texts = load_faiss_index(vector_path)

    processed_question = preprocess_question(query)
    q_embedding = embedder.encode([processed_question])[0]
    D, I = index.search(np.array([q_embedding]), k)

    candidate_texts = [texts[i] for i in I[0]]

    reranked_texts = cross_rerank(processed_question, candidate_texts, top_k=k_final)

    return reranked_texts
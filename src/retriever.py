import numpy as np
from src.embedder import VietnameseEmbedder, load_faiss_index

def preprocess_question(question: str) -> str:
    from underthesea import text_normalize, word_tokenize

    question = text_normalize(question.strip())
    tokenized = word_tokenize(question, format="text")
    return tokenized
    
# def retrieve_top_k(query, k=5, vector_path="embeddings/vector_store/faiss_index"):
def retrieve_top_k(query: str, 
                   k: int = 5,
                   vector_path: str = "embeddings/vector_store/faiss_index",
                   score_threshold: float = 0.55):
    
    embedder = VietnameseEmbedder()
    index, texts = load_faiss_index(vector_path)
    # ====================================================
    processed_question = preprocess_question(query)
    q_embedding = embedder.encode([processed_question])[0]
    
    # q_embedding = embedder.encode([query])[0]
    
    # ====================================================
    # D, I = index.search(np.array([q_embedding]), k)
    # return [texts[i] for i in I[0]]
    # ====================================================
    D, I = index.search(np.array([q_embedding]), k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if score >= score_threshold:
            results.append(texts[idx])
        else:
            print(f"Bỏ đoạn vì score thấp: {score:.4f}")
    
    return results if results else [texts[i] for i in I[0]] 
# ========================================================================   
from sklearn.metrics.pairwise import cosine_similarity
def mmr(doc_embeddings, query_embedding, k=5, lambda_param=0.5):
    """
    MMR: chọn k đoạn văn từ danh sách embedding sao cho vừa đa dạng vừa liên quan
    """
    selected = []
    candidate_indices = list(range(len(doc_embeddings)))
    doc_embeddings = np.array(doc_embeddings)

    for _ in range(k):
        mmr_scores = []

        for idx in candidate_indices:
            sim_to_query = cosine_similarity([query_embedding], [doc_embeddings[idx]])[0][0]
            sim_to_selected = max([cosine_similarity([doc_embeddings[idx]], [doc_embeddings[i]])[0][0] for i in selected], default=0)

            mmr_score = lambda_param * sim_to_query - (1 - lambda_param) * sim_to_selected
            mmr_scores.append((idx, mmr_score))

        best_idx = max(mmr_scores, key=lambda x: x[1])[0]
        selected.append(best_idx)
        candidate_indices.remove(best_idx)

    return selected
def retrieve_with_mmr(query, k=10, k_final=5, lambda_param=0.5):
    embedder = VietnameseEmbedder()
    index, texts = load_faiss_index("embeddings/vector_store/faiss_index")

    processed_question = preprocess_question(query)
    q_embedding = embedder.encode([processed_question])[0]

    D, I = index.search(np.array([q_embedding]), k)

    # Lấy top_k đoạn và embedding tương ứng
    candidate_texts = [texts[i] for i in I[0]]
    candidate_embeddings = embedder.encode(candidate_texts)

    # Re-rank bằng MMR
    selected_idxs = mmr(candidate_embeddings, q_embedding, k=k_final, lambda_param=lambda_param)
    return [candidate_texts[i] for i in selected_idxs]


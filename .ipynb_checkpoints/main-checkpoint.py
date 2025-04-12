from src.data_loader import load_pdf_text
from src.text_preprocessing import preprocess_text
from src.embedder import VietnameseEmbedder, save_faiss_index
from src.retriever import retrieve_top_k,retrieve_with_mmr
from src.chatbot import ask_gemini
from src.descripe_file import describe
import numpy as np
# 1. Load data
# text = load_pdf_text("data/raw/sample.pdf")

# # 2. Preprocess
# processed_sentences = preprocess_text(text)

# # 3. Embed & save
# embedder = VietnameseEmbedder()
# embeddings = embedder.encode(processed_sentences)
# save_faiss_index(np.array(embeddings), processed_sentences, "embeddings/vector_store/faiss_index")
# ====================================================================================================
# ====================================================================================================
promt=describe()
print(promt)
# # 4. Ask question
question = "Phạm vi áp dụng nội quy?"
# contexts = retrieve_top_k(question)
contexts = retrieve_with_mmr(question)
context_combined = "\n".join(contexts)
answer = ask_gemini(promt,question, context_combined)
print("💬 Trả lời:", answer)

question = "Trang phục và tác phong phải như nào?"
# contexts = retrieve_top_k(question)
contexts = retrieve_with_mmr(question)
context_combined = "\n".join(contexts)
answer = ask_gemini(promt,question, context_combined)
print("💬 Trả lời:", answer)

question = "Lương được trả vào ngày nào?"
# contexts = retrieve_top_k(question)
contexts = retrieve_with_mmr(question)
context_combined = "\n".join(contexts)
answer = ask_gemini(promt,question, context_combined)
print("💬 Trả lời:", answer)

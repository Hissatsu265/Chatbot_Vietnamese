
import google.generativeai as genai
import numpy as np
from src.embedder import VietnameseEmbedder, load_faiss_index 

def call_gemini_for_summary(prompt):
    genai.configure(api_key="AIzaSyCjIipLCPu...")
    model = genai.GenerativeModel('gemini-2.0-flash')

    response = model.generate_content(
        f"""Dưới đây là một số đoạn của một file tài liệu.
Hãy mô tả ngắn gọn, chính xác đây là loại tài liệu gì dưới 10 từ:\n\n{prompt}"""
    )

    return response.text

def describe(vector_path="embeddings/vector_store/faiss_index", n=5):
    index, texts = load_faiss_index(vector_path)
    first_n_chunks = texts[:n]

    sorted_by_length = sorted(texts, key=lambda x: len(x), reverse=True)
    longest_n_chunks = sorted_by_length[:n]

    # Kết hợp và loại bỏ trùng lặp
    combined_chunks = first_n_chunks + longest_n_chunks
    unique_contents = list(set(combined_chunks))

    final_prompt = "\n\n".join(unique_contents)
    description = call_gemini_for_summary(final_prompt)
    return description

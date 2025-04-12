from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

class VietnameseEmbedder:
    def __init__(self, model_name="dangvantuan/vietnamese-embedding"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]):
        return self.model.encode(texts)

def save_faiss_index(embeddings, texts, path):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, f"{path}.index")
    with open(f"{path}.meta", "wb") as f:
        pickle.dump(texts, f)

def load_faiss_index(path):
    index = faiss.read_index(f"{path}.index")
    with open(f"{path}.meta", "rb") as f:
        texts = pickle.load(f)
    return index, texts

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = 'dangvantuan/vietnamese-embedding'
VECTORSTORE_DIR = 'embeddings/vectordb'

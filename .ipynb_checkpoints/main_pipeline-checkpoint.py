"""
Vietnamese RAG (Retrieval-Augmented Generation) System
----------------------------------------------------
Hệ thống truy xuất và tạo câu trả lời thông minh dựa trên tài liệu PDF tiếng Việt.
Cho phép tương tác với người dùng thông qua giao diện dòng lệnh.

Pipeline:
1. Setup: Tải dữ liệu, tiền xử lý, tạo embeddings và lưu index
2. Chat: Cho phép người dùng nhập câu hỏi và nhận câu trả lời trong vòng lặp tương tác
"""

import numpy as np
import logging
import os
from typing import List, Optional, Dict, Any

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import các module cần thiết
from src.data_loader import load_pdf_text
from src.text_preprocessing import preprocess_text
from src.embedder import VietnameseEmbedder, save_faiss_index
from src.retriever import retrieve_top_k, retrieve_with_mmr
from src.chatbot import ask_gemini
from src.descripe_file import describe


class RAGPipeline:
    """Pipeline cho hệ thống RAG tiếng Việt"""
    
    def __init__(self):
        """Khởi tạo pipeline"""
        self.pdf_path = None
        self.index_path = None
        self.system_prompt = None
        self.is_setup_complete = False
    
    def setup(self, pdf_path: str, index_path: str = "embeddings/vector_store/faiss_index") -> bool:
        """
        Thiết lập và xây dựng vector store từ PDF
        
        Args:
            pdf_path: Đường dẫn đến file PDF nguồn
            index_path: Đường dẫn lưu/nạp FAISS index
            
        Returns:
            bool: Trạng thái thành công của quá trình setup
        """
        self.pdf_path = pdf_path
        self.index_path = index_path
        
        try:
            # Tạo thư mục chứa index nếu chưa tồn tại
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            
            logger.info(f"Đang tải dữ liệu từ {pdf_path}")
            text = load_pdf_text(pdf_path)
            
            logger.info("Đang tiền xử lý văn bản")
            processed_sentences = preprocess_text(text)
            
            logger.info("Đang tạo embeddings")
            embedder = VietnameseEmbedder()
            embeddings = embedder.encode(processed_sentences)
            
            logger.info(f"Đang lưu FAISS index tại {index_path}")
            save_faiss_index(np.array(embeddings), processed_sentences, index_path)
            
            # Tạo system prompt
            logger.info("Đang tạo system prompt")
            self.system_prompt = describe()
            
            self.is_setup_complete = True
            logger.info("Setup hoàn tất")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình setup: {str(e)}")
            return False
    
    def chat_loop(self, use_mmr: bool = True) -> None:
        """
        Vòng lặp chat cho phép người dùng nhập câu hỏi và nhận câu trả lời
        
        Args:
            use_mmr: Sử dụng phương pháp MMR để đa dạng kết quả tìm kiếm
        """
        if not self.is_setup_complete:
            logger.error("Vui lòng chạy phương thức setup() trước khi bắt đầu chat")
            return
        
        print("\n" + "="*50)
        print("🤖 CHATBOT TRẢ LỜI DỰA TRÊN TÀI LIỆU PDF")
        print("="*50)
        print("Nhập 'exit', 'quit' hoặc 'q' để thoát")
        print("="*50 + "\n")
        
        while True:
            # Nhận câu hỏi từ người dùng
            question = input("\n📝 Nhập câu hỏi của bạn: ")
            
            # Kiểm tra thoát
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Cảm ơn bạn đã sử dụng chatbot. Tạm biệt!")
                break
            
            # Bỏ qua câu hỏi trống
            if not question.strip():
                continue
                
            try:
                # Lấy ngữ cảnh liên quan dựa trên câu hỏi
                logger.info(f"Đang truy xuất ngữ cảnh cho câu hỏi: {question}")
                if use_mmr:
                    contexts = retrieve_with_mmr(question)
                else:
                    contexts = retrieve_top_k(question)
                
                context_combined = "\n".join(contexts)
                
                # Hiển thị thông báo chờ
                print("⏳ Đang xử lý câu trả lời...")
                
                # Tạo câu trả lời từ mô hình
                answer = ask_gemini(self.system_prompt, question, context_combined)
                
                # Hiển thị câu trả lời
                print(f"\n💬 Trả lời: {answer}")
                
            except Exception as e:
                logger.error(f"Lỗi khi xử lý câu hỏi: {str(e)}")
                print(f"\n❌ Đã xảy ra lỗi: {str(e)}")


def main():
    """Hàm chính để chạy hệ thống"""
    # Khởi tạo pipeline
    pipeline = RAGPipeline()
    
    # Thiết lập đường dẫn PDF
    pdf_path = "data/raw/sample.pdf"
    
    # Pipeline 1: Setup - Xây dựng vector store
    setup_success = pipeline.setup(pdf_path)
    
    if setup_success:
        # Pipeline 2: Chat - Bắt đầu vòng lặp chat
        pipeline.chat_loop(use_mmr=True)
    else:
        print("❌ Không thể khởi tạo hệ thống. Vui lòng kiểm tra lỗi.")


if __name__ == "__main__":
    main()
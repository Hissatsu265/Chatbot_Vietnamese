#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vietnamese RAG (Retrieval-Augmented Generation) System API
---------------------------------------------------------
Backend API cho hệ thống RAG tiếng Việt sử dụng FastAPI.

Các endpoints chính:
1. POST /setup: Tải và xử lý tài liệu PDF, xây dựng vector store
2. POST /query: Trả lời câu hỏi dựa trên tài liệu đã xử lý
3. GET /health: Kiểm tra trạng thái hoạt động của API
"""

import os
import shutil
import logging
import numpy as np
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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


# Định nghĩa các models Pydantic cho API
class QueryRequest(BaseModel):
    question: str = Field(..., description="Câu hỏi cần trả lời")
    use_mmr: bool = Field(True, description="Sử dụng MMR để đa dạng kết quả tìm kiếm")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="Câu trả lời từ hệ thống")
    contexts: List[str] = Field([], description="Các đoạn văn bản liên quan được sử dụng")
    processing_time: float = Field(..., description="Thời gian xử lý (ms)")


class SetupResponse(BaseModel):
    status: str = Field(..., description="Trạng thái thành công/thất bại")
    message: str = Field(..., description="Thông báo chi tiết")
    document_info: Optional[Dict[str, Any]] = Field(None, description="Thông tin về tài liệu đã xử lý")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Trạng thái hoạt động của API")
    setup_complete: bool = Field(..., description="Trạng thái đã setup hay chưa")
    document_loaded: Optional[str] = Field(None, description="Tên tài liệu đã tải (nếu có)")


class RAGService:
    """Dịch vụ RAG cung cấp chức năng xử lý văn bản và trả lời câu hỏi"""
    
    def __init__(self):
        """Khởi tạo dịch vụ RAG"""
        self.pdf_path = None
        self.index_path = "embeddings/vector_store/faiss_index"
        self.system_prompt = None
        self.is_setup_complete = False
        self.document_info = None
        self.embedder = VietnameseEmbedder()
        
        # Tạo thư mục chứa tài liệu và embedding nếu chưa tồn tại
        os.makedirs("uploads", exist_ok=True)
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
    
    async def setup(self, pdf_path: str) -> Dict[str, Any]:
        """
        Thiết lập và xây dựng vector store từ PDF
        
        Args:
            pdf_path: Đường dẫn đến file PDF nguồn
            
        Returns:
            Dict: Kết quả của quá trình setup
        """
        self.pdf_path = pdf_path
        
        try:
            logger.info(f"Đang tải dữ liệu từ {pdf_path}")
            text = load_pdf_text(pdf_path)
            
            logger.info("Đang tiền xử lý văn bản")
            processed_sentences = preprocess_text(text)
            
            logger.info("Đang tạo embeddings")
            embeddings = self.embedder.encode(processed_sentences)
            
            logger.info(f"Đang lưu FAISS index tại {self.index_path}")
            save_faiss_index(np.array(embeddings), processed_sentences, self.index_path)
            
            # Tạo system prompt
            logger.info("Đang tạo system prompt")
            self.system_prompt = describe()
            
            # Thông tin tài liệu
            self.document_info = {
                "filename": os.path.basename(pdf_path),
                "sentence_count": len(processed_sentences),
                "embedding_dimensions": embeddings[0].shape[0] if len(embeddings) > 0 else 0
            }
            
            self.is_setup_complete = True
            logger.info("Setup hoàn tất")
            
            return {
                "status": "success",
                "message": "Thiết lập thành công",
                "document_info": self.document_info
            }
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình setup: {str(e)}")
            self.is_setup_complete = False
            
            return {
                "status": "error",
                "message": f"Lỗi trong quá trình setup: {str(e)}",
                "document_info": None
            }
    
    async def answer_question(self, question: str, use_mmr: bool = True) -> Dict[str, Any]:
        """
        Trả lời câu hỏi dựa trên dữ liệu đã xử lý
        
        Args:
            question: Câu hỏi cần trả lời
            use_mmr: Sử dụng phương pháp MMR để đa dạng kết quả
            
        Returns:
            Dict: Chứa câu trả lời và thông tin liên quan
        """
        import time
        start_time = time.time()
        
        if not self.is_setup_complete:
            return {
                "answer": "Hệ thống chưa được thiết lập. Vui lòng tải lên tài liệu PDF trước.",
                "contexts": [],
                "processing_time": 0
            }
        
        try:
            # Lấy ngữ cảnh liên quan dựa trên câu hỏi
            logger.info(f"Đang truy xuất ngữ cảnh cho câu hỏi: {question}")
            if use_mmr:
                contexts = retrieve_with_mmr(question)
            else:
                contexts = retrieve_top_k(question)
            
            context_combined = "\n".join(contexts)
            
            # Tạo câu trả lời từ mô hình
            answer = ask_gemini(self.system_prompt, question, context_combined)
            
            processing_time = (time.time() - start_time) * 1000  # Chuyển đổi thành ms
            
            return {
                "answer": answer,
                "contexts": contexts,
                "processing_time": round(processing_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Lỗi khi xử lý câu hỏi: {str(e)}")
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "answer": f"Đã xảy ra lỗi khi xử lý câu hỏi: {str(e)}",
                "contexts": [],
                "processing_time": round(processing_time, 2)
            }


# Khởi tạo FastAPI app
app = FastAPI(
    title="Vietnamese RAG API",
    description="API cho hệ thống Retrieval-Augmented Generation tiếng Việt",
    version="1.0.0"
)

# Thêm middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production, nên giới hạn danh sách origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo service
rag_service = RAGService()


# Dependency để kiểm tra trạng thái setup
def verify_setup():
    if not rag_service.is_setup_complete:
        raise HTTPException(status_code=400, detail="Hệ thống chưa được thiết lập. Vui lòng gọi /setup trước.")
    return True


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Kiểm tra trạng thái của API"""
    return {
        "status": "operational",
        "setup_complete": rag_service.is_setup_complete,
        "document_loaded": os.path.basename(rag_service.pdf_path) if rag_service.pdf_path else None
    }


@app.post("/setup", response_model=SetupResponse)
async def setup_system(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Tải lên file PDF và thiết lập hệ thống
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")
    
    # Lưu file tạm
    pdf_path = f"uploads/{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Xử lý trong nền để API trả về nhanh
    background_tasks.add_task(rag_service.setup, pdf_path)
    
    return {
        "status": "processing",
        "message": f"Tài liệu {file.filename} đang được xử lý. Kiểm tra /health để biết trạng thái.",
        "document_info": None
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, _: bool = Depends(verify_setup)):
    """
    Trả lời câu hỏi dựa trên tài liệu đã xử lý
    """
    result = await rag_service.answer_question(request.question, request.use_mmr)
    return result


@app.post("/upload-and-query")
async def upload_and_query(
    question: str,
    use_mmr: bool = True,
    file: UploadFile = File(...)
):
    """
    Tải lên file PDF, thiết lập hệ thống và trả lời câu hỏi (tất cả trong một API)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")
    
    # Lưu file tạm
    pdf_path = f"uploads/{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Setup đồng bộ (đợi hoàn thành)
    await rag_service.setup(pdf_path)
    
    # Trả lời câu hỏi
    result = await rag_service.answer_question(question, use_mmr)
    return result


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
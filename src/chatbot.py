import google.generativeai as genai

genai.configure(api_key="AIzaSyDHi...")

def ask_gemini(promt,question, context, model_name="gemini-2.0-flash"):
    model = genai.GenerativeModel(model_name)
    print("context: ",context)
    prompt = f"""
    Bạn là một trợ lý AI thông minh. Dưới đây là các đoạn trích từ tài liệu là {promt}. 
    Hãy trả lời CHÍNH XÁC và NGẮN GỌN, chỉ dựa trên nội dung tài liệu.
    ---
    {context}
    ---
    Câu hỏi: {question}
    """
    response = model.generate_content(prompt)
    return response.text

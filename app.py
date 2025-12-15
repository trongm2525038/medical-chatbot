# app.py

from flask import Flask, render_template, request, jsonify
import chatbot_logic

app = Flask(__name__)

try:
    print("\n--- Khởi tạo Chatbot Logic ---")
    
    chatbot_logic.initialize_chatbot() 
    KNOWLEDGE_BASE = chatbot_logic.KNOWLEDGE_BASE
    model = chatbot_logic.model
    kb_embeddings = chatbot_logic.kb_embeddings
    
    print("--- Chatbot sẵn sàng phục vụ! ---")

except Exception as e:
    print(f"LỖI KHỞI TẠO CHATBOT: {e}")
    KNOWLEDGE_BASE = [] # Đặt về rỗng để chặn các request về sau
    
# -------------------------------------------------------------------

@app.route("/")
def index():
    """Hiển thị giao diện chat."""
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    """Xử lý yêu cầu POST từ giao diện web và trả về câu trả lời."""
    
    if not KNOWLEDGE_BASE:
        return jsonify({"response": "Lỗi hệ thống: Dữ liệu chưa được tải. Vui lòng kiểm tra log server."})
    
    user_message = request.json.get("message")
    
    if user_message:
        # Gọi hàm logic tìm kiếm câu trả lời
        response_text = chatbot_logic.get_response(
            user_message,
            kb_embeddings,
            KNOWLEDGE_BASE,
            model,
            chatbot_logic.SIMILARITY_THRESHOLD
        )
        
        return jsonify({"response": response_text})
        
    return jsonify({"response": "Vui lòng nhập câu hỏi."})

if __name__ == "__main__":
    app.run(debug=True)
pip install flask
pip install pandas openpyxl torch transformers sentence-transformers numpy scikit-learn

python app.py

Link: http://127.0.0.1:5000/

Các câu hỏi
Thời gian làm việc
Cách đặt lịch
Có hỗ trợ kết quả xét nghiệm online không
và nhiều câu hỏi khác
Xem tại data.xlsx

# Công nghệ sử dụng
Semantic Search - Tìm kiếm ngữ nghĩa - chatbot_logic.py - Trả lời câu hỏi dựa trên Ý nghĩa (không chỉ từ khóa).
Word Embeddings - Vector hóa ngôn ngữ - chatbot_logic.py - Biến câu hỏi thành vector số học để máy tính tính toán.
Sentence Transformers - Mô hình AI (BERT-based) - chatbot_logic.py - Công cụ tạo ra các vector Embeddings.
Cosine Similarity - Độ tương đồng Cosine - chatbot_logic.py - Thuật toán để đo lường mức độ khớp giữa hai vector câu hỏi.
Flask - Web Framework (Python) - app.py - Xử lý yêu cầu từ trình duyệt, định tuyến URL và tạo Web API.
Pandas - Thư viện xử lý dữ liệu - chatbot_logic.py - Đọc, làm sạch và chuẩn hóa dữ liệu FAQ từ file CSV/Excel.

# File chatbot_logic.py là bộ não (Brain) của Chatbot, nơi chứa tất cả logic xử lý ngôn ngữ tự nhiên (NLP) và tìm kiếm thông tin.

1. Công nghệ Chính: Semantic Search (Tìm kiếm Ngữ nghĩa)
Nguyên lý: Thay vì chỉ tìm các từ khóa chính xác (như thời gian làm việc vs thời gian hoạt động), Semantic Search hiểu rằng các câu có ý nghĩa tương đương nhau.
Vai trò trong Code: Khi người dùng hỏi một câu mới (user_query), nó được so sánh về mặt ngữ nghĩa với TẤT CẢ các câu hỏi đã có trong kho tri thức (KNOWLEDGE_BASE).

2. Công nghệ Nền tảng: Word Embeddings (Vector hóa Ngôn ngữ)
Khái niệm: Máy tính không hiểu chữ cái, nên chúng ta cần biến câu thành vector số (một chuỗi số dài, ví dụ: [0.12, -0.45, 0.98...]). Các vector có ý nghĩa gần nhau sẽ nằm gần nhau trong không gian toán học.
Công cụ: SentenceTransformer (Mô hình BERT/Transformer): Đây là mô hình Trí tuệ Nhân tạo hiện đại (dựa trên kiến trúc Transformer) được huấn luyện sẵn. Nó nhận vào một câu và trả về một vector Embedding đại diện cho ý nghĩa của câu đó.

3. Thuật toán Trả lời: Cosine Similarity (Độ tương đồng Cosine)
Khái niệm: Sau khi cả câu hỏi của người dùng và các câu hỏi trong dữ liệu được chuyển thành vector, ta dùng thuật toán Cosine Similarity để tính góc giữa hai vector này. Góc càng nhỏ (giá trị Similarity càng gần 1.0), ý nghĩa của hai câu càng giống nhau.
Vai trò trong Code: get_response(): Hàm này dùng cosine_similarity từ thư viện scikit-learn để tìm ra câu hỏi nào trong KNOWLEDGE_BASE khớp nhất với câu hỏi của người dùng.
SIMILARITY_THRESHOLD (Ngưỡng): Đây là ngưỡng quyết định. Nếu điểm tương đồng cao hơn ngưỡng (ví dụ: 0.65), chatbot trả lời. Nếu thấp hơn, chatbot từ chối trả lời (giúp tránh trả lời sai).

4. Xử lý Dữ liệu: Pandas
Vai trò: Thư viện Pandas được sử dụng trong hàm load_knowledge_base_from_file để dễ dàng đọc và thao tác với dữ liệu có cấu trúc từ file CSV (hoặc Excel).

# File app.py

1. Công nghệ Chính: Flask (Web Framework)
Khái niệm: Flask là một khung làm việc (framework) nhẹ của Python, dùng để xây dựng các ứng dụng web và API.

Vai trò trong Code: app = Flask(__name__): Khởi tạo ứng dụng web.

@app.route("/"): Định tuyến URL. Nó chỉ định rằng khi người dùng truy cập trang chủ (/), Flask sẽ chạy hàm index() và trả về giao diện HTML (index.html).

@app.route("/get_response", methods=["POST"]): Tạo một Web API Endpoint (điểm cuối API). Đây là điểm mà JavaScript (trong index.html) gửi câu hỏi của người dùng đến.

2. Quản lý Trạng thái (State Management)
Hàm initialize_chatbot(): Đây là một thủ thuật quan trọng. Nó được gọi một lần duy nhất khi server Flask khởi động. Việc này đảm bảo rằng các mô hình nặng (như SentenceTransformer) và tất cả các vector dữ liệu (kb_embeddings) chỉ được tải và tính toán một lần, giúp các yêu cầu trả lời sau đó diễn ra cực kỳ nhanh chóng.

request.json.get("message"): Flask nhận dữ liệu JSON được gửi từ JavaScript (chứa câu hỏi của người dùng).

jsonify({"response": response_text}): Sau khi chatbot_logic trả về câu trả lời, Flask đóng gói câu trả lời đó vào định dạng JSON để gửi ngược lại cho JavaScript hiển thị lên giao diện web.

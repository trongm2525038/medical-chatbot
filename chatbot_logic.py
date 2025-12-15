# chatbot_logic.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import os


KNOWLEDGE_BASE = []
model = None
kb_embeddings = None

EXCEL_FILE_PATH = 'data.csv' 
QUESTION_COLUMN = 'Question' 
ANSWER_COLUMN = 'Answer'     
SIMILARITY_THRESHOLD = 0.65  


def load_knowledge_base_from_file(file_path, question_col, answer_col):
    if not os.path.exists(file_path):
        print(f"LỖI TẢI DỮ LIỆU: Không tìm thấy file tại đường dẫn '{file_path}'.")
        return []
    
    try:
        df = pd.read_csv(file_path)
        
        if question_col not in df.columns or answer_col not in df.columns:
             print(f"LỖI DỮ LIỆU: File thiếu cột '{question_col}' hoặc '{answer_col}'.")
             return []

        df = df.dropna(subset=[question_col, answer_col])
        
        knowledge_base = []
        for index, row in df.iterrows():
            knowledge_base.append({
                "question": str(row[question_col]).strip(),
                "answer": str(row[answer_col]).strip()
            })
            
        return knowledge_base
        
    except Exception as e:
        print(f"LỖI XẢY RA khi đọc file dữ liệu: {e}")
        return []


def create_knowledge_embeddings(knowledge_base, model):
    """Tạo vector ngữ nghĩa cho tất cả các câu hỏi trong cơ sở tri thức."""
    
    questions = [item["question"] for item in knowledge_base]
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    question_embeddings = model.encode(
        questions, 
        convert_to_tensor=True, 
        device=device
    )
    
    return question_embeddings.cpu().numpy()

def get_response(user_query, kb_embeddings, knowledge_base, model, threshold):

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    user_embedding = model.encode(
        [user_query], 
        convert_to_tensor=True, 
        device=device
    ).cpu().numpy()
    
    similarities = cosine_similarity(user_embedding, kb_embeddings)[0]
    best_match_index = np.argmax(similarities)
    best_similarity_score = similarities[best_match_index]
    
    if best_similarity_score >= threshold:
        return knowledge_base[best_match_index]["answer"]
    else:
        return "Xin lỗi, tôi không tìm thấy thông tin cụ thể nào trong cơ sở dữ liệu của chúng tôi. Bạn có thể thử hỏi cách khác không?"



def initialize_chatbot():
    global KNOWLEDGE_BASE, model, kb_embeddings
    
    KNOWLEDGE_BASE = load_knowledge_base_from_file(
        file_path=EXCEL_FILE_PATH,
        question_col=QUESTION_COLUMN,
        answer_col=ANSWER_COLUMN
    )
    
    if not KNOWLEDGE_BASE:
        raise Exception("Không thể tải KNOWLEDGE_BASE từ file CSV.")

    print("Đang tải mô hình Embedding...")
    model = SentenceTransformer('all-mpnet-base-v2')
    print("Đã tải mô hình thành công.")
    
    kb_embeddings = create_knowledge_embeddings(KNOWLEDGE_BASE, model)
    print(f"Đã tạo {len(kb_embeddings)} vector dữ liệu.")
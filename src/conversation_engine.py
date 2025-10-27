"""
Conversation engine with agent for mental health chat
"""

import os
import json
from datetime import datetime
from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import FunctionTool
from src.global_settings import (
    INDEX_STORAGE, 
    CONVERSATION_FILE, 
    SCORES_FILE,
    SIMILARITY_TOP_K
)
from src.prompts import CUSTORM_AGENT_SYSTEM_TEMPLATE


def load_chat_store():
    """Load or initialize chat store"""
    if os.path.exists(CONVERSATION_FILE) and os.path.getsize(CONVERSATION_FILE) > 0:
        try:
            chat_store = SimpleChatStore.from_persist_path(CONVERSATION_FILE)
        except json.JSONDecodeError:
            chat_store = SimpleChatStore()
    else:
        chat_store = SimpleChatStore()
    return chat_store


def save_chat_store(chat_store):
    """Save chat store to file"""
    os.makedirs(os.path.dirname(CONVERSATION_FILE), exist_ok=True)
    chat_store.persist(persist_path=CONVERSATION_FILE)


def save_score(score, content, total_guess, username):
    """
    Save diagnostic score to file
    
    Args:
        score (str): Score of the user's mental health
        content (str): Content of the diagnosis
        total_guess (str): Total assessment of the user's mental health
        username (str): Username
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "username": username,
        "Time": current_time,
        "Score": score,
        "Content": content,
        "Total_guess": total_guess
    }
    
    # Load existing data
    try:
        with open(SCORES_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    
    # Append new entry
    data.append(new_entry)
    
    # Save back to file
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    with open(SCORES_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return f"Đã lưu kết quả chẩn đoán cho {username}"


def initialize_agent(username, user_info=""):
    """
    Initialize chatbot agent with tools
    
    Args:
        username: Username for chat history
        user_info: Additional user information
        
    Returns:
        OpenAIAgent: Configured agent
    """
    # Load chat store
    chat_store = load_chat_store()
    
    # Create memory
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key=username
    )
    
    # Load index
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
    index = load_index_from_storage(storage_context, index_id="vector")
    
    # Create DSM5 query engine
    dsm5_engine = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
    
    # Create DSM5 tool
    dsm5_tool = QueryEngineTool(
        query_engine=dsm5_engine,
        metadata=ToolMetadata(
            name="dsm5",
            description=(
                "Cung cấp các thông tin liên quan đến các bệnh tâm thần "
                "theo tiêu chuẩn DSM5. Sử dụng câu hỏi văn bản thuần túy chi tiết "
                "làm đầu vào cho công cụ này."
            ),
        )
    )
    
    # Create save score tool
    def save_score_wrapper(score: str, content: str, total_guess: str):
        """
        Lưu kết quả chẩn đoán sức khỏe tâm thần
        
        Args:
            score (str): Điểm số (kém/trung bình/bình thường/tốt)
            content (str): Nội dung chi tiết chẩn đoán
            total_guess (str): Tổng đoán về tình trạng
        """
        return save_score(score, content, total_guess, username)
    
    save_tool = FunctionTool.from_defaults(fn=save_score_wrapper)
    
    # Create agent
    agent = OpenAIAgent.from_tools(
        tools=[dsm5_tool, save_tool],
        memory=memory,
        system_prompt=CUSTORM_AGENT_SYSTEM_TEMPLATE.format(user_info=user_info),
        verbose=False
    )
    
    return agent, chat_store


def get_chat_history(username):
    """Get chat history for a user"""
    chat_store = load_chat_store()
    messages = chat_store.get_messages(username)
    return messages


def clear_chat_history(username):
    """Clear chat history for a user"""
    chat_store = load_chat_store()
    chat_store.delete_messages(username)
    save_chat_store(chat_store)
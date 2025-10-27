"""
Chat page - Conversation with AI psychologist
"""

import streamlit as st
from src.conversation_engine import initialize_agent, save_chat_store, get_chat_history
from src.slide_bar import render_sidebar
from src.global_settings import APP_TITLE, APP_ICON
from src.ingest_pipeline import initialize_settings

st.set_page_config(
    page_title=f"Trò chuyện - {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide"
)

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Vui lòng đăng nhập để sử dụng tính năng này!")
    st.stop()

# Initialize settings
initialize_settings()

# Render sidebar
render_sidebar()

# Page title
st.title("💬 Trò chuyện với Chuyên gia AI")

# Initialize agent
if 'agent' not in st.session_state:
    with st.spinner("Đang khởi tạo chuyên gia AI..."):
        user_info_str = ""
        if 'user_info' in st.session_state:
            user_info = st.session_state.user_info
            info_parts = []
            if user_info.get('age'):
                info_parts.append(f"Tuổi: {user_info['age']}")
            if user_info.get('gender'):
                info_parts.append(f"Giới tính: {user_info['gender']}")
            user_info_str = ", ".join(info_parts)
        
        agent, chat_store = initialize_agent(
            st.session_state.username,
            user_info_str
        )
        st.session_state.agent = agent
        st.session_state.chat_store = chat_store

# Display chat history
messages = get_chat_history(st.session_state.username)

# Create chat container
chat_container = st.container()

with chat_container:
    for message in messages:
        role = message.role
        content = message.content
        
        if role == 'user':
            with st.chat_message("user"):
                st.write(content)
        elif role == 'assistant' and content:
            with st.chat_message("assistant"):
                st.write(content)

# Chat input
user_input = st.chat_input("Nhập tin nhắn của bạn...")

if user_input:
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)
    
    # Get response from agent
    with st.spinner("Đang suy nghĩ..."):
        try:
            response = st.session_state.agent.chat(user_input)
            
            # Display assistant response
            with chat_container:
                with st.chat_message("assistant"):
                    st.write(str(response))
            
            # Save chat history
            save_chat_store(st.session_state.chat_store)
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {str(e)}")
            st.info("Vui lòng thử lại hoặc liên hệ quản trị viên nếu lỗi vẫn tiếp tục.")

# Sidebar options
with st.sidebar:
    st.markdown("---")
    st.markdown("### ⚙️ Tùy chọn")
    
    if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True):
        if st.session_state.chat_store:
            st.session_state.chat_store.delete_messages(st.session_state.username)
            save_chat_store(st.session_state.chat_store)
            st.success("Đã xóa lịch sử trò chuyện!")
            st.rerun()
    
    if st.button("🔄 Làm mới Agent", use_container_width=True):
        if 'agent' in st.session_state:
            del st.session_state.agent
        st.success("Đã làm mới Agent!")
        st.rerun()

# Information panel
with st.expander("ℹ️ Hướng dẫn sử dụng"):
    st.markdown("""
    ### Cách sử dụng tính năng trò chuyện:
    
    1. **Bắt đầu trò chuyện**: Gõ tin nhắn vào ô chat bên dưới
    2. **Chia sẻ cảm xúc**: Hãy chia sẻ những gì bạn đang cảm thấy một cách thoải mái
    3. **Nhận tư vấn**: Chuyên gia AI sẽ lắng nghe và đưa ra lời khuyên phù hợp
    4. **Nhận đánh giá**: Khi kết thúc, bạn sẽ nhận được đánh giá về sức khỏe tâm thần
    
    ### Lưu ý:
    - Hãy trả lời trung thực để nhận được đánh giá chính xác
    - Lịch sử trò chuyện được lưu trữ an toàn
    - Bạn có thể xóa lịch sử bất cứ lúc nào
    """)

with st.expander("⚠️ Lưu ý quan trọng"):
    st.markdown("""
    - Đây là công cụ hỗ trợ, **không thay thế** cho chẩn đoán y khoa
    - Nếu bạn có ý định tự gây hại, vui lòng gọi **1800 6567** (Đường dây nóng tâm lý)
    - Với các vấn đề nghiêm trọng, hãy tìm kiếm sự giúp đỡ từ chuyên gia y tế
    - Thông tin của bạn được bảo mật tuyệt đối
    """)
"""
Home page - Login and Registration
"""

import streamlit as st
from src.authenticate import login_user, register_user, get_user_info
from src.global_settings import APP_TITLE, APP_ICON

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def show_login():
    """Display login form"""
    st.title("🔐 Đăng nhập")
    
    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submit = st.form_submit_button("Đăng nhập", use_container_width=True)
        
        if submit:
            if username and password:
                success, user_info = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_info = user_info
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng!")
            else:
                st.warning("Vui lòng nhập đầy đủ thông tin!")


def show_register():
    """Display registration form"""
    st.title("📝 Đăng ký tài khoản")
    
    with st.form("register_form"):
        username = st.text_input("Tên đăng nhập *")
        password = st.text_input("Mật khẩu *", type="password")
        confirm_password = st.text_input("Xác nhận mật khẩu *", type="password")
        email = st.text_input("Email")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.text_input("Tuổi")
        with col2:
            gender = st.selectbox("Giới tính", ["", "Nam", "Nữ", "Khác"])
        
        submit = st.form_submit_button("Đăng ký", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.warning("Vui lòng nhập tên đăng nhập và mật khẩu!")
            elif password != confirm_password:
                st.error("Mật khẩu xác nhận không khớp!")
            else:
                success, message = register_user(username, password, email, age, gender)
                if success:
                    st.success(message)
                    st.info("Vui lòng đăng nhập để sử dụng hệ thống")
                else:
                    st.error(message)


def show_home():
    """Display home page for logged in users"""
    st.title(f"🏠 Chào mừng đến với {APP_TITLE}")
    
    st.markdown("""
    ## Giới thiệu
    
    Hệ thống Chăm sóc Sức khỏe Tinh thần là một ứng dụng AI được phát triển để hỗ trợ 
    người dùng trong việc:
    
    - 💬 **Trò chuyện và tư vấn tâm lý**: Trò chuyện với chuyên gia AI một cách tự nhiên và được tư vấn
    - 🔍 **Phân tích và chẩn đoán**: Đánh giá tình trạng sức khỏe tâm thần dựa trên tiêu chuẩn DSM-5
    - 📊 **Theo dõi tiến trình**: Theo dõi sức khỏe tâm thần theo thời gian
    
    ## Hướng dẫn sử dụng
    
    1. 💬 **Trò chuyện**: Truy cập trang "Trò chuyện" để bắt đầu nói chuyện với chuyên gia AI
    2. 📊 **Xem kết quả**: Truy cập trang "Sức khỏe của tôi" để xem lịch sử và thống kê
    
    ## Lưu ý quan trọng
    
    - ⚠️ Đây là công cụ hỗ trợ, không thay thế cho chẩn đoán y khoa chuyên nghiệp
    - 🔒 Thông tin của bạn được bảo mật an toàn
    - 💙 Nếu bạn cần hỗ trợ khẩn cấp, vui lòng liên hệ với chuyên gia y tế
    """)
    
    # Quick stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Người dùng", st.session_state.username)
    
    with col2:
        # Count chat messages
        from src.conversation_engine import get_chat_history
        messages = get_chat_history(st.session_state.username)
        st.metric("💬 Tin nhắn", len(messages))
    
    with col3:
        # Count assessments
        import json
        import os
        from src.global_settings import SCORES_FILE
        
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                scores = json.load(f)
                user_scores = [s for s in scores if s['username'] == st.session_state.username]
                st.metric("📋 Đánh giá", len(user_scores))
        except:
            st.metric("📋 Đánh giá", 0)


# Main app logic
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    with tab1:
        show_login()
    
    with tab2:
        show_register()
else:
    from src.slide_bar import render_sidebar
    render_sidebar()
    show_home()
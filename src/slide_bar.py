"""
Sidebar configuration for Streamlit app
"""

import streamlit as st


def render_sidebar():
    """Render sidebar with navigation and user info"""
    with st.sidebar:
        st.title("🧠 Mental Health Care")

        if 'username' in st.session_state:
            st.success(f"Xin chào, {st.session_state.username}!")

            st.markdown("---")
            st.markdown("### 📋 Menu")

            # Navigation
            pages = {
                "🏠 Trang chủ": "Home.py",
                "💬 Trò chuyện": "pages/2_Chat.py",
                "📊 Sức khỏe của tôi": "pages/1_User_Health.py"
            }

            st.markdown("---")

            # User info
            st.markdown("### 👤 Thông tin người dùng")
            if 'user_info' in st.session_state:
                user_info = st.session_state.user_info
                if user_info.get('email'):
                    st.text(f"📧 Email: {user_info['email']}")
                if user_info.get('age'):
                    st.text(f"🎂 Tuổi: {user_info['age']}")
                if user_info.get('gender'):
                    st.text(f"⚧ Giới tính: {user_info['gender']}")

            st.markdown("---")

            # Logout button
            if st.button("🚪 Đăng xuất", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        else:
            st.info("Vui lòng đăng nhập để sử dụng hệ thống")

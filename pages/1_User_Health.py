"""
User Health page - View health statistics and history
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.slide_bar import render_sidebar
from src.global_settings import APP_TITLE, APP_ICON, SCORES_FILE

st.set_page_config(
    page_title=f"Sức khỏe của tôi - {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide"
)

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Vui lòng đăng nhập để sử dụng tính năng này!")
    st.stop()

# Render sidebar
render_sidebar()

# Page title
st.title("📊 Sức khỏe Tinh thần của Tôi")

# Load user scores


def load_user_scores(username):
    """Load scores for specific user"""
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            all_scores = json.load(f)
            user_scores = [s for s in all_scores if s['username'] == username]
            return user_scores
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


# Get user scores
user_scores = load_user_scores(st.session_state.username)

if not user_scores:
    st.info("📝 Chưa có dữ liệu đánh giá. Hãy bắt đầu trò chuyện để nhận đánh giá sức khỏe tinh thần!")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(user_scores)
df['Time'] = pd.to_datetime(df['Time'])
df = df.sort_values('Time', ascending=False)

# Score mapping for visualization
score_mapping = {
    'tốt': 4,
    'bình thường': 3,
    'trung bình': 2,
    'kém': 1
}

df['Score_Numeric'] = df['Score'].str.lower().map(score_mapping)

# Statistics Section
st.markdown("## 📈 Thống kê tổng quan")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Tổng số đánh giá", len(df))

with col2:
    latest_score = df.iloc[0]['Score']
    st.metric("🎯 Đánh giá gần nhất", latest_score)

with col3:
    avg_score = df['Score_Numeric'].mean()
    score_labels = {4: 'Tốt', 3: 'Bình thường', 2: 'Trung bình', 1: 'Kém'}
    avg_label = score_labels[round(avg_score)]
    st.metric("📊 Điểm trung bình", avg_label)

with col4:
    # Get last 7 days data
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_scores = df[df['Time'] >= seven_days_ago]
    st.metric("📅 Đánh giá 7 ngày", len(recent_scores))

st.markdown("---")

# Chart Section
st.markdown("## 📉 Biểu đồ theo dõi")

# Time series chart
fig_timeline = go.Figure()

fig_timeline.add_trace(go.Scatter(
    x=df['Time'].iloc[::-1],
    y=df['Score_Numeric'].iloc[::-1],
    mode='lines+markers',
    name='Điểm sức khỏe',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=10, color='#1f77b4', symbol='circle')
))

fig_timeline.update_layout(
    title='Biểu đồ theo dõi sức khỏe tinh thần theo thời gian',
    xaxis_title='Thời gian',
    yaxis_title='Điểm số',
    yaxis=dict(
        tickmode='array',
        tickvals=[1, 2, 3, 4],
        ticktext=['Kém', 'Trung bình', 'Bình thường', 'Tốt']
    ),
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Score distribution
col1, col2 = st.columns(2)

with col1:
    score_counts = df['Score'].value_counts()

    fig_pie = px.pie(
        values=score_counts.values,
        names=score_counts.index,
        title='Phân bố điểm đánh giá',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Bar chart of scores over time
    fig_bar = px.bar(
        df.iloc[:10][::-1],
        x='Time',
        y='Score_Numeric',
        color='Score',
        title='10 đánh giá gần nhất',
        labels={'Score_Numeric': 'Điểm số', 'Time': 'Thời gian'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_yaxes(
        tickmode='array',
        tickvals=[1, 2, 3, 4],
        ticktext=['Kém', 'Trung bình', 'Bình thường', 'Tốt']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Detailed History
st.markdown("## 📋 Lịch sử chi tiết")

# Filter options
col1, col2 = st.columns([2, 1])

with col1:
    date_range = st.date_input(
        "Chọn khoảng thời gian",
        value=(df['Time'].min().date(), df['Time'].max().date()),
        max_value=datetime.now().date()
    )

with col2:
    score_filter = st.multiselect(
        "Lọc theo điểm",
        options=['Tốt', 'Bình thường', 'Trung bình', 'Kém'],
        default=['Tốt', 'Bình thường', 'Trung bình', 'Kém']
    )

# Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['Time'].dt.date >= start_date) &
        (filtered_df['Time'].dt.date <= end_date)
    ]

filtered_df = filtered_df[filtered_df['Score'].isin(score_filter)]

# Display filtered results
st.markdown(f"**Hiển thị {len(filtered_df)} kết quả**")

for idx, row in filtered_df.iterrows():
    with st.expander(f"📅 {row['Time'].strftime('%d/%m/%Y %H:%M:%S')} - Điểm: {row['Score']}"):
        st.markdown(f"**🎯 Điểm đánh giá:** {row['Score']}")
        st.markdown(f"**📝 Tổng đoán:** {row.get('Total_guess', 'N/A')}")
        st.markdown(f"**📄 Chi tiết:**")
        st.write(row.get('Content', 'Không có nội dung'))

st.markdown("---")

# Export data
st.markdown("## 💾 Xuất dữ liệu")

col1, col2 = st.columns(2)

with col1:
    # Export to CSV
    csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Tải xuống CSV",
        data=csv,
        file_name=f"mental_health_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    # Export to JSON
    json_str = filtered_df.to_json(
        orient='records', force_ascii=False, indent=2)
    st.download_button(
        label="📥 Tải xuống JSON",
        data=json_str,
        file_name=f"mental_health_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

# Recommendations
st.markdown("---")
st.markdown("## 💡 Khuyến nghị")

# Analyze recent trend
if len(recent_scores) >= 2:
    recent_avg = recent_scores['Score_Numeric'].mean()

    if recent_avg >= 3.5:
        st.success("""
        🎉 **Tuyệt vời!** Sức khỏe tinh thần của bạn đang ở trạng thái tốt.
        - Tiếp tục duy trì lối sống lành mạnh
        - Dành thời gian cho các hoạt động yêu thích
        - Kết nối với người thân và bạn bè
        """)
    elif recent_avg >= 2.5:
        st.info("""
        👍 **Khá tốt!** Sức khỏe tinh thần của bạn đang ở mức ổn định.
        - Duy trì các thói quen tích cực
        - Tìm kiếm các hoạt động giảm stress
        - Đảm bảo ngủ đủ giấc và ăn uống điều độ
        """)
    elif recent_avg >= 1.5:
        st.warning("""
        ⚠️ **Cần chú ý!** Sức khỏe tinh thần của bạn có dấu hiệu suy giảm.
        - Tăng cường nghỉ ngơi và thư giãn
        - Tham gia các hoạt động thể chất nhẹ nhàng
        - Cân nhắc nói chuyện với bạn bè hoặc người thân
        - Sử dụng ứng dụng thường xuyên để theo dõi
        """)
    else:
        st.error("""
        🚨 **Cần hỗ trợ!** Sức khỏe tinh thần của bạn đang gặp khó khăn.
        - Liên hệ với chuyên gia tâm lý ngay: **1800 6567**
        - Tìm kiếm sự hỗ trợ từ người thân
        - Không nên ở một mình
        - Đây chỉ là công cụ hỗ trợ, vui lòng tìm kiếm trợ giúp chuyên nghiệp
        """)
else:
    st.info(
        "Cần thêm dữ liệu để đưa ra khuyến nghị chi tiết. Hãy tiếp tục sử dụng ứng dụng!")

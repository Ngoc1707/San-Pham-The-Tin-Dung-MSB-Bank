import io
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CẤU HÌNH TRANG & META TAGS ĐỂ HIỆN THỊ KHI GỬI LINK ZALO/FB
# ---------------------------------------------------------
EXCEL_FILE = "danh_sach_khach_hang_MSB.xlsx"
IMAGE_URL_MSB = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/MSB_logo.svg/1200px-MSB_logo.svg.png"

st.set_page_config(
    page_title="MSB - Quản Lý Khách Hàng",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chèn HTML Meta Tags để tạo thumbnail xem trước khi gửi link
st.markdown(
    f"""
    <head>
        <meta property="og:title" content="MSB - Quản Lý Khách Hàng" />
        <meta property="og:description" content="Hệ thống Quản lý & Tiếp nhận thông tin Khách hàng MSB" />
        <meta property="og:image" content="{IMAGE_URL_MSB}" />
        <meta property="og:type" content="website" />
    </head>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HÀM XỬ LÝ DỮ LIỆU EXCEL
# ---------------------------------------------------------
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(
            columns=[
                "Số điện thoại",
                "Tên khách hàng",
                "Địa chỉ",
                "Thu nhập/tháng",
                "Có thẻ tín dụng chưa",
                "Ghi chú",
            ]
        )

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

if "customer_data" not in st.session_state:
    st.session_state.customer_data = load_data()

# ---------------------------------------------------------
# 1. SIDEBAR (THANH MENU BÊN TRÁI GIỐNG MẪU ACB)
# ---------------------------------------------------------
with st.sidebar:
    st.image(IMAGE_URL_MSB, use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Hệ thống MSB Lead</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.write("📁 **MENU QUẢN LÝ**")
    menu = st.radio(
        label="",
        options=[

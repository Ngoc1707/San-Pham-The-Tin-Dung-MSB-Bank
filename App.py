import io
import os
import pandas as pd
import streamlit as st

# Đường dẫn file Excel dùng để lưu trữ dữ liệu vĩnh viễn
EXCEL_FILE = "danh_sach_khach_hang.xlsx"

# Link logo MSB chuẩn
IMAGE_URL_MSB = (
    "https://haitrieu.com/wp-content/uploads/2022/02/Logo-MSB-Na.png"
)

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="MSB - Quản Lý Khách Hàng", page_icon="🏦", layout="wide"
)


# Hàm tải dữ liệu từ Excel
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrameSố

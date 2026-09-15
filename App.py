    import io
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CẤU HÌNH TRANG & CSS TÙY CHỈNH NỀN ĐỎ NHẠT MSB CHO SIDEBAR
# ---------------------------------------------------------
EXCEL_FILE = "danh_sach_khach_hang_MSB.xlsx"
IMAGE_URL_MSB = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/MSB_logo.svg/1200px-MSB_logo.svg.png"

st.set_page_config(
    page_title="MSB - Quản Lý Khách Hàng",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho Sidebar màu đỏ nhạt MSB (#FF4D4D)
st.markdown(
    """
    <style>
        /* Đổi màu nền thanh Sidebar sang màu đỏ nhạt MSB */
        [data-testid="stSidebar"] {
            background-color: #FF4D4D !important;
        }
        
        /* Đổi tất cả màu chữ, tiêu đề, văn bản trong Sidebar sang màu trắng */
        [data-testid="stSidebar"] *, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: #FFFFFF !important;
        }

        /* Đổi màu đường kẻ ngang trong Sidebar */
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.4) !important;
        }

        /* Tùy chỉnh hiệu ứng cho radio button/menu được chọn */
        [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Chèn HTML Meta Tags để tạo thumbnail xem trước khi gửi link Zalo/FB
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
# 1. SIDEBAR (THANH MENU BÊN TRÁI NỀN ĐỎ NHẠT MSB)
# ---------------------------------------------------------
with st.sidebar:
    st.image(IMAGE_URL_MSB, use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Hệ thống MSB Lead</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.write("📁 **MENU QUẢN LÝ**")
    menu = st.radio(
        label="",
        options=[
            "📌 Bảng điều khiển",
            "📋 Danh sách Leads",
            "➕ Thêm Lead mới",
            "🔄 Tiến độ xử lý",
            "📈 Báo cáo chỉ số"
        ],
        index=2
    )
    st.write("---")
    st.caption("MSB Lead Manager - Nhóm Ngọc Yên\nPhát triển cho Khối KHCN MSB")

# ---------------------------------------------------------
# 2. MÀN HÌNH CHÍNH (XỬ LÝ THEO MENU)
# ---------------------------------------------------------
if menu == "➕ Thêm Lead mới":
    # TIÊU ĐỀ CHÍNH
    st.markdown(
        "<h1 style='text-align: center; color: #FF4D4D; font-weight: bold;'>NGÂN HÀNG MSB</h1>",
        unsafe_allow_html=True,
    )

    tab_form, tab_admin = st.tabs(["📝 Form Điền Thông Tin", "🔒 Trang Admin"])

    # TAB 1: FORM
    with tab_form:
        st.header("Thông Tin Khách Hàng")

        with st.form("customer_form", clear_on_submit=True):
            phone = st.text_input("Số điện thoại *", placeholder="0901234567")
            name = st.text_input("Tên khách hàng *", placeholder="Nguyễn Văn A")
            address = st.text_input("Địa chỉ", placeholder="Quận 1, TP.HCM")
            
            income = st.number_input(
                "Thu nhập/tháng (VNĐ)",
                min_value=0,
                step=1000000,
                format="%d",
            )
            
            has_credit_card = st.radio(
                "Có thẻ tín dụng chưa?",
                options=["Chưa", "Rồi"],
                horizontal=True,
            )

            note = st.text_area("Ghi chú", placeholder="Nhu cầu mở thẻ, vay...")

            submitted = st.form_submit_button("Lưu lại", type="primary")

            if submitted:
                if not phone or not name:
                    st.error("Vui lòng điền đầy đủ Số điện thoại và Tên khách hàng!")
                else:
                    new_entry = {
                        "Số điện thoại": phone,
                        "Tên khách hàng": name,
                        "Địa chỉ": address,
                        "Thu nhập/tháng": f"{income:,} VNĐ",
                        "Có thẻ tín dụng chưa": has_credit_card,
                        "Ghi chú": note,
                    }

                    st.session_state.customer_data = pd.concat(
                        [st.session_state.customer_data, pd.DataFrame([new_entry])],
                        ignore_index=True,
                    )
                    save_data(st.session_state.customer_data)
                    st.success("Đã lưu thông tin khách hàng thành công vào file Excel!")

    # TAB 2: ADMIN
    with tab_admin:
        st.header("Quản Lý Dữ Liệu Khách Hàng")
        pin_input = st.text_input(
            "Nhập mã PIN để truy cập trang Admin:",
            type="password",
            max_chars=6,
            placeholder="******",
        )

        if pin_input == "123456":
            st.success("Xác thực thành công!")
            df = load_data()

            if df.empty:
                st.info("Chưa có dữ liệu khách hàng nào được lưu.")
            else:
                st.dataframe(df, use_container_width=True)
                with open(EXCEL_FILE, "rb") as f:
                    file_data = f.read()

                st.download_button(
                    label="📥 Tải File Excel Khách Hàng",
                    data=file_data,
                    file_name="danh_sach_khach_hang_MSB.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        elif pin_input != "":
            st.error("Mã PIN không chính xác! Vui lòng thử lại.")

else:
    st.title(menu)
    st.info("Chức năng đang được cập nhật.")

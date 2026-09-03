import os
import pandas as pd
import streamlit as st

# Đường dẫn file Excel dùng để lưu trữ dữ liệu vĩnh viễn
EXCEL_FILE = "danh_sach_khach_hang.xlsx"

# Cấu hình trang
st.set_page_config(page_title="MSB - Quản Lý Khách Hàng", layout="wide")
import os
import pandas as pd
import streamlit as st

EXCEL_FILE = "danh_sach_khach_hang.xlsx"

# Cấu hình trang
st.set_page_config(page_title="MSB - Quản Lý Khách Hàng", layout="wide")

# =========================================================
# 👇 VỊ TRÍ CHÈN CÁCH 1 (HIỂN THỊ LOGO MSB) 👇
# =========================================================
logo_url = (
    "https://msb.com.vn/documents/20121/0/logo-msb.png"  # Link ảnh logo MSB
)

try:
    st.image(logo_url, width=250)
except Exception:
    st.title("🏦 MSB - NGÂN HÀNG HÀNG HẢI")
# =========================================================

st.write("---")

# Các phần code phía dưới (load_data, các TAB form/admin) giữ nguyên...

# Hàm tải dữ liệu từ Excel
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


# Hàm lưu dữ liệu vào Excel
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")


# Khởi tạo dữ liệu trong Session State từ file Excel
if "customer_data" not in st.session_state:
    st.session_state.customer_data = load_data()

# 1. Hiển thị Logo MSB ở trên cùng
try:
    st.image("image_10b869.png", width=250)
except Exception:
    st.title("MSB BANK")

st.write("---")

# Tạo 2 tab: Form nhập liệu và Trang Admin
tab_form, tab_admin = st.tabs(["📝 Form Điền Thông Tin", "🔒 Trang Admin"])

# ================= TAB 1: FORM NHẬP THÔNG TIN =================
with tab_form:
    st.header("Thông Tin Khách Hàng")

    with st.form("customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            phone = st.text_input("Số điện thoại *", placeholder="0901234567")
            name = st.text_input("Tên khách hàng *", placeholder="Nguyễn Văn A")
            address = st.text_input("Địa chỉ", placeholder="Quận 1, TP.HCM")

        with col2:
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

        submitted = st.form_submit_button("Lưu lại")

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

                # Cập nhật DataFrame trong session state
                st.session_state.customer_data = pd.concat(
                    [
                        st.session_state.customer_data,
                        pd.DataFrame([new_entry]),
                    ],
                    ignore_index=True,
                )

                # Lưu ngay vào file Excel
                save_data(st.session_state.customer_data)

                st.success(
                    "Đã lưu thông tin khách hàng thành công vào file Excel!"
                )

# ================= TAB 2: TRANG ADMIN =================
with tab_admin:
    st.header("Quản Lý Dữ Liệu Khách Hàng")

    # Kiểm tra mã PIN xác thực
    pin_input = st.text_input(
        "Nhập mã PIN để truy cập trang Admin:",
        type="password",
        max_chars=6,
        placeholder="******",
    )

    if pin_input == "123456":
        st.success("Xác thực thành công!")

        # Luôn tải lại dữ liệu mới nhất từ file
        df = load_data()

        if df.empty:
            st.info("Chưa có dữ liệu khách hàng nào được lưu.")
        else:
            # Hiển thị bảng dữ liệu
            st.dataframe(df, use_container_width=True)

            # Đọc file trực tiếp để hỗ trợ nút Tải xuống
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

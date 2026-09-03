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

# =========================================================
# 1. TIÊU ĐỀ & LOGO MSB CĂN GIỮA BÊN DƯỚI
# =========================================================
st.markdown(
    "<h1 style='text-align: center; color: #EB1C24;'>NGÂN HÀNG MSB</h1>",
    unsafe_allow_html=True,
)

# Chia cột để căn giữa Logo
col_left, col_center, col_right = st.columns([1, 1, 1])

with col_center:
    try:
        st.image(IMAGE_URL_MSB, use_container_width=True)
    except Exception:
        st.warning("Không thể tải logo từ liên kết.")

st.write("---")

# =========================================================
# 2. TẠO TABS CHỨC NĂNG
# =========================================================
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

                # Cập nhật dữ liệu
                st.session_state.customer_data = pd.concat(
                    [
                        st.session_state.customer_data,
                        pd.DataFrame([new_entry]),
                    ],
                    ignore_index=True,
                )

                # Lưu vào file Excel
                save_data(st.session_state.customer_data)

                st.success(
                    "Đã lưu thông tin khách hàng thành công vào file Excel!"
                )

# ================= TAB 2: TRANG ADMIN =================
with tab_admin:
    st.header("Quản Lý Dữ Liệu Khách Hàng")

    # Xác thực mã PIN
    pin_input = st.text_input(
        "Nhập mã PIN để truy cập trang Admin:",
        type="password",
        max_chars=6,
        placeholder="******",
    )

    if pin_input == "123456":
        st.success("Xác thực thành công!")

        # Tải lại dữ liệu mới nhất từ file
        df = load_data()

        if df.empty:
            st.info("Chưa có dữ liệu khách hàng nào được lưu.")
        else:
            # Hiển thị bảng
            st.dataframe(df, use_container_width=True)

            # Đọc file để xuất Excel
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

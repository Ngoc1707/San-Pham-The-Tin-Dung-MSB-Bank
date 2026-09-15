import io
import os
import pandas as pd
import streamlit as st

# Đường dẫn file Excel lưu trữ dữ liệu
EXCEL_FILE = "danh_sach_khach_hang_MSB.xlsx"

# Link logo MSB
IMAGE_URL_MSB = "https://haitrieu.com/wp-content/uploads/2022/02/Logo-MSB-Na.png"

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="MSB Lead Manager - Nhóm Ngọc Yên",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
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
                "Trạng thái",
            ]
        )


# Hàm lưu dữ liệu vào Excel
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")


# Khởi tạo dữ liệu trong Session State
if "customer_data" not in st.session_state:
    st.session_state.customer_data = load_data()

# =========================================================
# GIAO DIỆN THANH BÊN (SIDEBAR MENU) - GIỐNG MẪU
# =========================================================
with st.sidebar:
    # Logo & Ảnh thương hiệu
    try:
        st.image(IMAGE_URL_MSB, use_container_width=True)
    except Exception:
        st.write("### NGÂN HÀNG MSB")

    st.markdown(
        "<p style='text-align: center; font-weight: bold;'>Hệ thống Lead Management</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

    st.markdown("📂 **MENU QUẢN LÝ**")

    # Radio button tạo menu chuyên nghiệp
    menu_choice = st.radio(
        label="Chọn chức năng:",
        options=[
            "📌 Bảng điều khiển",
            "📋 Danh sách Leads",
            "➕ Thêm Lead mới",
            "🔄 Tiến độ xử lý",
            "📊 Báo cáo chỉ số",
        ],
        index=2,  # Mặc định chọn "Thêm Lead mới"
        label_visibility="collapsed",
    )

    st.write("---")
    st.caption("MSB Lead Manager - Nhóm Ngọc Yên v3.0")
    st.caption("Phát triển cho Khối KHCN MSB")

# =========================================================
# XỬ LÝ NỘI DUNG THEO MENU CHỌN
# =========================================================

# 1. BẢNG ĐIỀU KHIỂN
if menu_choice == "📌 Bảng điều khiển":
    st.title("📌 Bảng Điều Khiển Tổng Quan")
    df = st.session_state.customer_data

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số Leads", len(df))
    col2.metric("Thẻ tín dụng đã mở", len(df[df["Có thẻ tín dụng chưa"] == "Rồi"]))
    col3.metric("Khách hàng mới", len(df[df["Có thẻ tín dụng chưa"] == "Chưa"]))

    st.info("Hệ thống quản lý Lead tập trung khối KHCN Ngân hàng MSB.")

# 2. DANH SÁCH LEADS (YÊU CẦU MÃ PIN ADMIN)
elif menu_choice == "📋 Danh sách Leads":
    st.title("📋 Danh Sách Leads Khách Hàng")

    pin_input = st.text_input(
        "Nhập mã PIN Quản trị viên để xem dữ liệu:",
        type="password",
        max_chars=6,
    )

    if pin_input == "123456":
        st.success("Xác thực thành công!")
        df = load_data()

        if df.empty:
            st.info("Chưa có dữ liệu khách hàng nào được lưu.")
        else:
            st.dataframe(df, use_container_width=True)

            # Tải file Excel
            with open(EXCEL_FILE, "rb") as f:
                file_data = f.read()

            st.download_button(
                label="📥 Tải File Excel Khách Hàng",
                data=file_data,
                file_name="danh_sach_khach_hang_MSB.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    elif pin_input != "":
        st.error("Mã PIN không chính xác!")

# 3. THÊM LEAD MỚI (FORM ĐIỀN THÔNG TIN)
elif menu_choice == "➕ Thêm Lead mới":
    st.title("➕ Thêm Lead Khách Hàng Mới")

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
        submitted = st.form_submit_button("Lưu Lead Mới")

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
                    "Trạng thái": "Mới tiếp nhận",
                }

                st.session_state.customer_data = pd.concat(
                    [
                        st.session_state.customer_data,
                        pd.DataFrame([new_entry]),
                    ],
                    ignore_index=True,
                )

                save_data(st.session_state.customer_data)
                st.success("Đã lưu thông tin Lead thành công!")

# 4. TIẾN ĐỘ XỬ LÝ
elif menu_choice == "🔄 Tiến độ xử lý":
    st.title("🔄 Tiến Độ Xử Lý Leads")
    st.write("Cập nhật trạng thái chăm sóc khách hàng của cán bộ bán hàng.")
    df = load_data()
    if not df.empty:
        st.dataframe(df[["Tên khách hàng", "Số điện thoại", "Ghi chú"]], use_container_width=True)
    else:
        st.info("Chưa có dữ liệu để xử lý.")

# 5. BÁO CÁO CHỈ SỐ
elif menu_choice == "📊 Báo cáo chỉ số":
    st.title("📊 Báo Cáo & Thống Kê Chỉ Số")
    st.write("Báo cáo hiệu suất chuyển đổi Leads khối KHCN.")
    df = load_data()
    if not df.empty:
        st.bar_chart(df["Có thẻ tín dụng chưa"].value_counts())
    else:
        st.info("Chưa có dữ liệu báo cáo.")

import io
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="MSB - Quản Lý Khách Hàng", layout="wide")

# Khởi tạo dữ liệu lưu trữ tạm thời trong Session State
if "customer_data" not in st.session_state:
    st.session_state.customer_data = pd.DataFrame(
        columns=[
            "Số điện thoại",
            "Tên khách hàng",
            "Địa chỉ",
            "Thu nhập/tháng",
            "Có thẻ tín dụng chưa",
            "Ghi chú",
        ]
    )

# 1. Hiển thị Logo MSB ở trên cùng
# Lưu ý: Thay 'image_10b869.png' bằng đường dẫn thực tế đến file ảnh logo MSB
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
                # Thêm dữ liệu mới vào DataFrame
                st.session_state.customer_data = pd.concat(
                    [
                        st.session_state.customer_data,
                        pd.DataFrame([new_entry]),
                    ],
                    ignore_index=True,
                )
                st.success("Đã lưu thông tin khách hàng thành công!")

# ================= TAB 2: TRANG ADMIN =================
with tab_admin:
    st.header("Quản Lý Dữ Liệu Khách Hàng")

    df = st.session_state.customer_data

    if df.empty:
        st.info("Chưa có dữ liệu khách hàng nào được lưu.")
    else:
        # Hiển thị bảng dữ liệu
        st.dataframe(df, use_container_width=True)

        # Tạo file Excel để xuất
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="KhachHang")

        # Nút xuất Excel
        st.download_button(
            label="📥 Xuất File Excel",
            data=buffer.getvalue(),
            file_name="danh_sach_khach_hang_MSB.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

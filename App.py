import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Quản lý khách hàng - MSB",
    page_icon="👤",
    layout="wide"
)

# ==========================================
# KHỞI TẠO DANH SÁCH KHÁCH HÀNG
# ==========================================
if "customers" not in st.session_state:
    st.session_state.customers = []

# ==========================================
# HÀM XUẤT EXCEL
# ==========================================
def export_excel():
    df = pd.DataFrame(st.session_state.customers)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Khách hàng")
    return output.getvalue()

# ==========================================
# HIỂN THỊ LOGO MSB Ở PHÍA TRÊN
# ==========================================
# Hiển thị logo MSB ở phần đầu giao diện
st.image("image_06bc46.png", width=250)

# ==========================================
# MENU SIDEBAR
# ==========================================
st.sidebar.title("📋 MENU")
page = st.sidebar.radio(
    "Chọn trang",
    [
        "👤 Nhập khách hàng",
        "🔐 Admin"
    ]
)

# ==========================================
# TRANG NHẬP KHÁCH HÀNG
# ==========================================
if page == "👤 Nhập khách hàng":
    st.title("👤 THÔNG TIN KHÁCH HÀNG")
    st.write("Vui lòng nhập đầy đủ thông tin khách hàng bên dưới.")
    st.divider()

    # --------------------------------------
    # FORM NHẬP THÔNG TIN
    # --------------------------------------
    phone = st.text_input(
        "📱 Số điện thoại",
        placeholder="Nhập số điện thoại"
    )
    name = st.text_input(
        "👤 Tên khách hàng",
        placeholder="Nhập tên khách hàng"
    )
    address = st.text_input(
        "📍 Địa chỉ",
        placeholder="Nhập địa chỉ"
    )
    
    # Bổ sung 2 trường mới theo yêu cầu
    income = st.number_input(
        "💵 Thu nhập / tháng (VNĐ)",
        min_value=0,
        step=1000000,
        format="%d"
    )
    has_credit_card = st.radio(
        "💳 Đã có thẻ tín dụng chưa?",
        ["Chưa có", "Đã có"],
        horizontal=True
    )

    note = st.text_area(
        "📝 Ghi chú",
        placeholder="Nhập ghi chú"
    )
    st.divider()

    # --------------------------------------
    # NÚT LƯU THÔNG TIN
    # --------------------------------------
    if st.button("💾 LƯU THÔNG TIN", type="primary", use_container_width=True):
        if phone.strip() == "":
            st.error("❌ Vui lòng nhập số điện thoại.")
        elif name.strip() == "":
            st.error("❌ Vui lòng nhập tên khách hàng.")
        else:
            # Tạo bản ghi khách hàng mới bao gồm các trường bổ sung
            customer = {
                "Số điện thoại": phone.strip(),
                "Tên khách hàng": name.strip(),
                "Địa chỉ": address.strip(),
                "Thu nhập/tháng (VNĐ)": f"{income:,}",
                "Thẻ tín dụng": has_credit_card,
                "Ghi chú": note.strip()
            }
            # Lưu vào session_state
            st.session_state.customers.append(customer)
            st.success("✅ Đã lưu thông tin khách hàng thành công!")

# ==========================================
# TRANG ADMIN
# ==========================================
elif page == "🔐 Admin":
    st.title("🔐 ADMIN")
    st.divider()

    # --------------------------------------
    # ĐĂNG NHẬP ADMIN
    # --------------------------------------
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("🔑 Mật khẩu", type="password")
        if st.button("ĐĂNG NHẬP", type="primary"):
            if password == "123456":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Sai mật khẩu.")

    # --------------------------------------
    # GIAO DIỆN ADMIN KHI ĐÃ ĐĂNG NHẬP
    # --------------------------------------
    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader("📊 DANH SÁCH KHÁCH HÀNG")
        with col2:
            if st.button("🚪 Đăng xuất"):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        st.divider()

        # Kiểm tra danh sách
        if len(st.session_state.customers) == 0:
            st.info("📭 Chưa có dữ liệu khách hàng.")
        else:
            df = pd.DataFrame(st.session_state.customers)

            st.metric("👥 Tổng số khách hàng", len(df))
            st.divider()

            # Hiển thị bảng danh sách
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()

            # Xuất file Excel
            excel_file = export_excel()
            st.download_button(
                label="📥 XUẤT FILE EXCEL",
                data=excel_file,
                file_name="danh_sach_khach_hang_MSB.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

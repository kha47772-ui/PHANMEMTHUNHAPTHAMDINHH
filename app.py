
import streamlit as st

st.set_page_config(
    page_title="Thẩm định khả năng vay vốn",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 PHẦN MỀM THẨM ĐỊNH VAY VỐN")
st.write("Tính tỷ lệ DTI và đánh giá khả năng vay của khách hàng.")

st.divider()

st.subheader("1. Nhập thông tin khách hàng")

# Nhập dữ liệu
STV = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=1_000_000,
    value=800_000_000,
    step=10_000_000
)

THV = st.number_input(
    "Thời hạn vay (năm)",
    min_value=1,
    value=5,
    step=1
)

LS = st.number_input(
    "Lãi suất vay (%/năm)",
    min_value=0.0,
    value=12.0,
    step=0.5
)

TN = st.number_input(
    "Thu nhập hàng tháng (VNĐ)",
    min_value=0,
    value=45_000_000,
    step=1_000_000
)

NC = st.number_input(
    "Khoản nợ cũ phải trả hàng tháng (VNĐ)",
    min_value=0,
    value=10_000_000,
    step=500_000
)

CPSH = st.number_input(
    "Chi phí sinh hoạt mỗi người/tháng (VNĐ)",
    min_value=0,
    value=4_000_000,
    step=500_000
)

SN = st.number_input(
    "Số người trong gia đình",
    min_value=1,
    value=3,
    step=1
)

st.divider()

# Nút tính toán
if st.button("TÍNH DTI VÀ ĐÁNH GIÁ", type="primary",
              use_container_width=True):

    # Quy đổi lãi suất năm sang tháng
    lai_suat_thang = (LS / 100) / 12

    # Tiền trả gốc hàng tháng theo cách tính trong đề bài
    tien_goc_thang = STV / (THV * 12)

    # Tiền lãi hàng tháng theo cách tính trong đề bài
    tien_lai_thang = STV * lai_suat_thang

    # Tổng nghĩa vụ trả nợ hàng tháng
    tong_no_thang = tien_goc_thang + tien_lai_thang + NC

    # Thu nhập còn lại sau chi phí sinh hoạt
    thu_nhap_con_lai = TN - CPSH * SN

    st.subheader("2. Kết quả thẩm định")

    if thu_nhap_con_lai <= 0:
        st.error(
            "Không thể tính DTI hợp lệ vì thu nhập sau "
            "chi phí sinh hoạt phải lớn hơn 0."
        )
    else:
        # Tính chỉ số DTI
        DTI = tong_no_thang / thu_nhap_con_lai

        st.metric(
            label="Chỉ số DTI",
            value=f"{DTI * 100:.2f}%"
        )

        st.write(
            f"**Tiền gốc hàng tháng:** {tien_goc_thang:,.0f} VNĐ"
        )
        st.write(
            f"**Tiền lãi hàng tháng:** {tien_lai_thang:,.0f} VNĐ"
        )
        st.write(
            f"**Tổng nghĩa vụ nợ hàng tháng:** "
            f"{tong_no_thang:,.0f} VNĐ"
        )
        st.write(
            f"**Thu nhập sau chi phí sinh hoạt:** "
            f"{thu_nhap_con_lai:,.0f} VNĐ"
        )

        # Quy tắc kết luận theo yêu cầu
        if DTI < 0.70:
            st.error("❌ KẾT LUẬN: KHÔNG ĐƯỢC VAY")
            st.write("Lý do: DTI nhỏ hơn 70%.")
        else:
            st.success("✅ KẾT LUẬN: ĐƯỢC VAY")
            st.write("Lý do: DTI lớn hơn hoặc bằng 70%.")

st.divider()
st.caption(
    "Lưu ý: Kết quả được tính theo công thức và quy tắc "
    "phân loại do người dùng cung cấp."
)

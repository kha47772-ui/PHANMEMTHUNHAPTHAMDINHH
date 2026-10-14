
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Lập kế hoạch trả nợ",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 LẬP KẾ HOẠCH TRẢ NỢ VAY")
st.write("Tính tiền gốc, tiền lãi và số tiền phải trả mỗi kỳ.")

st.subheader("1. Thông tin khoản vay")

STV = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=1_000_000,
    value=700_000_000,
    step=10_000_000
)

THV = st.number_input(
    "Thời hạn vay (năm)",
    min_value=1,
    value=5,
    step=1
)

LS1 = st.number_input(
    "Lãi suất 3 tháng đầu (%/năm)",
    min_value=0.0,
    value=9.0,
    step=0.5
)

LSHD = st.number_input(
    "Lãi suất huy động từ tháng 4 (%/năm)",
    min_value=0.0,
    value=10.0,
    step=0.5
)

BD = st.number_input(
    "Biên độ lãi suất (%)",
    min_value=0.0,
    value=4.0,
    step=0.5
)

st.info(
    "Ngày giải ngân: 22/10/2023. "
    "Ngân hàng thu lãi ngày 15, tính lãi ngày 10."
)

st.subheader("2. Chọn phương pháp tính lãi")

cach_tinh = st.radio(
    "Quy ước tính lãi",
    [
        "Theo tháng (30 ngày/tháng)",
        "Theo số ngày thực tế/360"
    ]
)

if st.button("LẬP BẢNG TRẢ NỢ", type="primary",
              use_container_width=True):

    so_ky = int(THV * 12)
    goc_ky = STV / so_ky
    lai_suat_sau = (LSHD + BD) / 100

    du_no = STV
    bang = []

    # Ngày thu lãi đầu tiên sau ngày giải ngân
    ngay_truoc = pd.Timestamp("2023-10-22")

    for ky in range(1, min(5, so_ky) + 1):

        # Ngày thu lãi: ngày 15 hằng tháng
        ngay_thu = ngay_truoc + pd.DateOffset(months=1)
        ngay_thu = ngay_thu.replace(day=15)

        # Lãi suất áp dụng
        if ky <= 3:
            ls = LS1 / 100
        else:
            ls = lai_suat_sau

        if cach_tinh == "Theo tháng (30 ngày/tháng)":
            so_ngay = 30
            lai = du_no * ls / 12
        else:
            so_ngay = (ngay_thu - ngay_truoc).days
            lai = du_no * ls * so_ngay / 360

        goc_tra = min(goc_ky, du_no)
        tong_tra = goc_tra + lai
        du_no_cuoi = du_no - goc_tra

        bang.append({
            "Kỳ": ky,
            "Ngày thu": ngay_thu.strftime("%d/%m/%Y"),
            "Dư nợ đầu kỳ": round(du_no),
            "Lãi suất (%/năm)": round(ls * 100, 2),
            "Số ngày tính lãi": so_ngay,
            "Tiền gốc": round(goc_tra),
            "Tiền lãi": round(lai),
            "Tổng trả": round(tong_tra),
            "Dư nợ cuối kỳ": round(du_no_cuoi)
        })

        du_no = du_no_cuoi
        ngay_truoc = ngay_thu

    df = pd.DataFrame(bang)

    st.subheader("3. Bảng kế hoạch trả nợ 5 kỳ đầu")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("4. Tổng hợp kỳ thứ 1 đến kỳ thứ 5")
    st.metric("Tổng tiền gốc", f"{df['Tiền gốc'].sum():,.0f} VNĐ")
    st.metric("Tổng tiền lãi", f"{df['Tiền lãi'].sum():,.0f} VNĐ")
    st.metric("Tổng tiền phải trả", f"{df['Tổng trả'].sum():,.0f} VNĐ")

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "Tải bảng trả nợ Excel (CSV)",
        data=csv,
        file_name="bang_ke_hoach_tra_no.csv",
        mime="text/csv",
        use_container_width=True
    )

st.caption(
    "Lưu ý: Bảng minh họa 5 kỳ đầu. "
    "Cần đối chiếu quy ước ngày tính lãi với giảng viên."
)

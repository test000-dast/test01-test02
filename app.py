import streamlit as st
import pandas as pd
import altair as alt

# ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="Multi-File Dashboard", page_icon="📊", layout="wide")

# ✅ ตรวจสอบโหมด (Viewer/Editor) ด้วย query_params
query_params = st.query_params
mode = query_params.get("mode", ["edit"])[0]  # ค่าเริ่มต้นเป็น "edit"

# ✅ ซ่อน Sidebar เมื่อเป็น Viewer
if mode == "edit":
    st.sidebar.title("🔧 ตั้งค่ากราฟ")

# ✅ โหลดไฟล์ CSV ล่วงหน้า (สำหรับโหมด Viewer)
if mode == "view":
    uploaded_files = ["data1.csv", "data2.csv"]  # ใส่ไฟล์ที่ต้องการให้โชว์
else:
    uploaded_files = st.sidebar.file_uploader("📂 อัปโหลดไฟล์ CSV", type=["csv"], accept_multiple_files=True)

# ✅ แสดงกราฟ
if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file) if isinstance(file, str) else pd.read_csv(file)

        if df.empty:
            st.warning(f"⚠️ ไฟล์ **{file}** ไม่มีข้อมูล")
            continue

        columns = df.columns.tolist()

        # ✅ ซ่อนตัวเลือกคอลัมน์เมื่อเป็น Viewer
        if mode == "edit":
            x_axis = st.sidebar.selectbox(f"📌 เลือกแกน X ({file})", columns, key=f"x_{file}")
            y_axis = st.sidebar.selectbox(f"📌 เลือกแกน Y ({file})", columns, key=f"y_{file}")
            chart_title = st.sidebar.text_input(f"📝 ชื่อกราฟ ({file})", f"กราฟของ {file}")
            sort_order = st.sidebar.checkbox(f"🔽 เรียงจากมากไปน้อย ({file})", value=True, key=f"sort_{file}")
        else:
            # ใช้ค่าที่ตั้งไว้ (แก้ให้เป็นคอลัมน์ที่ต้องการ)
            x_axis, y_axis = "ชื่อสินค้า", "ยอดขาย"
            chart_title = f"กราฟของ {file}"
            sort_order = True

        # ✅ แสดงเฉพาะกราฟ
        if x_axis and y_axis and pd.api.types.is_numeric_dtype(df[y_axis]):
            if sort_order:
                df = df.sort_values(by=y_axis, ascending=False)

            x_type = 'ordinal' if df[x_axis].dtype == object else 'quantitative'

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type='quantitative')
            ).properties(title=chart_title, width=1000, height=500)

            text = alt.Chart(df).mark_text(
                align='center', baseline='bottom', dy=-5, fontSize=12, color='black'
            ).encode(
                x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type='quantitative'),
                text=y_axis
            )

            st.altair_chart(chart + text, use_container_width=True)



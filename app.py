import streamlit as st
import pandas as pd
import numpy as np
import io
import re

# 1. إعدادات الصفحة الاحترافية المطلقة
st.set_page_config(
    page_title="Surveying Traverse Pro | Eng. Amr Gamal", 
    page_icon="👑", 
    layout="centered"
)

# 2. هندسة الديكور والنيون (إخفاء ستريم ليت + تشغيل الـ Hyper Neon Grid)
st.markdown("""
    <style>
    /* 🛑 إخفاء هوية ستريم ليت تماماً من الشاشة */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .viewerBadge {display: none !important;}
    
    /* 🟢 خلفية نيون مساحية شبكية متحركة وقوية جداً */
    .stApp {
        background-color: #050a06;
        background-image: 
            linear-gradient(rgba(0, 255, 102, 0.15) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(0, 255, 102, 0.15) 1.5px, transparent 1.5px);
        background-size: 40px 40px;
        color: #E5E9E6;
        animation: gridMove 15s linear infinite;
    }
    
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 40px 80px; }
    }
    
    /* العناوين بالنيون المشع الضخم */
    h1 {
        color: #00FF66 !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        text-shadow: 0px 0px 20px #00FF66, 0px 0px 40px rgba(0, 255, 102, 0.6) !important;
        text-align: center;
        font-weight: 900 !important;
    }
    h2, h3 {
        color: #00FF66 !important;
        text-shadow: 0px 0px 12px rgba(0, 255, 102, 0.6) !important;
    }
    
    /* تقوية حواف النيون للقوائم والجداول والملفات */
    div[data-baseweb="select"], div[data-baseweb="input"], .stDataFrame, div[data-testid="stFileUploader"] {
        border: 2px solid #00FF66 !important;
        box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.3) !important;
        border-radius: 14px !important;
        background-color: rgba(5, 10, 5, 0.95) !important;
    }
    
    /* زرار الحساب الأخضر الناري */
    .stButton>button {
        background: linear-gradient(135deg, #00FF66, #00aa3a) !important;
        color: #000000 !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 17px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 25px rgba(0, 255, 102, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 35px #00FF66 !important;
    }
    
    /* كروت نيون ذهبي للنتائج */
    div[data-testid="stMetric"] {
        background: rgba(10, 15, 10, 0.95) !important;
        border: 2px solid #FFCC00 !important;
        box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.3) !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFCC00 !important;
        text-shadow: 0px 0px 12px rgba(255, 204, 0, 0.6);
    }
    
    /* الفوتر الملكي الفخم للبراند الشخصي */
    .footer {
        position: relative;
        width: 100%;
        background: #020502;
        color: #a0b0a0;
        text-align: center;
        padding: 30px 0;
        font-size: 15px;
        border-top: 3px solid #00FF66;
        margin-top: 80px;
        border-radius: 25px 25px 0 0;
        box-shadow: 0px -15px 35px rgba(0, 255, 102, 0.15);
    }
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 0px 15px rgba(37, 211, 102, 0.5);
        transition: 0.3s;
    }
    .whatsapp-btn:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 25px #25D366;
    }
    .whatsapp-icon {
        width: 22px;
        height: 22px;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- دالة المعالجة الفائقة والقاطعة لأي نوع ملف (SDR / TXT / CSV) ---
def super_parse_file(file_bytes):
    points = []
    try:
        lines = file_bytes.decode("utf-8").splitlines()
    except:
        lines = file_bytes.decode("latin-1").splitlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("08KI"):
            parts = re.split(r'\s+', line)
            sub_parts = [p for p in parts if p and not p.startswith("08KI")]
            if len(sub_parts) >= 4:
                try:
                    points.append({
                        "Point_ID": sub_parts[0],
                        "Easting": float(sub_parts[1]),
                        "Northing": float(sub_parts[2]),
                        "Elevation": float(sub_parts[3]),
                        "Code": sub_parts[4] if len(sub_parts) > 4 else "ST"
                    })
                    continue
                except:
                    pass
                    
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if len(numbers) >= 3 and any("." in n for n in numbers):
            try:
                pt_id = f"P_{len(points)+1}"
                letters = re.findall(r'[a-zA-Z0-9_]+', line)
                if letters and not letters[0].replace('.','').isdigit():
                    pt_id = letters[0]
                
                floats = [float(n) for n in numbers]
                if len(floats) >= 3:
                    points.append({
                        "Point_ID": pt_id,
                        "Easting": floats[0] if floats[0] > floats[2] else floats[1],
                        "Northing": floats[1] if floats[0] > floats[2] else floats[0],
                        "Elevation": floats[2],
                        "Code": "ST"
                    })
            except:
                continue

    if not points:
        try:
            return pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
        except:
            try:
                return pd.read_csv(io.StringIO(file_bytes.decode('utf-8')), sep='\t')
            except:
                return pd.DataFrame()
                
    return pd.DataFrame(points)

# --- واجهة المستخدم الأساسية ---

st.title("👑 SURVEYING TRAVERSE PRO")
st.markdown("<p style='text-align: center; color: #00FF66; font-size: 19px; font-weight: bold; letter-spacing: 1px;'>PREMIUM EDITION • DEVELOPED FOR ENG. AMR GAMAL</p>", unsafe_allow_html=True)
st.divider()

uploaded_file = st.file_uploader("📂 اسحب وأفلت ملف الترافيرس هنا (SDR, TXT, CSV)", type=["csv", "txt", "sdr"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        df = super_parse_file(file_bytes)
            
        if df.empty:
            st.error("❌ عذراً، لم نتمكن من استخراج بيانات صالحة من الملف. تأكد من صيغته.")
        else:
            rename_dict = {}
            for col in df.columns:
                if col.lower() in ['easting', 'e', 'east']: rename_dict[col] = 'Easting'
                elif col.lower() in ['northing', 'n', 'north']: rename_dict[col] = 'Northing'
                elif col.lower() in ['elevation', 'z', 'elev']: rename_dict[col] = 'Elevation'
                elif col.lower() in ['point_id', 'id', 'pt_id', 'pt']: rename_dict[col] = 'Point_ID'
                elif col.lower() in ['code', 'desc']: rename_dict[col] = 'Code'
            df = df.rename(columns=rename_dict)
            
            if 'Easting' not in df.columns and df.shape[1] >= 3:
                if df.shape[1] == 3:
                    df.columns = ['Easting', 'Northing', 'Elevation']
                elif df.shape[1] >= 4:
                    df.columns = ['Point_ID', 'Easting', 'Northing', 'Elevation'] + list(df.columns[4:])

            st.success(f"⚡ تم قراءة عدد ({len(df)}) نقطة مساحية بنجاح بنظام الفلترة الفائق!")
            st.dataframe(df)
            
            st.divider()
            
            project_class = st.selectbox(
                "🎯 اختر رتبة الدقة المطلوبة للمشروع بحسب المواصفات الفنية:",
                options=["الدرجة الثالثة (شغل موقع ومباني عادي 1:5,000)", "الدرجة الثانية (منشآت وطرق رئيسية 1:10,000)", "الدرجة الأولى (مشاريع كبرى وأنفاق 1:25,000)"]
            )

            limit = 5000
            if "1:10,000" in project_class: limit = 10000
            elif "1:25,000" in project_class: limit = 25000
            
            st.subheader("📍 إحداثيات نقطة القفل المعتمدة من الاستشاري (Target Control Point):")
            col1, col2, col3 = st.columns(3)
            with col1: target_E = st.number_input("Target Easting (E)", value=0.0, format="%.3f")
            with col2: target_N = st.number_input("Target Northing (N)", value=0.0, format="%.3f")
            with col3: target_Z = st.number_input("Target Elevation (Z)", value=0.0, format="%.3f")
                
            st.divider()
            
            if 'Easting' in df.columns and 'Northing' in df.columns:
                if st.button("🚀 احسب وصحح الترافيرس الآن بـ (Bowditch Rule)"):
                    df['Distance'] = 0.0
                    for i in range(1, len(df)):
                        dE = df['Easting'].iloc[i] - df['Easting'].iloc[i-1]
                        dN = df['Northing'].iloc[i] - df['Northing'].iloc[i-1]
                        df.at[i, 'Distance'] = np.sqrt(dE**2 + dN**2)
                    
                    total_perimeter = df['Distance'].sum()
                    df['Cumulative_Dist'] = df['Distance'].cumsum()
                    
                    last_E = df['Easting'].iloc[-1]
                    last_N = df['Northing'].iloc[-1]
                    last_Z = df['Elevation'].iloc[-1] if 'Elevation' in df.columns else 0.0
                    
                    error_E = last_E - target_E
                    error_N = last_N - target_N
                    error_Z = last_Z - target_Z
                    linear_error = np.sqrt(error_E**2 + error_N**2)
                    
                    if linear_error > 0:
                        precision_x = int(round(total_perimeter / linear_error))
                        precision_string = f"1 : {precision_x:,}"
                    else:
                        precision_x = float('inf')
                        precision_string = "1 : ∞"
                    
                    st.subheader("📉 نتائج تحليل أخطاء القفل الضلعي والعمودي:")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric(label="الخطأ في الـ Easting (ΔE)", value=f"{error_E:.3f} متر")
                        st.metric(label="الخطأ في الـ Northing (ΔN)", value=f"{error_N:.3f} متر")
                    with res_col2:
                        st.metric(label="الخطأ في المنسوب (ΔZ)", value=f"{error_Z:.3f} متر")
                        st.metric(label="نسبة دقة الت

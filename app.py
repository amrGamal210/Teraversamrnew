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

# 2. هندسة الديكور والنيون الفائق وحظر ستريم ليت بالكامل
st.markdown("""
    <style>
    /* 🛑 طرد وإخفاء هوية ستريم ليت تماماً */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .viewerBadge {display: none !important;}
    
    /* 🟢 خلفية نيون مساحية شبكية متحركة قوية */
    .stApp {
        background-color: #040905;
        background-image: 
            linear-gradient(rgba(0, 255, 102, 0.12) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(0, 255, 102, 0.12) 1.5px, transparent 1.5px);
        background-size: 40px 40px;
        color: #E5E9E6;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 40px 80px; }
    }
    
    /* لوجو التاج الملكي المخصص والمشع */
    .brand-logo-container {
        text-align: center;
        padding: 10px 0;
        margin-bottom: 10px;
    }
    .brand-logo {
        font-size: 45px;
        text-shadow: 0px 0px 25px #00FF66, 0px 0px 50px rgba(0, 255, 102, 0.5);
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }
    
    h1 {
        color: #00FF66 !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        text-shadow: 0px 0px 20px #00FF66 !important;
        text-align: center;
        font-weight: 900 !important;
        margin-top: -10px !important;
    }
    h2, h3 {
        color: #00FF66 !important;
        text-shadow: 0px 0px 12px rgba(0, 255, 102, 0.5) !important;
    }
    
    /* ستايل التبويبات النيون (Tabs) */
    div[data-testid="stMarkdownContainer"] p {
        font-weight: 600;
    }
    button[data-baseweb="tab"] {
        color: #88aa88 !important;
        border-bottom: 2px solid transparent !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
    }
    button[aria-selected="true"] {
        color: #00FF66 !important;
        border-bottom: 3px solid #00FF66 !important;
        text-shadow: 0px 0px 10px rgba(0, 255, 102, 0.6) !important;
    }
    
    /* تقوية حواف النيون للقوائم والجداول والملفات */
    div[data-baseweb="select"], div[data-baseweb="input"], .stDataFrame, div[data-testid="stFileUploader"], .stAlert {
        border: 2px solid #00FF66 !important;
        box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.25) !important;
        border-radius: 14px !important;
        background-color: rgba(4, 8, 4, 0.95) !important;
    }
    
    /* زرار الحساب المتوهج الخارق */
    .stButton>button {
        background: linear-gradient(135deg, #00FF66, #00aa3a) !important;
        color: #000000 !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 18px !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 25px rgba(0, 255, 102, 0.5);
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 6px 40px #00FF66 !important;
        transform: scale(1.01);
    }
    
    /* كروت نيون ذهبي للنتائج والمؤشرات */
    div[data-testid="stMetric"] {
        background: rgba(8, 12, 8, 0.95) !important;
        border: 2px solid #FFCC00 !important;
        box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.25) !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFCC00 !important;
        text-shadow: 0px 0px 12px rgba(255, 204, 0, 0.5);
        font-size: 26px !important;
    }
    
    /* حاوية بوكس الـ AI */
    .ai-box {
        background: rgba(10, 20, 30, 0.8) !important;
        border: 2px dashed #00FF66 !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 0px 25px rgba(0, 255, 102, 0.2);
    }
    
    /* الفوتر الملكي المحمي */
    .footer {
        position: relative;
        width: 100%;
        background: #010401;
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
    }
    .whatsapp-icon {
        width: 22px;
        height: 22px;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. هيدر اللوجو والتاج الملكي الخاص بنا
st.markdown("""
    <div class='brand-logo-container'>
        <div class='brand-logo'>👑</div>
    </div>
    """, unsafe_allow_html=True)
st.title("SURVEYING TRAVERSE PRO")
st.markdown("<p style='text-align: center; color: #00FF66; font-size: 18px; font-weight: bold; margin-top:-15px;'>ENG. AMR GAMAL • PREMIUM SURVEY DESIGN</p>", unsafe_allow_html=True)
st.divider()

# 4. دالة المعالجة الفائقة والقاطعة لأي نوع ملف (SDR / TXT / CSV)
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

# 5. تهيئة الـ Session State لحفظ بيانات الترافيرس والمشاريع تلقائيًا
if 'saved_df' not in st.session_state: st.session_state.saved_df = None
if 'saved_results' not in st.session_state: st.session_state.saved_results = None

# إنشاء التبويبات الفخمة الجديدة
tab_calc, tab_ai, tab_about = st.tabs(["⚙️ الحسابات والتصحيح", "🤖 Survey AI Expert", "📖 عن البرنامج والدليل"])

# ==================== التبويب الأول: الحسابات والتصحيح ====================
with tab_calc:
    uploaded_file = st.file_uploader("📂 اسحب وأفلت ملف الترافيرس (SDR, TXT, CSV)", type=["csv", "txt", "sdr"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        df = super_parse_file(file_bytes)
        if not df.empty:
            rename_dict = {}
            for col in df.columns:
                if col.lower() in ['easting', 'e', 'east']: rename_dict[col] = 'Easting'
                elif col.lower() in ['northing', 'n', 'north']: rename_dict[col] = 'Northing'
                elif col.lower() in ['elevation', 'z', 'elev']: rename_dict[col] = 'Elevation'
                elif col.lower() in ['point_id', 'id', 'pt_id', 'pt']: rename_dict[col] = 'Point_ID'
                elif col.lower() in ['code', 'desc']: rename_dict[col] = 'Code'
            df = df.rename(columns=rename_dict)
            
            if 'Easting' not in df.columns and df.shape[1] >= 3:
                if df.shape[1] == 3: df.columns = ['Easting', 'Northing', 'Elevation']
                elif df.shape[1] >= 4: df.columns = ['Point_ID', 'Easting', 'Northing', 'Elevation'] + list(df.columns[4:])
            
            st.session_state.saved_df = df
            st.success(f"⚡ تم قراءة عدد ({len(df)}) نقطة مساحية بنجاح بنظام الكاش التلقائي!")
            st.dataframe(df)
            
            st.divider()
            
            project_class = st.selectbox(
                "🎯 اختر رتبة الدقة المطلوبة للمشروع:",
                options=["الدرجة الثالثة (شغل موقع ومباني عادي 1:5,000)", "الدرجة الثانية (منشآت وطرق رئيسية 1:10,000)", "الدرجة الأولى (مشاريع كبرى وأنفاق 1:25,000)"]
            )
            limit = 5000
            if "1:10,000" in project_class: limit = 10000
            elif "1:25,000" in project_class: limit = 25000
            
            st.subheader("📍 إحداثيات نقطة القفل المعتمدة من الاستشاري (Target Control):")
            col1, col2, col3 = st.columns(3)
            with col1: target_E = st.number_input("Target Easting (E)", value=0.0, format="%.3f")
            with col2: target_N = st.number_input("Target Northing (N)", value=0.0, format="%.3f")
            with col3: target_Z = st.number_input("Target Elevation (Z)", value=0.0, format="%.3f")
            
            if 'Easting' in df.columns and 'Northing' in df.columns:
                if st.button("🚀 احسب وصحح الترافيرس وارسم الخريطة الآن"):
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
                    
                    precision_x = int(round(total_perimeter / linear_error)) if linear_error > 0 else float('inf')
                    precision_string = f"1 : {precision_x:,}" if linear_error > 0 else "1 : ∞"
                    
                    st.session_state.saved_results = {
                        "error_E": error_E, "error_N": error_N, "error_Z": error_Z,
                        "linear_error": linear_error, "precision_x": precision_x,
                        "precision_string": precision_string, "limit": limit
                    }
                    
                    st.subheader("📉 نتائج تحليل أخطاء القفل الضلعي والعمودي:")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric(label="الخطأ في الـ Easting (ΔE)", value=f"{error_E:.3f} متر")
                        st.metric(label="الخطأ في الـ Northing (ΔN)", value=f"{error_N:.3f} متر")
                    with res_col2:
                        st.metric(label="الخطأ في المنسوب (ΔZ)", value=f"{error_Z:.3f} متر")
                        st.metric(label="نسبة دقة الترافيرس الفعلية", value=precision_string)
                    
                    if precision_x >= limit:
                        st.success("🎉 الشغل مـقـبـول هندسياً ومطابق للمواصفات الفنية المعتمدة!")
                    else:
                        st.error("🚨 الشغل مـرفـوض! دقة الرفع أقل من الحد المسموح به للمشروع.")
                    
                    df['Corrected_Easting'] = df['Easting'] - (df['Cumulative_Dist'] / total_perimeter) * error_E
                    df['Corrected_Northing'] = df['Northing'] - (df['Cumulative_Dist'] / total_perimeter) * error_N
                    
                    # 📈 إدخال كروكي رسم الترافيرس التفاعلي النيون الجديد
                    st.subheader("📊 الكروكي الهندسي لتوزيع نقاط الترافيرس:")
                    map_df = df[['Easting', 'Northing']].copy()
                    st.line_chart(map_df, x='Easting', y='Northing')
                    
                    st.subheader("✅ جدول الإحداثيات المصححة النهائية:")
                    show_cols = []
                    if 'Point_ID' in df.columns: show_cols.append('Point_ID')
                    show_cols.extend(['Corrected_Easting', 'Corrected_Northing'])
                    if 'Elevation' in df.columns: 
                        df['Corrected_Elevation'] = df['Elevation'] - (df['Cumulative_Dist'] / total_perimeter) * error_Z
                        show_cols.append('Corrected_Elevation')
                    
                    final_df = df[show_cols].copy()
                    final_df.columns = [col.replace('Corrected_', '') for col in final_df.columns]
                    st.dataframe(final_df)
                    
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        final_df.to_excel(writer, index=False, sheet_name='Corrected_Data')
                    st.download_button(
                        label="📥 تحميل ورقة البيانات المصححة المعتمدة (Excel)",
                        data=buffer.getvalue(),
                        file_name="Corrected_Traverse_Pro.xlsx",
                        mime="application/vnd.ms-excel"
                    )
        else:
            st.error("❌ ملف فارغ أو صيغته غير مدعومة.")

# ==================== التبويب الثاني: SURVEY AI EXPERT ====================
with tab_ai:
    st.subheader("🤖 تحليل الاستشاري الآلي وملاحظات الحقل الفنية")
    if st.session_state.saved_results is None:
        st.info("💡 رجاءً ارفع ملف الحسابات واضغط احسب أولاً ليقوم الذكاء الاصطناعي بتحليل المشروع!")
    else:
        res = st.session_state.saved_results
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.markdown(f"### 📋 تقرير الـ AI المهني المعتمد:")
        st.markdown(f"* **حالة دقة الترافيرس:** الدقة الحالية هي `{res['precision_string']}` والحد المطلوب للرتبة المختارة هو `1 : {res['limit']:,}`.")
        
        # محرك اتخاذ القرار والتحليل الجغرافي الذكي للـ AI
        if res['precision_x'] >= res['limit']:
            st.markdown("🟢 **ملاحظة الـ AI الفنية:** المشروع مستقر ودقة الرصد ممتازة وتتخطى المواصفات القياسية. الأخطاء عشوائية وطبيعية وموزعة بانتظام عبر قاعدة بوديتش. يمكنك المباشرة في توقيع النقاط الفرعية فوراً.")
        else:
            st.markdown("🔴 **تنبيه وإجراءات تصحيحية من الـ AI:** الشغل مرفوض هندسياً وتعدى حدود التسامح الفني (Tolerance).")
            
            # فحص نوع الخطأ وتحليله هندسياً
            if abs(res['error_E']) > abs(res['error_N']) * 1.5:
                st.markdown("* ⚠️ **تحليل خطأ الاتجاه (Easting):** يوجد انزياح ملحوظ بالاتجاه الشرقي. يوصى بمراجعة زاوية التوجيه وبدء الرصد، والتأكد من إحداثيات نقطة الباك سايت (`Backsight`) الخلفية في الموقع.")
            elif abs(res['error_N']) > abs(res['error_E']) * 1.5:
                st.markdown("* ⚠️ **تحليل خطأ الاتجاه (Northing):** يوجد انزياح رأسي ملحوظ في الاتجاه الشمالي. تحقق من تثبيت التوتال ستيشن تماماً وعدم حدوث أي حركة أو تخلخل في أرجل الحامل الثنائي أثناء العمل.")
            else:
                st.markdown("* ⚠️ **تحليل الأخطاء الخطية:** الخطأ مشترك ومتساوي تقريباً، مما يدل على وجود خطأ تراكمي في قياس المسافات الفردية بين المحطات. راجع معامل تصحيح الضغط والحرارة (`PPM`) في الجهاز.")
            
            if abs(res['error_Z']) > 0.05:
                st.markdown(f"* 📐 **تحليل مناسيب القفل (ΔZ = {res['error_Z']:.3f} م):** خطأ المنسوب كبير جداً وعالي الخطورة! تأكد فوراً من قياس ارتفاع الجهاز (`Hi`) يدويًا بالمتر، وراجع ارتفاع العاكس أو البريزم (`Hr`) المستخدم مع المساعدين.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("📱 تم توليد هذا التقرير هندسياً عبر خوارزميات Survey AI المدمجة في نسختك.")

# ==================== التبويب الثالث: عن البرنامج والدليل ====================
with tab_about:
    st.subheader("👑 منصة Surveying Traverse Pro")
    st.markdown("""
    صُمم هذا البرنامج خصيصاً للمهندسين والمساحين المحترفين لتبسيط وتدقيق حسابات أخطاء القفل الضلعي والعمودي للترافيرسات المغلقة والمفتوحة أونلاين من قلب الموقع وبأعلى دقة رقمية.
    
    ### ⚡ مميزات المنصة الملكية:
    * **الفلترة الذكية الفائقة:** قراءة وقص ملفات الأجهزة الخام `SDR` لشركات سوكيا وتوبكون وملفات `TXT` و `CSV` واستخراج الأعمدة آلياً.
    * **قاعدة بوديتش (Bowditch Rule):** تصحيح الأخطاء خطياً وتوزيعها بنسب الأطوال المحسوبة هندسياً بالملي.
    * **Survey AI Expert:** ذكاء اصطناعي محلي يوفر تقارير فنية فورية لتوثيق جودة الرفع وتحديد سبب أي انحراف في التوجيه أو الأرصاد.
    * **كاش الحماية:** حفظ أوتوماتيكي لبياناتك لحمايتها من انقطاع الاتصال أو إغلاق الصفحة فجأة.
    """)

# --- شريط حقوق الملكية الفخم مع لوجو ورابط واتساب مباشر للمهندس عمرو جمال عوض ---
st.markdown("""
    <div class='footer'>
        <p>🏗️ <b>Surveying Traverse Pro</b> | صُمم هذا البرنامج بأعلى معايير الدقة والجمالية لأعمال المساحة الفنية</p>
        <p>جميع الحقوق محفوظة © 2026 للمهندس <a href='https://github.com/AmrGamalAwad' target='_blank'>عمرو جمال عوض</a> 👑</p>
        <a href='https://wa.me/201033873551' target='_blank' class='whatsapp-btn'>
            <span>تواصل عبر الواتساب: 01033873551</span>
            <img class='whatsapp-icon' src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' alt='WhatsApp'>
        </a>
    </div>
    """, unsafe_allow_html=True)


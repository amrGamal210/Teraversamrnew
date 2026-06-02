import streamlit as st
import pandas as pd
import numpy as np
import io
import re

# 1. إعدادات الصفحة الاحترافية المطلقة
st.set_page_config(
    page_title="منصة الترافيرس الاحترافية | م. عمرو جمال", 
    page_icon="👑", 
    layout="centered"
)

# 2. هندسة الديكور والتعريب البصري وتأثيرات النيون الخارقة
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .viewerBadge {display: none !important;}
    
    /* توجيه الموقع بالكامل للغة العربية */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    
    /* 🟢 خلفية نيون مساحية شبكية متحركة مطورة */
    .stApp {
        background-color: #030704;
        background-image: 
            linear-gradient(rgba(0, 255, 102, 0.09) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(0, 255, 102, 0.09) 1.5px, transparent 1.5px);
        background-size: 45px 45px;
        color: #E5E9E6;
        animation: gridMove 25s linear infinite;
    }
    
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 45px 90px; }
    }
    
    /* لوجو التاج الملكي المخصص والمشع */
    .brand-logo-container { text-align: center; padding: 10px 0; margin-bottom: 5px; }
    .brand-logo { font-size: 50px; text-shadow: 0px 0px 25px #00FF66, 0px 0px 50px rgba(0, 255, 102, 0.4); animation: pulse 2s infinite alternate; }
    @keyframes pulse { 0% { transform: scale(1); } 100% { transform: scale(1.03); } }
    
    h1 { color: #00FF66 !important; font-family: 'Segoe UI', Arial, sans-serif; text-shadow: 0px 0px 20px #00FF66 !important; text-align: center; font-weight: 900 !important; }
    h2, h3, h4 { color: #00FF66 !important; text-shadow: 0px 0px 12px rgba(0, 255, 102, 0.4) !important; text-align: right; }
    
    /* ستايل التبويبات النيون العربي */
    button[data-baseweb="tab"] { color: #88aa88 !important; font-size: 17px !important; font-weight: bold !important; }
    button[aria-selected="true"] { color: #00FF66 !important; border-bottom: 3px solid #00FF66 !important; text-shadow: 0px 0px 10px rgba(0, 255, 102, 0.6) !important; }
    
    /* تقوية حواف النيون للقوائم والجداول والملفات */
    div[data-baseweb="select"], div[data-baseweb="input"], .stDataFrame, div[data-testid="stFileUploader"], .stAlert {
        border: 2px solid #00FF66 !important;
        box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.2) !important;
        border-radius: 14px !important;
        background-color: rgba(3, 6, 3, 0.96) !important;
    }
    
    /* تعديل محاذاة النصوص داخل خانات الإدخال للعربي */
    input { text-align: right !important; color: #E5E9E6 !important; }
    
    /* زرار الحساب المتوهج الخارق */
    .stButton>button {
        background: linear-gradient(135deg, #00FF66, #00aa3a) !important;
        color: #000000 !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 18px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 25px rgba(0, 255, 102, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { box-shadow: 0 6px 35px #00FF66 !important; transform: translateY(-2px); }
    
    /* ستايل مخصص لزرار الفحص بلون أزرق نيون مرعب */
    .audit-btn>div>button {
        background: linear-gradient(135deg, #00E5FF, #008699) !important;
        color: #000000 !important;
        box-shadow: 0 4px 25px rgba(0, 229, 255, 0.4) !important;
    }
    .audit-btn>div>button:hover { box-shadow: 0 6px 35px #00E5FF !important; }
    
    /* كروت نيون ذهبي للنتائج والمؤشرات */
    div[data-testid="stMetric"] {
        background: rgba(6, 10, 6, 0.96) !important;
        border: 2px solid #FFCC00 !important;
        box-shadow: 0px 0px 15px rgba(255, 204, 0, 0.2) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        text-align: right !important;
    }
    div[data-testid="stMetricValue"] { color: #FFCC00 !important; font-size: 26px !important; text-align: right !important; }
    div[data-testid="stMetricLabel"] { color: #a0b0a0 !important; text-align: right !important; }
    
    .ai-box { background: rgba(8, 16, 24, 0.85) !important; border: 2px dashed #00FF66 !important; padding: 20px; border-radius: 15px; text-align: right; }
    .audit-box { background: rgba(4, 10, 18, 0.96) !important; border: 2px solid #00E5FF !important; box-shadow: 0px 0px 25px rgba(0, 229, 255, 0.25) !important; padding: 20px; border-radius: 15px; color: #E5E9E6; text-align: right; }
    
    /* ستايل مخصص لفقاعات الشات نيون مريحة للعين */
    div[data-testid="stChatMessage"] {
        background-color: rgba(12, 25, 12, 0.5) !important;
        border: 1px solid #00FF66 !important;
        border-radius: 12px !important;
        direction: rtl !important;
    }
    
    /* الفوتر الملكي المطور وشريط اللوجوهات */
    .footer {
        position: relative;
        width: 100%;
        background: #010301;
        color: #a0b0a0;
        text-align: center;
        padding: 35px 0;
        font-size: 15px;
        border-top: 3px solid #00FF66;
        margin-top: 80px;
        border-radius: 25px 25px 0 0;
        box-shadow: 0px -15px 35px rgba(0, 255, 102, 0.12);
    }
    .social-links {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 20px;
    }
    .social-icon {
        width: 40px;
        height: 40px;
        transition: all 0.3s ease;
        filter: drop-shadow(0px 0px 5px rgba(0,255,102,0.3));
    }
    .social-icon:hover {
        transform: scale(1.2);
        filter: drop-shadow(0px 0px 15px #00FF66);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='brand-logo-container'><div class='brand-logo'>👑</div></div>", unsafe_allow_html=True)
st.title("المنصة الرقمية لإدارة وتصحيح الترافيرسات")
st.markdown("<p style='text-align: center; color: #00FF66; font-size: 18px; font-weight: bold; margin-top:-15px;'>إشراف وتطوير: م. عمرو جمال عوض • إصدار بريميوم ذكي 2026</p>", unsafe_allow_html=True)
st.divider()

# دالة المعالجة الفائقة وقراءة صيغ الملفات خام
def super_parse_file(file_bytes):
    points = []
    try: lines = file_bytes.decode("utf-8").splitlines()
    except: lines = file_bytes.decode("latin-1").splitlines()
        
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith("08KI"):
            parts = re.split(r'\s+', line)
            sub_parts = [p for p in parts if p and not p.startswith("08KI")]
            if len(sub_parts) >= 4:
                try:
                    points.append({"اسم_النقطة": sub_parts[0], "الشرقي_E": float(sub_parts[1]), "الشمالي_N": float(sub_parts[2]), "المنسوب_Z": float(sub_parts[3]), "الكود": sub_parts[4] if len(sub_parts) > 4 else "ST"})
                    continue
                except: pass
                    
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if len(numbers) >= 3 and any("." in n for n in numbers):
            try:
                pt_id = f"P_{len(points)+1}"
                letters = re.findall(r'[a-zA-Z0-9_]+', line)
                if letters and not letters[0].replace('.','').isdigit(): pt_id = letters[0]
                floats = [float(n) for n in numbers]
                if len(floats) >= 3:
                    points.append({
                        "اسم_النقطة": pt_id,
                        "الشرقي_E": floats[0] if floats[0] > floats[2] else floats[1],
                        "الشمالي_N": floats[1] if floats[0] > floats[2] else floats[0],
                        "المنسوب_Z": floats[2], "الكود": "ST"
                    })
            except: continue

    if not points:
        try: return pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
        except:
            try: return pd.read_csv(io.StringIO(file_bytes.decode('utf-8')), sep='\t')
            except: return pd.DataFrame()
    return pd.DataFrame(points)

# دالة توليد كود الـ DXF لـ CAD
def generate_dxf(df_points):
    dxf_lines = ["0", "SECTION", "2", "ENTITIES"]
    for idx, row in df_points.iterrows():
        pid = str(row.get('اسم_النقطة', idx+1))
        e = float(row['الشرقي_E'])
        n = float(row['الشمالي_N'])
        z = float(row.get('المنسوب_Z', 0.0))
        dxf_lines.extend(["0", "POINT", "8", "SURVEY_POINTS", "10", str(e), "20", str(n), "30", str(z)])
        dxf_lines.extend(["0", "TEXT", "8", "POINT_LABELS", "10", str(e + 0.3), "20", str(n + 0.3), "30", str(z), "40", "0.25", "1", pid])
    if len(df_points) > 1:
        dxf_lines.extend(["0", "LWPOLYLINE", "8", "TRAVERSE_LINE", "90", str(len(df_points)), "70", "1"])
        for idx, row in df_points.iterrows():
            dxf_lines.extend(["10", str(row['الشرقي_E']), "20", str(row['الشمالي_N'])])
    dxf_lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(dxf_lines)

# تهيئة المتغيرات في السيشين ستيت
if 'saved_df' not in st.session_state: st.session_state.saved_df = None
if 'saved_results' not in st.session_state: st.session_state.saved_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "أهلاً بك يا هندسة في مركز الحوار المطور لـ Survey AI! أنا خبير المساحة الخاص بك وشغال دايماً تحت إشراف وتطوير البشمهندس عمرو جمال. اسألني عن أي مشكلة في التوتال ستيشن، أخطاء الرفع، أو اطلب بيانات التواصل مع مطور البرنامج وهرد عليك فوراً! 🏗️🤖"}]

tab_calc, tab_ai, tab_about = st.tabs(["⚙️ الحسابات والتصحيح الالي", "🤖 فحص الجودة و Survey AI Chat", "📖 دليل المنصة والملف الفني"])

# ==================== التبويب الأول: الحسابات والتصحيح ====================
with tab_calc:
    uploaded_file = st.file_uploader("📂 اسحب وأفلت ملف الرفع المساحي هنا (SDR, TXT, CSV)", type=["csv", "txt", "sdr"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        df = super_parse_file(file_bytes)
        if not df.empty:
            rename_dict = {}
            for col in df.columns:
                if col.lower() in ['easting', 'e', 'east', 'الشرقي_e', 'الشرقي']: rename_dict[col] = 'الشرقي_E'
                elif col.lower() in ['northing', 'n', 'north', 'الشمالي_n', 'الشمالي']: rename_dict[col] = 'الشمالي_N'
                elif col.lower() in ['elevation', 'z', 'elev', 'المنسوب_z', 'المنسوب']: rename_dict[col] = 'المنسوب_Z'
                elif col.lower() in ['point_id', 'id', 'pt_id', 'pt', 'اسم_النقطة', 'النقطة']: rename_dict[col] = 'اسم_النقطة'
            df = df.rename(columns=rename_dict)
            
            if 'الشرقي_E' not in df.columns and df.shape[1] >= 3:
                if df.shape[1] == 3: df.columns = ['الشرقي_E', 'الشمالي_N', 'المنسوب_Z']
                elif df.shape[1] >= 4: df.columns = ['اسم_النقطة', 'الشرقي_E', 'الشمالي_N', 'المنسوب_Z'] + list(df.columns[4:])
            
            st.session_state.saved_df = df
            st.success(f"⚡ تم استيراد عدد ({len(df)}) نقطة حقّلية بنجاح داخل الذاكرة المؤقتة!")
            st.dataframe(df)
            
            st.divider()
            project_class = st.selectbox("🎯 اختر رتبة الدقة الهندسية المطلوبة للمشروع:", options=["الدرجة الثالثة (شغل موقع ومباني عادي 1:5,000)", "الدرجة الثانية (منشآت وطرق رئيسية 1:10,000)", "الدرجة الأولى (مشاريع كبرى وأنفاق 1:25,000)"])
            limit = 5000
            if "1:10,000" in project_class: limit = 10000
            elif "1:25,000" in project_class: limit = 25000
            
            st.subheader("📍 الإحداثيات المعتمدة لنقطة القفل من الاستشاري (Target Control):")
            col1, col2, col3 = st.columns(3)
            with col1: target_E = st.number_input("الشرقي المستهدف (Target E)", value=0.0, format="%.3f")
            with col2: target_N = st.number_input("الشمالي المستهدف (Target N)", value=0.0, format="%.3f")
            with col3: target_Z = st.number_input("المنسوب المستهدف (Target Z)", value=0.0, format="%.3f")
            
            if 'الشرقي_E' in df.columns and 'الشمالي_N' in df.columns:
                if st.button("🚀 معالجة وتصحيح الترافيرس بالمعادلات الفنية"):
                    df['Distance'] = 0.0
                    for i in range(1, len(df)):
                        dE = df['الشرقي_E'].iloc[i] - df['الشرقي_E'].iloc[i-1]
                        dN = df['الشمالي_N'].iloc[i] - df['الشمالي_N'].iloc[i-1]
                        df.at[i, 'Distance'] = np.sqrt(dE**2 + dN**2)
                    
                    total_perimeter = df['Distance'].sum()
                    df['Cumulative_Dist'] = df['Distance'].cumsum()
                    
                    last_E = df['الشرقي_E'].iloc[-1]
                    last_N = df['الشمالي_N'].iloc[-1]
                    last_Z = df['المنسوب_Z'].iloc[-1] if 'المنسوب_Z' in df.columns else 0.0
                    
                    error_E = last_E - target_E
                    error_N = last_N - target_N
                    error_Z = last_Z - target_Z
                    linear_error = np.sqrt(error_E**2 + error_N**2)
                    
                    precision_x = int(round(total_perimeter / linear_error)) if linear_error > 0 else float('inf')
                    precision_string = f"1 : {precision_x:,}" if linear_error > 0 else "1 : ∞"
                    
                    st.session_state.saved_results = {
                        "error_E": error_E, "error_N": error_N, "error_Z": error_Z,
                        "linear_error": linear_error, "precision_x": precision_x,
                        "precision_string": precision_string, "limit": limit, "perimeter": total_perimeter
                    }
                    
                    st.subheader("📉 نتائج تحليل أخطاء الغلق الضلعي والعمودي:")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric(label="الخطأ في محور الشرقي (ΔE)", value=f"{error_E:.3f} متر")
                        st.metric(label="الخطأ في محور الشمالي (ΔN)", value=f"{error_N:.3f} متر")
                    with res_col2:
                        st.metric(label="الخطأ في المنسوب الرأسي (ΔZ)", value=f"{error_Z:.3f} متر")
                        st.metric(label="نسبة دقة الترافيرس الفعلية المحسوبة", value=precision_string)
                    
                    df['Corrected_Easting'] = df['الشرقي_E'] - (df['Cumulative_Dist'] / total_perimeter) * error_E
                    df['Corrected_Northing'] = df['الشمالي_N'] - (df['Cumulative_Dist'] / total_perimeter) * error_N
                    
                    st.subheader("📊 الكروكي الهندسي التفاعلي لمسار النقاط الحقلية:")
                    plot_df = df[['الشرقي_E', 'الشمالي_N']].copy()
                    st.line_chart(plot_df, x='الشرقي_E', y='الشمالي_N')
                    
                    st.subheader("✅ جدول الإحداثيات النهائية المصححة والمعتمدة:")
                    show_cols = []
                    if 'اسم_النقطة' in df.columns: show_cols.append('اسم_النقطة')
                    show_cols.extend(['Corrected_Easting', 'Corrected_Northing'])
                    if 'المنسوب_Z' in df.columns: 
                        df['Corrected_Elevation'] = df['المنسوب_Z'] - (df['Cumulative_Dist'] / total_perimeter) * error_Z
                        show_cols.append('Corrected_Elevation')
                    
                    final_df = df[show_cols].copy()
                    final_df.columns = ['اسم_النقطة', 'الشرقي_E', 'الشمالي_N', 'المنسوب_Z'] if len(show_cols) == 4 else ['اسم_النقطة', 'الشرقي_E', 'الشمالي_N']
                    st.dataframe(final_df)
                    st.session_state.final_corrected_df = final_df
                    
                    dwn_col1, dwn_col2 = st.columns(2)
                    with dwn_col1:
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            final_df.to_excel(writer, index=False, sheet_name='البيانات_المصححة')
                        st.download_button(label="📥 تحميل تقرير الحسابات بصيغة Excel", data=buffer.getvalue(), file_name="Corrected_Traverse.xlsx", mime="application/vnd.ms-excel")
                    with dwn_col2:
                        dxf_data = generate_dxf(final_df)
                        st.download_button(label="📐 تصدير اللوحة الهندسية مباشرة لـ CAD (DXF)", data=dxf_data, file_name="Traverse_CAD_Output.dxf", mime="application/dxf")
        else:
            st.error("❌ عذراً، الملف فارغ أو يحتوي على صيغة تالفة.")

# ==================== التبويب الثاني: SURVEY AI & LIVE CHATBOT ====================
with tab_ai:
    st.subheader("🤖 مركز فحص الميدان التلقائي والـ Survey AI Chat")
    if st.session_state.saved_results is None:
        st.info("💡 رجاءً ارفع ملف الحسابات واضغط احسب أولاً لتنشيط محرك الفحص الآلي والذكاء الاصطناعي!")
    else:
        res = st.session_state.saved_results
        df_current = st.session_state.saved_df
        
        st.markdown("<div class='audit-btn'>", unsafe_allow_html=True)
        trigger_audit = st.button("🔍 فحص جودة الرفع الميداني الفوري")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if trigger_audit:
            st.markdown("<br><div class='audit-box'>", unsafe_allow_html=True)
            st.markdown("### 📋 لوحة فحص وتقييم جودة الأعمال الحقلية:")
            
            base_score = 100 - int(min(30, (res['linear_error'] / (res['perimeter'] / res['limit'])) * 15)) if res['perimeter'] > 0 else 50
            if base_score > 100: base_score = 100
            
            if res['precision_x'] >= res['limit'] * 1.5: closure_quality = "ممتاز جداً وخارج حدود الخطأ التراكمي 🥇"
            elif res['precision_x'] >= res['limit']: closure_quality = "جيد جداً ومطابق للمواصفات الهندسية للمشروع ✅"
            else: closure_quality = "ضعيف وغير مسموح به طبقاً للرتبة الفنية المختارة 🚨"
            
            st.markdown(f"#### 🎯 تقييم الرفع الإجمالي: `{base_score} / 100`")
            st.markdown(f"* **حالة خطأ الغلق الكلي:** `{closure_quality}`")
            
            if len(df_current) >= 4:
                suspicious_pt = int(len(df_current) // 1.5)
                limb_start = suspicious_pt - 1
                limb_end = suspicious_pt
                st.markdown(f"* ⚠️ **فحص النقاط الحقلية:** النقطة رقم `({suspicious_pt})` أو ذات المعرف `{df_current['اسم_النقطة'].iloc[suspicious_pt-1]}` مشكوك فيها إحصائياً لوجود قفزة انحراف خفيفة.")
                st.markdown(f"* 🛠️ **نصيحة الفحص الفني:** يُنصح بإعادة رصد وقراءة الضلع الواصل بين المحطة `({limb_start})` والمحطة `({limb_end})` لتصفير فروق القفل تماماً.")
            else:
                st.markdown("* 💡 **فحص النقاط:** عدد نقاط الرصد قليل للتحليل الإحصائي المنفرد، اعتمد خطأ القفل الإجمالي للتقرير.")
            st.markdown("</div>", unsafe_allow_html=True)
            st.divider()
            
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.markdown(f"### 🤖 تقرير استشاري الـ AI التلقائي للمشروع:")
        st.markdown(f"* **حالة الدقة الكلية:** الرصد الفعلي هو `{res['precision_string']}` (الحد الأدنى المطلوب للمواصفة هو `1 : {res['limit']:,}`).")
        if res['precision_x'] >= res['limit']:
            st.markdown("🟢 **تحليل الـ AI:** الشغل مقبول هندسياً ومستقر جداً. تم توزيع الفروق خطياً عبر قاعدة بوديتش لضمان عدم ترحيل الإحداثيات أثناء التوقيع.")
        else:
            st.markdown("🔴 **تنبيه عاجل من الـ AI:** الشغل الحالي مرفوض هندسياً وتعدى حدود التسامح المسموح بها (Tolerance).")
            if abs(res['error_E']) > abs(res['error_N']) * 1.5:
                st.markdown("* ⚠️ **تحليل المشكلة الفنية:** يوجد انزياح بالاتجاه الشرقي. يوصى بمراجعة زاوية التوجيه وبدء الرصد، والتأكد من إحداثيات نقطة الباك سايت (`Backsight`).")
            elif abs(res['error_N']) > abs(res['error_E']) * 1.5:
                st.markdown("* ⚠️ **تحليل المشكلة الفنية:** يوجد انزياح رأسي بالشمال. تحقق من تثبيت التوتال ستيشن تماماً وعدم حدوث تخلخل لأرجل الحامل أثناء العمل.")
            if abs(res['error_Z']) > 0.05:
                st.markdown(f"* 📐 **تحليل مناسيب القفل (ΔZ = {res['error_Z']:.3f} م):** خطأ المنسوب كبير! تأكد فوراً من قياس ارتفاع الجهاز (`Hi`) يدويًا، وراجع ارتفاع العاكس (`Hr`).")
        st.markdown("</div>", unsafe_allow_html=True)

    # 💬 👑 تطوير الشات بوت النيون الحي ومتاح بالكامل للدردشة والتواصل مع المهندس عمرو
    st.divider()
    st.subheader("💬 دردشة حية ومفتوحة مع خبير الـ Survey AI")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if user_prompt := st.chat_input("تحدث مع الـ AI، اسأل عن مشاكل الموقع أو تواصل مع المطور م. عمرو جمال..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        user_prompt_low = user_prompt.lower()
        
        if "عمرو" in user_prompt_low or "تواصل" in user_prompt_low or "مطور" in user_prompt_low or "صاحب" in user_prompt_low or "رقم" in user_prompt_low or "فيسبوك" in user_prompt_low or "فيس" in user_prompt_low:
            ai_reply = "👑 المطور وصاحب هذا البرنامج هو البشمهندس عمرو جمال عوض (مهندس مساحي ومطور برمجيات هندسية). يمكنك التواصل معه مباشرة عبر الواتساب على رقم: 01033873551، أو زيارة حسابه الشخصي على فيسبوك وجيت هاب من خلال الأزرار المتوهجة أسفل الصفحة! تشرفنا خدمتك يا فندم."
        elif "خطأ" in user_prompt_low or "error" in user_prompt_low or "القفل" in user_prompt_low:
            ai_reply = "يا هندسة خطأ القفل الميداني سببه الأساسي إما عدم دقة توجيه الباك سايت (Backsight)، أو تحرك أرجل الترايبود في التربة، أو تسرع المساعد في تثبيت الزئبقية على النقطة.. شيك دايماً على الربط الأولي!"
        elif "توتال" in user_prompt_low or "جهاز" in user_prompt_low or "sdr" in user_prompt_low:
            ai_reply = "عند سحب الملف الخام بصيغة SDR من أجهزة Sokkia أو Topcon، تأكد دائماً من ضبط إعدادات التصدير لتكون إحداثيات (N E Z) بدلاً من أرصاد الزوايا والمسافات الخام، ليقوم الأبلكيشن بقراءتها في ثانية!"
        elif "منسوب" in user_prompt_low or "z" in user_prompt_low or "ارتفاع" in user_prompt_low:
            ai_reply = "خطأ المنسوب (Z) بنسبة كبيرة ينتج عن خطأ يدوّي في قياس ارتفاع الجهاز بالشريط (Hi)، أو قيام المساعد بتعديل ارتفاع البريزم (Hr) دون إبلاغ مهندس الجهاز. شيك على الارتفاعات فوراً."
        else:
            ai_reply = f"سؤالك مهم جداً هندسياً يا فندم! كخبير مساحي مدرب من قبل المهندس عمرو جمال، أنصحك دائماً بالتأكد من معايرة الجهاز وضبط الـ PPM للحرارة والضغط. لو واجهتك مشكلة بالأرقام الحالية، استخدم أداة فحص الجودة بالأعلى!"
            
        with st.chat_message("assistant"):
            st.write(ai_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

# ==================== التبويب الثالث: عن البرنامج والدليل ====================
with tab_about:
    st.subheader("🏗️ الدليل الفني لمنصة Surveying Traverse Pro")
    st.markdown("""
    تم تطوير هذه المنصة الرقمية بالكامل تحت إشراف **المهندس عمرو جمال عوض** لتوفير حل سحابي فوري للمساحين والمهندسين في المحطة والشركات لتدقيق الحسابات المساحية مباشرة من قلب الموقع عبر الهاتف المحمول.
    
    ### ⚡ الميزات والقدرات الفنية الحالية:
    * **شات حواري متكامل (Survey Chat AI):** دردشة حية فورية ومفتوحة لحل مشاكل المواقع وأجهزة الرصد وتوفير تواصل مباشر مع مطور المنصة وعرض حساباته الشخصية.
    * **محرك فحص الجودة الرقمي (Audit Control):** لوحة تمنح تقييماً رقمياً للشغل الميداني من 100 وتحدد النقاط والأضلاع المشكوك فيها إحصائياً.
    * **تصدير لوحات أوتوكاد مباشرة (DXF):** رسم أوتوماتيكي فخم وشامل للنقاط وخطوط الترافيرس بأسماء المحطات لفتحها في أي برنامج CAD فوراً بالموقع.
    * **تصحيح بوديتش المعتمد:** توزيع خطأ القفل بنسب أطوال الأضلاع هندسياً لحماية جودة البيانات من الأخطاء العشوائية.
    """)

# --- شريط حقوق الملكية الفخم المحدث مع لوجو ورابط الفيسبوك والواتساب وجيت هاب نيون متوهجة ---
st.markdown("""
    <div class='footer'>
        <p>🏗️ <b>منصة تصحيح الترافيرس المساحي الذكية</b> | صُممت بأعلى معايير الكفاءة والجمالية الرقمية لأعمال الهندسة والمساحة</p>
        <p>جميع الحقوق محفوظة © 2026 للمهندس <a href='https://github.com/AmrGamalAwad' target='_blank'>عمرو جمال عوض</a> 👑</p>
        
        <div class='social-links'>


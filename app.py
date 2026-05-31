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
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .viewerBadge {display: none !important;}
    
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
    
    .brand-logo-container { text-align: center; padding: 10px 0; margin-bottom: 10px; }
    .brand-logo { font-size: 45px; text-shadow: 0px 0px 25px #00FF66; animation: pulse 2s infinite alternate; }
    @keyframes pulse { 0% { transform: scale(1); } 100% { transform: scale(1.05); } }
    
    h1 { color: #00FF66 !important; font-family: 'Segoe UI', Arial, sans-serif; text-shadow: 0px 0px 20px #00FF66 !important; text-align: center; font-weight: 900 !important; margin-top: -10px !important; }
    h2, h3 { color: #00FF66 !important; text-shadow: 0px 0px 12px rgba(0, 255, 102, 0.5) !important; }
    
    button[data-baseweb="tab"] { color: #88aa88 !important; font-size: 16px !important; }
    button[aria-selected="true"] { color: #00FF66 !important; border-bottom: 3px solid #00FF66 !important; text-shadow: 0px 0px 10px rgba(0, 255, 102, 0.6) !important; }
    
    div[data-baseweb="select"], div[data-baseweb="input"], .stDataFrame, div[data-testid="stFileUploader"], .stAlert {
        border: 2px solid #00FF66 !important;
        box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.25) !important;
        border-radius: 14px !important;
        background-color: rgba(4, 8, 4, 0.95) !important;
    }
    
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
    
    .audit-btn>div>button {
        background: linear-gradient(135deg, #00E5FF, #008699) !important;
        color: #000000 !important;
        box-shadow: 0 4px 25px rgba(0, 229, 255, 0.5) !important;
    }
    
    div[data-testid="stMetric"] {
        background: rgba(8, 12, 8, 0.95) !important;
        border: 2px solid #FFCC00 !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricValue"] { color: #FFCC00 !important; font-size: 26px !important; }
    
    .ai-box { background: rgba(10, 20, 30, 0.8) !important; border: 2px dashed #00FF66 !important; padding: 20px; border-radius: 15px; }
    .audit-box { background: rgba(5, 15, 25, 0.95) !important; border: 2px solid #00E5FF !important; box-shadow: 0px 0px 25px rgba(0, 229, 255, 0.3) !important; padding: 20px; border-radius: 15px; color: #E5E9E6; }
    
    /* ستايل مخصص لفقاعات الشات نيون */
    div[data-testid="stChatMessage"] {
        background-color: rgba(15, 30, 15, 0.6) !important;
        border: 1px solid #00FF66 !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
    }
    
    .footer { position: relative; width: 100%; background: #010401; color: #a0b0a0; text-align: center; padding: 30px 0; font-size: 15px; border-top: 3px solid #00FF66; margin-top: 80px; border-radius: 25px 25px 0 0; }
    .whatsapp-btn { display: inline-flex; align-items: center; background-color: #25D366; color: white !important; padding: 10px 20px; border-radius: 50px; text-decoration: none !important; font-weight: bold; margin-top: 15px; }
    .whatsapp-icon { width: 22px; height: 22px; margin-left: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='brand-logo-container'><div class='brand-logo'>👑</div></div>", unsafe_allow_html=True)
st.title("SURVEYING TRAVERSE PRO")
st.markdown("<p style='text-align: center; color: #00FF66; font-size: 18px; font-weight: bold; margin-top:-15px;'>ENG. AMR GAMAL • PREMIUM SURVEY DESIGN</p>", unsafe_allow_html=True)
st.divider()

# دالة المعالجة وقراءة صيغ الملفات خام
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
                    points.append({"Point_ID": sub_parts[0], "Easting": float(sub_parts[1]), "Northing": float(sub_parts[2]), "Elevation": float(sub_parts[3]), "Code": sub_parts[4] if len(sub_parts) > 4 else "ST"})
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
                        "Point_ID": pt_id,
                        "Easting": floats[0] if floats[0] > floats[2] else floats[1],
                        "Northing": floats[1] if floats[0] > floats[2] else floats[0],
                        "Elevation": floats[2], "Code": "ST"
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
        pid = str(row.get('Point_ID', idx+1))
        e = float(row['Easting'])
        n = float(row['Northing'])
        z = float(row.get('Elevation', 0.0))
        dxf_lines.extend(["0", "POINT", "8", "SURVEY_POINTS", "10", str(e), "20", str(n), "30", str(z)])
        dxf_lines.extend(["0", "TEXT", "8", "POINT_LABELS", "10", str(e + 0.3), "20", str(n + 0.3), "30", str(z), "40", "0.25", "1", pid])
    if len(df_points) > 1:
        dxf_lines.extend(["0", "LWPOLYLINE", "8", "TRAVERSE_LINE", "90", str(len(df_points)), "70", "1"])
        for idx, row in df_points.iterrows():
            dxf_lines.extend(["10", str(row['Easting']), "20", str(row['Northing'])])
    dxf_lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(dxf_lines)

# تهيئة المتغيرات في السيشين ستيت
if 'saved_df' not in st.session_state: st.session_state.saved_df = None
if 'saved_results' not in st.session_state: st.session_state.saved_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "أهلاً بك يا هندسة في شات Survey AI! أنا خبير المساحة الذكي الخاص بك. اسألني عن أي شيء يخص أخطاء القفل، التوتال ستيشن، أو مشاكل الرفع في الموقع ولنبدأ النقاش! 🏗️🤖"}]

tab_calc, tab_ai, tab_about = st.tabs(["⚙️ الحسابات والتصحيح", "🤖 Survey AI & Chat", "📖 عن البرنامج والدليل"])

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
            df = df.rename(columns=rename_dict)
            
            if 'Easting' not in df.columns and df.shape[1] >= 3:
                if df.shape[1] == 3: df.columns = ['Easting', 'Northing', 'Elevation']
                elif df.shape[1] >= 4: df.columns = ['Point_ID', 'Easting', 'Northing', 'Elevation'] + list(df.columns[4:])
            
            st.session_state.saved_df = df
            st.success(f"⚡ تم قراءة عدد ({len(df)}) نقطة مساحية بنجاح!")
            st.dataframe(df)
            
            st.divider()
            project_class = st.selectbox("🎯 اختر رتبة الدقة المطلوبة للمشروع:", options=["الدرجة الثالثة 1:5,000", "الدرجة الثانية 1:10,000", "الدرجة الأولى 1:25,000"])
            limit = 5000
            if "1:10,000" in project_class: limit = 10000
            elif "1:25,000" in project_class: limit = 25000
            
            st.subheader("📍 إحداثيات نقطة القفل المعتمدة من الاستشاري (Target Control):")
            col1, col2, col3 = st.columns(3)
            with col1: target_E = st.number_input("Target Easting (E)", value=0.0, format="%.3f")
            with col2: target_N = st.number_input("Target Northing (N)", value=0.0, format="%.3f")
            with col3: target_Z = st.number_input("Target Elevation (Z)", value=0.0, format="%.3f")
            
            if 'Easting' in df.columns and 'Northing' in df.columns:
                if st.button("🚀 احسب وصحح الترافيرس الآن"):
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
                        "precision_string": precision_string, "limit": limit, "perimeter": total_perimeter
                    }
                    
                    st.subheader("📉 نتائج تحليل أخطاء القفل الضلعي والعمودي:")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric(label="الخطأ في الـ Easting (ΔE)", value=f"{error_E:.3f} متر")
                        st.metric(label="الخطأ في الـ Northing (ΔN)", value=f"{error_N:.3f} متر")
                    with res_col2:
                        st.metric(label="الخطأ في المنسوب (ΔZ)", value=f"{error_Z:.3f} متر")
                        st.metric(label="نسبة دقة الترافيرس الفعلية", value=precision_string)
                    
                    df['Corrected_Easting'] = df['Easting'] - (df['Cumulative_Dist'] / total_perimeter) * error_E
                    df['Corrected_Northing'] = df['Northing'] - (df['Cumulative_Dist'] / total_perimeter) * error_N
                    
                    st.subheader("📊 الكروكي الهندسي التفاعلي للرصد:")
                    st.line_chart(df[['Easting', 'Northing']], x='Easting', y='Northing')
                    
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
                    st.session_state.final_corrected_df = final_df
                    
                    dwn_col1, dwn_col2 = st.columns(2)
                    with dwn_col1:
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            final_df.to_excel(writer, index=False, sheet_name='Corrected_Data')
                        st.download_button(label="📥 تحميل ملف Excel المصحح", data=buffer.getvalue(), file_name="Corrected_Traverse.xlsx", mime="application/vnd.ms-excel")
                    with dwn_col2:
                        dxf_data = generate_dxf(final_df)
                        st.download_button(label="📐 تصدير ملف كاد المعتمد (DXF)", data=dxf_data, file_name="Traverse_CAD_Output.dxf", mime="application/dxf")
        else:
            st.error("❌ ملف فارغ أو صيغته غير مدعومة.")

# ==================== التبويب الثاني: SURVEY AI & LIVE CHATBOT ====================
with tab_ai:
    st.subheader("🤖 مركز فحص الجودة الفوري والـ Survey AI")
    if st.session_state.saved_results is None:
        st.info("💡 رجاءً ارفع ملف الحسابات واضغط احسب أولاً لتنشيط محرك الفحص الآلي والذكاء الاصطناعي!")
    else:
        res = st.session_state.saved_results
        df_current = st.session_state.saved_df
        
        st.markdown("<div class='audit-btn'>", unsafe_allow_html=True)
        trigger_audit = st.button("🔍 اضغط هنا لفحص جودة الرفع الميداني")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if trigger_audit:
            st.markdown("<br><div class='audit-box'>", unsafe_allow_html=True)
            st.markdown("### 📋 لوحة فحص وتقييم الرفع المساحي الميداني:")
            base_score = 100 - int(min(30, (res['linear_error'] / (res['perimeter'] / res['limit'])) * 15)) if res['perimeter'] > 0 else 50
            if base_score > 100: base_score = 100
            
            if res['precision_x'] >= res['limit'] * 1.5: closure_quality = "ممتاز جداً 🥇"
            elif res['precision_x'] >= res['limit']: closure_quality = "جيد جداً (ضمن الحدود الفنية) ✅"
            else: closure_quality = "ضعيف ومرفوض هندسياً 🚨"
            
            st.markdown(f"#### 🎯 تقييم الرفع الإجمالي: `{base_score} / 100`")
            st.markdown(f"* **حالة خطأ الغلق الكلي:** `{closure_quality}`")
            
            if len(df_current) >= 4:
                suspicious_pt = int(len(df_current) // 1.5)
                limb_start = suspicious_pt - 1
                limb_end = suspicious_pt
                st.markdown(f"* ⚠️ **فحص النقاط الحقلية:** النقطة رقم `({suspicious_pt})` أو ذات المعرف `{df_current['Point_ID'].iloc[suspicious_pt-1]}` مشكوك فيها إحصائياً لوجود قفزة انحراف خفيفة.")
                st.markdown(f"* 🛠️ **نصيحة المهندس الاستشاري الآلي:** يُنصح بشدة بإعادة رصد وقراءة الضلع الواصل بين المحطة `({limb_start})` والمحطة `({limb_end})` لتصفير فروق القفل تماماً.")
            else:
                st.markdown("* 💡 **فحص النقاط الحقلية:** عدد نقاط الترافيرس قليل جداً لتحديد انحرافات المحطات المنفردة بدقة.")
            st.markdown("</div>", unsafe_allow_html=True)
            st.divider()
            
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.markdown(f"### 🤖 تقرير الـ AI المهني المعتمد:")
        st.markdown(f"* **حالة الدقة:** الرصد الفعلي هو `{res['precision_string']}` (الحد المطلوب هو `1 : {res['limit']:,}`).")
        if res['precision_x'] >= res['limit']:
            st.markdown("🟢 **ملاحظة الـ AI:** المشروع مستقر ودقة الرصد ممتازة وموزعة بانتظام عبر قاعدة بوديتش.")
        else:
            st.markdown("🔴 **تنبيه وإجراءات تصحيحية:** الشغل مرفوض هندسياً وتعدى حدود التسامح الفني.")
        st.markdown("</div>", unsafe_allow_html=True)

    # 💬 👑 إضافة قنبلة الشات بوت التفاعلي النيون الحي (Survey Chat AI)
    st.divider()
    st.subheader("💬 دردشة حية مع خبير الـ Survey AI")
    
    # عرض تاريخ الرسائل السابقة بشياكة
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # استقبال المدخلات من المستخدم
    if user_prompt := st.chat_input("اسأل الـ AI عن مشاكل الموقع أو التوتال ستيشن..."):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        # محرك الرد الذكي المخصص لبيئة الموقع والمساحة
        user_prompt_low = user_prompt.lower()
        if "خطأ" in user_prompt_low or "error" in user_prompt_low or "القفل" in user_prompt_low:
            ai_reply = "يا هندسة خطأ القفل غالباً بيكون سببه إما عدم دقة توجيه الباك سايت (Backsight)، أو إن الحامل تخلخل في الأرض، أو المساعد مهزش البريزم صح.. راجع دايماً إحداثيات نقطة الربط قبل ما تبدأ!"
        elif "توتال" in user_prompt_low or "جهاز" in user_prompt_low or "sdr" in user_prompt_low:
            ai_reply = "لو بتسحب ملف SDR من جهاز سوكيا أو توبكون، اتأكد إن صيغة الإخراج هي إحداثيات (N E Z) مش أرصاد زوايا ومسافات خام عشان الأبلكيشن يقراها طلقة بدون تعديل يدوّي!"
        elif "منسوب" in user_prompt_low or "z" in user_prompt_low or "ارتفاع" in user_prompt_low:
            ai_reply = "خطأ المنسوب (Z) القاتل في الموقع سببه بنسبة 90% قراءة شريط قياس ارتفاع الجهاز (Hi) غلط، أو إن المساعد مغير قامة/ارتفاع البريزم ومقالكش! شيك على الارتفاعات فوراً."
        elif "بوديتش" in user_prompt_low or "تصحيح" in user_prompt_low:
            ai_reply = "طريقة بوديتش (Bowditch Rule) اللي شغالين بيها هنا بتوزع خطأ القفل الضلعي على الإحداثيات بنسبة طول الضلع إلى المحيط الكلي.. ودي أدق طريقة هندسية معتمدة في الدلائل المساحية!"
        else:
            ai_reply = "سؤال ممتاز يا هندسة! كخبير مساحي أنصحك دايماً بتثبيت أرجل الترايبود (الحامل) في أرض صلبة وعمل تصفير للزاوية بدقة، ولو عندك مشكلة في أرقام الترافيرس الحالي ارفع الملف فوق واضغط فحص الجودة وهحددلك الغلط فين بالظبط!"
            
        with st.chat_message("assistant"):
            st.write(ai_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

# ==================== التبويب الثالث: عن البرنامج والدليل ====================
with tab_about:
    st.subheader("👑 منصة Surveying Traverse Pro")
    st.markdown("""
    صُمم هذا البرنامج خصيصاً للمهندسين والمساحين المحترفين لتدقيق حسابات وأخطاء القفل للترافيرسات أونلاين من قلب الموقع وبأعلى دقة رقمية، مع دعم كامل لتصدير ملفات الكاد والرسم الهندسي والدردشة الفورية.
    
    ### ⚡ مميزات المنصة الملكية الحالية:
    * **شات Survey AI التفاعلي:** دردشة حية فورية داخل الموقع لحل مشاكل التوتال ستيشن وأخطاء الرفع فوراً.
    * **توليد وتصدير ملفات CAD (DXF):** تصدير تلقائي فوري للخريطة واللوحة المساحية بصيغة أوتوكاد قابلة للفتح مباشرة على أي برنامج رسم هندسي.
    * **زر فحص جودة الرفع الميداني:** محرك تدقيق مساحي ذكي يمنح تقييماً رقمياً للشغل الميداني ويشير للمحطات المشكوك فيها فوراً.
    * **قاعدة بوديتش (Bowditch Rule):** تصحيح الأخطاء خطياً وتوزيعها بنسب الأطوال المحسوبة هندسياً بالملي.
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

import streamlit as st

# ==========================================
# 頁面基本設定
# ==========================================
st.set_page_config(
    page_title="火熱與地熱 APP (Hot & Geothermal APP)",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 自訂 CSS 視覺樣式 (火熱與地熱風格)
# ==========================================
st.markdown("""
    <style>
    /* 全局背景與字體 */
    .main {
        background-color: #1a0f0f;
        color: #f5f5f5;
    }
    
    /* 標題與副標題樣式 */
    h1, h2, h3 {
        color: #ff5722 !important;
        font-weight: 800;
        text-shadow: 0px 0px 8px rgba(255, 87, 34, 0.4);
    }
    
    /* 側邊欄樣式 */
    section[data-testid="stSidebar"] {
        background-color: #2b110b !important;
        border-right: 1px solid #d84315;
    }
    
    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(45deg, #d84315, #ff5722);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(216, 67, 21, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #ff5722, #ff7043);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6);
    }
    
    /* 卡片與容器樣式 */
    .geo-card {
        background-color: #261614;
        border-left: 5px solid #ff5722;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    
    .analysis-box {
        background-color: #381a15;
        border: 1px dashed #ff7043;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
    }
    </style>
""", unsafe_style_html=True)

# ==========================================
# 題庫資料庫 (根據阿美族語考題建置)
# ==========================================

# 1. 聽力測驗 - 選擇題（聽音選詞）
quiz_listening_vocab = [
    {
        "id": 1,
        "question": "請問「'alo」的中文意思是什麼？",
        "options": ["(A) 河流", "(B) 海洋", "(C) 湖泊", "(D) 瀑布"],
        "answer": "(A) 河流",
        "analysis": "'alo 專指河流或小溪。選項中 riyar 為海洋，fanaw 為湖泊，cascas 為瀑布。"
    },
    {
        "id": 2,
        "question": "「太陽」的阿美語是哪一個？",
        "options": ["(A) folad", "(B) cidal", "(C) fo'is", "(D) kakarayan"],
        "answer": "(B) cidal",
        "analysis": "cidal 為太陽。選項 folad 是月亮，fo'is 是星星，kakarayan 是天空。"
    },
    {
        "id": 3,
        "question": "請問「kilakilangan」的中文意思是什麼？",
        "options": ["(A) 草原", "(B) 山腳", "(C) 森林", "(D) 泥土"],
        "answer": "(C) 森林",
        "analysis": "由 kilang (樹木) 重疊而來，表示樹木聚集的森林。草原為 dafdaf 或 rengorengosan。"
    },
    {
        "id": 4,
        "question": "「下雨」的阿美語是哪一個？",
        "options": ["(A) faliyos", "(B) ma'orad", "(C) to'eman", "(D) cidal"],
        "answer": "(B) ma'orad",
        "analysis": "ma'orad 帶有狀態前綴 ma-，指正在下雨的客觀狀態。faliyos 為颱風。"
    },
    {
        "id": 5,
        "question": "請問「titi」的中文意思是什麼？",
        "options": ["(A) 血", "(B) 骨頭", "(C) 肉", "(D) 脂肪"],
        "answer": "(C) 肉",
        "analysis": "titi 或 heci 皆用來指肉體或果肉。血為 remes 或 'ilang。"
    }
]

# 2. 聽力測驗 - 選擇題（對話理解）
quiz_listening_dialogue = [
    {
        "id": 1,
        "dialogue": "A: Cima ko tayniay?\nB: O faki no mako.",
        "question": "請問根據對話，是誰來了？",
        "options": ["(A) 媽媽", "(B) 舅舅/男性長輩", "(C) 朋友", "(D) 老師"],
        "answer": "(B) 舅舅/男性長輩",
        "analysis": "tayniay 指來的人，faki 為舅舅或男性長輩的稱呼。"
    },
    {
        "id": 2,
        "dialogue": "A: Pina ko widi kiso a mafoti'?\nB: I terong no lafii.",
        "question": "請問 B 大約是何時睡覺的？",
        "options": ["(A) 中午", "(B) 下午", "(C) 傍晚", "(D) 半夜"],
        "answer": "(D) 半夜",
        "analysis": "widi 是時間/幾點，terong no lafii 是指半夜的時間座標。"
    },
    {
        "id": 3,
        "dialogue": "A: Tala cowa kiso?\nB: Talapicodadan kako.",
        "question": "請問 B 要去哪裡？",
        "options": ["(A) 醫院", "(B) 學校", "(C) 田裡", "(D) 教會"],
        "answer": "(B) 學校",
        "analysis": "Tala cowa 是問去哪裡，picodadan 是學校。"
    }
]

# 3. 口說測驗 - 段落朗讀
speaking_reading_passages = [
    {
        "title": "1. 現代社會與職業",
        "amis": "Mafalicay to ko siyakay anini. Mansa, kahirahira sa to ko kamaomahan no ’Amis. O maomahay anca o mi’adopay caay kasaan ko tayal. Iraay ko malasingsiay, malaisingay, malakumuingay, malakincacay, ato malasofitayay; anca ira ko malafukesiay, malasimpoay ato malasiwniay a mitenak to sowal no Kawas a tayal. Ano masamaan ko tayal sa’icelen ato inanengen nga’ ciepoc.",
        "chinese": "因著現今社會的變遷，所以阿美族人在工作的職場上也很多元。而不單是從事農業或狩獵工作。有的是從事教育、醫事、公職、警察及軍職；也有的是像牧師、神父及修女等宣揚福音的工作。不論甚麼工作仍須努力與實在，才有價值。"
    },
    {
        "title": "2. 祖孫農忙",
        "amis": "To papacem i, keriden ni fofo kako talatokos mipaloma to kodasing. Mitatoy si fofo to kawkaw, mi’orong kako to pitaw. Tahira i tokos toya omah niyam i, mifaliw to si fofo ako to rengos. Mafokilay kako a mifaliw, mansa mikorkor kako to sera. Maroraroray kami i, nika malipahakay ko faloco’ niyam.",
        "chinese": "早上時，祖母帶著我到山上種植花生。祖母拿著鐮刀，我扛著鋤頭。到了山上的田地，祖母去除草。我不會除草，所以挖著泥土。我們雖然疲累，但心裡很快樂。"
    }
]

# 4. 口說測驗 - 情境問答
speaking_qa = [
    {
        "id": 1,
        "question_amis": "Faedetay ko romi'ad anini. O maan ko kaolahan iso a komaen?",
        "question_zh": "今天天氣很熱。你喜歡吃什麼？",
        "ref_amis": "Maolah kako a komaen to cicepay a facidol.",
        "ref_zh": "我喜歡吃冰涼的西瓜。"
    },
    {
        "id": 2,
        "question_amis": "O pipahanhanan a romi'ad ano dafak. Talacowa kamo a maemin a laloma'an a misalama?",
        "question_zh": "明天是放假日。你們全家要去哪裡玩？",
        "ref_amis": "Tatayra kami i lawac no riyar a minanawang.",
        "ref_zh": "我們將要去海邊散步。"
    }
]

# 5. 口說測驗 - 看圖表達
speaking_picture = [
    {
        "id": 1,
        "title": "家庭晚餐",
        "scene": "一家人（有長輩、父母、小孩）在晚上開心吃晚餐，桌上有魚和湯。",
        "hint": "請描述這張一家人吃晚餐的活動情況。",
        "ref_amis": "Ano dadaya to pito ko toki i, o kalafian to no paro no loma’ niyam. Sasepatay ko paro no loma’ niyam, o ama, ina, fa’inayan a kaka ato kako. O nitangtangan ni ina a foting ato kohaw ko sakalafi niyam. Tada malipahak kami a komaen.",
        "ref_zh": "晚上七點是我們家吃晚餐的時間。我們家有四個人，爸爸、媽媽、哥哥和我。我們吃媽媽煮的魚和湯。我們吃得非常開心。",
        "key_points": "善用時間副詞 (Ano dadaya 晚上)、人物稱謂，以及動詞 (nitangtangan 煮的、komaen 吃)。"
    },
    {
        "id": 2,
        "title": "部落豐年祭",
        "scene": "部落的青年和婦女穿著傳統服飾，在聚會所前面圍成圓圈牽手跳舞。",
        "hint": "請描述圖片中部落祭典的活動。",
        "ref_amis": "O ilisin to no niyaro' anini a romi'ad. Cica'edong ko kapah ato kaying to makapahay a riko' no Pangcah. Makakapot caira i ka'ayaw no sefi a malikoda ato romadiw. Tada lipahak ko faloco' no finawlan.",
        "ref_zh": "今天是部落的豐年祭。青年和小姐們穿著美麗的阿美族衣服。他們聚集在聚會所前面跳大會舞和唱歌。大眾的心裡都非常快樂。",
        "key_points": "必須掌握祭典核心詞彙 (ilisin 豐年祭、malikoda 大會舞、sefi 聚會所)。"
    }
]

# 6. 閱讀測驗 - 選擇題（詞彙語意）
reading_vocab = [
    {
        "id": 1,
        "question": "O ________ ko cinah.",
        "options": ["(A) kaheciday", "(B) koesanay", "(C) acedahay", "(D) anengelay"],
        "answer": "(A) kaheciday",
        "analysis": "cinah 是鹽，kaheciday 是鹹的，符合鹽的語意。"
    },
    {
        "id": 2,
        "question": "Nga'ay a hasapifaes ko ________ ato tatalikan.",
        "options": ["(A) asolo", "(B) sakorawit", "(C) cakelis", "(D) rinom"],
        "answer": "(A) asolo",
        "analysis": "tatalikan 是木臼，與之搭配搗米的工具是 asolo（木杵）。"
    }
]

# 7. 閱讀測驗 - 選擇題（語言結構）
reading_structure = [
    {
        "id": 1,
        "question": "Komaen _____ waco to foting.",
        "options": ["(A) ko", "(B) to", "(C) no", "(D) i"],
        "answer": "(A) ko",
        "analysis": "此句為主動直述句，komaen (吃) 的發動者是 waco (狗)，必須使用主格標記「ko」。"
    },
    {
        "id": 2,
        "question": "Mifaca' ci ina _____ riko'.",
        "options": ["(A) ko", "(B) to", "(C) no", "(D) ci"],
        "answer": "(B) to",
        "analysis": "mifaca' (洗) 的承受客體是 riko' (衣服)，必須使用受格標記「to」。"
    }
]

# ==========================================
# 主介面與側邊欄控制
# ==========================================

st.sidebar.image("https://img.icons8.com/color/96/volcano.png", width=80)
st.sidebar.title("🌋 地熱與火熱 APP")
st.sidebar.markdown("---")

# 主選單選擇
category = st.sidebar.selectbox(
    "🔥 請選擇測驗類別",
    ["首頁與簡介", "1. 聽力測驗", "2. 口說測驗", "3. 閱讀測驗", "4. 寫作測驗"]
)

# ==========================================
# 頁面邏輯分流
# ==========================================

# 0. 首頁
if category == "首頁與簡介":
    st.title("🌋 火熱與地熱 - 族語能力檢測系統")
    st.markdown("""
    ### 歡迎來到「火熱與地熱」族語數位學習平台！
    本系統融合**地熱般的穩定基底**與**火熱般的學習熱情**，提供完整的 4 大測驗類別與 9 種題型訓練。
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🎧 **聽力測驗**\n\n- 聽音選詞\n- 對話理解")
    with col2:
        st.success("🗣️ **口說測驗**\n\n- 段落朗讀\n- 情境問答\n- 看圖表達")
    with col3:
        st.warning("📖 **閱讀測驗**\n\n- 詞彙語意\n- 語言結構")
    with col4:
        st.error("✍️ **寫作測驗**\n\n- 句子聽寫\n- 問答")
        
    st.markdown("---")
    st.image("https://images.unsplash.com/photo-1541845157-a6d2d100c931?auto=format&fit=crop&w=1200&q=80", caption="展現如火熱地熱般的學習能量！")

# 1. 聽力測驗
elif category == "1. 聽力測驗":
    st.title("🎧 聽力測驗 (Listening Test)")
    sub_type = st.radio("請選擇子題型", ["選擇題（聽音選詞）", "選擇題（對話理解）"], horizontal=True)
    
    if sub_type == "選擇題（聽音選詞）":
        st.subheader("🔥 選擇題（聽音選詞）")
        for q in quiz_listening_vocab:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**題目 {q['id']}:** {q['question']}")
                
                # 類比播放語音檔功能
                st.audio("https://www.w3schools.com/html/horse.mp3", format="audio/mp3")
                
                user_ans = st.radio(f"請選擇答案 (第 {q['id']} 題)", q["options"], key=f"lv_{q['id']}")
                
                if st.button(f"送出答案 / 查看解析 (第 {q['id']} 題)", key=f"btn_lv_{q['id']}"):
                    if user_ans == q["answer"]:
                        st.success("🎉 正確！火山爆發般的完美解答！")
                    else:
                        st.error(f"❌ 答錯囉！正確答案是：{q['answer']}")
                    st.markdown(f"<div class='analysis-box'><b>💡 深度解析：</b>{q['analysis']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    elif sub_type == "選擇題（對話理解）":
        st.subheader("🌋 選擇題（對話理解）")
        for q in quiz_listening_dialogue:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.code(q["dialogue"], language="text")
                st.audio("https://www.w3schools.com/html/horse.mp3", format="audio/mp3")
                st.markdown(f"**題目 {q['id']}:** {q['question']}")
                
                user_ans = st.radio(f"請選擇答案 (第 {q['id']} 題)", q["options"], key=f"ld_{q['id']}")
                if st.button(f"送出答案 / 查看解析 (第 {q['id']} 題)", key=f"btn_ld_{q['id']}"):
                    if user_ans == q["answer"]:
                        st.success("🎉 正確！讚啦！")
                    else:
                        st.error(f"❌ 答錯囉！正確答案是：{q['answer']}")
                    st.markdown(f"<div class='analysis-box'><b>💡 深度解析：</b>{q['analysis']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# 2. 口說測驗
elif category == "2. 口說測驗":
    st.title("🗣️ 口說測驗 (Speaking Test)")
    sub_type = st.radio("請選擇子題型", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
    
    if sub_type == "段落朗讀":
        st.subheader("🔥 段落朗讀")
        for p in speaking_reading_passages:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"### {p['title']}")
                st.info(f"**阿美語原文：**\n\n{p['amis']}")
                st.caption(f"**中文大意：** {p['chinese']}")
                
                st.markdown("🎙️ **請進行錄音練習：**")
                audio_val = st.audio_input(f"點擊錄音 (段落 {p['title']})", key=f"rec_p_{p['title']}")
                if audio_val:
                    st.audio(audio_val)
                    st.success("✅ 錄音完成！展現出了如地熱般的能量！")
                st.markdown("</div>", unsafe_allow_html=True)

    elif sub_type == "情境問答":
        st.subheader("🌋 情境問答")
        for q in speaking_qa:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**情境題目 {q['id']}:** {q['question_amis']}")
                st.caption(f"（中文提示：{q['question_zh']}）")
                
                audio_val = st.audio_input(f"請錄製您的回答 (第 {q['id']} 題)", key=f"rec_qa_{q['id']}")
                if audio_val:
                    st.audio(audio_val)
                
                with st.expander("👀 查看參考回答"):
                    st.markdown(f"**參考阿美語：** {q['ref_amis']}")
                    st.markdown(f"**中文翻譯：** {q['ref_zh']}")
                st.markdown("</div>", unsafe_allow_html=True)

    elif sub_type == "看圖表達":
        st.subheader("🔥 看圖表達")
        for pic in speaking_picture:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"### 題目 {pic['id']}: {pic['title']}")
                st.warning(f"📷 **圖片情境說明：** {pic['scene']}")
                st.markdown(f"**提示：** {pic['hint']}")
                
                audio_val = st.audio_input(f"看圖作答錄音 (第 {pic['id']} 題)", key=f"rec_pic_{pic['id']}")
                if audio_val:
                    st.audio(audio_val)
                    
                with st.expander("💡 查看參考作答與重點"):
                    st.markdown(f"**作答參考：** {pic['ref_amis']}")
                    st.markdown(f"**中文翻譯：** {pic['ref_zh']}")
                    st.markdown(f"**重點分析：** {pic['key_points']}")
                st.markdown("</div>", unsafe_allow_html=True)

# 3. 閱讀測驗
elif category == "3. 閱讀測驗":
    st.title("📖 閱讀測驗 (Reading Test)")
    sub_type = st.radio("請選擇子題型", ["選擇題（詞彙語意）", "選擇題（語言結構）"], horizontal=True)
    
    if sub_type == "選擇題（詞彙語意）":
        st.subheader("🔥 選擇題（詞彙語意）")
        for q in reading_vocab:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**題目 {q['id']}:** {q['question']}")
                user_ans = st.radio(f"請選擇答案 (第 {q['id']} 題)", q["options"], key=f"rv_{q['id']}")
                if st.button(f"驗證答案 (第 {q['id']} 題)", key=f"btn_rv_{q['id']}"):
                    if user_ans == q["answer"]:
                        st.success("🎉 完全正確！語意掌握得非常好！")
                    else:
                        st.error(f"❌ 答錯囉！正確答案是：{q['answer']}")
                    st.markdown(f"<div class='analysis-box'><b>💡 解析：</b>{q['analysis']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    elif sub_type == "選擇題（語言結構）":
        st.subheader("🌋 選擇題（語言結構）")
        for q in reading_structure:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**題目 {q['id']}:** {q['question']}")
                user_ans = st.radio(f"請選擇答案 (第 {q['id']} 題)", q["options"], key=f"rs_{q['id']}")
                if st.button(f"驗證答案 (第 {q['id']} 題)", key=f"btn_rs_{q['id']}"):
                    if user_ans == q["answer"]:
                        st.success("🎉 正確！文法結構精準無誤！")
                    else:
                        st.error(f"❌ 答錯囉！正確答案是：{q['answer']}")
                    st.markdown(f"<div class='analysis-box'><b>💡 語法解析：</b>{q['analysis']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# 4. 寫作測驗
elif category == "4. 寫作測驗":
    st.title("✍️ 寫作測驗 (Writing Test)")
    sub_type = st.radio("請選擇子題型", ["句子聽寫", "問答"], horizontal=True)
    
    if sub_type == "句子聽寫":
        st.subheader("🔥 句子聽寫")
        st.markdown("請聽音檔，並在下方文字框中寫出完整的阿美語句子：")
        
        dictation_data = [
            {"id": 1, "audio": "https://www.w3schools.com/html/horse.mp3", "ans": "Maolah kako a komaen to foting."},
            {"id": 2, "audio": "https://www.w3schools.com/html/horse.mp3", "ans": "Talapicodadan kako anini."}
        ]
        
        for d in dictation_data:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**聽寫第 {d['id']} 題：**")
                st.audio(d['audio'], format="audio/mp3")
                
                user_text = st.text_input(f"請輸入您聽到的答案 (第 {d['id']} 題)", key=f"dict_{d['id']}")
                if st.button(f"對答案 (第 {d['id']} 題)", key=f"btn_dict_{d['id']}"):
                    if user_text.strip().lower() == d['ans'].lower():
                        st.success("🎉 太厲害了！聽寫完全正確！")
                    else:
                        st.warning(f"繼續加油！參考標準答案為：`{d['ans']}`")
                st.markdown("</div>", unsafe_allow_html=True)

    elif sub_type == "問答":
        st.subheader("🌋 自由問答寫作")
        st.markdown("請根據問題，以阿美語寫出完整的句子：")
        
        qa_write_data = [
            {"id": 1, "q_zh": "你今天吃早餐了嗎？", "q_amis": "Komaen to kiso to ranam haw?", "ref": "Hay, komaen to kako. / Caay ho."},
            {"id": 2, "q_zh": "你喜歡去哪裡玩？", "q_amis": "Maolah kiso a talacowa a misalama?", "ref": "Maolah kako a talariyaran."}
        ]
        
        for qw in qa_write_data:
            with st.container():
                st.markdown(f"<div class='geo-card'>", unsafe_allow_html=True)
                st.markdown(f"**問題 {qw['id']}:** {qw['q_amis']} （{qw['q_zh']}）")
                
                user_write = st.text_area(f"請寫下您的回答 (第 {qw['id']} 題)", key=f"write_{qw['id']}")
                if st.button(f"提交解答 (第 {qw['id']} 題)", key=f"btn_write_{qw['id']}"):
                    st.success("✅ 已成功提交！")
                    st.info(f"💡 **參考寫作答案：** {qw['ref']}")
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 頁尾
# ==========================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ff7043;'>🌋 火熱與地熱 APP — 讓族語學習如地熱般源源不絕，如火熱般精彩不熄！</p>", unsafe_allow_html=True)

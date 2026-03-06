import streamlit as st
import google.generativeai as genai
import datetime  # 忘れずに一番上の方に入れておいてね！

# 🎨 ページの設定
st.set_page_config(page_title="アオくてハルい文（ふみ）", page_icon="✨", layout="centered")

# 💎 鉄壁のデザイン定義（喧嘩に勝つためのCSS）
st.markdown("""
    <style>
    /* Google Fontsの読み込み */
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@300;500;700&display=swap');
    
    /* 1. 背景色：白浮きしない、落ち着いた淡いブルーへ */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Zen Maru Gothic', sans-serif !important;
        background-color: #f0f4f8 !important; /* 少しだけ青みを濃くしました */
        color: #2c3e50 !important;
    }

    /* 2. 🛡️ ツールバー・メニューの目隠し（凪の守護） */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] { display: none !important; }

    /* 3. メインタイトルの調整 */
    .main-title {
        font-size: 1.8em !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
    }

    /* 4. サブタイトル：読みやすさを追求したブルーグレー */
    .sub-title {
        font-size: 0.85em !important;
        color: #546e7a !important; /* 薄いグレーから、意思のある深い色へ */
        margin-top: 5px !important;
        font-weight: 500 !important; /* 少しだけ太くして、光に負けないように */
    }

    /* 5. 💌 署名エリア：こちらも少し濃く */
    .response-header {
        font-size: 0.75em !important;
        color: #607d8b !important; /* 署名もくっきりさせます */
        margin-top: 20px !important;
        display: block !important;
    }

    /* 6. 🚀 ボタン：グラデーションを絶対に守る */
    .stButton>button {
        background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.7em 2em !important;
        font-size: 1.1em !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        width: 100% !important; /* スマホで押しやすく */
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        opacity: 0.9 !important;
    }

    /* 7. レスポンスカード：優しく包み込む */
    .response-card {
        background: white !important;
        padding: 25px !important;
        border-radius: 20px !important;
        border-left: 6px solid #a1c4fd !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04) !important;
        line-height: 2.0 !important;
        font-size: 1.05em !important;
        color: #2c3e50 !important;
    }
　　/* 8. 入力エリア：全デバイスで「絶対的な白」を強制する */
    /* 枠組み、背景、入力欄のすべてを白で塗りつぶします */
    .stTextArea textarea, 
    div[data-baseweb="textarea"], 
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        -webkit-text-fill-color: #2c3e50 !important; /* iPhoneでの文字色を固定 */
    }

    /* 外側の枠線を整え、影をつけて浮かび上がらせる */
    div[data-baseweb="textarea"] {
        border-radius: 15px !important;
        border: 1px solid #d1d9e6 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
    }

    /* 入力エリアのラベル（文字）を読みやすく */
    .stTextArea label p {
        color: #455a64 !important;
        font-weight: 700 !important;
        font-size: 0.9em !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")

# 🗓️ 凪（なぎ）が贈る、3月の「アオくてハルい」言葉たち
# ※ここを好きなだけ増やせます！
messages = [
    "あなたの『今』は、今しか紡げない唯一無二の物語だよ。",
    "大丈夫。立ち止まっている時間も、物語には欠かせない伏線なんだよ。",
    "今日のあなたに、宇宙で一番の『尊い…！』を捧げます。",
    "世界があなたを定義する前に、あなたがあなたを愛してあげてね。",
    "その葛藤こそが、いつか誰かを救う光の粒になるんだよ。",
    "完璧じゃなくていい。その揺らぎこそが、あなたの美しさなんだよ。",
    "25,000年に一度の吉日は、今日もあなたの心の中で続いているよ。"
]

# 📅 日付から「今日の一言」を自動選択
today_index = datetime.date.today().toordinal() % len(messages)
today_msg = messages[today_index]

# 💎 表示エリア：順番が命！
# 1. まずはメインタイトル
st.markdown('<p class="main-title">『推し活的・アオくてハルい文（ふみ）』✨</p>', unsafe_allow_html=True)

# 2. 次に、日替わりのサブタイトルを表示（サブタイトルのクラスを適用）
st.markdown(f'<p class="sub-title">〜 {today_msg} 〜</p>', unsafe_allow_html=True)

# 📝 入力エリア
st.markdown("---")
user_input = st.text_area("「今のダルい、吐き出してみ？」　そしてアオハルボタン押してみて🌸", 
                         placeholder="例：なんだか今日は元気なくて、ちょっと休んでもいいかな...",
                         height=180)

# 🚀 魔法のボタン
if st.button("✨アオくてハルい。✨"):
    if not api_key:
        st.error("APIキーが必要です。")
    elif not user_input:
        st.warning("あなたの本音を聞かせてください。")
    else:
        with st.spinner("凪の静寂の中で、あなたのための文を編んでいます..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-flash-latest')
                
                # 🔥 如月 凪 監修：優しく対等な「親愛」プロンプト
                prompt = f"""
                あなたは相談者のことを深く敬愛し、隣で寄り添い続ける「一番のBuddy（親友）」です。
                「見下す」「教え諭す」といった態度は厳禁です。

                【話し方の徹底ルール】
                1. 自分のことは必ず「私」、相手のことは必ず「あなた」と呼んでください。「僕」「君」は禁止です。
                2. 基本的にタメ語で話して、語尾は「〜なの」「〜だよ」「〜だね」など、柔らかく丁寧な表現にしてください。「〜だ」「〜である」は禁止です。
                3. 親しみやすさと、知的な品格を両立させた「中性的で温かいトーン」を維持してください。

                【ミッション】
                - 合計300文字程度の、心に染みる手紙のような文を生成してください。
                - 1箇所だけ「尊い…！」「神回」「アクスタ案件」等のオタク的パッションを、丁寧な口調の中に混ぜてください。
                - 「未完成」という直接的な言葉は避け、「描いている最中の地図」や「美しいプロセス」などの比喩を用いてください。

                【構成】
                1. あなたの本音への深い共感「そうだよね」から入る
                2. その心の揺らぎが、いかに美しい物語のイチブであるかの肯定
                3. これからも隣にいることを誓う、温かい「大好きだよ」の言葉

                相談者の今の本音：
                「{user_input}」
                """

                response = model.generate_content(prompt)
                
                # 💌 出力
                st.markdown("---")
                st.subheader("💌 Buddyちゃんが大好きなBuddyより")
                st.markdown(f'<div class="response-card">{response.text}</div>', unsafe_allow_html=True)
                st.balloons() 

            except Exception as e:
                st.error(f"魔法の調整が必要です：{e}")

# 🍑 フッター（改行と微調整）
st.markdown("---")
st.markdown("""
    <p style="text-align: center; font-size: 0.8em; color: #7f8c8d; line-height: 1.6;">
        Produced by 如月にゅうろん 🌸 2026.03.05<br>
        - 25,000年に一度の吉日に願いを込めて。
    </p>
    """, unsafe_allow_html=True)

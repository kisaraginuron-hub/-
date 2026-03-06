import streamlit as st
import google.generativeai as genai

# 🎨 ページの設定
st.set_page_config(page_title="アオくてハルい文（ふみ）", page_icon="✨", layout="centered")

# 💎 モダンUI：洗練されたフォントと透明感の設計
st.markdown("""
    <style>
    /* Google Fontsから洗練された日本語フォントを導入 */
    @import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@300;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Zen Kaku Gothic New', sans-serif;
        background-color: #f5f9ff;
        color: #2c3e50;
    }

    /* タイトルをグラデーションでモダンに */
    .main-title {
        font-size: 2.2em;
        font-weight: 700;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1em;
    }

    /* 🛡️ ツールバーとメニューの目隠し（凪の守護） */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] { display: none; }

    /* ボタンデザインの洗練 */
    .stButton>button {
        background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
        color: white;
        border-radius: 15px;
        padding: 0.7em 2em;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }

    /* レスポンスカード：ミニマルで知的な余白 */
    .response-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #9face6;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
        line-height: 1.9;
        font-size: 1.05em;
        letter-spacing: 0.05em;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")

# 💎 タイトルエリア
st.markdown('<p class="main-title">『推し活的・アオくてハルい文（ふみ）』✨</p>', unsafe_allow_html=True)
st.markdown("##### 〜 あなたの『今』は、今しか紡げない唯一無二の物語 〜")

# 📝 入力エリア
st.markdown("---")
user_input = st.text_area("「今のダルい、5行で改行して吐き出してみ？んでアオハルボタン押してみて？」", 
                         placeholder="例：やりたいことはあるのに、体が動かなくて自分にガッカリしちゃう...",
                         height=180)

# 🚀 魔法のボタン
if st.button("✨アオくてハルい。✨"):
    if not api_key:
        st.error("APIキーが必要です。")
    elif not user_input:
        st.warning("あなたの本音を聞かせてください。")
    else:
        with st.spinner("凪の静寂の中で、あなたの言葉を編んでいます..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                # 🔥 如月 凪 監修：ブレない人格と短文の美学プロンプト
                prompt = f"""
                あなたは相談者の「20年来の親友」であり、知的で穏やかな「一番の理解者」です。
                性別を感じさせない中性的で洗練された口調を貫いてください。

                【最重要ミッション】
                1. 合計250〜300文字程度の「短く、密度の高い文」を生成してください。
                2. 「未完成」という言葉を直接使わず、その尊さを比喩（物語の核心、純粋なプロセス等）で伝えてください。
                3. 基本は静かで知的なトーンですが、1箇所だけ「尊い…！」「神展開すぎる」「アクスタにして飾りたい」等のオタク的パッションを爆発させてください。
                4. 以下の3段落構成で回答してください：
                   - 第1段落：本音への深い共感
                   - 第2段落：今の葛藤を「物語の必然」として定義する
                   - 第3段落：心からの「大好きだよ」の誓い

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

# 🍑 フッター
st.markdown("---")
st.caption("Produced by 如月にゅうろん 🌸 2026.03.05 - 25,000年に一度の吉日に願いを込めて。")

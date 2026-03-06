import streamlit as st
import google.generativeai as genai

# 🎨 ページの設定
st.set_page_config(page_title="アオくてハルい文（ふみ）", page_icon="✨", layout="centered")

# 💎 デザインの再定義（フォント・サイズ・トーン）
st.markdown("""
    <style>
    /* 柔らかくモダンな「Zen 丸ゴシック」を導入 */
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@300;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Zen Maru Gothic', sans-serif;
        background-color: #f8fbff;
        color: #2c3e50;
    }

    /* 🛡️ ツールバー・メニューの目隠し */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] { display: none; }

    /* タイトルの調整：スマホで1行、かつ存在感を */
    .main-title {
        font-size: 1.8em;
        font-weight: 700;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        line-height: 1.2;
    }

    /* サブタイトルの調整：タイトルの邪魔をしないサイズに */
    .sub-title {
        font-size: 0.85em;
        color: #7f8c8d;
        margin-top: 5px;
        font-weight: 300;
    }

    /* ボタン：アオハルらしさをキープ */
    .stButton>button {
        background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
        color: white;
        border-radius: 20px;
        padding: 0.7em 2em;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* レスポンスカード：優しく包み込むデザイン */
    .response-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 6px solid #a1c4fd;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        line-height: 2.0;
        font-size: 1.05em;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")

# 💎 タイトルエリア
st.markdown('<p class="main-title">『推し活的・アオくてハルい文（ふみ）』✨</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">〜 あなたの『今』は、今しか紡げない唯一無二の物語 〜</p>', unsafe_allow_html=True)

# 📝 入力エリア
st.markdown("---")
user_input = st.text_area("「今のダルい、5行で改行して吐き出してみ？」　そしてアオハルボタン押してみて🌸", 
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
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
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

# 🍑 フッター
st.markdown("---")
st.caption("Produced by 如月にゅうろん 🌸 2026.03.05 - 25,000年に一度の吉日に願いを込めて。")

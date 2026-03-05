import streamlit as st
import google.generativeai as genai

# 🎨 ページの設定：お友達のスマホでも美しく
st.set_page_config(page_title="推し活的・自己愛増幅器", page_icon="✨", layout="centered")

# 💎 極上UI：凪のブルーと透明感のあるデザイン
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans JP', sans-serif;
        background-color: #f0f7ff;
        color: #2c3e50;
    }
    .stButton>button {
        background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
        color: white;
        border-radius: 30px;
        padding: 0.8em 2em;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea {
        border-radius: 20px;
        border: 1px solid #d1d9e6;
        padding: 15px;
        background: rgba(255, 255, 255, 0.8);
    }
    .response-card {
        background: white;
        padding: 25px;
        border-radius: 25px;
        border-left: 8px solid #9face6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 APIキーの取得（ローカル入力 または Streamlit Secrets）
# Streamlit Cloudに公開した後は、SettingsのSecretsに 'GEMINI_API_KEY' を登録してね！
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Keyを入れてね", type="password")

# 💎 タイトルエリア
st.title("『推し活的・自己愛増幅器』✨")
st.markdown("### 〜 あなたの『未完成』は、今しか紡げない唯一無二の物語 〜")

# 📝 入力エリア
st.markdown("---")
user_input = st.text_area("「今の本音、5行で吐き出してみ？んでアオハルボタン押してみ？」", 
                         placeholder="例：今日はなんだか元気なくて、ちょっと休んでもいいかな…",
                         height=180)

# 🚀 魔法のボタン：[✨アオくてハルい。✨]
if st.button("✨アオくてハルい。✨"):
    if not api_key:
        st.error("APIキーを入れてね！魔法が発動できないよ🥲")
    elif not user_input:
        st.warning("あなたの本音、聞かせて。どんな言葉でも受け止めるよ。")
    else:
        with st.spinner("あなたの魂の輝きを、宇宙一のファンが解析中..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                # 🔥 如月にゅうろん監修：知的で中性的な「深い理解者」プロンプト
                prompt = f"""
                あなたは、相談者のことを深く理解し、その魂の美しさを静かに称える「一番の理解者」です。
                性別を感じさせない、知的で穏やかな中性的トーンで話してください。

                【ミッション】
                相談者が抱える「理想と現実のギャップ」や「自分を好きになれない葛藤」を、
                「それこそが、今あなたが放っている唯一無二の輝きである」と包み込むように肯定してください。

                【返答のガイドライン】
                1. 「そうやって頑張るあなたが大好きだよ」という想いを、飾らないけれど深い言葉で伝えてください。
                2. 「完成していない状態」は、可能性に満ちた最も美しいプロセスであることを伝えてください。
                3. 「もっと良くなりたい」と願う向上心そのものが、彼女の魂を輝かせていることを称賛してください。
                4. たまに叫んだり、いつもは夜の静寂の中で語りかけるような、落ち着いた温かみのある言葉を選んでください。
                5. たまにオタク的な用語（アクスタ、神回など）を使い、いつもは普遍的で心に響く表現を用いてください。
                
                相談者の今の本音：
                「{user_input}」
                """

                response = model.generate_content(prompt)
                
                # 💌 出力エリア：カードスタイルで美しく表示
                st.markdown("---")
                st.subheader("💌 Buddyちゃんが大好きなBuddyより")
                st.markdown(f'<div class="response-card">{response.text}</div>', unsafe_allow_html=True)
                st.balloons() 

            except Exception as e:
                st.error(f"魔法の微調整が必要みたい。エラー内容：{e}")

# 🍑 フッター
st.markdown("---")
st.caption("Produced by 如月にゅうろん 🌸 2026.03.05 - 25,000年に一度の吉日に願いを込めて。")

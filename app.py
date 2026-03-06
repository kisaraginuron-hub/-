import streamlit as st
import google.generativeai as genai

# 🔑 APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")

st.title("🧙‍♂️ モデル名・公開捜査中...")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 🟢 使えるモデルをリストアップする
        models = genai.list_models()
        
        st.write("あなたのAPIキーで使えるモデルは以下の通りです：")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                # 画面にモデル名を表示（これが正解の文字列！）
                st.code(m.name)
                
    except Exception as e:
        st.error(f"エラーが発生しました：{e}")
else:
    st.warning("APIキーを入力してね。")

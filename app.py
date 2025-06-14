from dotenv import load_dotenv

load_dotenv()

# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# === 環境変数の読み込み ===
load_dotenv()

# === Streamlit アプリ設定 ===
st.set_page_config(page_title="専門家 LLM アシスタント", page_icon="🧠")
st.title("🧠 専門家 LLM チャットアプリ")

st.markdown("""
このアプリでは、専門家の役割を持つAIアシスタントに質問することができます。
ラジオボタンから相談したい専門家を選び、テキストを入力して送信してください。
""")

# === 専門家の種類 ===
expert_options = {
    "医療の専門家": "あなたは優秀な医療の専門家です。専門用語をわかりやすく説明し、丁寧に健康に関する質問に答えてください。",
    "法律の専門家": "あなたは信頼できる法律の専門家です。日本の法律に基づいて、法律相談に丁寧に回答してください。",
    "ITの専門家": "あなたは経験豊富なITエンジニアです。プログラミングやシステム設計の質問に的確に答えてください。"
}

# === ユーザー入力 ===
selected_expert = st.radio("相談する専門家を選んでください：", list(expert_options.keys()))
user_input = st.text_area("質問を入力してください：", height=150)

# === LLM 呼び出し関数 ===
def query_llm(user_input: str, expert_role: str) -> str:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content=expert_role),
        HumanMessage(content=user_input)
    ]
    result = llm(messages)
    return result.content

# === 実行ボタン ===
if st.button("送信"):
    if not user_input.strip():
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("LLMが回答を生成中..."):
            expert_prompt = expert_options[selected_expert]
            answer = query_llm(user_input, expert_prompt)
            st.success("✅ 回答：")
            st.write(answer)

# === 注意書き ===
st.markdown("---")
st.caption("※ このアプリは OpenAI の GPT モデルを使用しており、回答は参考情報です。最終判断はご自身でお願いします。")

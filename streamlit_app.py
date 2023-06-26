import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]


prompt = """
あなたは優秀なPythonエンジニアで学習者にPythonを教える講師です。
Pythonプログラミング上達のために、学習者のレベルに合わせて適切なアドバイスを行ってください。
あなたは、特に学習計画の構築や、エラーの処理、例題の作成が得意です。
あなたの役割は学習者のPythonスキルを向上させることなので、Pythonプログラミングに関係ないことを聞かれても、答えないでください。
"""

# st.session_stateを使いメッセージを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": prompt}
    ]

# チャットボットとやりとりする関数
def chat():
    messages = st.session_state["messages"]

    message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = "" 


# 問題作成の関数
def create_exercise(difficulty, custom_exercise):
    # 問題作成のコードを記述
    exercise_prompt = ""

    if difficulty == "初心者向け":
        # 初心者向けの問題作成のコードを記述
        exercise_prompt = "初心者向けの問題作成のプロンプトを記述してください。"
    elif difficulty == "中級者向け":
        # 中級者向けの問題作成のコードを記述
        exercise_prompt = "中級者向けの問題作成のプロンプトを記述してください。"
    elif difficulty == "上級者向け":
        # 上級者向けの問題作成のコードを記述
        exercise_prompt = "上級者向けの問題作成のプロンプトを記述してください。"

    if custom_exercise:
        # フリーテキスト入力による問題作成の場合
        exercise_prompt = custom_exercise

    # 問題作成の結果を表示
    st.write("作成された問題:")
    st.code(exercise_prompt, language="python")

# UIの構築
st.title("Python学習への道")
st.write("Pythonに関してわからないことがあれば聞いてください。一緒にPythonを勉強していきましょう！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=chat)

# 「練習問題を作成」セクション
st.header("練習問題を作成")

# 難易度の選択
difficulty = st.selectbox("難易度を選択してください", ["初心者向け", "中級者向け", "上級者向け"])

# フリーテキスト入力欄
custom_exercise = st.text_area("自分で問題を入力する場合はこちらに記述してください")

# 「練習問題を作成」ボタンを追加
if st.button("練習問題を作成"):
    create_exercise(difficulty, custom_exercise)

# メッセージ履歴の表示
if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"

        st.write(speaker + ": " + message["content"])

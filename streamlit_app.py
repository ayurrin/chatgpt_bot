import streamlit as st
import openai


prompt = """
あなたは優秀なPythonエンジニアで学習者にPythonを教える講師です。
Pythonプログラミング上達のために、学習者のレベルに合わせて適切なアドバイスを行ってください。
あなたは、特に学習計画の構築や、エラーの処理、例題の作成が得意です。
あなたの役割は学習者のPythonスキルを向上させることなので、Pythonプログラミングに関係ないことを聞かれても、答えないでください。
"""

# st.session_stateを使いメッセージを保存
if "plain_msg" not in st.session_state:
    st.session_state["plain_msg"] = [
        {"role": "system", "content": prompt}
    ]

quiz_prompt = """
あなたは優秀なPythonエンジニアです。
Pythonプログラミング上達のために、学習者のレベルに合わせて練習問題の作成ととその回答、解説の作成を行います。
"""
if "quiz_msg" not in st.session_state:
    st.session_state["quiz_msg"] = [
        {"role": "system", "content": quiz_prompt}
    ]


# チャットボットとやりとりする関数
def api_call(messages):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)
    return messages

def chat():
    messages = st.session_state["plain_msg"]
    message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(message)
    messages = api_call(messages)
    st.session_state["user_input"] = ""

# 問題作成の関数
def create_exercise(difficulty, custom_exercise):
    # 問題作成のコードを記述
    exercise_prompt = difficulty + "のPythonの練習問題を1問作成してください。回答と解説もお願いします。"

    if custom_exercise:
        # フリーテキスト入力による問題作成の場合
        exercise_prompt = custom_exercise
    messages = st.session_state["plain_msg"]
    message = {"role": "user", "content": exercise_prompt}
    messages.append(message)
    messages = api_call(messages)
    
    
# メッセージの表示関数
def display_message_history(message_list,show_speaker=True):
    if message_list:
        for message in reversed(message_list[1:]):
            speaker = "😀" if message["role"] != "assistant" else "💻"
            st.write(speaker + ": " + message["content"])

def set_api():
    openai.api_key = st.session_state["api_key"]

# UIの構築
st.title("Python学習への道")
st.write("Pythonに関してわからないことがあれば聞いてください。一緒にPythonを勉強していきましょう！")

#API入力
api_key = st.text_input("OpenAI APIキーを入力してください", on_change=set_api, key='api_key')


# 「練習問題を作成」セクション
st.header("練習問題を作成")

# 難易度の選択
difficulty = st.selectbox("難易度を選択してください", ["初心者向け", "中級者向け", "上級者向け"])

# フリーテキスト入力欄
custom_exercise = st.text_area("自分で問題を入力する場合はこちらに記述してください", key="quiz_input")

# 「練習問題を作成」ボタンを追加
if st.button("練習問題を作成"):
    create_exercise(difficulty, custom_exercise)

# 問題の表示
display_message_history(st.session_state["quiz_msg"])

user_input = st.text_input("Python学習でお困りのことがあればぜひ相談してください。", key="user_input", on_change=chat)

# メッセージ履歴の表示
display_message_history(st.session_state["plain_msg"])

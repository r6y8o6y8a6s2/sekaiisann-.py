import streamlit as st

# ページ設定
st.set_page_config(
    page_title="世界遺産 4択クイズ",
    page_icon="🏛️",
    layout="centered"
)

# --- クイズデータ（ここに問題を追加していくだけで増やせます） ---
QUIZ_DATA = [
    {
        "question": "問題(1) 古都奈良の文化財について、構成資産として正しいものはどれか。",
        "options": ["① 薬師寺", "② 延暦寺", "③ 金剛峯寺", "④ 鹿苑寺"],
        "answer": "① 薬師寺",
        "explanation": "正解は「① 薬師寺」です！延暦寺と鹿苑寺（金閣寺）は『古都京都の文化財』、金剛峯寺は『紀伊山地の霊場と参詣道』の構成資産です。"
    },
    {
        "question": "問題(2) 日本初の世界遺産（1993年登録）に含まれていないものはどれか。",
        "options": ["① 法隆寺地域の仏教建造物", "② 姫路城", "③ 屋久島", "④ 白川郷・五箇山の合掌造り集落"],
        "answer": "④ 白川郷・五箇山の合掌造り集落",
        "explanation": "1993年に日本初として登録されたのは、法隆寺、姫路城、屋久島、白神山地の4件です。白川郷は1995年に登録されました。"
    },
    {
        "question": "問題(3) 負の遺産（人類の悲劇を伝える遺産）に分類されるものはどれか。",
        "options": ["① 厳島神社", "② 原爆ドーム", "③ 富岡製糸場と絹産業遺産群", "④ 日光の社寺"],
        "answer": "② 原爆ドーム",
        "explanation": "原爆ドーム（広島平和記念碑）は、核兵器の惨禍を伝える負の遺産として1996年に登録されました。"
    }
]

# --- セッション状態（現在の問題番号・スコア・回答状況）の初期化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# タイトルと進捗バー
st.title("🏛️ 世界遺産 4択マスター")
st.progress((st.session_state.current_q) / len(QUIZ_DATA))
st.markdown("---")

# --- クイズ出題・判定ロジック ---
if st.session_state.current_q < len(QUIZ_DATA):
    q = QUIZ_DATA[st.session_state.current_q]
    
    # 問題文の表示
    st.subheader(q["question"])
    st.write("")

    # 四択ボタンの表示（2列×2行のグリッド配置で見やすく）
    col1, col2 = st.columns(2)
    for i, option in enumerate(q["options"]):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            # すでに回答済みの場合はボタンを無効化（二重押し防止）
            if st.button(option, key=f"opt_{i}", use_container_width=True, disabled=st.session_state.answered):
                st.session_state.answered = True
                st.session_state.selected_option = option
                if option == q["answer"]:
                    st.session_state.score += 1
                st.rerun()  # 画面を即座に更新して結果を表示

    # ボタンを押した直後の判定表示
    if st.session_state.answered:
        st.markdown("---")
        if st.session_state.selected_option == q["answer"]:
            st.success("🎉 **正解！**")
        else:
            st.error(f"😢 **不正解…** （あなたの回答: {st.session_state.selected_option}）")
        
        # 解説ボックス
        st.info(f"💡 **解説:** {q['explanation']}")

        # 次の問題へ進むボタン
        if st.button("次の問題へ ➡️", type="primary"):
            st.session_state.current_q += 1
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

# --- 全問終了後の結果画面 ---
else:
    st.balloons()
    st.header("🎊 全問終了！お疲れ様でした！")
    st.metric(label="最終スコア", value=f"{st.session_state.score} / {len(QUIZ_DATA)} 問正解")
    
    if st.button("最初からもう一度挑戦する 🔄", type="primary"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.rerun()

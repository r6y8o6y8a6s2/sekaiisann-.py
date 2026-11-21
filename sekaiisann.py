import random
import re
import time
from datetime import date, datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="世界遺産検定 4択マスター",
    page_icon="🏛️",
    layout="centered",
)

# --- CSSスタイル定義 ---
st.markdown("""
<style>
    .trivia-box {
        background-color: #f0f7ff;
        border-left: 5px solid #0d6efd;
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        color: #111827;
    }
    .correct-box {
        background-color: #d1e7dd;
        border-left: 5px solid #198754;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #0f5132;
    }
    .incorrect-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #842029;
    }
    .explanation-box {
        background-color: #e7f1ff;
        border-left: 5px solid #084298;
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        color: #052c65;
    }
    .pass-banner {
        background-color: #d1e7dd;
        border: 2px solid #198754;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        color: #0f5132;
        margin-bottom: 16px;
    }
    .fail-banner {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        color: #664d03;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

QUIZ_DATA = [
    {
        "question": "法隆寺地域の仏教建造物が日本で初めて世界遺産に登録された年はいつか。",
        "options": ["① 1985年", "② 1993年", "③ 1997年", "④ 2000年"],
        "answer": "② 1993年",
        "explanation": "正解は「1993年」です。姫路城とともに、日本で初めて世界遺産（文化遺産）に登録されました。",
        "tag": "登録年: 1993年 / 基準(i)(ii)(iv)(vi)",
        "trivia": "法隆寺の金堂や五重塔は、世界最古の木造建築群として知られています。"
    }
]


# --- ヘルパー関数：選択肢のシャッフル ---
def prepare_quiz_session(questions_list):
    prepared = []
    for q in questions_list:
        q_copy = q.copy()
        clean_options = [re.sub(r'^[①②③④]\s*', '', opt) for opt in q_copy["options"]]
        clean_answer = re.sub(r'^[①②③④]\s*', '', q_copy["answer"])

        random.shuffle(clean_options)

        prefixes = ["①", "②", "③", "④"]
        new_options = []
        new_answer = ""
        for idx, text in enumerate(clean_options):
            labeled_opt = f"{prefixes[idx]} {text}"
            new_options.append(labeled_opt)
            if text == clean_answer:
                new_answer = labeled_opt

        q_copy["options"] = new_options
        q_copy["answer"] = new_answer
        prepared.append(q_copy)
    return prepared


# --- セッション状態の初期化 ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "home"
if "shuffled_quiz" not in st.session_state:
    st.session_state.shuffled_quiz = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []
if "bookmarked_questions" not in st.session_state:
    st.session_state.bookmarked_questions = set()
if "history" not in st.session_state:
    st.session_state.history = []
if "mode_label" not in st.session_state:
    st.session_state.mode_label = ""
if "is_mock_exam" not in st.session_state:
    st.session_state.is_mock_exam = False
if "quiz_results_log" not in st.session_state:
    st.session_state.quiz_results_log = []
if "forgetting_curve_log" not in st.session_state:
    st.session_state.forgetting_curve_log = {}
if "study_dates" not in st.session_state:
    st.session_state.study_dates = {str(date.today())}

# タイトル
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 世界遺産検定 4択マスター</h2>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 1. ホーム画面
# ==========================================
if st.session_state.app_mode == "home":
    if "daily_trivia" not in st.session_state:
        st.session_state.daily_trivia = random.choice(QUIZ_DATA)

    dt = st.session_state.daily_trivia
    st.markdown(f"""
        <div class="trivia-box">
            <b>💡 本日の世界遺産トリビア</b><br>
            {dt['trivia']}
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 学習メニューを選択")

    if st.button("🎓 本番模擬試験をスタート（全問）", type="primary", use_container_width=True):
        mock_list = QUIZ_DATA.copy()
        random.shuffle(mock_list)
        st.session_state.shuffled_quiz = prepare_quiz_session(mock_list)
        st.session_state.app_mode = "quiz"
        st.session_state.mode_label = "🎓 本番模擬試験モード（合格ライン70%）"
        st.session_state.is_mock_exam = True
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.wrong_questions = []
        st.session_state.quiz_results_log = []
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.rerun()

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        wrong_count = len(st.session_state.wrong_questions)
        if st.button(f"❌ 間違い復習 ({wrong_count}問)", disabled=(wrong_count == 0), use_container_width=True):
            review_list = st.session_state.wrong_questions.copy()
            random.shuffle(review_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(review_list)
            st.session_state.app_mode = "quiz"
            st.session_state.mode_label = "🔄 間違い復習モード"
            st.session_state.is_mock_exam = False
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.quiz_results_log = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

    with col2:
        bm_count = len(st.session_state.bookmarked_questions)
        if st.button(f"⭐ ブックマーク ({bm_count}問)", disabled=(bm_count == 0), use_container_width=True):
            bm_list = [q for q in QUIZ_DATA if q["question"] in st.session_state.bookmarked_questions]
            random.shuffle(bm_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(bm_list)
            st.session_state.app_mode = "quiz"
            st.session_state.mode_label = "⭐ ブックマーク復習モード"
            st.session_state.is_mock_exam = False
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.quiz_results_log = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

    with col3:
        fc_due_list = [q for q in QUIZ_DATA if q["question"] in st.session_state.forgetting_curve_log]
        if st.button(f"🧠 忘却曲線復習 ({len(fc_due_list)}問)", disabled=(len(fc_due_list) == 0), use_container_width=True):
            random.shuffle(fc_due_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(fc_due_list)
            st.session_state.app_mode = "quiz"
            st.session_state.mode_label = "🧠 忘却曲線・最適復習モード"
            st.session_state.is_mock_exam = False
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.quiz_results_log = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

# ==========================================
# 2. クイズ・模擬試験プレイ画面
# ==========================================
elif st.session_state.app_mode == "quiz":
    active_quiz = st.session_state.shuffled_quiz
    st.caption(f"【{st.session_state.mode_label}】")

    if st.session_state.current_q < len(active_quiz):
        q = active_quiz[st.session_state.current_q]

        TIMELIMIT = 20
        if "start_time" not in st.session_state or st.session_state.get("current_q_tracked") != st.session_state.current_q:
            st.session_state.start_time = time.time()
            st.session_state.current_q_tracked = st.session_state.current_q

        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, TIMELIMIT - elapsed)

        if remaining == 0 and not st.session_state.answered:
            st.session_state.answered = True
            st.session_state.selected_option = "時間切れ"
            orig_q = next((item for item in QUIZ_DATA if item["question"] == q["question"]), q)
            if orig_q not in st.session_state.wrong_questions:
                st.session_state.wrong_questions.append(orig_q)
            st.session_state.forgetting_curve_log[q["question"]] = str(datetime.now())

            st.session_state.quiz_results_log.append({
                "question": q["question"], "user_answer": "時間切れ", "correct_answer": q["answer"],
                "is_correct": False, "explanation": q["explanation"]
            })
            st.rerun()

        st.markdown(f"⏱️ **制限時間残り: {remaining}秒 / 20秒**")
        st.progress(remaining / TIMELIMIT)

        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
        with top_col2:
            is_bm = q["question"] in st.session_state.bookmarked_questions
            bm_label = "⭐ 登録済" if is_bm else "☆ ブックマーク"
            if st.button(bm_label, key=f"bm_{st.session_state.current_q}", use_container_width=True):
                if is_bm:
                    st.session_state.bookmarked_questions.remove(q["question"])
                else:
                    st.session_state.bookmarked_questions.add(q["question"])
                st.rerun()

        st.markdown(f"**{q['question']}**")
        st.write("")

        col1, col2 = st.columns(2)
        for i, option in enumerate(q["options"]):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                if st.button(option, key=f"opt_{i}_{st.session_state.current_q}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.selected_option = option

                    is_correct = (option[:1] == q["answer"][:1])
                    if is_correct:
                        st.session_state.score += 1
                        if q["question"] in st.session_state.forgetting_curve_log:
                            del st.session_state.forgetting_curve_log[q["question"]]
                    else:
                        orig_q = next((item for item in QUIZ_DATA if item["question"] == q["question"]), q)
                        if orig_q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(orig_q)
                        st.session_state.forgetting_curve_log[q["question"]] = str(datetime.now())

                    st.session_state.quiz_results_log.append({
                        "question": q["question"], "user_answer": option, "correct_answer": q["answer"],
                        "is_correct": is_correct, "explanation": q["explanation"]
                    })
                    st.rerun()

        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option == "時間切れ":
                st.markdown(f'<div class="incorrect-box">⏰ <b>時間切れです！</b> 正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)
            elif st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="explanation-box">
                    <b>💡 解説:</b> {q['explanation']}<br><br>
                    <span style="font-size: 0.9em; background-color: #ffffff; padding: 3px 6px; border-radius: 4px; color: #084298;">📌 <b>検定ポイント:</b> {q['tag']}</span>
                </div>
            """, unsafe_allow_html=True)

            if st.button("次の問題へ ➡️", type="primary"):
                st.session_state.current_q += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()
        else:
            time.sleep(1)
            st.rerun()

    # ==========================================
    # 3. 結果発表画面
    # ==========================================
    else:
        total_len = len(active_quiz)
        accuracy = round((st.session_state.score / total_len) * 100, 1) if total_len > 0 else 0

        if st.session_state.is_mock_exam:
            st.header("🎓 本番模擬試験 結果発表")
            if accuracy >= 70.0:
                st.balloons()
                st.markdown(f"""
                    <div class="pass-banner">
                        <h2>🎉 合格圏内クリア！おめでとうございます！</h2>
                        <p style="font-size: 1.2em;">得点率: <b>{accuracy}%</b>（合格基準 70%以上）</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="fail-banner">
                        <h2>💪 合格ラインまであと一歩！</h2>
                        <p style="font-size: 1.2em;">得点率: <b>{accuracy}%</b>（合格基準 70%以上）</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.balloons()
            st.header("🎊 お疲れ様でした！結果発表")

        st.metric(label="獲得スコア / 正答率", value=f"{st.session_state.score} / {total_len} 問正解 ({accuracy}%)")

        if not st.session_state.get("history_recorded", False):
            attempt_num = len(st.session_state.history) + 1
            st.session_state.history.append({"回数": f"{attempt_num}回目", "正答率(%)": accuracy})
            st.session_state.study_dates.add(str(date.today()))
            st.session_state.history_recorded = True

        st.markdown("---")
        st.subheader("📋 今回の全問レビュー（答え合わせ）")
        for idx, log in enumerate(st.session_state.quiz_results_log):
            status = "🟢 正解" if log["is_correct"] else "🔴 不正解"
            with st.expander(f"第{idx+1}問: {status} - {log['question'][:30]}..."):
                st.write(f"**問題:** {log['question']}")
                st.write(f"あなたの回答: {log['user_answer']}")
                st.write(f"正しい答え: **{log['correct_answer']}**")
                st.info(f"解説: {log['explanation']}")

        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 ホーム画面に戻る", type="primary", use_container_width=True):
                st.session_state.app_mode = "home"
                st.session_state.history_recorded = False
                st.rerun()
        with col2:
            wrong_cnt = len(st.session_state.wrong_questions)
            if st.button(f"❌ 間違い復習 ({wrong_cnt}問)", disabled=(wrong_cnt == 0), use_container_width=True):
                review_list = st.session_state.wrong_questions.copy()
                random.shuffle(review_list)
                st.session_state.shuffled_quiz = prepare_quiz_session(review_list)
                st.session_state.app_mode = "quiz"
                st.session_state.mode_label = "🔄 間違い復習モード"
                st.session_state.is_mock_exam = False
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.wrong_questions = []
                st.session_state.quiz_results_log = []
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.session_state.history_recorded = False
                st.rerun()

import streamlit as st
import pandas as pd
import random
import re
import time
from datetime import datetime, date, timedelta

# ページ設定
st.set_page_config(
    page_title="世界遺産 4択マスター（プロ仕様・完全版）",
    page_icon="🏛️",
    layout="centered"
)

# --- 🌙 / ☀️ 動的テーマカラー（ダークモード対応） ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    bg_color = "#1e1e1e"
    card_bg = "#2d2d2d"
    text_color = "#f8f9fa"
    border_color = "#444444"
    correct_bg = "#0f5132"
    incorrect_bg = "#842029"
    expl_bg = "#084298"
else:
    bg_color = "#ffffff"
    card_bg = "#f8f9fa"
    text_color = "#212529"
    border_color = "#dee2e6"
    correct_bg = "#d1e7dd"
    incorrect_bg = "#f8d7da"
    expl_bg = "#cfe2ff"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .correct-box {{ padding: 15px; border-radius: 8px; background-color: {correct_bg}; color: {'#ffffff' if st.session_state.dark_mode else '#0f5132'}; margin-bottom: 10px; }}
    .incorrect-box {{ padding: 15px; border-radius: 8px; background-color: {incorrect_bg}; color: {'#ffffff' if st.session_state.dark_mode else '#842029'}; margin-bottom: 10px; }}
    .explanation-box {{ padding: 15px; border-radius: 8px; background-color: {expl_bg}; color: {'#ffffff' if st.session_state.dark_mode else '#084298'}; margin-bottom: 15px; }}
    .trivia-box {{ padding: 15px; border-radius: 8px; background-color: #fff3cd; color: #664d03; margin-bottom: 20px; border-left: 5px solid #ffc107; }}
    .flashcard {{ padding: 30px; border-radius: 12px; background-color: {card_bg}; border: 2px solid {border_color}; text-align: center; margin-bottom: 20px; }}
    .pass-banner {{ padding: 20px; border-radius: 10px; background-color: {correct_bg}; color: {'#ffffff' if st.session_state.dark_mode else '#0f5132'}; text-align: center; border: 2px solid #198754; margin-bottom: 15px; }}
    .fail-banner {{ padding: 20px; border-radius: 10px; background-color: {incorrect_bg}; color: {'#ffffff' if st.session_state.dark_mode else '#842029'}; text-align: center; border: 2px solid #dc3545; margin-bottom: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 🗺️ 日本の世界遺産 位置データ（マップ表示用） ---
JAPAN_HERITAGE_MAP = [
    {"name": "知床", "region": "北海道・東北", "type": "自然遺産", "year": 2005, "lat": 44.0933, "lon": 145.1219},
    {"name": "北海道・北東北の縄文遺跡群（三内丸山遺跡）", "region": "北海道・東北", "type": "文化遺産", "year": 2021, "lat": 40.8114, "lon": 140.6975},
    {"name": "白神山地", "region": "北海道・東北", "type": "自然遺産", "year": 1993, "lat": 40.4714, "lon": 140.1303},
    {"name": "平泉－仏国土（浄土）を表現する建築・庭園及び考古学的遺跡群", "region": "北海道・東北", "type": "文化遺産", "year": 2011, "lat": 39.0014, "lon": 141.1083},
    {"name": "日光の社寺", "region": "関東", "type": "文化遺産", "year": 1999, "lat": 36.7581, "lon": 139.5989},
    {"name": "富岡製糸場と絹産業遺産群", "region": "関東", "type": "文化遺産", "year": 2014, "lat": 36.2553, "lon": 138.8878},
    {"name": "小笠原諸島", "region": "関東", "type": "自然遺産", "year": 2011, "lat": 27.0944, "lon": 142.1917},
    {"name": "国立西洋美術館（ル・コルビュジエの建築作品）", "region": "関東", "type": "文化遺産", "year": 2016, "lat": 35.7154, "lon": 139.7758},
    {"name": "佐渡島の金山", "region": "中部", "type": "文化遺産", "year": 2024, "lat": 38.0422, "lon": 138.2589},
    {"name": "白川郷・五箇山の合掌造り集落", "region": "中部", "type": "文化遺産", "year": 1995, "lat": 36.2569, "lon": 136.9061},
    {"name": "富士山－信仰の対象と芸術の源泉", "region": "中部", "type": "文化遺産", "year": 2013, "lat": 35.3606, "lon": 138.7274},
    {"name": "古都京都の文化財", "region": "近畿", "type": "文化遺産", "year": 1994, "lat": 35.0394, "lon": 135.7292},
    {"name": "古都奈良の文化財", "region": "近畿", "type": "文化遺産", "year": 1998, "lat": 34.6890, "lon": 135.8398},
    {"name": "法隆寺地域の仏教建造物", "region": "近畿", "type": "文化遺産", "year": 1993, "lat": 34.6142, "lon": 135.7356},
    {"name": "姫路城", "region": "近畿", "type": "文化遺産", "year": 1993, "lat": 34.8394, "lon": 134.6939},
    {"name": "紀伊山地の霊場と参詣道", "region": "近畿", "type": "文化遺産", "year": 2004, "lat": 33.8403, "lon": 135.7736},
    {"name": "百舌鳥・古市古墳群", "region": "近畿", "type": "文化遺産", "year": 2019, "lat": 34.5547, "lon": 135.4875},
    {"name": "石見銀山遺跡とその文化的景観", "region": "中国・四国", "type": "文化遺産", "year": 2007, "lat": 35.1069, "lon": 132.4367},
    {"name": "原爆ドーム", "region": "中国・四国", "type": "文化遺産", "year": 1996, "lat": 34.3955, "lon": 132.4536},
    {"name": "厳島神社", "region": "中国・四国", "type": "文化遺産", "year": 1996, "lat": 34.2961, "lon": 132.3197},
    {"name": "「神宿る島」宗像・沖ノ島と関連遺産群", "region": "九州・沖縄", "type": "文化遺産", "year": 2017, "lat": 34.2414, "lon": 130.1044},
    {"name": "明治日本の産業革命遺産（軍艦島など）", "region": "九州・沖縄", "type": "文化遺産", "year": 2015, "lat": 32.6278, "lon": 129.7386},
    {"name": "長崎と天草地方の潜伏キリシタン関連遺産", "region": "九州・沖縄", "type": "文化遺産", "year": 2018, "lat": 32.7342, "lon": 129.8703},
    {"name": "屋久島", "region": "九州・沖縄", "type": "自然遺産", "year": 1993, "lat": 30.3586, "lon": 130.5283},
    {"name": "奄美大島、徳之島、沖縄島北部及び西表島", "region": "九州・沖縄", "type": "自然遺産", "year": 2021, "lat": 28.2931, "lon": 129.3667},
    {"name": "琉球王国のグスク及び関連遺産群", "region": "九州・沖縄", "type": "文化遺産", "year": 2000, "lat": 26.2170, "lon": 127.7195},
]

# --- セッション状態の初期データベース管理 ---
if "quiz_master_data" not in st.session_state:
    st.session_state.quiz_master_data = [
        {
            "id": 1, "category": "🏛️ 寺社・建築", "difficulty": "標準",
            "question": "法隆寺地域の仏教建造物が日本で初めて世界遺産に登録された年はいつか。",
            "options": ["① 1985年", "② 1993年", "③ 1997年", "④ 2000年"],
            "answer": "② 1993年",
            "explanation": "正解は「1993年」です。姫路城とともに、日本で初めて世界遺産（文化遺産）に登録されました。",
            "tag": "登録年: 1993年 / 基準(i)(ii)(iv)(vi)", "trivia": "法隆寺の金堂や五重塔は、世界最古の木造建築群として知られています。"
        },
        {
            "id": 2, "category": "🏛️ 寺社・建築", "difficulty": "基礎",
            "question": "姫路城の別称として正しいものはどれか。",
            "options": ["① 烏城", "② 鶴ヶ城", "③ 白鷺城", "④ 金城"],
            "answer": "③ 白鷺城",
            "explanation": "正解は「白鷺城（しらさぎじょう）」です。鮮やかな白漆喰の壁が羽を広げた白鷺に例えられます。",
            "tag": "登録年: 1993年 / 基準(i)(iv)", "trivia": "姫路城の大天守は、江戸時代初期の優れた城郭建築の最高傑作です。"
        },
        {
            "id": 3, "category": "🏛️ 寺社・建築", "difficulty": "標準",
            "question": "古都京都の文化財の構成資産に含まれない寺社・城郭はどれか。",
            "options": ["① 清水寺", "② 二条城", "③ 東大寺", "④ 下鴨神社"],
            "answer": "③ 東大寺",
            "explanation": "正解は「東大寺」です。東大寺は「古都奈良の文化財」の構成資産です。",
            "tag": "登録年: 1994年 / 基準(ii)(iv)", "trivia": "古都京都の文化財は、京都市・宇治市・大津市にまたがる17の資産で構成されています。"
        },
        {
            "id": 4, "category": "🏛️ 寺社・建築", "difficulty": "標準",
            "question": "白川郷・五箇山の合掌造り集落において、特徴的な急勾配の屋根の角度はおおよそ何度か。",
            "options": ["① 30〜40度", "② 45〜60度", "③ 70〜80度", "④ 90度"],
            "answer": "② 45〜60度",
            "explanation": "正解は「45〜60度」です。豪雪地帯の重い雪が滑り落ちやすいように急勾配になっています。",
            "tag": "登録年: 1995年 / 基準(iv)(v)", "trivia": "合掌造りの屋根裏は、かつて重要な産業であった養蚕の作業場として利用されていました。"
        },
        {
            "id": 5, "category": "🏛️ 寺社・建築", "difficulty": "難問",
            "question": "厳島神社（広島県）の社殿が海上に建てられている理由として正しいものはどれか。",
            "options": ["① 津波を防ぐため", "② 島全体が神域のため", "③ 海上交通の目印", "④ 要塞にするため"],
            "answer": "② 島全体が神域のため",
            "explanation": "弥山全体がご神体として信仰されていたため、大地を傷つけぬよう海上に造られました。",
            "tag": "登録年: 1996年 / 基準(i)(ii)(iv)", "trivia": "満潮時には社殿や大鳥居が海に浮かんでいるように見える、世界でも珍しい神社です。"
        },
        {
            "id": 6, "category": "🌲 自然遺産", "difficulty": "基礎",
            "question": "屋久島に自生する樹齢数千年を超える代表的な植物はどれか。",
            "options": ["① ブナの巨木", "② 屋久杉（スギ）", "③ ヒノキの古木", "④ 天然のマツ"],
            "answer": "② 屋久杉（スギ）",
            "explanation": "正解は「屋久杉（スギ）」です。標高500mを超える山地に自生しており、ユネスコ自然遺産に登録されています。",
            "tag": "登録年: 1993年 / 基準(vii)(ix)", "trivia": "屋久島は豊かな降水量に恵まれ、独特の垂直分布を持つ生態系が広がっています。"
        },
        {
            "id": 7, "category": "🌲 自然遺産", "difficulty": "標準",
            "question": "白神山地が世界自然遺産に登録される決め手となった、原生的な森林を構成する樹木はどれか。",
            "options": ["① アカマツ", "② スギ林", "③ ブナの原生林", "④ カエデの林"],
            "answer": "③ ブナの原生林",
            "explanation": "正解は「ブナの原生林」です。人手の加わっていない世界最大級のブナ林が残されていることが評価されました。",
            "tag": "登録年: 1993年 / 基準(ix)", "trivia": "白神山地は青森県と秋田県にまたがる広大な山地です。"
        },
        {
            "id": 8, "category": "📜 歴史・条約", "difficulty": "標準",
            "question": "原爆ドーム（広島平和記念碑）の設計を手掛けた建築家の出身国はどこか。",
            "options": ["① チェコ", "② ドイツ", "③ フランス", "④ イギリス"],
            "answer": "① チェコ",
            "explanation": "正解は「チェコ」です。チェコ人の建築家ヤン・レッツェルによって設計されました。",
            "tag": "登録年: 1996年 / 基準(vi)", "trivia": "原爆ドームは核兵器の惨禍を今に伝える負の歴史の象徴です。"
        },
        {
            "id": 9,
            "category": "📜 歴史・条約",
            "difficulty": "基礎",
            "question": "世界遺産条約が採択された年はいつか。",
            "options": ["① 1945年", "② 1972年", "③ 1992年", "④ 2003年"],
            "answer": "② 1972年",
            "explanation": "正解は「1972年」のユネスコ総会で採択されました。",
            "tag": "ユネスコ総会での採択年", "trivia": "正式名称は「世界の文化及び自然遺産の保護に関する条約」です。"
        },
        {
            "id": 10,
            "category": "📅 年代・基準・制度",
            "difficulty": "標準",
            "question": "世界遺産の登録基準において、文化遺産の基準の数はいくつあるか。",
            "options": ["① 4つ（(i)〜(iv)）", "② 6つ（(i)〜(vi)）", "③ 10つ（(i)〜(x)）", "④ 12つ"],
            "answer": "② 6つ（(i)〜(vi)）",
            "explanation": "正解は「6つ（(i)〜(vi)」です。自然遺産の基準は4つであり、合わせて10個の基準があります。",
            "tag": "検定頻出：登録基準の数", "trivia": "文化遺産は(i)〜(vi)、自然遺産は(vii)〜(x)の基準が設けられています。"
        }
    ]

QUIZ_DATA = st.session_state.quiz_master_data

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

# --- その他のセッション状態の初期化 ---
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "home" # "home", "quiz", "flashcard", "map", "creator"
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
if "bookmarked_ids" not in st.session_state:
    st.session_state.bookmarked_ids = set()
if "history" not in st.session_state:
    st.session_state.history = []
if "category_mistakes" not in st.session_state:
    st.session_state.category_mistakes = {}
if "mode_label" not in st.session_state:
    st.session_state.mode_label = ""
if "is_mock_exam" not in st.session_state:
    st.session_state.is_mock_exam = False
if "quiz_results_log" not in st.session_state:
    st.session_state.quiz_results_log = []
# 暗記カード用
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = False
if "mastered_card_ids" not in st.session_state:
    st.session_state.mastered_card_ids = set()
if "fc_filter_unmastered" not in st.session_state:
    st.session_state.fc_filter_unmastered = False
# 忘却曲線スケジュール用（問題IDごとに間違えた日付を保存）
if "forgetting_curve_log" not in st.session_state:
    st.session_state.forgetting_curve_log = {} # {id: datetime_str}
# ストリーク
if "study_dates" not in st.session_state:
    st.session_state.study_dates = {str(date.today())}

# ==========================================
# サイドバー（ダッシュボード・テーマ切替・忘却曲線アラート）
# ==========================================
st.sidebar.title("📊 学習ダッシュボード")

# 機能4：ダークモード / ライトモード切替
is_dark = st.sidebar.toggle("🌙 ダークモードに切り替え", value=st.session_state.dark_mode)
if is_dark != st.session_state.dark_mode:
    st.session_state.dark_mode = is_dark
    st.rerun()

st.sidebar.markdown("---")

total_sets = len(st.session_state.history)
streak_days = len(st.session_state.study_dates)

if total_sets == 0:
    rank_title = "🌱 世界遺産ビギナー"
elif total_sets < 3:
    rank_title = "🥉 遺産トラベラー"
elif total_sets < 7:
    rank_title = "🥈 検定チャレンジャー"
else:
    rank_title = "👑 世界遺産マイスター"

st.sidebar.markdown(f"**現在のランク:** {rank_title}")
st.sidebar.markdown(f"🔥 **連続学習記録:** {streak_days} 日目（累計 {total_sets} セット）")

# 機能2：忘却曲線に基づく復習アラート
due_review_count = len(st.session_state.forgetting_curve_log)
if due_review_count > 0:
    st.sidebar.warning(f"🧠 忘却曲線アラート: 復習適齢期の問題が **{due_review_count}問** あります！")

st.sidebar.markdown("---")

if st.session_state.app_mode == "quiz":
    total_q = len(st.session_state.shuffled_quiz)
    current_progress = st.session_state.current_q
    st.sidebar.metric(label="現在の進捗", value=f"{current_progress} / {total_q} 問")
    st.sidebar.progress(current_progress / total_q if total_q > 0 else 0)
    st.sidebar.markdown(f"**現在のスコア:** {st.session_state.score} 点")

st.sidebar.subheader("📈 成績推移（正答率）")
if len(st.session_state.history) > 0:
    df_hist = pd.DataFrame(st.session_state.history)
    st.sidebar.line_chart(df_hist.set_index("回数")["正答率(%)"])
else:
    st.sidebar.caption("履歴がここにグラフ化されます。")

st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ 分野別・弱点分析")
if len(st.session_state.category_mistakes) > 0:
    df_mistakes = pd.DataFrame(list(st.session_state.category_mistakes.items()), columns=["分野", "ミス回数"])
    st.sidebar.bar_chart(df_mistakes.set_index("分野"))
else:
    st.sidebar.caption("ミスした分野が自動集計されます。")

# タイトル
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 世界遺産検定 4択マスター（プロ仕様）</h2>', unsafe_allow_html=True)
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
            <b>💡 本日の世界遺産トリビア（{dt['category']}）</b><br>
            {dt['trivia']}
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 プロ仕様 学習メニュー")
    
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🎓 本番模擬試験", type="primary", use_container_width=True):
            mock_list = QUIZ_DATA.copy()
            random.shuffle(mock_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(mock_list[:min(30, len(mock_list))])
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
    with col_nav2:
        if st.button("📇 暗記カード", use_container_width=True):
            st.session_state.app_mode = "flashcard"
            st.session_state.flashcard_index = 0
            st.session_state.flashcard_flipped = False
            st.rerun()
    with col_nav3:
        if st.button("🗺️ 遺産マップ", use_container_width=True):
            st.session_state.app_mode = "map"
            st.rerun()
    with col_nav4:
        if st.button("✍️ 問題作成", use_container_width=True):
            st.session_state.app_mode = "creator"
            st.rerun()

    st.markdown("---")
    st.subheader("⚙️ カスタム練習クイズ")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        categories = ["すべて"] + list(dict.fromkeys([q["category"] for q in QUIZ_DATA]))
        selected_category = st.selectbox("📚 分野・ジャンル：", categories)
    with col_f2:
        difficulties = ["すべて", "基礎", "標準", "難問"]
        selected_diff = st.selectbox("🎖️ 難易度レベル：", difficulties)
    
    mode = st.radio(
        "📝 挑戦する問題数：",
        ["サクッと10問", "ハーフ20問", "全問網羅"],
        horizontal=True
    )
    
    st.write("")
    
    if st.button("🚀 カスタムクイズをスタート！", use_container_width=True):
        filtered_data = QUIZ_DATA.copy()
        if selected_category != "すべて":
            filtered_data = [q for q in filtered_data if q["category"] == selected_category]
        if selected_diff != "すべて":
            filtered_data = [q for q in filtered_data if q["difficulty"] == selected_diff]
        
        if not filtered_data:
            st.warning("条件に一致する問題がありません！")
        else:
            if "10問" in mode:
                limit = min(10, len(filtered_data))
            elif "20問" in mode:
                limit = min(20, len(filtered_data))
            else:
                limit = len(filtered_data)
            
            random.shuffle(filtered_data)
            st.session_state.shuffled_quiz = prepare_quiz_session(filtered_data[:limit])
            st.session_state.app_mode = "quiz"
            st.session_state.mode_label = "カスタム練習モード"
            st.session_state.is_mock_exam = False
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
        bm_count = len(st.session_state.bookmarked_ids)
        if st.button(f"⭐ ブックマーク ({bm_count}問)", disabled=(bm_count == 0), use_container_width=True):
            bm_list = [q for q in QUIZ_DATA if q["id"] in st.session_state.bookmarked_ids]
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
        fc_due_list = [q for q in QUIZ_DATA if q["id"] in st.session_state.forgetting_curve_log]
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
# 2. 🗺️ マップビュワー
# ==========================================
elif st.session_state.app_mode == "map":
    st.subheader("🗺️ 日本の世界遺産 エリア＆マップビュワー")
    df_map = pd.DataFrame(JAPAN_HERITAGE_MAP)
    
    regions = ["すべて"] + list(dict.fromkeys(df_map["region"].tolist()))
    sel_region = st.selectbox("📍 表示する地方エリア：", regions)
    
    df_filtered = df_map if sel_region == "すべて" else df_map[df_map["region"] == sel_region]
    
    st.map(df_filtered[["lat", "lon"]])
    st.dataframe(
        df_filtered[["name", "region", "type", "year"]].rename(
            columns={"name": "世界遺産名", "region": "地方", "type": "種別", "year": "登録年"}
        ),
        use_container_width=True, hide_index=True
    )
    
    if st.button("🏠 ホームに戻る", type="primary", use_container_width=True):
        st.session_state.app_mode = "home"
        st.rerun()

# ==========================================
# 3. ✍️ マイ問題帳（オリジナル問題追加機能）
# ==========================================
elif st.session_state.app_mode == "creator":
    st.subheader("✍️ マイ問題帳（オリジナル問題の作成）")
    st.caption("自分でひっかけ問題や覚えたい知識を入力し、問題集をカスタマイズできます！")
    
    with st.form("custom_quiz_form"):
        new_q = st.text_input("問題文：")
        new_cat = st.selectbox("分野：", ["🏛️ 寺社・建築", "🌲 自然遺産", "📜 歴史・条約", "📅 年代・基準・制度"])
        new_diff = st.selectbox("難易度：", ["基礎", "標準", "難問"])
        
        st.markdown("**4つの選択肢（※18文字以内を推奨）**")
        opt1 = st.text_input("選択肢①", value="① ")
        opt2 = st.text_input("選択肢②", value="② ")
        opt3 = st.text_input("選択肢③", value="③ ")
        opt4 = st.text_input("選択肢④", value="④ ")
        
        correct_opt = st.selectbox("正解の選択肢：", [opt1, opt2, opt3, opt4])
        new_expl = st.text_area("解説文：")
        new_tag = st.text_input("検定ポイント（タグ）：", value="オリジナル問題 / 登録年: 2026年")
        new_trivia = st.text_input("トリビア（豆知識）：", value="自分が作ったオリジナル問題です！")
        
        submitted = st.form_submit_button("📥 問題を追加して保存する", type="primary")
        if submitted:
            if new_q and opt1 and opt2 and opt3 and opt4:
                new_id = max([item["id"] for item in st.session_state.quiz_master_data]) + 1
                custom_item = {
                    "id": new_id,
                    "category": new_cat,
                    "difficulty": new_diff,
                    "question": new_q,
                    "options": [opt1, opt2, opt3, opt4],
                    "answer": correct_opt,
                    "explanation": new_expl,
                    "tag": new_tag,
                    "trivia": new_trivia
                }
                st.session_state.quiz_master_data.append(custom_item)
                st.success("🎉 新しい問題がデータベースに正常に追加されました！")
            else:
                st.error("問題文とすべての選択肢を入力してください。")

    st.write("")
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.session_state.app_mode = "home"
        st.rerun()

# ==========================================
# 4. 📇 暗記カードモード
# ==========================================
elif st.session_state.app_mode == "flashcard":
    st.subheader("📇 暗記カードモード（音声読み上げ対応）")
    
    mastered_cnt = len(st.session_state.mastered_card_ids)
    total_cnt = len(QUIZ_DATA)
    st.progress(mastered_cnt / total_cnt)
    st.caption(f"習得状況: {mastered_cnt} / {total_cnt} 枚 習得済み")
    
    filter_unmastered = st.checkbox("🔴 「まだ怪しい」カードだけ表示", value=st.session_state.fc_filter_unmastered)
    if filter_unmastered != st.session_state.fc_filter_unmastered:
        st.session_state.fc_filter_unmastered = filter_unmastered
        st.session_state.flashcard_index = 0
        st.session_state.flashcard_flipped = False
        st.rerun()
        
    fc_list = [q for q in QUIZ_DATA if q["id"] not in st.session_state.mastered_card_ids] if st.session_state.fc_filter_unmastered else QUIZ_DATA

    if not fc_list:
        st.success("🎉 すべてのカードを習得しました！")
        if st.button("🏠 ホームに戻る", type="primary"):
            st.session_state.app_mode = "home"
            st.rerun()
    else:
        idx = st.session_state.flashcard_index % len(fc_list)
        card = fc_list[idx]
        is_mastered = card["id"] in st.session_state.mastered_card_ids
        status_badge = "🟢 習得済み" if is_mastered else "🔴 未習得"
        
        st.markdown(f"**カード {idx+1} / {len(fc_list)}** | `{card['category']}` | {status_badge}")
        
        # 機能1：音声読み上げ（JavaScript Web Speech API連携）
        speech_text = card['question'] if not st.session_state.flashcard_flipped else f"正解は、{card['answer']}。解説、{card['explanation']}"
        st.markdown(f"""
            <script>
            function speakText() {{
                const text = "{speech_text}";
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'ja-JP';
                window.speechSynthesis.speak(utterance);
            }}
            </script>
        """, unsafe_allow_html=True)
        
        if not st.session_state.flashcard_flipped:
            st.markdown(f"""
                <div class="flashcard">
                    <h3>❓ 問題・テーマ</h3>
                    <p style="font-size: 1.25em; font-weight: bold; margin-top: 20px;">{card['question']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_f_btn1, col_f_btn2 = st.columns(2)
            with col_f_btn1:
                if st.button("🔄 答えを見る", type="primary", use_container_width=True):
                    st.session_state.flashcard_flipped = True
                    st.rerun()
            with col_f_btn2:
                st.markdown('<button onclick="speakText()" style="width:100%; height:40px; border-radius:5px; background-color:#ffc107; border:none; font-weight:bold; cursor:pointer;">🔊 音声で聴く</button>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="flashcard">
                    <h3>🎉 正解・重要ポイント</h3>
                    <p style="font-size: 1.25em; font-weight: bold; color: #198754; margin-top: 15px;">正解: {card['answer']}</p>
                    <p style="margin-top: 15px;"><b>解説:</b> {card['explanation']}</p>
                    <p style="margin-top: 10px; font-size: 0.9em; color: #0d6efd;">📌 {card['tag']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.button("🟢 完璧に覚えた！", use_container_width=True):
                    st.session_state.mastered_card_ids.add(card["id"])
                    st.session_state.flashcard_index = (idx + 1) % max(1, len(fc_list))
                    st.session_state.flashcard_flipped = False
                    st.rerun()
            with col_s2:
                if st.button("🔴 まだ怪しい…", use_container_width=True):
                    if card["id"] in st.session_state.mastered_card_ids:
                        st.session_state.mastered_card_ids.remove(card["id"])
                    st.session_state.flashcard_index = (idx + 1) % max(1, len(fc_list))
                    st.session_state.flashcard_flipped = False
                    st.rerun()
                
        st.write("")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            if st.button("⬅️ 前のカード", use_container_width=True):
                st.session_state.flashcard_index = (idx - 1) % len(fc_list)
                st.session_state.flashcard_flipped = False
                st.rerun()
        with col_c2:
            if st.button("🏠 ホームに戻る", use_container_width=True):
                st.session_state.app_mode = "home"
                st.rerun()
        with col_c3:
            if st.button("次のカード ➡️", use_container_width=True):
                st.session_state.flashcard_index = (idx + 1) % len(fc_list)
                st.session_state.flashcard_flipped = False
                st.rerun()

# ==========================================
# 5. クイズ・模擬試験プレイ画面
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
            orig_q = next((item for item in QUIZ_DATA if item["id"] == q["id"]), q)
            if orig_q not in st.session_state.wrong_questions:
                st.session_state.wrong_questions.append(orig_q)
            st.session_state.category_mistakes[q['category']] = st.session_state.category_mistakes.get(q['category'], 0) + 1
            st.session_state.forgetting_curve_log[q["id"]] = str(datetime.now()) # 忘却曲線用に記録
            
            st.session_state.quiz_results_log.append({
                "question": q["question"], "user_answer": "時間切れ", "correct_answer": q["answer"],
                "is_correct": False, "explanation": q["explanation"]
            })
            st.rerun()

        st.markdown(f"⏱️ **制限時間残り: {remaining}秒 / 20秒**")
        st.progress(remaining / TIMELIMIT)

        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            st.markdown(f"### `{q['category']}` | 難易度: **{q['difficulty']}**")
        with top_col2:
            is_bm = q["id"] in st.session_state.bookmarked_ids
            bm_label = "⭐ 登録済" if is_bm else "☆ ブックマーク"
            if st.button(bm_label, key=f"bm_{q['id']}_{st.session_state.current_q}", use_container_width=True):
                if is_bm:
                    st.session_state.bookmarked_ids.remove(q["id"])
                else:
                    st.session_state.bookmarked_ids.add(q["id"])
                st.rerun()

        st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
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
                        # 正解したら忘却曲線ログから削除
                        if q["id"] in st.session_state.forgetting_curve_log:
                            del st.session_state.forgetting_curve_log[q["id"]]
                    else:
                        orig_q = next((item for item in QUIZ_DATA if item["id"] == q["id"]), q)
                        if orig_q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(orig_q)
                        st.session_state.category_mistakes[q['category']] = st.session_state.category_mistakes.get(q['category'], 0) + 1
                        st.session_state.forgetting_curve_log[q["id"]] = str(datetime.now()) # 忘却曲線スケジュール登録
                    
                    st.session_state.quiz_results_log.append({
                        "question": q["question"], "user_answer": option, "correct_answer": q["answer"],
                        "is_correct": is_correct, "explanation": q["explanation"]
                    })
                    st.rerun()

        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option == "時間切れ":
                st.markdown('<div class="incorrect-box">⏰ <b>時間切れです！</b> 正解は <b>%s</b> です。</div>' % q["answer"], unsafe_allow_html=True)
            elif st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="explanation-box">
                    <b>💡 解説:</b> {q['explanation']}<br><br>
                    <span style="font-size: 0.9em; background-color: rgba(255,255,255,0.2); padding: 3px 6px; border-radius: 4px;">📌 <b>検定ポイント:</b> {q['tag']}</span>
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
    # 6. 結果発表画面
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
        st.subheader("📊 弱点・分野別ミス分析レポート")
        if len(st.session_state.category_mistakes) > 0:
            df_m = pd.DataFrame(list(st.session_state.category_mistakes.items()), columns=["分野", "累積ミス回数"])
            st.bar_chart(df_m.set_index("分野"))

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

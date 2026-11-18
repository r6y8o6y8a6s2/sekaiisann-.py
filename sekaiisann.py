import streamlit as st
import pandas as pd
import random
import re
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="世界遺産 4択マスター（検定2級対策）",
    page_icon="🏛️",
    layout="centered"
)

# --- 💡 カスタムCSS ---
st.markdown("""
    <style>
    .correct-box { padding: 15px; border-radius: 8px; background-color: #d1e7dd; color: #0f5132; margin-bottom: 10px; }
    .incorrect-box { padding: 15px; border-radius: 8px; background-color: #f8d7da; color: #842029; margin-bottom: 10px; }
    .explanation-box { padding: 15px; border-radius: 8px; background-color: #cfe2ff; color: #084298; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- QUIZ_DATA（全選択肢18文字以内・全問題に一意のIDを付与） ---
QUIZ_DATA = [
    # --- 【分野：寺社・建築】 ---
    {
        "id": 1,
        "category": "🏛️ 寺社・建築",
        "question": "法隆寺地域の仏教建造物が日本で初めて世界遺産に登録された年はいつか。",
        "options": ["① 1985年", "② 1993年", "③ 1997年", "④ 2000年"],
        "answer": "② 1993年",
        "explanation": "正解は「1993年」です。姫路城とともに、日本で初めて世界遺産（文化遺産）に登録されました。",
        "tag": "登録年: 1993年 / 基準(i)(ii)(iv)(vi)"
    },
    {
        "id": 2,
        "category": "🏛️ 寺社・建築",
        "question": "姫路城の別称として正しいものはどれか。",
        "options": ["① 烏城", "② 鶴ヶ城", "③ 白鷺城", "④ 金城"],
        "answer": "③ 白鷺城",
        "explanation": "正解は「白鷺城（しらさぎじょう）」です。鮮やかな白漆喰の壁が羽を広げた白鷺に例えられます。",
        "tag": "登録年: 1993年 / 基準(i)(iv)"
    },
    {
        "id": 3,
        "category": "🏛️ 寺社・建築",
        "question": "古都京都の文化財の構成資産に含まれない寺社・城郭はどれか。",
        "options": ["① 清水寺", "② 二条城", "③ 東大寺", "④ 下鴨神社"],
        "answer": "③ 東大寺",
        "explanation": "正解は「東大寺」です。東大寺は「古都奈良の文化財」の構成資産です。",
        "tag": "登録年: 1994年 / 基準(ii)(iv)"
    },
    {
        "id": 4,
        "category": "🏛️ 寺社・建築",
        "question": "白川郷・五箇山の合掌造り集落において、特徴的な急勾配の屋根の角度はおおよそ何度か。",
        "options": ["① 30〜40度", "② 45〜60度", "③ 70〜80度", "④ 90度"],
        "answer": "② 45〜60度",
        "explanation": "正解は「45〜60度」です。豪雪地帯の重い雪が滑り落ちやすいように急勾配になっています。",
        "tag": "登録年: 1995年 / 基準(iv)(v)"
    },
    {
        "id": 5,
        "category": "🏛️ 寺社・建築",
        "question": "厳島神社（広島県）の社殿が海上に建てられている理由として正しいものはどれか。",
        "options": ["① 津波を防ぐため", "② 島全体が神域のため", "③ 海上交通の目印", "④ 要塞にするため"],
        "answer": "② 島全体が神域のため",
        "explanation": "弥山全体がご神体として信仰されていたため、大地を傷つけぬよう海上に造られました。",
        "tag": "登録年: 1996年 / 基準(i)(ii)(iv)"
    },
    {
        "id": 6,
        "category": "🏛️ 寺社・建築",
        "question": "奈良時代の仏教文化を伝える「古都奈良の文化財」の構成資産に含まれないものはどれか。",
        "options": ["① 平城宮跡", "② 唐招提寺", "③ 興福寺", "④ 平等院鳳凰堂"],
        "answer": "④ 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。平等院は京都府宇治市にあり「古都京都の文化財」の構成資産です。",
        "tag": "登録年: 1998年 / 基準(ii)(iv)(vi)"
    },
    {
        "id": 7,
        "category": "🏛️ 寺社・建築",
        "question": "日光の社寺（栃木県）で、世界遺産登録の対象となっている社寺の数と内訳はどれか。",
        "options": ["① 2社1寺", "② 3社3寺", "③ 1社2寺", "④ 5社5寺"],
        "answer": "① 2社1寺",
        "explanation": "正解は「2社1寺」です。二荒山神社、日光東照宮の2社と、日光山輪王寺の1寺で構成されています。",
        "tag": "登録年: 1999年 / 基準(i)(iv)(vi)"
    },
    {
        "id": 8,
        "category": "🏛️ 寺社・建築",
        "question": "平泉－仏国土（浄土）を表現する遺跡群（岩手県）において、中心的な存在である寺院はどれか。",
        "options": ["① 中尊寺", "② 円覚寺", "③ 善光寺", "④ 金沢寺"],
        "answer": "① 中尊寺",
        "explanation": "正解は「中尊寺」です。金色堂に代表されるように、仏国土を地上に再現しようとした思想が形になっています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi)"
    },
    {
        "id": 9,
        "category": "🏛️ 寺社・建築",
        "question": "法隆寺の金堂や五重塔に代表される、世界最古の木造建築群が持つ建築様式の特徴はどれか。",
        "options": ["① 伝統的木造軸組構法", "② すべて石造りの壁", "③ 鉄筋コンクリート製", "④ レンガ造りアーチ"],
        "answer": "① 伝統的木造軸組構法",
        "explanation": "釘を一切使わない飛鳥時代の優れた木造建築技術（伝統的木造軸組構法）が受け継がれています。",
        "tag": "建築技術 / 基準(i)(iv)"
    },
    {
        "id": 10,
        "category": "🏛️ 寺社・建築",
        "question": "古都京都の文化財の構成資産の一つである「宇治市」にある世界遺産といえばどこか。",
        "options": ["① 平等院鳳凰堂", "② 石山寺の本堂", "③ 三井寺の金堂", "④ 醍醐寺の五重塔"],
        "answer": "① 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。10円硬貨のデザインにも描かれている平安時代の阿弥陀堂建築です。",
        "tag": "構成資産: 平等院・宇治上神社"
    },

    # --- 【分野：自然遺産】 ---
    {
        "id": 11,
        "category": "🌲 自然遺産",
        "question": "屋久島に自生する樹齢数千年を超える代表的な植物はどれか。",
        "options": ["① ブナの巨木", "② 屋久杉（スギ）", "③ ヒノキの古木", "④ 天然のマツ"],
        "answer": "② 屋久杉（スギ）",
        "explanation": "正解は「屋久杉（スギ）」です。標高500mを超える山地に自生しており、ユネスコ自然遺産に登録されています。",
        "tag": "登録年: 1993年 / 基準(vii)(ix)"
    },
    {
        "id": 12,
        "category": "🌲 自然遺産",
        "question": "白神山地が世界自然遺産に登録される決め手となった、原生的な森林を構成する樹木はどれか。",
        "options": ["① アカマツ", "② スギ林", "③ ブナの原生林", "④ カエデの林"],
        "answer": "③ ブナの原生林",
        "explanation": "正解は「ブナの原生林」です。人手の加わっていない世界最大級のブナ林が残されていることが評価されました。",
        "tag": "登録年: 1993年 / 基準(ix)"
    },
    {
        "id": 13,
        "category": "🌲 自然遺産",
        "question": "知床が世界自然遺産に登録された最大の理由として評価された生態系上の特徴はどれか。",
        "options": ["① 亜熱帯のマングローブ", "② 流氷と陸上生態系の関係", "③ 標高3000mの高山帯", "④ 固有の砂漠気候帯"],
        "answer": "② 流氷と陸上生態系の関係",
        "explanation": "低緯度で流氷が接岸し、海の生き物と陸の動物が密接につながっている点が評価されました。",
        "tag": "登録年: 2005年 / 基準(ix)(x)"
    },
    {
        "id": 14,
        "category": "🌲 自然遺産",
        "question": "小笠原諸島が自然遺産に登録された主な理由は何か。",
        "options": ["① 大規模なサンゴ礁", "② 独自の進化（固有種）", "③ 世界最大の活火山", "④ 深海魚の豊かな生態系"],
        "answer": "② 独自の進化（固有種）",
        "explanation": "一度も大陸と陸続きになったことがない海洋島で、生物が独自の進化を遂げたためです。",
        "tag": "登録年: 2011年 / 基準(ix)"
    },
    {
        "id": 15,
        "category": "🌲 自然遺産",
        "question": "奄美大島、徳之島、沖縄島北部及び西表島が自然遺産に登録された最大の要因は何か。",
        "options": ["① 固有種・絶滅危惧種", "② 日本最大のサンゴ礁", "③ 世界一の年間降水量", "④ 完全な無人島であること"],
        "answer": "① 固有種・絶滅危惧種",
        "explanation": "アマミノクロウサギなど高い固有種・絶滅危惧種の生息地であることが評価されました。",
        "tag": "登録年: 2021年 / 基準(x)"
    },
    {
        "id": 16,
        "category": "🌲 自然遺産",
        "question": "富士山－信仰の対象と芸術の源泉（静岡・山梨県）の登録種別はどれか。",
        "options": ["① 自然遺産", "② 文化遺産", "③ 複合遺産", "④ 無形文化遺産"],
        "answer": "② 文化遺産",
        "explanation": "正解は「文化遺産」です。自然遺産ではなく、信仰や芸術の源泉として文化遺産に登録されています。",
        "tag": "登録年: 2013年 / 基準(iii)(vi)"
    },

    # --- 【分野：歴史・条約・産業遺産】 ---
    {
        "id": 17,
        "category": "📜 歴史・条約",
        "question": "原爆ドーム（広島平和記念碑）の設計を手掛けた建築家の出身国はどこか。",
        "options": ["① チェコ", "② ドイツ", "③ フランス", "④ イギリス"],
        "answer": "① チェコ",
        "explanation": "正解は「チェコ」です。チェコ人の建築家ヤン・レッツェルによって設計されました。",
        "tag": "登録年: 1996年 / 基準(vi)"
    },
    {
        "id": 18,
        "category": "📜 歴史・条約",
        "question": "琉球王国のグスク及び関連遺産群の中で、首里城跡とともに登録された城の名称はどれか。",
        "options": ["① 熊本城の跡地", "② 中城城跡", "③ 大阪城の石垣", "④ 名古屋城の天守"],
        "answer": "② 中城城跡",
        "explanation": "正解は「中城城跡」です。沖縄県にある幾つものグスク（城）や関連遺産が登録されています。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi)"
    },
    {
        "id": 19,
        "category": "📜 歴史・条約",
        "question": "紀伊山地の霊場と参詣道において、3つの「霊場」に含まれないものはどれか。",
        "options": ["① 高野山", "② 吉野・大峯", "③ 熊野三山", "④ 比叡山"],
        "answer": "④ 比叡山",
        "explanation": "正解は「比叡山」です。比叡山は京都・滋賀にあり、紀伊山地の霊場には含まれません。",
        "tag": "登録年: 2004年 / 基準(ii)(iii)(iv)(vi)"
    },
    {
        "id": 20,
        "category": "📜 歴史・条約",
        "question": "石見銀山遺跡（島根県）の世界遺産登録の決め手となった、特徴的な鉱石採掘・精錬法は何か。",
        "options": ["① 水銀圧搾法", "② 灰吹法", "③ アマルガム法", "④ 露天掘り手法"],
        "answer": "② 灰吹法",
        "explanation": "正解は「灰吹法（はいふきほう）」です。銀を効率よく抽出する高度な技術として評価されました。",
        "tag": "登録年: 2007年 / 基準(ii)(iii)"
    },
    {
        "id": 21,
        "category": "📜 歴史・条約",
        "question": "富岡製糸場と絹産業遺産群（群馬県）の構成資産に含まれないものはどれか。",
        "options": ["① 富岡製糸場", "② 荒船風穴", "③ 高山社跡", "④ 横浜赤レンガ倉庫"],
        "answer": "④ 横浜赤レンガ倉庫",
        "explanation": "正解は「横浜赤レンガ倉庫」です。富岡製糸場、田島家住宅、高山社跡、荒船風穴の4資産です。",
        "tag": "登録年: 2014年 / 基準(ii)(iv)"
    },
    {
        "id": 22,
        "category": "📜 歴史・条約",
        "question": "明治日本の産業革命遺産の構成資産として正しくないものはどれか。",
        "options": ["① 官営八幡製鉄所", "② 軍艦島（端島炭坑）", "③ 長崎グラバー住宅", "④ 萩反射炉"],
        "answer": "③ 長崎グラバー住宅",
        "explanation": "正解は「長崎グラバー住宅」です。グラバー園内の旧住宅は世界遺産の構成資産ではありません。",
        "tag": "登録年: 2015年 / 基準(ii)(iv)"
    },
    {
        "id": 23,
        "category": "📜 歴史・条約",
        "question": "「神宿る島」宗像・沖ノ島と関連遺産群において、一般人の立ち入りが原則禁止されている島はどれか。",
        "options": ["① 沖ノ島", "② 大島", "③ 相島", "④ 宗像大島"],
        "answer": "① 沖ノ島",
        "explanation": "正解は「沖ノ島」です。島全体がご神体であり、今でも厳格な禁忌が守られています。",
        "tag": "登録年: 2017年 / 基準(ii)(iii)"
    },
    {
        "id": 24,
        "category": "📜 歴史・条約",
        "question": "長崎と天草地方の潜伏キリシタン関連遺産の構成資産に含まれないものはどれか。",
        "options": ["① 大浦天主堂", "② 原城跡", "③ 久賀島の集落", "④ 首里城跡"],
        "answer": "④ 首里城跡",
        "explanation": "正解は「首里城跡」です。首里城跡は沖縄県の世界遺産であり、潜伏キリシタン関連遺産には含まれません。",
        "tag": "登録年: 2018年 / 基準(iii)"
    },
    {
        "id": 25,
        "category": "📜 歴史・条約",
        "question": "北海道・北東北の縄文遺跡群の代表的な構成資産として正しくないものはどれか。",
        "options": ["① 三内丸山遺跡", "② 大湯環状列石", "③ 函館山要塞跡", "④ 小牧野遺跡"],
        "answer": "③ 函館山要塞跡",
        "explanation": "正解は「函館山要塞跡」です。近代の軍事遺跡であり、縄文遺跡群には含まれません。",
        "tag": "登録年: 2021年 / 基準(iii)(v)"
    },
    {
        "id": 26,
        "category": "📜 歴史・条約",
        "question": "佐渡島の金山が新しく世界文化遺産に登録された年はいつか。",
        "options": ["① 2022年", "② 2023年", "③ 2024年", "④ 2025年"],
        "answer": "③ 2024年",
        "explanation": "正解は「2024年」です。インドのニューデリーで開催された世界遺産委員会で登録が決定しました。",
        "tag": "登録年: 2024年 / 基準(iv)"
    },

    # --- 【分野：年代・登録基準・条約の仕組み】 ---
    {
        "id": 27,
        "category": "📅 年代・基準・制度",
        "question": "世界遺産条約が採択された年はいつか。",
        "options": ["① 1945年", "② 1972年", "③ 1992年", "④ 2003年"],
        "answer": "② 1972年",
        "explanation": "正解は「1972年」のユネスコ総会で採択されました。",
        "tag": "ユネスコ総会での採択年"
    },
    {
        "id": 28,
        "category": "📅 年代・基準・制度",
        "question": "ユネスコ（UNESCO）の本部が置かれている都市はどこか。",
        "options": ["① ジュネーブ", "② ニューヨーク", "③ パリ", "④ ローマ"],
        "answer": "③ パリ",
        "explanation": "正解は「パリ（フランス）」です。ユネスコの本部はパリに置かれています。",
        "tag": "国際機関の本部"
    },
    {
        "id": 29,
        "category": "📅 年代・基準・制度",
        "question": "世界遺産の登録基準において、文化遺産の基準の数はいくつあるか。",
        "options": ["① 4つ（(i)〜(iv)）", "② 6つ（(i)〜(vi)）", "③ 10つ（(i)〜(x)）", "④ 12つ"],
        "answer": "② 6つ（(i)〜(vi)）",
        "explanation": "正解は「6つ（(i)〜(vi)」です。自然遺産の基準は4つであり、合わせて10個の基準があります。",
        "tag": "検定頻出：登録基準の数"
    },
    {
        "id": 30,
        "category": "📅 年代・基準・制度",
        "question": "世界遺産リストに登録されるための条件として最も重要な概念は何か。",
        "options": ["① 顕著な普遍的価値（OUV）", "② 年間100万人の観光客", "③ 最新のハイテク建築", "④ 入場料が無料であること"],
        "answer": "① 顕著な普遍的価値（OUV）",
        "explanation": "正解は「顕著な普遍的価値（OUV）」です。人類全体にとってきわめて重要な価値が求められます。",
        "tag": "検定必須キーワード：OUV"
    },
    {
        "id": 31,
        "category": "📅 年代・基準・制度",
        "question": "次のうち、日本の「無形文化遺産」に登録されているものはどれか。",
        "options": ["① 法隆寺の金堂", "② 姫路城の大天守", "③ 和食（日本人の伝統食）", "④ 原爆ドームの遺構"],
        "answer": "③ 和食（日本人の伝統食）",
        "explanation": "正解は「和食」です。建造物などは世界遺産（文化遺産）、伝統技術や食文化などは無形文化遺産です。",
        "tag": "無形文化遺産と世界遺産の区別"
    }
]

# --- ヘルパー関数：問題と選択肢をシャッフルして準備する ---
def prepare_quiz_session(questions_list):
    prepared = []
    for q in questions_list:
        q_copy = q.copy()
        # 1. 元の選択肢テキストから「① 」などの先頭記号を取り除く
        clean_options = [re.sub(r'^[①②③④]\s*', '', opt) for opt in q_copy["options"]]
        clean_answer = re.sub(r'^[①②③④]\s*', '', q_copy["answer"])
        
        # 2. 選択肢の並び順をランダムにシャッフルする
        random.shuffle(clean_options)
        
        # 3. 新しい並び順に合わせて「①〜④」を振り直す
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
if "game_started" not in st.session_state:
    st.session_state.game_started = False
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
    st.session_state.bookmarked_ids = set()  # ブックマークした問題のIDを保存
if "history" not in st.session_state:
    st.session_state.history = []            # 過去の学習履歴（正答率など）を保存
if "mode_label" not in st.session_state:
    st.session_state.mode_label = ""

# ==========================================
# サイドバー（学習ダッシュボード ＆ 成績グラフ）
# ==========================================
st.sidebar.title("📊 学習ダッシュボード")
st.sidebar.markdown("---")

if st.session_state.game_started:
    total_q = len(st.session_state.shuffled_quiz)
    current_progress = st.session_state.current_q
    st.sidebar.metric(label="現在の進捗", value=f"{current_progress} / {total_q} 問")
    st.sidebar.progress(current_progress / total_q if total_q > 0 else 0)
    st.sidebar.markdown(f"**現在のスコア:** {st.session_state.score} 点")
else:
    st.sidebar.info("クイズをスタートすると、リアルタイムの進捗が表示されます。")

st.sidebar.markdown("---")
st.sidebar.subheader("📈 過去の成績推移（正答率）")
if len(st.session_state.history) > 0:
    df_hist = pd.DataFrame(st.session_state.history)
    st.sidebar.line_chart(df_hist.set_index("回数")["正答率(%)"])
    st.sidebar.caption(f"これまでの挑戦回数: {len(st.session_state.history)}回 / ブックマーク数: {len(st.session_state.bookmarked_ids)}問")
else:
    st.sidebar.caption("まだ学習履歴がありません。1セット解き終わるとグラフが表示されます！")

# タイトル
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 世界遺産検定 4択マスター</h2>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 1. モード選択・ホーム画面
# ==========================================
if not st.session_state.game_started:
    st.subheader("🎯 学習モード＆分野を選択")
    
    categories = ["すべて"] + list(dict.fromkeys([q["category"] for q in QUIZ_DATA]))
    selected_category = st.selectbox("📚 学習する分野・ジャンル：", categories)
    
    mode = st.radio(
        "📝 挑戦する問題数：",
        ["サクッと10問", "ハーフ20問", "全問網羅"]
    )
    
    st.write("")
    
    # 通常スタートボタン
    if st.button("🚀 通常クイズをスタートする！", type="primary", use_container_width=True):
        if selected_category == "すべて":
            filtered_data = QUIZ_DATA.copy()
        else:
            filtered_data = [q for q in QUIZ_DATA if q["category"] == selected_category]
        
        if not filtered_data:
            st.warning("該当する問題がありません！")
        else:
            if "10問" in mode:
                limit = min(10, len(filtered_data))
            elif "20問" in mode:
                limit = min(20, len(filtered_data))
            else:
                limit = len(filtered_data)
            
            random.shuffle(filtered_data)
            # 問題順と選択肢順の両方をシャッフルしてセット
            st.session_state.shuffled_quiz = prepare_quiz_session(filtered_data[:limit])
            st.session_state.game_started = True
            st.session_state.mode_label = "通常モード"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

    st.write("")
    col1, col2 = st.columns(2)
    
    # 復習モードボタン
    with col1:
        wrong_count = len(st.session_state.wrong_questions)
        if st.button(f"❌ 間違いを復習する ({wrong_count}問)", disabled=(wrong_count == 0), use_container_width=True):
            review_list = st.session_state.wrong_questions.copy()
            random.shuffle(review_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(review_list)
            st.session_state.game_started = True
            st.session_state.mode_label = "🔄 間違い復習モード"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()
            
    # ブックマークモードボタン
    with col2:
        bm_count = len(st.session_state.bookmarked_ids)
        if st.button(f"⭐ ブックマーク問題を解く ({bm_count}問)", disabled=(bm_count == 0), use_container_width=True):
            bm_list = [q for q in QUIZ_DATA if q["id"] in st.session_state.bookmarked_ids]
            random.shuffle(bm_list)
            st.session_state.shuffled_quiz = prepare_quiz_session(bm_list)
            st.session_state.game_started = True
            st.session_state.mode_label = "⭐ ブックマーク復習モード"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

# ==========================================
# 2. クイズプレイ中の画面
# ==========================================
else:
    active_quiz = st.session_state.shuffled_quiz
    
    if st.session_state.mode_label != "通常モード":
        st.caption(f"【{st.session_state.mode_label}】で学習中です")

    if st.session_state.current_q < len(active_quiz):
        q = active_quiz[st.session_state.current_q]
        
        # 上部バー：分野タグ と ⭐ブックマークボタン
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            st.markdown(f"### `{q['category']}`")
        with top_col2:
            is_bm = q["id"] in st.session_state.bookmarked_ids
            bm_label = "⭐ 登録済" if is_bm else "☆ ブックマーク"
            if st.button(bm_label, key=f"bm_{q['id']}", use_container_width=True):
                if is_bm:
                    st.session_state.bookmarked_ids.remove(q["id"])
                else:
                    st.session_state.bookmarked_ids.add(q["id"])
                st.rerun()

        st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
        st.markdown(f"**{q['question']}**")
        st.write("")

        # 四択ボタン（シャッフル済みの選択肢を表示）
        col1, col2 = st.columns(2)
        for i, option in enumerate(q["options"]):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                if st.button(option, key=f"opt_{i}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.selected_option = option
                    
                    if option[:1] == q["answer"][:1]:
                        st.session_state.score += 1
                    else:
                        # 元の問題データを wrong_questions に追加
                        orig_q = next((item for item in QUIZ_DATA if item["id"] == q["id"]), q)
                        if orig_q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(orig_q)
                    st.rerun()

        # 判定・解説の表示
        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)
            
            explanation_html = f"""
            <div class="explanation-box">
                <b>💡 解説:</b> {q['explanation']}<br><br>
                <span style="font-size: 0.9em; background-color: #ffffff; padding: 3px 6px; border-radius: 4px; color: #084298;">📌 <b>検定ポイント:</b> {q['tag']}</span>
            </div>
            """
            st.markdown(explanation_html, unsafe_allow_html=True)

            if st.button("次の問題へ ➡️", type="primary"):
                st.session_state.current_q += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()

    # ==========================================
    # 3. 全問終了後の結果画面
    # ==========================================
    else:
        st.balloons()
        st.header("🎊 お疲れ様でした！結果発表")
        
        total_len = len(active_quiz)
        accuracy = round((st.session_state.score / total_len) * 100, 1) if total_len > 0 else 0
        
        st.metric(label="獲得スコア / 正答率", value=f"{st.session_state.score} / {total_len} 問正解 ({accuracy}%)")
        
        # 履歴への記録（重複防止のため、未記録の場合のみ追加）
        if not st.session_state.get("history_recorded", False):
            attempt_num = len(st.session_state.history) + 1
            st.session_state.history.append({
                "回数": f"{attempt_num}回目",
                "正答率(%)": accuracy
            })
            st.session_state.history_recorded = True
        
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 ホーム画面に戻る", type="primary", use_container_width=True):
                st.session_state.game_started = False
                st.session_state.history_recorded = False
                st.rerun()
        with col2:
            wrong_cnt = len(st.session_state.wrong_questions)
            if st.button(f"❌ 間違いを復習する ({wrong_cnt}問)", disabled=(wrong_cnt == 0), use_container_width=True):
                review_list = st.session_state.wrong_questions.copy()
                random.shuffle(review_list)
                st.session_state.shuffled_quiz = prepare_quiz_session(review_list)
                st.session_state.game_started = True
                st.session_state.mode_label = "🔄 間違い復習モード"
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.wrong_questions = []
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.session_state.history_recorded = False
                st.rerun()

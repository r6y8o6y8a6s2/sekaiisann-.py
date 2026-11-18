import streamlit as st
import random
import re

# ページ設定
st.set_page_config(
    page_title="世界遺産 4択マスター（検定2級対策）",
    page_icon="🏛️",
    layout="centered"
)

# --- 💡 カスタムCSS（解説やカードのデザインをリッチにするため） ---
st.markdown("""
    <style>
    .correct-box { padding: 15px; border-radius: 8px; background-color: #d1e7dd; color: #0f5132; margin-bottom: 10px; }
    .incorrect-box { padding: 15px; border-radius: 8px; background-color: #f8d7da; color: #842029; margin-bottom: 10px; }
    .explanation-box { padding: 15px; border-radius: 8px; background-color: #cfe2ff; color: #084298; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- QUIZ_DATA（年代・登録基準を含む全50問のデータベース） ---
QUIZ_DATA = [
    # --- 【分野：寺社・建築】 ---
    {
        "category": "🏛️ 寺社・建築",
        "question": "法隆寺地域の仏教建造物が日本で初めて世界遺産に登録された年はいつか。",
        "options": ["① 1985年", "② 1993年", "③ 1997年", "④ 2000年"],
        "answer": "② 1993年",
        "explanation": "正解は「② 1993年」です。姫路城とともに、日本で初めて世界遺産（文化遺産）に登録されました。",
        "tag": "登録年: 1993年 / 基準(i)(ii)(iv)(vi)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "姫路城の別称として正しいものはどれか。",
        "options": ["① 烏城", "② 鶴ヶ城", "③ 白鷺城", "④ 金城"],
        "answer": "③ 白鷺城",
        "explanation": "正解は「③ 白鷺城（しらさぎじょう／はくろじょう）」です。鮮やかな白漆喰の壁が羽を広げた白鷺に例えられます。",
        "tag": "登録年: 1993年 / 基準(i)(iv)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "古都京都の文化財の構成資産に含まれない寺社・城郭はどれか。",
        "options": ["① 清水寺", "② 二条城", "③ 東大寺", "④ 賀茂御祖神社（下鴨神社）"],
        "answer": "③ 東大寺",
        "explanation": "正解は「③ 東大寺」です。東大寺は「古都奈良の文化財」の構成資産です。京都の文化財は17の寺社・城郭で構成されます。",
        "tag": "登録年: 1994年 / 基準(ii)(iv)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "白川郷・五箇山の合掌造り集落において、特徴的な急勾配の茅葺き屋根の角度はおおよそ何度か。",
        "options": ["① 30〜40度", "② 45〜60度", "③ 70〜80度", "④ 90度"],
        "answer": "② 45〜60度",
        "explanation": "正解は「② 45〜60度」です。豪雪地帯の重い雪が滑り落ちやすくするため、また屋根裏で養蚕を行うために急勾配になっています。",
        "tag": "登録年: 1995年 / 基準(iv)(v)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "厳島神社（広島県）の社殿が海上に建てられている理由として正しいものはどれか。",
        "options": ["① 津波を防ぐため", "② 島全体が神域とされ、大地を傷つけないようにするため", "③ 海上交通の目印にするため", "④ 敵の侵入を防ぐ要塞にするため"],
        "answer": "② 島全体が神域とされ、大地を傷つけないようにするため",
        "explanation": "正解は「②」です。弥山（みせん）全体がご神体として信仰されていたため、潮の満ち引きを利用して社殿が海上に造られました。",
        "tag": "登録年: 1996年 / 基準(i)(ii)(iv)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "奈良時代の仏教文化を伝える「古都奈良の文化財」の構成資産に含まれるものはどれか。",
        "options": ["① 平城宮跡", "② 唐招提寺", "③ 興福寺", "④ すべて正解"],
        "answer": "④ すべて正解",
        "explanation": "正解は「④ すべて正解」です。東大寺、興福寺、春日大社、元興寺、薬師寺、唐招提寺、平城宮跡、春日山原始林の8資産が登録されています。",
        "tag": "登録年: 1998年 / 基準(ii)(iv)(vi)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "日光の社寺（栃木県）で、世界遺産登録の対象となっている社寺の数と内訳はどれか。",
        "options": ["① 2社1寺", "② 3社3寺", "③ 1社2寺", "④ 5社5寺"],
        "answer": "① 2社1寺",
        "explanation": "正解は「① 2社1寺」です。二荒山神社、日光東照宮の2社と、日光山輪王寺の1寺で構成されています。",
        "tag": "登録年: 1999年 / 基準(i)(iv)(vi)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "平泉－仏国土（浄土）を表現する建築・庭園・考古遺跡群（岩手県）において、中心的な存在である寺院はどれか。",
        "options": ["① 中尊寺", "② 円覚寺", "③ 善光寺", "④ 金沢寺"],
        "answer": "① 中尊寺",
        "explanation": "正解は「① 中尊寺」です。金色堂に代表されるように、奥州藤原氏が仏国土（浄土）を地上に再現しようとした思想が形になっています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "法隆寺の金堂や五重塔に代表される、世界最古の木造建築群が持つ建築様式の特徴はどれか。",
        "options": ["① 釘を一切使わない伝統的木造軸組構法", "② すべて石造りの外壁で補強されている", "③ 鉄筋コンクリートで復元されている", "④ レンガ造りのアーチ構造"],
        "answer": "① 釘を一切使わない伝統的木造軸組構法",
        "explanation": "正解は「①」です。飛鳥時代の優れた木造建築技術が現在まで受け継がれています。",
        "tag": "建築技術 / 基準(i)(iv)"
    },
    {
        "category": "🏛️ 寺社・建築",
        "question": "古都京都の文化財の構成資産の一つである「宇治市」にある世界遺産といえばどこか。",
        "options": ["① 平等院（鳳凰堂）", "② 石山寺", "③ 三井寺", "④ 醍醐寺"],
        "answer": "① 平等院（鳳凰堂）",
        "explanation": "正解は「① 平等院鳳凰堂」です。10円硬貨のデザインにも描かれている平安時代の阿弥陀堂建築の傑作です。",
        "tag": "構成資産: 平等院・宇治上神社"
    },

    # --- 【分野：自然遺産】 ---
    {
        "category": "🌲 自然遺産",
        "question": "屋久島に自生する樹齢数千年を超える代表的な植物はどれか。",
        "options": ["① ブナ", "② スギ", "③ ヒノキ", "④ マツ"],
        "answer": "② スギ",
        "explanation": "正解は「② スギ」です。標高500mを超える山地に屋久杉が自生しており、ユネスコ自然遺産に登録されています。",
        "tag": "登録年: 1993年 / 基準(vii)(ix)"
    },
    {
        "category": "🌲 自然遺産",
        "question": "白神山地が世界自然遺産に登録される決め手となった、日本最大級の原生的なブナ林が広がっている山地はどこか。",
        "options": ["① 奥羽山脈", "② 飛騨山脈", "③ 白神山地（青森・秋田県境）", "④ 木曽山脈"],
        "answer": "③ 白神山地（青森・秋田県境）",
        "explanation": "正解は「③ 白神山地」です。人手の加わっていない世界最大級のブナの原生林が残されていることが評価されました。",
        "tag": "登録年: 1993年 / 基準(ix)"
    },
    {
        "category": "🌲 自然遺産",
        "question": "知床が世界自然遺産に登録された最大の理由として評価された生態系上の特徴はどれか。",
        "options": ["① 亜熱帯のマングローブ林", "② 流氷がもたらす豊かな海洋生態系と陸上生態系の相互関係", "③ 標高3000m級の高山植物帯", "④ 固有の砂漠気候"],
        "answer": "② 流氷がもたらす豊かな海洋生態系と陸上生態系の相互関係",
        "explanation": "正解は「②」です。北半球で最も低緯度で流氷が接岸し、海の生き物と陸の動物（ヒグマやシマフクロウなど）が密接につながっている点が評価されました。",
        "tag": "登録年: 2005年 / 基準(ix)(x)"
    },
    {
        "category": "🌲 自然遺産",
        "question": "小笠原諸島が自然遺産に登録された主な理由は何か。",
        "options": ["① 大規模なサンゴ礁があるから", "② 一度も大陸と陸続きになったことがなく、独自の進化を遂げた固有種が多いから（ガラパゴス的進化）", "③ 世界最大の活火山があるから", "④ 深海魚の宝庫だから"],
        "answer": "② 一度も大陸と陸続きになったことがない「海洋島」で、独自の進化（固有種）が見られるから",
        "explanation": "正解は「②」です。大陸から遠く離れた海洋島であるため、生物が独自の進化を遂げ「東洋のガラパゴス」とも称されます。",
        "tag": "登録年: 2011年 / 基準(ix)"
    },
    {
        "category": "🌲 自然遺産",
        "question": "奄美大島、徳之島、沖縄島北部及び西表島が自然遺産に登録された最大の要因は何か。",
        "options": ["① アマミノクロウサギやイリオモテヤマネコなど、高い固有種・絶滅危惧種の生息地であること", "② 日本最大のサンゴ礁が広がっていること", "③ 世界で最も降水量が多いこと", "④ 人口が非常に少ない手つかずの島であること"],
        "answer": "① アマミノクロウサギやイリオモテヤマネコなど、高い固有種・絶滅危惧種の生息地であること",
        "explanation": "正解は「①」です。大陸から分離した歴史を持つ亜熱帯の島々で、独自の進化を遂げた生物多様性のホットスポットとなっています。",
        "tag": "登録年: 2021年 / 基準(x)"
    },
    {
        "category": "🌲 自然遺産",
        "question": "富士山－信仰の対象と芸術の源泉（静岡・山梨県）の構成資産に含まれないものはどれか。",
        "options": ["① 富士山山頂の神域", "② 白糸の滝", "③ 三保松原", "④ 東京タワー"],
        "answer": "④ 東京タワー",
        "explanation": "正解は「④ 東京タワー」です。富士山は「文化遺産」として登録されており、周辺の神社や登山道、三保松原などが構成資産です。",
        "tag": "登録年: 2013年（文化遺産） / 基準(iii)(vi)"
    },

    # --- 【分野：歴史・条約・産業遺産】 ---
    {
        "category": "📜 歴史・条約",
        "question": "原爆ドーム（広島平和記念碑）の設計を手掛けたチェコの建築家は誰か。",
        "options": ["① ヤン・レッツェル", "② アントニン・レーニン", "③ ブルーノ・タウト", "④ ジョサイア・コンドル"],
        "answer": "① ヤン・レッツェル",
        "explanation": "正解は「① ヤン・レッツェル」です。元々は「広島県物産陳列館」として1915年に竣工しました。",
        "tag": "登録年: 1996年 / 基準(vi)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "琉球王国のグスク及び関連遺産群の中で、首里城跡とともに世界遺産に登録された城（グスク）の名称として正しくないものはどれか。",
        "options": ["① 中城城跡", "② 勝連城跡", "③ 今帰仁城跡", "④ 熊本城跡"],
        "answer": "④ 熊本城跡",
        "explanation": "正解は「④ 熊本城跡」です。熊本城は日本のお城ですが、琉球王国のグスク群（沖縄県）の構成資産ではありません。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "紀伊山地の霊場と参詣道において、3つの「霊場」に含まれないものはどれか。",
        "options": ["① 高野山", "② 吉野・大峯", "③ 熊野三山", "④ 比叡山"],
        "answer": "④ 比叡山",
        "explanation": "正解は「④ 比叡山」です。比叡山は京都・滋賀にまたがり、紀伊山地の霊場（高野山、吉野・大峯、熊野三山）には含まれません。",
        "tag": "登録年: 2004年 / 基準(ii)(iii)(iv)(vi)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "石見銀山遺跡（島根県）の特徴的な鉱石採掘・精錬法として世界遺産登録の決め手となった技術は何か。",
        "options": ["① アマルガム法", "② 灰吹法（はいふきほう）", "③ 水銀圧搾法", "④ 露天掘り法"],
        "answer": "② 灰吹法（はいふきほう）",
        "explanation": "正解は「② 灰吹法」です。中国から伝来したこの技術を高度化させ、良質な銀を大量に生産したことで世界の貿易に大きな影響を与えました。",
        "tag": "登録年: 2007年 / 基準(ii)(iii)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "富岡製糸場と絹産業遺産群（群馬県）の構成資産に含まれないものはどれか。",
        "options": ["① 富岡製糸場", "② 田島家住宅（蚕種製造）", "③ 荒船風穴", "④ 横浜赤レンガ倉庫"],
        "answer": "④ 横浜赤レンガ倉庫",
        "explanation": "正解は「④ 横浜赤レンガ倉庫」です。富岡製糸場のほか、高山社跡、田島家住宅、荒船風穴の4つの資産で構成されています。",
        "tag": "登録年: 2014年 / 基準(ii)(iv)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "明治日本の産業革命製鉄・製鋼、造船、石炭産業の構成資産として正しくないものはどれか。",
        "options": ["① 官営八幡製鉄所", "② 軍艦島（端島炭坑）", "③ 長崎グラバー住宅", "④ 萩反射炉"],
        "answer": "③ 長崎グラバー住宅",
        "explanation": "正解は「③ 長崎グラバー住宅」です。グラバー園内の旧グラバー住宅は世界遺産の構成資産ではありません。",
        "tag": "登録年: 2015年 / 基準(ii)(iv)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "「神宿る島」宗像・沖ノ島と関連遺産群（福岡県）において、一般人の立ち入りが原則禁止されている島はどれか。",
        "options": ["① 沖ノ島", "② 大島", "③ 相島", "④ 宗像大島"],
        "answer": "① 沖ノ島",
        "explanation": "正解は「① 沖ノ島」です。島全体がご神体であり、今でも厳格な禁忌（女人禁制や男性でも上陸前の沐浴など）が守られています。",
        "tag": "登録年: 2017年 / 基準(ii)(iii)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "長崎と天草地方の潜伏キリシタン関連遺産（長崎・熊本県）の構成資産に含まれる集落・教会の組み合わせとして正しいものはどれか。",
        "options": ["① 大浦天主堂", "② 原城跡", "③ 久賀島の集落", "④ すべて正解"],
        "answer": "④ すべて正解",
        "explanation": "正解は「④ すべて正解」です。禁教期に信仰を続けた潜伏キリシタンの歴史を物語る12の資産で構成されています。",
        "tag": "登録年: 2018年 / 基準(iii)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "北海道・北東北の縄文遺跡群（北海道・青森・岩手・秋田）の代表的な構成資産として正しくないものはどれか。",
        "options": ["① 三内丸山遺跡", "② 大湯環状列石", "③ 函館山要塞跡", "④ 小牧野遺跡"],
        "answer": "③ 函館山要塞跡",
        "explanation": "正解は「③ 函館山要塞跡」は近代の軍事遺跡であり、縄文遺跡群には含まれません。",
        "tag": "登録年: 2021年 / 基準(iii)(v)"
    },
    {
        "category": "📜 歴史・条約",
        "question": "佐渡島の金山が新しく世界文化遺産に登録された年はいつか。",
        "options": ["① 2022年", "② 2023年", "③ 2024年", "④ 2025年"],
        "answer": "③ 2024年",
        "explanation": "正解は「③ 2024年」です。インドのニューデリーで開催された世界遺産委員会で、日本26件目の世界遺産として登録が決定しました。",
        "tag": "登録年: 2024年 / 基準(iv)"
    },

    # --- 【分野：年代・登録基準・条約の仕組み】 ---
    {
        "category": "📅 年代・基準・制度",
        "question": "世界遺産条約（世界の文化及び自然遺産の保護に関する条約）が採択された年はいつか。",
        "options": ["① 1945年", "② 1972年", "③ 1992年", "④ 2003年"],
        "answer": "② 1972年",
        "explanation": "正解は「② 1972年」のユネスコ総会で採択されました（日本が受諾したのは1992年です）。",
        "tag": "ユネスコ総会での採択年"
    },
    {
        "category": "📅 年代・基準・制度",
        "question": "ユネスコ（UNESCO）の本部が置かれている都市はどこか。",
        "options": ["① ジュネーブ", "② ニューヨーク", "③ パリ", "④ ローマ"],
        "answer": "③ パリ",
        "explanation": "正解は「③ パリ（フランス）」です。ユネスコの本部はパリに置かれています。",
        "tag": "国際機関の本部"
    },
    {
        "category": "📅 年代・基準・制度",
        "question": "世界遺産の登録基準（クライテリア）において、文化遺産の基準の数はいくつあるか。",
        "options": ["① 4つ（(i)〜(iv)）", "② 6つ（(i)〜(vi)）", "③ 10つ（(i)〜(x)）", "④ 12つ"],
        "answer": "② 6つ（(i)〜(vi)）",
        "explanation": "正解は「② 6つ（(i)〜(vi)」です。自然遺産の基準は4つ（(vii)〜(x)）であり、合わせて10個の基準が存在します。",
        "tag": "検定頻出：登録基準の数"
    },
    {
        "category": "📅 年代・基準・制度",
        "question": "世界遺産リストに登録されるための条件として、最も重要な概念は何か。",
        "options": ["① 顕著な普遍的価値（OUV：Outstanding Universal Value）", "② 観光客が年間100万人以上訪れること", "③ 最新のハイテク建築であること", "④ 入場料が無料であること"],
        "answer": "① 顕著な普遍的価値（OUV：Outstanding Universal Value）",
        "explanation": "正解は「① 顕著な普遍的価値（OUV）」です。人類全体にとってきわめて重要で、国境を越えた普遍的な価値を持つことが求められます。",
        "tag": "検定必須キーワード：OUV"
    },
    {
        "category": "📅 年代・基準・制度",
        "question": "次のうち、日本の「無形文化遺産」に登録されているものではないものはどれか。",
        "options": ["① 能楽", "② 歌舞伎", "③ 和食", "④ 東京タワー"],
        "answer": "④ 東京タワー",
        "explanation": "正解は「④ 東京タワー」です。無形文化遺産ではなく、世界遺産（建造物）でもありません。",
        "tag": "無形文化遺産と世界遺産の区別"
    }
]

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
    st.session_state.wrong_questions = []  # 間違えた問題を蓄積するリスト
if "is_review_mode" not in st.session_state:
    st.session_state.is_review_mode = False

# ==========================================
# サイドバー（進捗状況の「見える化」＆分野別フィルター）
# ==========================================
st.sidebar.title("📊 学習ダッシュボード")
st.sidebar.markdown("---")

# 進捗の見える化
if st.session_state.game_started:
    total_q = len(st.session_state.shuffled_quiz)
    current_progress = st.session_state.current_q
    st.sidebar.metric(label="現在の進捗", value=f"{current_progress} / {total_q} 問")
    st.sidebar.progress(current_progress / total_q if total_q > 0 else 0)
    st.sidebar.markdown(f"**現在のスコア:** {st.session_state.score} 点")
else:
    st.sidebar.info("モードを選んでクイズをスタートすると、ここにリアルタイムの進捗が表示されます。")

st.sidebar.markdown("---")
st.sidebar.markdown("💡 **検定2級合格のコツ**\n間違えた問題は自動で記録されます。最後に「復習モード」で苦手をつぶしましょう！")

# タイトル
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 世界遺産検定 4択マスター</h2>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 1. モード選択・ホーム画面
# ==========================================
if not st.session_state.game_started:
    st.subheader("🎯 学習モード＆分野を選択")
    
    # 分野別フィルター
    categories = ["すべて"] + list(set([q["category"] for q in QUIZ_DATA]))
    selected_category = st.selectbox("📚 学習する分野・ジャンル：", categories)
    
    # 挑戦する問題数
    mode = st.radio(
        "📝 挑戦する問題数：",
        ["サクッと10問", "ハーフ20問", "全問網羅"]
    )
    
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 クイズをスタートする！", type="primary", use_container_width=True):
            # 分野でフィルタリング
            if selected_category == "すべて":
                filtered_data = QUIZ_DATA.copy()
            else:
                filtered_data = [q for q in QUIZ_DATA if q["category"] == selected_category]
            
            if not filtered_data:
                st.warning("該当する問題がありません！")
            else:
                # 問題数の制限
                if "10問" in mode:
                    limit = min(10, len(filtered_data))
                elif "20問" in mode:
                    limit = min(20, len(filtered_data))
                else:
                    limit = len(filtered_data)
                
                random.shuffle(filtered_data)
                st.session_state.shuffled_quiz = filtered_data[:limit]
                st.session_state.game_started = True
                st.session_state.is_review_mode = False
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.wrong_questions = []
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()
                
    # 復習モードボタン（間違えた問題がある場合のみ活性化）
    with col2:
        wrong_count = len(st.session_state.wrong_questions)
        if st.button(f"❌ 間違いを復習する ({wrong_count}問)", disabled=(wrong_count == 0), use_container_width=True):
            st.session_state.shuffled_quiz = st.session_state.wrong_questions.copy()
            st.session_state.game_started = True
            st.session_state.is_review_mode = True
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.wrong_questions = []  # リセットして再挑戦
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

# ==========================================
# 2. クイズプレイ中の画面
# ==========================================
else:
    active_quiz = st.session_state.shuffled_quiz
    
    if st.session_state.is_review_mode:
        st.caption("🔄 【復習モード中】直近で間違えた問題に再挑戦しています！")

    if st.session_state.current_q < len(active_quiz):
        q = active_quiz[st.session_state.current_q]
        
        # 分野タグを表示
        st.markdown(f"### `{q['category']}`")
        clean_question = re.sub(r'^問題\(\d+\)\s*', '', q["question"])
        st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
        st.markdown(f"**{clean_question}**")
        st.write("")

        # 四択ボタン
        col1, col2 = st.columns(2)
        for i, option in enumerate(q["options"]):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                if st.button(option, key=f"opt_{i}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.selected_option = option
                    
                    # 記号（①〜④）が一致しているかで判定
                    if option[:1] == q["answer"][:1]:
                        st.session_state.score += 1
                    else:
                        # 間違えた問題を蓄積（重複防止）
                        if q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(q)
                    st.rerun()

        # 判定・解説の表示（リッチUI）
        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)
            
            # 解説ボックス
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
        st.metric(label="獲得スコア", value=f"{st.session_state.score} / {len(active_quiz)} 問正解")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 モード選択に戻る", type="primary", use_container_width=True):
                st.session_state.game_started = False
                st.rerun()
        with col2:
            wrong_cnt = len(st.session_state.wrong_questions)
            if st.button(f"❌ 間違えた問題だけ復習する ({wrong_cnt}問)", disabled=(wrong_cnt == 0), use_container_width=True):
                st.session_state.shuffled_quiz = st.session_state.wrong_questions.copy()
                st.session_state.game_started = True
                st.session_state.is_review_mode = True
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.wrong_questions = []
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()

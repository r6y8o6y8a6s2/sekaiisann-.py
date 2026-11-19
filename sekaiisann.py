import streamlit as st
import pandas as pd
import random
import re
import time
from datetime import datetime, date, timedelta

# ページ設定
st.set_page_config(
    page_title="世界遺産 4択マスター（検定2級対策）",
    page_icon="🏛️",
    layout="centered"
)

# --- 💡 カスタムCSS（ライトテーマ固定） ---
st.markdown("""
    <style>
    .correct-box { padding: 15px; border-radius: 8px; background-color: #d1e7dd; color: #0f5132; margin-bottom: 10px; }
    .incorrect-box { padding: 15px; border-radius: 8px; background-color: #f8d7da; color: #842029; margin-bottom: 10px; }
    .explanation-box { padding: 15px; border-radius: 8px; background-color: #cfe2ff; color: #084298; margin-bottom: 15px; }
    .trivia-box { padding: 15px; border-radius: 8px; background-color: #fff3cd; color: #664d03; margin-bottom: 20px; border-left: 5px solid #ffc107; }
    .flashcard { padding: 30px; border-radius: 12px; background-color: #f8f9fa; border: 2px solid #dee2e6; text-align: center; margin-bottom: 20px; }
    .pass-banner { padding: 20px; border-radius: 10px; background-color: #d1e7dd; color: #0f5132; text-align: center; border: 2px solid #198754; margin-bottom: 15px; }
    .fail-banner { padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #842029; text-align: center; border: 2px solid #dc3545; margin-bottom: 15px; }
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

# --- QUIZ_DATA（全31問・全選択肢18文字以内・カテゴリー/難易度なし） ---
QUIZ_DATA = [
    {
        "id": 1,
        "question": "法隆寺地域の仏教建造物が日本で初めて世界遺産に登録された年はいつか。",
        "options": ["① 1985年", "② 1993年", "③ 1997年", "④ 2000年"],
        "answer": "② 1993年",
        "explanation": "正解は「1993年」です。姫路城とともに、日本で初めて世界遺産（文化遺産）に登録されました。",
        "tag": "登録年: 1993年 / 基準(i)(ii)(iv)(vi)",
        "trivia": "法隆寺の金堂や五重塔は、世界最古の木造建築群として知られています。"
    },
    {
        "id": 2,
        "question": "姫路城の別称として正しいものはどれか。",
        "options": ["① 烏城", "② 鶴ヶ城", "③ 白鷺城", "④ 金城"],
        "answer": "③ 白鷺城",
        "explanation": "正解は「白鷺城（しらさぎじょう）」です。鮮やかな白漆喰の壁が羽を広げた白鷺に例えられます。",
        "tag": "登録年: 1993年 / 基準(i)(iv)",
        "trivia": "姫路城の大天守は、江戸時代初期の優れた城郭建築の最高傑作です。"
    },
    {
        "id": 3,
        "question": "古都京都の文化財の構成資産に含まれない寺社・城郭はどれか。",
        "options": ["① 清水寺", "② 二条城", "③ 東大寺", "④ 下鴨神社"],
        "answer": "③ 東大寺",
        "explanation": "正解は「東大寺」です。東大寺は「古都奈良の文化財」の構成資産です。",
        "tag": "登録年: 1994年 / 基準(ii)(iv)",
        "trivia": "古都京都の文化財は、京都市・宇治市・大津市にまたがる17の資産で構成されています。"
    },
    {
        "id": 4,
        "question": "白川郷・五箇山の合掌造り集落において、特徴的な急勾配の屋根の角度はおおよそ何度か。",
        "options": ["① 30〜40度", "② 45〜60度", "③ 70〜80度", "④ 90度"],
        "answer": "② 45〜60度",
        "explanation": "正解は「45〜60度」です。豪雪地帯の重い雪が滑り落ちやすいように急勾配になっています。",
        "tag": "登録年: 1995年 / 基準(iv)(v)",
        "trivia": "合掌造りの屋根裏は、かつて重要な産業であった養蚕の作業場として利用されていました。"
    },
    {
        "id": 5,
        "question": "厳島神社（広島県）の社殿が海上に建てられている理由として正しいものはどれか。",
        "options": ["① 津波を防ぐため", "② 島全体が神域のため", "③ 海上交通の目印", "④ 要塞にするため"],
        "answer": "② 島全体が神域のため",
        "explanation": "弥山全体がご神体として信仰されていたため、大地を傷つけぬよう海上に造られました。",
        "tag": "登録年: 1996年 / 基準(i)(ii)(iv)",
        "trivia": "満潮時には社殿や大鳥居が海に浮かんでいるように見える、世界でも珍しい神社です。"
    },
    {
        "id": 6,
        "question": "奈良時代の仏教文化を伝える「古都奈良の文化財」の構成資産に含まれないものはどれか。",
        "options": ["① 平城宮跡", "② 唐招提寺", "③ 興福寺", "④ 平等院鳳凰堂"],
        "answer": "④ 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。平等院は京都府宇治市にあり「古都京都の文化財」の構成資産です。",
        "tag": "登録年: 1998年 / 基準(ii)(iv)(vi)",
        "trivia": "奈良の文化財は、平城宮跡や東大寺など平城京ゆかりの8資産で構成されています。"
    },
    {
        "id": 7,
        "question": "日光の社寺（栃木県）で、世界遺産登録の対象となっている社寺の数と内訳はどれか。",
        "options": ["① 2社1寺", "② 3社3寺", "③ 1社2寺", "④ 5社5寺"],
        "answer": "① 2社1寺",
        "explanation": "正解は「2社1寺」です。二荒山神社、日光東照宮の2社と、日光山輪王寺の1寺で構成されています。",
        "tag": "登録年: 1999年 / 基準(i)(iv)(vi)",
        "trivia": "境内には国宝や重要文化財に指定された荘厳な建造物が多数立ち並んでいます。"
    },
    {
        "id": 8,
        "question": "平泉－仏国土（浄土）を表現する遺跡群（岩手県）において、中心的な存在である寺院はどれか。",
        "options": ["① 中尊寺", "② 円覚寺", "③ 善光寺", "④ 金沢寺"],
        "answer": "① 中尊寺",
        "explanation": "正解は「中尊寺」です。金色堂に代表されるように、仏国土を地上に再現しようとした思想が形になっています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi)",
        "trivia": "平泉の遺跡群は、奥州藤原氏が築いた独自の浄土思想を伝える貴重な文化遺産です。"
    },
    {
        "id": 9,
        "question": "法隆寺の金堂や五重塔に代表される、世界最古の木造建築群が持つ建築様式の特徴はどれか。",
        "options": ["① 伝統的木造軸組構法", "② すべて石造りの壁", "③ 鉄筋コンクリート製", "④ レンガ造りアーチ"],
        "answer": "① 伝統的木造軸組構法",
        "explanation": "釘を一切使わない飛鳥時代の優れた木造建築技術（伝統的木造軸組構法）が受け継がれています。",
        "tag": "建築技術 / 基準(i)(iv)",
        "trivia": "日本の木造建築は湿潤な気候に適しており、高い耐震性と耐久性を誇ります。"
    },
    {
        "id": 10,
        "question": "古都京都の文化財の構成資産の一つである「宇治市」にある世界遺産といえばどこか。",
        "options": ["① 平等院鳳凰堂", "② 石山寺の本堂", "③ 三井寺の金堂", "④ 醍醐寺の五重塔"],
        "answer": "① 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。10円硬貨のデザインにも描かれている平安時代の阿弥陀堂建築です。",
        "tag": "構成資産: 平等院・宇治上神社",
        "trivia": "宇治上神社は日本最古の神社建築本殿として知られています。"
    },
    {
        "id": 11,
        "question": "屋久島に自生する樹齢数千年を超える代表的な植物はどれか。",
        "options": ["① ブナの巨木", "② 屋久杉（スギ）", "③ ヒノキの古木", "④ 天然のマツ"],
        "answer": "② 屋久杉（スギ）",
        "explanation": "正解は「屋久杉（スギ）」です。標高500mを超える山地に自生しており、ユネスコ自然遺産に登録されています。",
        "tag": "登録年: 1993年 / 基準(vii)(ix)",
        "trivia": "屋久島は豊かな降水量に恵まれ、独特の垂直分布を持つ生態系が広がっています。"
    },
    {
        "id": 12,
        "question": "白神山地が世界自然遺産に登録される決め手となった、原生的な森林を構成する樹木はどれか。",
        "options": ["① アカマツ", "② スギ林", "③ ブナの原生林", "④ カエデの林"],
        "answer": "③ ブナの原生林",
        "explanation": "正解は「ブナの原生林」です。人手の加わっていない世界最大級のブナ林が残されていることが評価されました。",
        "tag": "登録年: 1993年 / 基準(ix)",
        "trivia": "白神山地は青森県と秋田県にまたがる広大な山地です。"
    },
    {
        "id": 13,
        "question": "知床が世界自然遺産に登録された最大の理由として評価された生態系上の特徴はどれか。",
        "options": ["① 亜熱帯のマングローブ", "② 流氷と陸上生態系の関係", "③ 標高3000mの高山帯", "④ 固有の砂漠気候帯"],
        "answer": "② 流氷と陸上生態系の関係",
        "explanation": "低緯度で流氷が接岸し、海の生き物と陸の動物が密接につながっている点が評価されました。",
        "tag": "登録年: 2005年 / 基準(ix)(x)",
        "trivia": "知床は北半球における流氷の南限にあたります。"
    },
    {
        "id": 14,
        "question": "小笠原諸島が自然遺産に登録された主な理由は何か。",
        "options": ["① 大規模なサンゴ礁", "② 独自の進化（固有種）", "③ 世界最大の活火山", "④ 深海魚の豊かな生態系"],
        "answer": "② 独自の進化（固有種）",
        "explanation": "一度も大陸と陸続きになったことがない海洋島で、生物が独自の進化を遂げたためです。",
        "tag": "登録年: 2011年 / 基準(ix)",
        "trivia": "小笠原諸島は「東洋のガラパゴス」とも称される独自の生態系を持っています。"
    },
    {
        "id": 15,
        "question": "奄美大島、徳之島、沖縄島北部及び西表島が自然遺産に登録された最大の要因はどれか。",
        "options": ["① 固有種・絶滅危惧種", "② 日本最大のサンゴ礁", "③ 世界一の年間降水量", "④ 完全な無人島であること"],
        "answer": "① 固有種・絶滅危惧種",
        "explanation": "アマミノクロウサギなど高い固有種・絶滅危惧種の生息地であることが評価されました。",
        "tag": "登録年: 2021年 / 基準(x)",
        "trivia": "イリオモテヤマネコやヤンバルクイナなど、世界的にも貴重な固有種が生息しています。"
    },
    {
        "id": 16,
        "question": "富士山－信仰の対象と芸術の源泉（静岡・山梨県）の登録種別はどれか。",
        "options": ["① 自然遺産", "② 文化遺産", "③ 複合遺産", "④ 無形文化遺産"],
        "answer": "② 文化遺産",
        "explanation": "正解は「文化遺産」です。自然遺産ではなく、信仰や芸術の源泉として文化遺産に登録されています。",
        "tag": "登録年: 2013年 / 基準(iii)(vi)",
        "trivia": "富士山はその美しい容姿から、古くより人々の信仰の対象であり芸術のモチーフでした。"
    },
    {
        "id": 17,
        "question": "原爆ドーム（広島平和記念碑）の設計を手掛けた建築家の出身国はどこか。",
        "options": ["① チェコ", "② ドイツ", "③ フランス", "④ イギリス"],
        "answer": "① チェコ",
        "explanation": "正解は「チェコ」です。チェコ人の建築家ヤン・レッツェルによって設計されました。",
        "tag": "登録年: 1996年 / 基準(vi)",
        "trivia": "原爆ドームは核兵器の惨禍を今に伝える負の歴史の象徴です。"
    },
    {
        "id": 18,
        "question": "琉球王国のグスク及び関連遺産群の中で、首里城跡とともに登録された城の名称はどれか。",
        "options": ["① 熊本城の跡地", "② 中城城跡", "③ 大阪城の石垣", "④ 名古屋城の天守"],
        "answer": "② 中城城跡",
        "explanation": "正解は「中城城跡」です。沖縄県にある幾つものグスク（城）や関連遺産が登録されています。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi)",
        "trivia": "琉球のグスクは独特の曲りくねった城壁や高度な石積み技術が見られます。"
    },
    {
        "id": 19,
        "question": "紀伊山地の霊場と参詣道において、3つの「霊場」に含まれないものはどれか。",
        "options": ["① 高野山", "② 吉野・大峯", "③ 熊野三山", "④ 比叡山"],
        "answer": "④ 比叡山",
        "explanation": "正解は「比叡山」です。比叡山は京都・滋賀にあり、紀伊山地の霊場には含まれません。",
        "tag": "登録年: 2004年 / 基準(ii)(iii)(iv)(vi)",
        "trivia": "紀伊山地の霊場と参詣道は、神仏習合の文化を色濃く残す壮大な文化的景観です。"
    },
    {
        "id": 20,
        "question": "石見銀山遺跡（島根県）の世界遺産登録の決め手となった、特徴的な鉱石採掘・精錬法は何か。",
        "options": ["① 水銀圧搾法", "② 灰吹法", "③ アマルガム法", "④ 露天掘り手法"],
        "answer": "② 灰吹法",
        "explanation": "正解は「灰吹法（はいふきほう）」です。銀を効率よく抽出する高度な技術として評価されました。",
        "tag": "登録年: 2007年 / 基準(ii)(iii)",
        "trivia": "石見銀山で生産された銀は、16〜17世紀の世界的銀流通に大きな影響を与えました。"
    },
    {
        "id": 21,
        "question": "富岡製糸場と絹産業遺産群（群馬県）の構成資産に含まれないものはどれか。",
        "options": ["① 富岡製糸場", "② 荒船風穴", "③ 高山社跡", "④ 横浜赤レンガ倉庫"],
        "answer": "④ 横浜赤レンガ倉庫",
        "explanation": "正解は「横浜赤レンガ倉庫」です。富岡製糸場、田島家住宅、高山社跡、荒船風穴の4資産です。",
        "tag": "登録年: 2014年 / 基準(ii)(iv)",
        "trivia": "日本の近代化を支えた製糸・蚕糸業の技術革新を物語る遺産群です。"
    },
    {
        "id": 22,
        "question": "明治日本の産業革命遺産の構成資産として正しくないものはどれか。",
        "options": ["① 官営八幡製鉄所", "② 軍艦島（端島炭坑）", "③ 長崎グラバー住宅", "④ 萩反射炉"],
        "answer": "③ 長崎グラバー住宅",
        "explanation": "正解は「長崎グラバー住宅」です。グラバー園内の旧住宅は世界遺産の構成資産ではありません。",
        "tag": "登録年: 2015年 / 基準(ii)(iv)",
        "trivia": "重工業・造船・製鉄などの分野における日本および世界の産業発展の歴史を伝えています。"
    },
    {
        "id": 23,
        "question": "「神宿る島」宗像・沖ノ島と関連遺産群において、一般人の立ち入りが原則禁止されている島はどれか。",
        "options": ["① 沖ノ島", "② 大島", "③ 相島", "④ 宗像大島"],
        "answer": "① 沖ノ島",
        "explanation": "正解は「沖ノ島」です。島全体がご神体であり、今でも厳格な禁忌が守られています。",
        "tag": "登録年: 2017年 / 基準(ii)(iii)",
        "trivia": "古代の祭祀遺跡から多数の国家鎮護の宝物が発見され、「海の正倉院」とも呼ばれます。"
    },
    {
        "id": 24,
        "question": "長崎と天草地方の潜伏キリシタン関連遺産の構成資産に含まれないものはどれか。",
        "options": ["① 大浦天主堂", "② 原城跡", "③ 久賀島の集落", "④ 首里城跡"],
        "answer": "④ 首里城跡",
        "explanation": "正解は「首里城跡」です。首里城跡は沖縄県の世界遺産であり、潜伏キリシタン関連遺産には含まれません。",
        "tag": "登録年: 2018年 / 基準(iii)",
        "trivia": "禁教期に独自の信仰を密かに続けた人々の歴史と文化的伝統を伝えています。"
    },
    {
        "id": 25,
        "question": "北海道・北東北の縄文遺跡群の代表的な構成資産として正しくないものはどれか。",
        "options": ["① 三内丸山遺跡", "② 大湯環状列石", "③ 函館山要塞跡", "④ 小牧野遺跡"],
        "answer": "③ 函館山要塞跡",
        "explanation": "正解は「函館山要塞跡」です。近代の軍事遺跡であり、縄文遺跡群には含まれません。",
        "tag": "登録年: 2021年 / 基準(iii)(v)",
        "trivia": "採集・漁労・狩猟による定住生活の発展と精神文化を示す貴重な遺跡群です。"
    },
    {
        "id": 26,
        "question": "佐渡島の金山が新しく世界文化遺産に登録された年はいつか。",
        "options": ["① 2022年", "② 2023年", "③ 2024年", "④ 2025年"],
        "answer": "③ 2024年",
        "explanation": "正解は「2024年」です。インドのニューデリーで開催された世界遺産委員会で登録が決定しました。",
        "tag": "登録年: 2024年 / 基準(iv)",
        "trivia": "手作業による伝統的な採掘技術から近代的な機械化まで、長期間の生産システムが良好に残されています。"
    },
    {
        "id": 27,
        "question": "世界遺産条約が採択された年はいつか。",
        "options": ["① 1945年", "② 1972年", "③ 1992年", "④ 2003年"],
        "answer": "② 1972年",
        "explanation": "正解は「1972年」のユネスコ総会で採択されました。",
        "tag": "ユネスコ総会での採択年",
        "trivia": "正式名称は「世界の文化及び自然遺産の保護に関する条約」です。"
    },
    {
        "id": 28,
        "question": "ユネスコ（UNESCO）の本部が置かれている都市はどこか。",
        "options": ["① ジュネーブ", "② ニューヨーク", "③ パリ", "④ ローマ"],
        "answer": "③ パリ",
        "explanation": "正解は「パリ（フランス）」です。ユネスコの本部はパリに置かれています。",
        "tag": "国際機関の本部",
        "trivia": "ユネスコは教育・科学・文化の発展と協力を通じて平和に貢献することを目指しています。"
    },
    {
        "id": 29,
        "question": "世界遺産の登録基準において、文化遺産の基準の数はいくつあるか。",
        "options": ["① 4つ（(i)〜(iv)）", "② 6つ（(i)〜(vi)）", "③ 10つ（(i)〜(x)）", "④ 12つ"],
        "answer": "② 6つ（(i)〜(vi)）",
        "explanation": "正解は「6つ（(i)〜(vi)」です。自然遺産の基準は4つであり、合わせて10個の基準があります。",
        "tag": "検定頻出：登録基準の数",
        "trivia": "文化遺産は(i)〜(vi)、自然遺産は(vii)〜(x)の基準が設けられています。"
    },
    {
        "id": 30,
        "question": "世界遺産リストに登録されるための条件として最も重要な概念は何か。",
        "options": ["① 顕著な普遍的価値（OUV）", "② 年間100万人の観光客", "③ 最新のハイテク建築", "④ 入場料が無料であること"],
        "answer": "① 顕著な普遍的価値（OUV）",
        "explanation": "正解は「顕著な普遍的価値（OUV）」です。人類全体にとってきわめて重要な価値が求められます。",
        "tag": "検定必須キーワード：OUV",
        "trivia": "OUV（Outstanding Universal Value）は世界遺産の審査において最も核心となる基準です。"
    },
    {
        "id": 31,
        "question": "次のうち、日本の「無形文化遺産」に登録されているものはどれか。",
        "options": ["① 法隆寺の金堂", "② 姫路城の大天守", "③ 和食（日本人の伝統食）", "④ 原爆ドームの遺構"],
        "answer": "③ 和食（日本人の伝統食）",
        "explanation": "正解は「和食」です。建造物などは世界遺産（文化遺産）、伝統技術や食文化などは無形文化遺産です。",
        "tag": "無形文化遺産と世界遺産の区別",
        "trivia": "無形文化遺産には、芸能や伝統工芸技術、食文化などが登録されています。"
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
if "bookmarked_ids" not in st.session_state:
    st.session_state.bookmarked_ids = set()
if "history" not in st.session_state:
    st.session_state.history = []
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
# 忘却曲線スケジュール用
if "forgetting_curve_log" not in st.session_state:
    st.session_state.forgetting_curve_log = {}
# ストリーク
if "study_dates" not in st.session_state:
    st.session_state.study_dates = {str(date.today())}

# ==========================================
# サイドバー（ダッシュボード・忘却曲線アラート）
# ==========================================
st.sidebar.title("📊 学習ダッシュボード")
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
    
    col_nav1, col_nav2, col_nav3 = st.columns(3)
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

    st.markdown("---")
    st.subheader("⚙️ カスタム練習クイズ")
    
    mode = st.radio(
        "📝 挑戦する問題数：",
        ["サクッと10問", "ハーフ20問", "全問網羅"],
        horizontal=True
    )
    
    st.write("")
    
    if st.button("🚀 カスタムクイズをスタート！", use_container_width=True):
        filtered_data = QUIZ_DATA.copy()
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
# 3. 📇 暗記カードモード
# ==========================================
elif st.session_state.app_mode == "flashcard":
    st.subheader("📇 暗記カードモード（音声読み上げ対応）")
    
    mastered_cnt = len(st.session_state.mastered_card_ids)
    total_cnt = len(QUIZ_DATA)
    st.progress(mastered_cnt / total_cnt if total_cnt > 0 else 0)
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
        
        st.markdown(f"**カード {idx+1} / {len(fc_list)}** | {status_badge}")
        
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
# 4. クイズ・模擬試験プレイ画面
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
            st.session_state.forgetting_curve_log[q["id"]] = str(datetime.now())
            
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
            is_bm = q["id"] in st.session_state.bookmarked_ids
            bm_label = "⭐ 登録済" if is_bm else "☆ ブックマーク"
            if st.button(bm_label, key=f"bm_{q['id']}_{st.session_state.current_q}", use_container_width=True):
                if is_bm:
                    st.session_state.bookmarked_ids.remove(q["id"])
                else:
                    st.session_state.bookmarked_ids.add(q["id"])
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
                        if q["id"] in st.session_state.forgetting_curve_log:
                            del st.session_state.forgetting_curve_log[q["id"]]
                    else:
                        orig_q = next((item for item in QUIZ_DATA if item["id"] == q["id"]), q)
                        if orig_q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(orig_q)
                        st.session_state.forgetting_curve_log[q["id"]] = str(datetime.now())
                    
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
    # 5. 結果発表画面
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

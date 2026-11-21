import random
import re
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
    /* 選択肢ボタンの箱を大きくし、長文でも折り返して収まるように調整 */
    div.stButton > button {
        min-height: 64px;
        height: auto !important;
        padding: 14px 18px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.5 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
    div.stButton > button p {
        font-size: 1.05rem !important;
        margin: 0 !important;
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
    },
    {
        "question": "1992年に採択された「文化的景観」の概念が、1993年に世界で初めて適用された遺産はどれか。",
        "options": ["① トンガリロ国立公園", "② イエローストーン国立公園", "③ 屋久島", "④ 法隆寺地域の仏教建造物"],
        "answer": "① トンガリロ国立公園",
        "explanation": "正解は「トンガリロ国立公園」です。1992年に採択された文化的景観の概念は、1993年にニュージーランドの『トンガリロ国立公園』で初めて適用されました。",
        "tag": "採択年: 1992年 / 初適用: 1993年",
        "trivia": "文化的景観は文化遺産に分類されますが、文化遺産と自然遺産の境界に位置する遺産といえます。"
    },
    {
        "question": "文化的景観の3つのカテゴリーのうち、「庭園や公園、宗教的空間など、人間によって意図的に設計され創造された景観」を指すものはどれか。",
        "options": ["① 意匠された景観", "② 有機的に進化する景観", "③ 関連する景観", "④ 継続する景観"],
        "answer": "① 意匠された景観",
        "explanation": "正解は「意匠された景観」です。文化的景観は『意匠された景観』『有機的に進化する景観』『関連する景観』の3つのカテゴリーに分類されます。",
        "tag": "文化的景観 / 3つのカテゴリー",
        "trivia": "『関連する景観』は、自然の要素がその地の民族に大きな影響を与え、宗教的、芸術的、文学的な要素と強く関連する景観を指します。"
    },
    {
        "question": "文化的景観のカテゴリーの一つ「有機的に進化する景観」のうち、すでに発展過程が終了している景観を何と呼ぶか。",
        "options": ["① 残存する景観", "② 継続する景観", "③ 意匠された景観", "④ 関連する景観"],
        "answer": "① 残存する景観",
        "explanation": "正解は「残存する景観」です。『有機的に進化する景観』は、すでに発展過程が終了している『残存する景観』と、現在も伝統的な社会のなかで進化する『継続する景観』に分けられます。",
        "tag": "有機的に進化する景観 / 分類",
        "trivia": "有機的に進化する景観は、社会や経済、政治、宗教などの要求によって生まれ、農林水産業などの産業とも関連しています。"
    },
    {
        "question": "国境線を越えて多国間に広がる自然遺産などを登録する際に考えられ、多国間の協力の下で遺産を保護・保全することを目指す概念はどれか。",
        "options": ["① トランスバウンダリー・サイト", "② シリアル・サイト", "③ バッファー・ゾーン", "④ 危機遺産"],
        "answer": "① トランスバウンダリー・サイト",
        "explanation": "正解は「トランスバウンダリー・サイト」です。国境を越える遺産の概念であり、文化遺産でもかつてひとつの文化圏であった地域が国境で分断されている場合などに用いられます。",
        "tag": "トランスバウンダリー・サイト",
        "trivia": "自然遺産ではオランダとドイツ、デンマークにまたがる『ワッデン海』、文化遺産ではスペインとスロベニアにまたがる『アルマデンとイドリア：水銀鉱山の遺跡』などが例として挙げられています。"
    },
    {
        "question": "文化や歴史的背景、自然環境などが共通する資産を、ひとつの遺産として顕著な普遍的価値を有するものとみなし登録する仕組みを何と呼ぶか。",
        "options": ["① トランスバウンダリー・サイト", "② シリアル・サイト", "③ 文化的景観", "④ グローバル・ストラテジー"],
        "answer": "② シリアル・サイト",
        "explanation": "正解は「シリアル・サイト」です。連続性のある遺産を指し、文化遺産では中国の『福建土楼群』、自然遺産ではロシアの『カムチャツカ火山群』などがあたります。",
        "tag": "シリアル・サイト",
        "trivia": "それぞれの資産が国境を越えて存在する場合、トランスバウンダリー・サイトともなります。"
    },
    {
        "question": "近年、小笠原諸島から東京湾までを世界遺産管理エリアとして保護するなど、遺産保護のあり方も多様化している中で、従来の代わりに設定されることがある区域はどれか。",
        "options": ["① バッファー・ゾーン", "② 特別保護地区", "③ 生態系回廊", "④ 文化圏エリア"],
        "answer": "① バッファー・ゾーン",
        "explanation": "正解は「バッファー・ゾーン」です。世界遺産では遺産を「資産（プロパティ）」と呼び、バッファー・ゾーンを設定する代わりに広域を管理エリアとして保護する例などが見られます。",
        "tag": "遺産保護の多様化",
        "trivia": "『小笠原諸島』では、バッファー・ゾーンを設定する代わりに小笠原諸島から東京湾までを世界遺産管理エリアとして保護する取り組みが紹介されています。"
    },
    {
        "question": "世界で最初の世界遺産が誕生した翌年の1979年に、地震の被害を受けて初めて危機遺産リストに記載された遺産はどれか。",
        "options": ["① モンテネグロの『コトルの文化歴史地域と自然』", "② オマーンの『アラビアオリックスの保護地区』", "③ ドイツの『ドレスデン・エルベ渓谷』", "④ 英国の『リヴァプール海商都市』"],
        "answer": "① モンテネグロの『コトルの文化歴史地域と自然』",
        "explanation": "正解は「モンテネグロの『コトルの文化歴史地域と自然』」です。1979年に自然災害により初めて危機遺産リストに記載されました。",
        "tag": "危機遺産",
        "trivia": "危機遺産リストに記載された場合、保有国は保全計画の作成と実行が求められ、世界遺産基金の活用や財政的・技術的援助を受けることが可能になります。"
    },
    {
        "question": "危機遺産リストに記載されることなく、保護区内での資源開発により2007年に世界遺産リストから削除された遺産はどれか。",
        "options": ["① アラビアオリックスの保護地区", "② ドレスデン・エルベ渓谷", "③ リヴァプール海商都市", "④ コトルの文化歴史地域と自然"],
        "answer": "① アラビアオリックスの保護地区",
        "explanation": "正解は「アラビアオリックスの保護地区」です。2007年にオマーンの同遺産が、2009年にドイツの『ドレスデン・エルベ渓谷』が、2021年には英国の『リヴァプール海商都市』が世界遺産リストから削除されています。",
        "tag": "世界遺産リストからの削除",
        "trivia": "『ドレスデン・エルベ渓谷』は橋の建設による景観破壊、『リヴァプール海商都市』はバッファー・ゾーンを含む港湾開発が削除の原因とされています。"
    },
    {
        "question": "近年、都市部における経済開発による景観破壊や、紛争による遺産破壊などが問題となる例として挙げられている遺産はどれか。",
        "options": ["① 『ウィーンの歴史地区』やシリア・ヤマリの遺産", "② 『ワッデン海』や『アルマデンとイドリア』", "③ 『福建土楼群』や『カムチャツカ火山群』", "④ 『小笠原諸島』や『コトルの文化歴史地域と自然』"],
        "answer": "① 『ウィーンの歴史地区』やシリア・ヤマリの遺産",
        "explanation": "正解は「『ウィーンの歴史地区』やシリア・ヤマリの遺産」です。武力紛争・戦争による破壊、都市開発や観光開発による景観悪化、密猟や違法伐採など、重大かつ明確な危険にさらされる場合に危機遺産リストに記載されます。",
        "tag": "危機遺産の要因",
        "trivia": "自然遺産の場合、一度遺産の価値が損なわれると修復が難しいこともあり、早めの対応が求められます。"
    },
    {
        "question": "登録基準のうち、「人類の創造的資質を示す傑作。」と定義されているものはどれか。",
        "options": ["① (i)", "② (ii)", "③ (iii)", "④ (iv)"],
        "answer": "① (i)",
        "explanation": "正解は「(i)」です。登録基準(i)は「人類の創造的資質を示す傑作。」を指します。",
        "tag": "登録基準(i)",
        "trivia": "登録基準(ii)は建築や技術、記念碑、都市計画、景観設計の発展において、ある期間または世界の文化圏内での重要な価値観の交流を示すものです。"
    },
    {
        "question": "登録基準のうち、「ひときわ優れた自然美や美的重要性をもつ、類まれな自然現象や地域。」と定義されているものはどれか。",
        "options": ["① (vi)", "② (vii)", "③ (viii)", "④ (ix)"],
        "answer": "② (vii)",
        "explanation": "正解は「(vii)」です。登録基準(vii)は自然美や美的重要性をもつ自然現象や地域に関する基準です。",
        "tag": "登録基準(vii)",
        "trivia": "登録基準(viii)は生命の進化の記録や地形形成における重要な地質学的過程、または地形学的・自然地理学的特徴を含む、地球の歴史の主要段階を示す顕著な見本です。"
    },
    {
        "question": "登録基準のうち、「絶滅の恐れのある、学術上・保全上顕著な普遍的価値をもつ野生種の生息域を含む、生物多様性の保全のために最も重要かつ代表的な自然生息域。」と定義されているものはどれか。",
        "options": ["① (vii)", "② (viii)", "③ (ix)", "④ (x)"],
        "answer": "④ (x)",
        "explanation": "正解は「(x)」です。登録基準(x)は絶滅危惧種の生息域などで、生物多様性を示す遺産に関わる基準です。",
        "tag": "登録基準(x)",
        "trivia": "登録基準(ix)は陸上や淡水域、沿岸、海洋の生態系、また動植物群集の進化、発展において重要な、現在進行中の生態学的・生物学的過程を表す顕著な見本です。"
    },
    {
        "question": "世界遺産委員会を構成する国の数と、通常開催される頻度の組み合わせとして正しいものはどれか。",
        "options": ["① 21カ国 － 1年に1度", "② 15カ国 － 2年に1度", "③ 25カ国 － 1年に1度", "④ 21カ国 － 2年に1度"],
        "answer": "① 21カ国 － 1年に1度",
        "explanation": "正解は「21カ国 － 1年に1度」です。世界遺産委員会は21カ国で構成され、通常1年に1度開催される政府間委員会で、世界遺産リストや危機遺産リストの記載に関する審議などを行います。",
        "tag": "世界遺産委員会",
        "trivia": "委員国の任期は6年ですが、各締約国に均等に機会が与えられるように、自発的に4年で任期を終えることや、任期終了後、次の立候補まで間を6年あけることなどが求められています。"
    },
    {
        "question": "1992年に設立され、パリのユネスコ本部内に常設されている世界遺産委員会事務局を担う機関はどれか。",
        "options": ["① 世界遺産センター", "② ICOMOS（イコモス）", "③ IUCN（アイユーシーエヌ）", "④ ICCROM（イクロム）"],
        "answer": "① 世界遺産センター",
        "explanation": "正解は「世界遺産センター」です。推薦書の受理や登録、世界遺産委員会の運営、世界遺産及び世界遺産条約の広報活動などを行います。",
        "tag": "世界遺産センター",
        "trivia": "ICOMOSは1965年設立（本部パリ・NGO）、IUCNは1948年設立（本部スイス・グラン）、ICCROMは1959年設立（本部イタリア・ローマ・政府間機関）で、いずれも世界遺産委員会に諮問機関として参加します。"
    },
    {
        "question": "文化財の保存及び修復の研究のための国際センターであり、本部をイタリアのローマにおく政府間機関はどれか。",
        "options": ["① ICCROM（イクロム）", "② ICOMOS（イコモス）", "③ IUCN（アイユーシーエヌ）", "④ 世界遺産条約締約国会議"],
        "answer": "① ICCROM（イクロム）",
        "explanation": "正解は「ICCROM（イクロム）」です。ユネスコでの採択を経て1959年に設立され、不動産と動産両方の文化遺産の保全強化を目的とした研究や記録の作成・助言、技術支援などを行います。",
        "tag": "ICCROM",
        "trivia": "ICOMOSは建築物や考古学的遺産の保全、IUCNは自然の多様性の保全と持続可能な自然資源の利用のために世界中の科学者を支援することを目的としています。"
    },
    {
        "question": "日本が世界遺産条約を締結した年と、そのときの締約国順の組み合わせとして正しいものはどれか。",
        "options": ["① 1992年 － 125番目", "② 1993年 － 125番目", "③ 1992年 － 100番目", "④ 1972年 － 125番目"],
        "answer": "① 1992年 － 125番目",
        "explanation": "正解は「1992年 － 125番目」です。1951年に第二次世界大戦後最初に加盟した国際機関はユネスコであり、1972年に世界遺産条約がユネスコ総会で採択されたときの議長国は日本でした。",
        "tag": "日本と世界遺産",
        "trivia": "2024〜2025年の分担金では、日本はアメリカ合衆国と中華人民共和国に次ぐ3番目のユネスコ分担金拠出国として約8％の金額を拠出しています。"
    },
    {
        "question": "日本の自然遺産について、暫定リストの中から推薦候補を決定する際に協議を行う省庁の組み合わせはどれか。",
        "options": ["① 環境省と林野庁", "② 文化庁と内閣官房", "③ 環境省と文部科学省", "④ 文化庁と環境省"],
        "answer": "① 環境省と林野庁",
        "explanation": "正解は「環境省と林野庁」です。日本の文化財や記念物は、文化財保護法などの保護下にあるものは文化庁が、稼働中の産業遺産などを含むものは2013年より内閣官房がそれぞれ暫定リストから推薦候補を決定します。",
        "tag": "推薦候補の決定",
        "trivia": "それぞれの推薦候補の中から毎年9月頃に開催される「世界遺産条約関係省庁連絡会議」でユネスコの世界遺産センターへ推薦する候補が選出され、最終的に閣議了解されます。"
    },
    {
        "question": "環境資源の持続可能な利用と環境保全を促進することを目的に進められている計画はどれか。",
        "options": ["① 人間と生物圏計画（MAB計画）", "② グローバル・ストラテジー", "③ ヌビアの遺跡群救済キャンペーン", "④ ヴェネツィア憲章"],
        "answer": "① 人間と生物圏計画（MAB計画）",
        "explanation": "正解は「人間と生物圏計画（MAB計画）」です。ユネスコが推進する計画で、生物圏保存地域の区域分け（核心地域・緩衝地域・移行地帯など）が行われます。",
        "tag": "MAB計画",
        "trivia": "世界遺産登録を目指す日本の遺産では、保護法制や管理体制の枠組みともあわせて持続可能な保全が重視されます。"
    },
    {
        "question": "次の出来事のうち、1959年に起きたものとして正しいものはどれか。",
        "options": ["① ICCROM設立", "② IUCN設立", "③ ICOMOS設立", "④ ハーグ条約採択"],
        "answer": "① ICCROM設立",
        "explanation": "正解は「ICCROM設立」です。年表では1948年にIUCN設立、1954年にハーグ条約採択、1959年にICCROM設立、1965年にICOMOS設立となっています。",
        "tag": "年表・1959年",
        "trivia": "1931年のアテネ憲章採択、1960年のヌビアの遺跡群救済キャンペーン開始、1964年のヴェネツィア憲章採択なども重要な流れとして整理されています。"
    },
    {
        "question": "1972年に起きた出来事として正しいものはどれか。",
        "options": ["① 世界遺産条約採択・国連人間環境会議開催", "② 最初の世界遺産12件が誕生", "③ 文化的景観採択・ユネスコの世界遺産センター設立", "④ グローバル・ストラテジー採択"],
        "answer": "① 世界遺産条約採択・国連人間環境会議開催",
        "explanation": "正解は「世界遺産条約採択・国連人間環境会議開催」です。1972年に国連人間環境会議の開催や世界遺産条約の採択が行われ、1978年に最初の世界遺産12件が誕生しました。",
        "tag": "年表・1972年",
        "trivia": "1992年には日本が世界遺産条約を締結したほか、ユネスコの世界遺産センター設立や文化的景観採択があり、1994年にグローバル・ストラテジーが採択されました。"
    },
    {
        "question": "年表の出来事について、起きた順として正しいものはどれか。",
        "options": [
            "① 1945年 ユネスコ憲章採択 → 1964年 ヴェネツィア憲章採択 → 1978年 最初の世界遺産12件が誕生",
            "② 1964年 ヴェネツィア憲章採択 → 1945年 ユネスコ憲章採択 → 1978年 最初の世界遺産12件が誕生",
            "③ 1978年 最初の世界遺産12件が誕生 → 1964年 ヴェネツィア憲章採択 → 1994年 グローバル・ストラテジー採択",
            "④ 1992年 日本が世界遺産条約締結 → 1972年 世界遺産条約採択 → 1994年 グローバル・ストラテジー採択"
        ],
        "answer": "① 1945年 ユネスコ憲章採択 → 1964年 ヴェネツィア憲章採択 → 1978年 最初の世界遺産12件が誕生",
        "explanation": "正解は「1945年 ユネスコ憲章採択 → 1964年 ヴェネツィア憲章採択 → 1978年 最初の世界遺産12件が誕生」です。1945年（第二次世界大戦終結・ユネスコ憲章採択）、1964年（ヴェネツィア憲章採択）、1978年（最初の世界遺産12件誕生）の順です。",
        "tag": "時系列・順番",
        "trivia": "1931年のアテネ憲章採択から始まり、1994年のグローバル・ストラテジー採択に至る流れを押さえておくと整理しやすくなります。"
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

        # 長文選択肢でも読みやすく枠内に収まるよう1列で大きく表示
        for i, option in enumerate(q["options"]):
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
            if st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>正解は <b>{q["answer"]}</b> です。</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="explanation-box">
                    <b>💡 解説:</b> {q['explanation']}<br><br>
                    <span style="font-size: 0.9em; background-color: #ffffff; padding: 3px 6px; border-radius: 4px; color: #084298;">📌 <b>検定ポイント:</b> {q['tag']}</span>
                </div>
            """, unsafe_allow_html=True)

            if st.button("次の問題へ ➡️", type="primary", use_container_width=True):
                st.session_state.current_q += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
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

import random
import re
from datetime import date, datetime
import streamlit as st

st.set_page_config(
    page_title="日本の世界遺産検定 4択マスター",
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

# ここに問題を追加してください
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
    "question": "「北海道・北東北の縄文遺跡群」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2021年に登録された文化遺産で、構成資産は17の考古遺跡からなる。",
      "② 岩手県、宮城県、秋田県、青森県の4県に位置する。",
      "③ 農耕社会への移行と定着の過程を示す資産である。",
      "④ 登録基準は（i）（iv）が適用されている。"
    ],
    "answer": "① 2021年に登録された文化遺産で、構成資産は17の考古遺跡からなる。",
    "explanation": "正解は①です。「北海道・北東北の縄文遺跡群」は2021年に登録された文化遺産で、北海道・青森県・岩手県・秋田県の17の考古遺跡で構成されています[cite: 22]。②は宮城県ではなく北海道[cite: 22]、③は農耕社会以前（狩猟・漁労・採集による定住）[cite: 22]、④は登録基準（iii）（v）が正しい内容です[cite: 22]。",
    "tag": "登録年: 2021年 / 基準(iii)(v) / 北海道・北東北の縄文遺跡群",
    "trivia": "縄文時代は紀元前13000年から前400年の長期にわたり、定住の開始・発展・成熟の過程が6つのステージに区分されています[cite: 22, 23]。"
  },
  {
    "question": "「北海道・北東北の縄文遺跡群」の構成資産と、その特徴や位置づけの組み合わせとして、正しくないものはどれか。",
    "options": [
      "① 大平山元遺跡 — ステージ1「定住の開始」の「居住地の形成」にあたり、土器片が出土している。",
      "② 垣ノ島遺跡 — 定住開始の「集落の成立」にあたり、長期間居住できる竪穴建物の出現を示している。",
      "③ 三内丸山遺跡 — ステージ2「定住の発展」の「拠点集落の出現」にあたり、日本で最も多い2,000点を超える土偶などが出土している。",
      "④ 大湯環状列石 — ステージ3「定住の成熟」にあたり、最大径52mの万座と最大径44mの野中堂の3つの環状列石からなる。"
    ],
    "answer": "④ 大湯環状列石 — ステージ3「定住の成熟」にあたり、最大径52mの万座と最大径44mの野中堂の3つの環状列石からなる。",
    "explanation": "正解は④です。秋田県の大湯環状列石は最大径52mの「万座」と最大径44mの「野中堂」の「2つ」の環状列石からなります[cite: 23]（「3つ」ではありません）。①〜③はいずれも紙面の記載どおり正しい説明です[cite: 23]。",
    "tag": "登録年: 2021年 / 基準(iii)(v) / 構成資産",
    "trivia": "三内丸山遺跡では、竪穴建物や掘立柱建物、列状に並んだ土坑墓、埋設土器、盛土、貯蔵穴、道路、大型建物などが計画的に配置されていました[cite: 23]。"
  },
  {
    "question": "「北海道・北東北の縄文遺跡群」において、縄文時代を区分する3つの大きなステージの名称として、正しい組み合わせはどれか。",
    "options": [
      "① 定住の開始 — 定住の発展 — 定住の成熟",
      "② 集落の形成 — 拠点の拡大 — 祭祀の確立",
      "③ 定住の萌芽 — 集落の発展 — 社会の完成",
      "④ 居住の開始 — 文化の成熟 — 祭祀の分離"
    ],
    "answer": "① 定住の開始 — 定住の発展 — 定住の成熟",
    "explanation": "正解は①です。縄文時代は「定住の開始」「定住の発展」「定住の成熟」の3つの大きなステージに区分され、さらにそれぞれ2つに小区分して6つのステージに分けられています[cite: 22, 23]。",
    "tag": "登録年: 2021年 / 基準(iii)(v) / 6つのステージ",
    "trivia": "北海道、青森県、岩手県、秋田県の関係自治体は、包括的保存計画を策定し、縄文遺跡群世界遺産本部などを設置して保存・管理に取り組んでいます[cite: 23]。"
  },
  {
    "question": "「平泉—仏国土（浄土）を表す建築・庭園及び考古学的遺跡群—」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2011年に登録された文化遺産で、登録基準は（ii）（vi）が適用されている。",
      "② 奥州藤原氏ゆかりの遺産で、中尊寺、毛越寺、観自在王院跡、無量光院跡、高館の5資産からなる。",
      "③ 11世紀後半から12世紀後半の約200年間にわたり平泉は文化の隆盛を誇った。",
      "④ 軍事力を背景とした武家政治の中心地として栄えたことが評価された。"
    ],
    "answer": "① 2011年に登録された文化遺産で、登録基準は（ii）（vi）が適用されている。",
    "explanation": "正解は①です。2011年に登録された文化遺産で、登録基準は（ii）（vi）です[cite: 24]。②の5資産の最後は高館ではなく「金鶏山」[cite: 24]、③の隆盛は約100年間[cite: 24]、④は「軍事に頼らない平和的な政治」を実現したと記載されています[cite: 24]。",
    "tag": "登録年: 2011年 / 基準(ii)(vi) / 平泉",
    "trivia": "藤原清衡は堀河天皇の勅命を受けて中尊寺を再興し、金色堂を建立しました[cite: 24]。"
  },
  {
    "question": "「平泉—仏国土（浄土）を表す建築・庭園及び考古学的遺跡群—」の構成資産とその特徴の組み合わせとして、正しくないものはどれか。",
    "options": [
      "① 中尊寺 — 阿弥陀如来の極楽浄土を金箔で表現した金色堂には、藤原3代の遺体と4代泰衡の首級が納められている。",
      "② 毛越寺 — 12世紀中頃に2代基衡が造営した寺院で、「大泉が池」を中心とする浄土庭園には平安時代の遺構として日本唯一、最大規模の「遣水」が残る。",
      "③ 観自在王院跡 — 基衡の妻が建立し、1573年の火災で伽藍が焼失した後は浄土庭園が公園として残る。",
      "④ 無量光院跡 — 藤原3代で最も繁栄した時代を築いた基衡が、平等院鳳凰堂を模した阿弥陀堂を建築し、浄土庭園を造営した。"
    ],
    "answer": "④ 無量光院跡 — 藤原3代で最も繁栄した時代を築いた基衡が、平等院鳳凰堂を模した阿弥陀堂を建築し、浄土庭園を造営した。",
    "explanation": "正解は④です。無量光院を造営したのは基衡ではなく3代「秀衡」です[cite: 24, 25]。①〜③はいずれも紙面の記載どおり正しい組み合わせです[cite: 24, 25]。",
    "tag": "登録年: 2011年 / 基準(ii)(vi) / 構成資産",
    "trivia": "金鶏山は浄土庭園において仏国土を空間的に表現する際の中心的役割を果たす山です[cite: 25]。"
  },
  {
    "question": "「平泉—仏国土（浄土）を表す建築・庭園及び考古学的遺跡群—」の浄土庭園や建築に関する次の文中の空欄（ A ）、（ B ）に当てはまる語句の組み合わせとして、正しいものはどれか。\n\n「金色堂は、阿弥陀如来の仏国土（浄土）を表現した仏堂建築であり、自然崇拝と仏教の融合は、庭園設計と造園によって仏国土（浄土）を現世に創り上げるという、日本独自の方法を編み出した。仏教とともに伽藍造営や作庭の技術も伝来したが、これが日本古来の水辺の祭祀場における水景の理念と結びついて、独自の（ A ）を完成させた。このような浄土庭園は、（ B ）における建築・作庭技術の価値観の交流を示している。」",
    "options": [
      "① A. 浄土庭園 — B. 東アジア",
      "② A. 枯山水庭園 — B. 東南アジア",
      "③ A. 浄土庭園 — B. 南アジア",
      "④ A. 枯山水庭園 — B. 東アジア"
    ],
    "answer": "① A. 浄土庭園 — B. 東アジア",
    "explanation": "正解は①です。水辺の祭祀場における水景の理念と結びついて独自の「浄土庭園」を完成させ、「東アジア」における建築・作庭技術の価値観の交流を示していると記されています[cite: 25]。",
    "tag": "登録年: 2011年 / 基準(ii)(vi) / 浄土庭園",
    "trivia": "11世紀末には末法思想が広がり、浄土思想が興隆したことで、死後に仏国土（浄土）に行き成仏することが切望されるようになりました[cite: 25]。"
  },
  {
    "question": "「佐渡島の金山」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2024年に登録された文化遺産で、登録基準は（iv）が適用されている。",
      "② 新潟県北西部の沖合約35kmに浮かぶ佐渡島は、北部の小佐渡山地と南部の大佐渡山地、その間の国中平野に分かれる。",
      "③ 佐渡島に世界遺産として登録されたのは「西三川砂金山」と「道遊の割戸」の2つである。",
      "④ 佐渡島の金山では、16世紀後半から19世紀半ばまで機械化による大量採掘が続けられた。"
    ],
    "answer": "① 2024年に登録された文化遺産で、登録基準は（iv）が適用されている。",
    "explanation": "正解は①です。2024年に登録された文化遺産で、登録基準は（iv）です[cite: 26]。②は北部が「大佐渡山地」、南部が「小佐渡山地」[cite: 26]、③は「西三川砂金山」と「相川鶴子金銀山」[cite: 26]、④は機械化されておらず「手作業」による採掘が続けられました[cite: 27]。",
    "tag": "登録年: 2024年 / 基準(iv) / 佐渡島の金山",
    "trivia": "佐渡島にはかつて55の金、銀、銅、鉛の鉱山があったと考えられています[cite: 26]。"
  },
  {
    "question": "「佐渡島の金山」の2つの鉱山と、その鉱床の入り方や採掘方法の組み合わせとして、正しいものはどれか。",
    "options": [
      "① 西三川砂金山 — 山に対して横向きに入る「堆積砂金鉱床」で、水の勢いで採掘する「大流し」が行われた。",
      "② 西三川砂金山 — 山に対して縦に入る「鉱脈鉱床」で、「露頭掘り」や「坑道掘り」が行われた。",
      "③ 相川鶴子金銀山 — 山に対して横向きに入る「堆積砂金鉱床」で、「大流し」が行われた。",
      "④ 相川鶴子金銀山 — 砂金採掘に特化した「大流し」が行われ、小規模で専門分化していない生産体制の集落が形成された。"
    ],
    "answer": "① 西三川砂金山 — 山に対して横向きに入る「堆積砂金鉱床」で、水の勢いで採掘する「大流し」が行われた。",
    "explanation": "正解は①です。西三川砂金山は横向きに入る「堆積砂金鉱床」で「大流し」が行われ[cite: 26, 27]、相川鶴子金銀山は縦に入る「鉱脈鉱床」で「露頭掘り」や「坑道掘り」が行われ、専門分化した大規模な生産体制による計画的な大規模集落が形成されました[cite: 27]。",
    "tag": "登録年: 2024年 / 基準(iv) / 採掘技術",
    "trivia": "西三川砂金山は『今昔物語集』に砂金の採取が行われていたという説話が残る佐渡島最古の砂金山です[cite: 26]。"
  },
  {
    "question": "「佐渡島の金山」に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① 江戸時代を通じて徳川幕府の直轄領であり、幕府によって金生産に必要な人材が全国から集められた。",
      "② 佐渡島では鉱山に隣接して集落が形成され、その構造は各鉱山の特質や生産組織の変遷を反映している。",
      "③ 佐渡島の鉱山での労働は過酷であり、なかでも朝鮮半島出身者が排水作業などのより危険な労働に従事していた。",
      "④ 世界遺産委員会では韓国からの反発は一切予想されず、事前の両国政府間協議や説明の展示も行われなかった。"
    ],
    "answer": "④ 世界遺産委員会では韓国からの反発は一切予想されず、事前の両国政府間協議や説明の展示も行われなかった。",
    "explanation": "正解は④です。韓国からの反発も予想されたが、事前に両国政府間で協議が行われ説明の展示などもなされたことから、登録時に韓国政府代表が歴史の「正の面と負の面」を認識すべきなどのコメントを出したのみで、無事に登録されました[cite: 27]。",
    "tag": "登録年: 2024年 / 基準(iv) / 歴史と保全",
    "trivia": "幕府は金の産出量に応じて必要な投資を行い、労働条件の改善策を講じ、長期的・戦略的な観点から生産体制を維持するための生産設備の統合や再配置を行いました[cite: 27]。"
  },
  {
    "question": "「日光の社寺」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 1999年に登録された文化遺産で、登録基準は（i）（iv）（vi）が適用されている。",
      "② 東照宮、二荒山神社、輪王寺の二社一寺に属する103棟の建造物群のみが登録されている。",
      "③ 日光山の始まりは、修験者の天海が開山した8世紀末にさかのぼる。",
      "④ 東照宮は、徳川幕府2代将軍の徳川秀忠の時代に「寛永の大造替」と呼ばれる大改修を受けた。"
    ],
    "answer": "① 1999年に登録された文化遺産で、登録基準は（i）（iv）（vi）が適用されている。",
    "explanation": "正解は①です。1999年に登録された文化遺産で、登録基準は（i）（iv）（vi）です[cite: 28]。②は103棟の建造物群と「周辺の自然環境」[cite: 28]、③は開山したのは「勝道上人」[cite: 28]、④は「寛永の大造替」を受けたのは徳川幕府3代将軍「徳川家光」の時代です[cite: 28]。",
    "tag": "登録年: 1999年 / 基準(i)(iv)(vi) / 日光の社寺",
    "trivia": "東照宮を代表する建築物の陽明門は、高さ11.1m、横幅7mの大きさを誇り、500を超える彫刻で飾られています[cite: 28, 29]。"
  },
  {
    "question": "「日光の社寺」の構成資産である二社一寺に関する次の記述のうち、正しくないものはどれか。",
    "options": [
      "① 東照宮は天海が家康の霊廟として造営した神社で、家康は「東方薬師瑠璃光如来」として祀られている。",
      "② 二荒山神社の祭神は大己貴命、田心姫命、味耜高彦根命の三神で、日光山の主峰・男体山、女峰山、太郎山の山の神とされる。",
      "③ 二荒山神社の八棟造りで建てられた本社社殿は、寛永の大造替の前から残る貴重な建造物である。",
      "④ 輪王寺は勝道上人が766年に創建した四本龍寺を起源にもち、家光の霊廟である大猷院は金と黒を主体とする華やかな造りになっている。"
    ],
    "answer": "④ 輪王寺は勝道上人が766年に創建した四本龍寺を起源にもち、家光の霊廟である大猷院は金と黒を主体とする華やかな造りになっている。",
    "explanation": "正解は④です。輪王寺の「大猷院」は、家光の遺言により、金と黒を主体とする「落ち着いた造り」になっています[cite: 29]（「華やかな造り」ではありません）。①〜③は紙面の記載どおり正しい内容です[cite: 28, 29]。",
    "tag": "登録年: 1999年 / 基準(i)(iv)(vi) / 二社一寺",
    "trivia": "明治政府が神道を国家宗教にすることを目指して公布した神仏分離令により、山内の建造物は東照宮と二荒山神社、輪王寺の2社1寺に分けられました[cite: 29]。"
  },
  {
    "question": "「日光の社寺」の輪王寺に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 慈眼堂には1643年に没した勝道上人が祀られている。",
      "② 本堂の三仏堂は日光山内最大の建造物で、千手観音、阿弥陀如来、馬頭観音が祀られている。",
      "③ 三仏堂は江戸時代後期に現在の場所に移転された。",
      "④ 輪王寺からは国宝の二天門と重要文化財37棟の計39棟が世界遺産に登録されている。"
    ],
    "answer": "② 本堂の三仏堂は日光山内最大の建造物で、千手観音、阿弥陀如来、馬頭観音が祀られている。",
    "explanation": "正解は②です。三仏堂は日光山内最大の建造物で、千手観音、阿弥陀如来、馬頭観音が祀られています[cite: 29]。①の慈眼堂に祀られているのは「天海」[cite: 29]、③は「明治に入ってからの神仏分離令によって現在の場所に移転」[cite: 29]、④は国宝の「大猷院」と重要文化財37棟の計「38棟」が世界遺産に登録されています[cite: 29]。",
    "tag": "登録年: 1999年 / 基準(i)(iv)(vi) / 輪王寺",
    "trivia": "輪王寺は、天海が復興した60棟余りの建造物を含み、1653年には家光の霊廟である大猷院が造営されました[cite: 29]。"
  },
  {
    "question": "「富岡製糸場と絹産業遺産群」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2014年に登録された文化遺産で、登録基準は（ii）（iv）が適用されている。",
      "② 「富岡製糸場」「田島弥平旧宅」「高山社跡」「岩鼻火薬製造所跡」の4資産からなる。",
      "③ 富岡製糸場は1871年に操業を開始すると、高品質な生糸を輸出し世界中から高い評価を得た。",
      "④ 新たな製糸場の建設にあたり、高い製糸技術をもつイギリスから技師ポール・ブリュナが招聘された。"
    ],
    "answer": "① 2014年に登録された文化遺産で、登録基準は（ii）（iv）が適用されている。",
    "explanation": "正解は①です。2014年に登録された文化遺産で、登録基準は（ii）（iv）です[cite: 30]。②の4資産の最後は「荒船風穴」[cite: 30]、③の操業開始は「1872年」[cite: 31]、④は「フランス」から技師ポール・ブリュナが招聘されました[cite: 31]。",
    "tag": "登録年: 2014年 / 基準(ii)(iv) / 富岡製糸場",
    "trivia": "富岡製糸場で働く工女の多くは全国の士族の子女であり、技術を身につけた工女らはやがて各地に戻り製糸の技術指導を行いました[cite: 31]。"
  },
  {
    "question": "「富岡製糸場と絹産業遺産群」の構成資産とその特徴の組み合わせとして、正しくないものはどれか。",
    "options": [
      "① 富岡製糸場 — 日本古来の木造の柱からなる骨組みに西欧由来のレンガを組み合わせる木骨レンガ造などの和洋折衷の様式で、トラス構造を採用している。",
      "② 田島弥平旧宅 — 養蚕農家の田島弥平が自然の通風を重視した養蚕法である「清涼育」を確立し、越屋根をもつ建物は近代養蚕農家建築の原点とされる。",
      "③ 高山社跡 — 高山長五郎が温度と湿度を管理する養蚕法である「清温育」を確立し、生家で研究と指導を行った。",
      "④ 荒船風穴 — 人工の冷凍設備を利用して繭を保存した国内最大規模の蚕種貯蔵施設である。"
    ],
    "answer": "④ 荒船風穴 — 人工の冷凍設備を利用して繭を保存した国内最大規模の蚕種貯蔵施設である。",
    "explanation": "正解は④です。荒船風穴は人工の冷凍設備ではなく、「天然の風穴の冷風」を利用した国内最大規模の「蚕種貯蔵施設」です[cite: 31]。①〜③はいずれも紙面の記載どおり正しい内容です[cite: 31]。",
    "tag": "登録年: 2014年 / 基準(ii)(iv) / 構成資産",
    "trivia": "富岡製糸場と3つの関連遺産は技術交流を行うことで養蚕技術を発展させ、日本は20世紀初頭には世界一の生糸輸出国となりました[cite: 31]。"
  },
  {
    "question": "「富岡製糸場と絹産業遺産群」の背景や評価に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 江戸末期、鎖国政策を終えた日本は伝統的に生産されてきた絹織物を輸出品として貿易に乗り出した。",
      "② 明治維新を経て「殖産興業」による「富国強兵」を掲げた明治政府は、生糸の品質改善と生産向上の技術革新に取り組んだ。",
      "③ 富岡製糸場の工場建設地には、養蚕が盛んであったことから広い土地と豊かな水は重視されずに選ばれた。",
      "④ 富岡製糸場と3つの関連遺産は、東アジアから西欧へ一方的な技術移転が行われた点が評価された。"
    ],
    "answer": "② 明治維新を経て「殖産興業」による「富国強兵」を掲げた明治政府は、生糸の品質改善と生産向上の技術革新に取り組んだ。",
    "explanation": "正解は②です[cite: 30]。①は絹織物ではなく「生糸」[cite: 30]、③は「広い土地と豊かな水」を誇り、養蚕が盛んであった富岡が選ばれた[cite: 31]、④は「西欧から東アジアへ計画的な技術移転」が行われた点が評価されました[cite: 31]。",
    "tag": "登録年: 2014年 / 基準(ii)(iv) / 技術革新",
    "trivia": "富岡製糸場では、少しでも多くの繰糸器を工場内に置けるよう中央に柱のない広い空間を確保する工夫がなされました[cite: 31]。"
  },
  {
    "question": "「ル・コルビュジエの建築作品：近代建築運動への顕著な貢献」に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 2016年に登録された文化遺産で、登録基準は（i）（ii）（vi）が適用されている。",
      "② フランス出身の建築家ル・コルビュジエが手がけた6ヵ国に点在する17の建築作品からなる。",
      "③ 複数の大陸にまたがる世界初のトランスバウンダリー・サイトである。",
      "④ 日本の構成資産として、東京の国立西洋美術館と上野の森公園が含まれる。"
    ],
    "answer": "① 2016年に登録された文化遺産で、登録基準は（i）（ii）（vi）が適用されている。",
    "explanation": "正解は①です。2016年に登録された文化遺産で、登録基準は（i）（ii）（vi）です[cite: 32]。②は「スイス出身」で「7ヵ国」[cite: 32]、③は「トランス・コンチネンタル・サイト」[cite: 32]、④の日本の構成資産は「国立西洋美術館」です[cite: 32, 33]。",
    "tag": "登録年: 2016年 / 基準(i)(ii)(vi) / ル・コルビュジエ",
    "trivia": "「ピロティ」はフランス語で杭を意味し、建物の一階部分の柱で建物を支えて空中に浮くような軽やかな造形を生み出す工法です[cite: 32]。"
  },
  {
    "question": "「ル・コルビュジエの建築作品：近代建築運動への顕著な貢献」の構成資産とその特徴の組み合わせとして、正しくないものはどれか。",
    "options": [
      "① サヴォワ邸と庭師小屋 — パリ郊外に1931年竣工。ピロティや自由な平面、屋上庭園といった近代建築の五原則をすべて満たす傑作。",
      "② ロンシャンの礼拝堂 — ロンシャンに1955年竣工。合理性を求めた五原則から離れ、よりデザインと空間を自由に追求した後期ル・コルビュジエの代表作。",
      "③ チャンディガールのキャピトル・コンプレックス — インドのパンジャーブ州にあり、ル・コルビュジエの都市計画が唯一実現したもの。",
      "④ クルチェット邸 — フランスにあり、暑い気候に対応するため現地の建築様式が取り入れられている。"
    ],
    "answer": "④ クルチェット邸 — フランスにあり、暑い気候に対応するため現地の建築様式が取り入れられている。",
    "explanation": "正解は④です。クルチェット邸はフランスではなく「アルゼンチン共和国」のブエノスアイレス州都ラ・プラタに1953年竣工した南米唯一の作品です[cite: 33]。①〜③はいずれも紙面の記載どおり正しい内容です[cite: 33]。",
    "tag": "登録年: 2016年 / 基準(i)(ii)(vi) / 構成資産",
    "trivia": "ギエット邸はベルギーのフランドル地方アントワープに1927年竣工し、ベルギーの画家ルネ・ギエットのためにデザインされたアトリエ兼住居です[cite: 33]。"
  },
  {
    "question": "「ル・コルビュジエの建築作品：近代建築運動への顕著な貢献」の国立西洋美術館に関する次の記述のうち、正しいものはどれか。",
    "options": [
      "① 実業家の松方幸次郎が1920年代までに収集し、戦後フランスに押収されていた「松方コレクション」を展示する目的で建設された。",
      "② 1959年に開館し、展示作品が増えても内側から外側に向かって展示室を追加できる「無限成長美術館」という概念が採用されている。",
      "③ 天井の高さや柱の間隔、外壁のタイルのサイズなどは、ル・コルビュジエ独自の寸法「ピロティ」に則っている。",
      "④ 松方コレクションの寄贈返還の条件は、日本政府が建築家に「モデュロール」を起用することだった。"
    ],
    "answer": "① 実業家の松方幸次郎が1920年代までに収集し、戦後フランスに押収されていた「松方コレクション」を展示する目的で建設された。",
    "explanation": "正解は①です[cite: 32]。②は「内側から外側」ではなく「巻貝が中心から外側に向かうように」[cite: 32]、③は「ピロティ」ではなく独自の寸法「モデュロール」[cite: 32]、④の寄贈返還の条件は「専用の美術館建設」で、建築の依頼はル・コルビュジエでした[cite: 32]。",
    "tag": "登録年: 2016年 / 基準(i)(ii)(vi) / 国立西洋美術館",
    "trivia": "国立西洋美術館本館にも、建物の一階部分を柱で支える「ピロティ」が採用されています[cite: 32]。"
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


def start_quiz(questions, mode_label, is_mock_exam=False):
    quiz_list = questions.copy()
    random.shuffle(quiz_list)
    st.session_state.shuffled_quiz = prepare_quiz_session(quiz_list)
    st.session_state.app_mode = "quiz"
    st.session_state.mode_label = mode_label
    st.session_state.is_mock_exam = is_mock_exam
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.wrong_questions = []
    st.session_state.quiz_results_log = []
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.history_recorded = False


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
st.markdown('<h2 style="font-size: 1.8rem;">🏛️ 日本の遺産検定 4択マスター</h2>', unsafe_allow_html=True)
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

    if st.button(f"🎓 本番模擬試験をスタート（全{len(QUIZ_DATA)}問）", type="primary", use_container_width=True):
        start_quiz(QUIZ_DATA, "🎓 本番模擬試験モード（合格ライン70%）", is_mock_exam=True)
        st.rerun()

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        wrong_count = len(st.session_state.wrong_questions)
        if st.button(f"❌ 間違い復習 ({wrong_count}問)", disabled=(wrong_count == 0), use_container_width=True):
            start_quiz(st.session_state.wrong_questions, "🔄 間違い復習モード", is_mock_exam=False)
            st.rerun()

    with col2:
        fc_due_list = [q for q in QUIZ_DATA if q["question"] in st.session_state.forgetting_curve_log]
        if st.button(f"🧠 忘却曲線復習 ({len(fc_due_list)}問)", disabled=(len(fc_due_list) == 0), use_container_width=True):
            start_quiz(fc_due_list, "🧠 忘却曲線・最適復習モード", is_mock_exam=False)
            st.rerun()

# ==========================================
# 2. クイズ・模擬試験プレイ画面
# ==========================================
elif st.session_state.app_mode == "quiz":
    active_quiz = st.session_state.shuffled_quiz
    st.caption(f"【{st.session_state.mode_label}】")

    if st.session_state.current_q < len(active_quiz):
        q = active_quiz[st.session_state.current_q]

        st.subheader(f"第{st.session_state.current_q + 1}問 / 全{len(active_quiz)}問")
        st.markdown(f"**{q['question']}**")
        st.write("")

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
                    "question": q["question"],
                    "user_answer": option,
                    "correct_answer": q["answer"],
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                })
                st.rerun()

        if st.session_state.answered:
            st.markdown("---")
            if st.session_state.selected_option[:1] == q["answer"][:1]:
                st.markdown('<div class="correct-box">🎉 <b>正解です！</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="incorrect-box">😢 <b>不正解…</b> （あなたの回答: {st.session_state.selected_option}）<br>'
                    f'正解は <b>{q["answer"]}</b> です。</div>',
                    unsafe_allow_html=True,
                )

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
                start_quiz(st.session_state.wrong_questions, "🔄 間違い復習モード", is_mock_exam=False)
                st.rerun()

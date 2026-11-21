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
    },
    {
        "question": "古都京都の文化財の構成資産に含まれない寺社・城郭はどれか。",
        "options": ["① 清水寺", "② 二条城", "③ 東大寺", "④ 下鴨神社"],
        "answer": "③ 東大寺",
        "explanation": "正解は「東大寺」です。東大寺は「古都奈良の文化財」の構成資産です。",
        "tag": "登録年: 1994年 / 基準(ii)(iv)",
        "trivia": "古都京都の文化財は、京都市・宇治市・大津市にまたがる17の資産で構成されています。"
    },
    {
        "question": "白川郷・五箇山の合掌造り集落において、特徴的な急勾配の屋根の角度はおおよそ何度か。",
        "options": ["① 30〜40度", "② 45〜60度", "③ 70〜80度", "④ 90度"],
        "answer": "② 45〜60度",
        "explanation": "正解は「45〜60度」です。豪雪地帯の重い雪が滑り落ちやすいように急勾配になっています。",
        "tag": "登録年: 1995年 / 基準(iv)(v)",
        "trivia": "合掌造りの屋根裏は、かつて重要な産業であった養蚕の作業場として利用されていました。"
    },
    {
        "question": "奈良時代の仏教文化を伝える「古都奈良の文化財」の構成資産に含まれないものはどれか。",
        "options": ["① 平城宮跡", "② 唐招提寺", "③ 興福寺", "④ 平等院鳳凰堂"],
        "answer": "④ 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。平等院は京都府宇治市にあり「古都京都の文化財」の構成資産です。",
        "tag": "登録年: 1998年 / 基準(ii)(iv)(vi)",
        "trivia": "奈良の文化財は、平城宮跡や東大寺など平城京ゆかりの8資産で構成されています。"
    },
    {
        "question": "平泉－仏国土（浄土）を表現する遺跡群（岩手県）において、中心的な存在である寺院はどれか。",
        "options": ["① 中尊寺", "② 円覚寺", "③ 善光寺", "④ 金沢寺"],
        "answer": "① 中尊寺",
        "explanation": "正解は「中尊寺」です。金色堂に代表されるように、仏国土を地上に再現しようとした思想が形になっています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi)",
        "trivia": "平泉の遺跡群は、奥州藤原氏が築いた独自の浄土思想を伝える貴重な文化遺産です。"
    },
    {
        "question": "法隆寺の金堂や五重塔に代表される、世界最古の木造建築群が持つ建築様式の特徴はどれか。",
        "options": ["① 伝統的木造軸組構法", "② すべて石造りの壁", "③ 鉄筋コンクリート製", "④ レンガ造りアーチ"],
        "answer": "① 伝統的木造軸組構法",
        "explanation": "釘を一切使わない飛鳥時代の優れた木造建築技術（伝統的木造軸組構法）が受け継がれています。",
        "tag": "建築技術 / 基準(i)(iv)",
        "trivia": "日本の木造建築は湿潤な気候に適しており、高い耐震性と耐久性を誇ります。"
    },
    {
        "question": "古都京都の文化財の構成資産の一つである「宇治市」にある世界遺産といえばどこか。",
        "options": ["① 平等院鳳凰堂", "② 石山寺の本堂", "③ 三井寺の金堂", "④ 醍醐寺の五重塔"],
        "answer": "① 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。10円硬貨のデザインにも描かれている平安時代の阿弥陀堂建築です。",
        "tag": "構成資産: 平等院・宇治上神社",
        "trivia": "宇治上神社は日本最古の神社建築本殿として知られています。"
    },
    {
        "question": "知床が世界自然遺産に登録された最大の理由として評価された生態系上の特徴はどれか。",
        "options": ["① 亜熱帯のマングローブ", "② 流氷と陸上生態系の関係", "③ 標高3000mの高山帯", "④ 固有の砂漠気候帯"],
        "answer": "② 流氷と陸上生態系の関係",
        "explanation": "低緯度で流氷が接岸し、海の生き物と陸の動物が密接につながっている点が評価されました。",
        "tag": "登録年: 2005年 / 基準(ix)(x)",
        "trivia": "知床は北半球における流氷の南限にあたります。"
    },
    {
        "question": "小笠原諸島が自然遺産に登録された主な理由は何か。",
        "options": ["① 大規模なサンゴ礁", "② 独自の進化（固有種）", "③ 世界最大の活火山", "④ 深海魚の豊かな生態系"],
        "answer": "② 独自の進化（固有種）",
        "explanation": "一度も大陸と陸続きになったことがない海洋島で、生物が独自の進化を遂げたためです。",
        "tag": "登録年: 2011年 / 基準(ix)",
        "trivia": "小笠原諸島は「東洋のガラパゴス」とも称される独自の生態系を持っています。"
    },
    {
        "question": "奄美大島、徳之島、沖縄島北部及び西表島が自然遺産に登録された最大の要因はどれか。",
        "options": ["① 固有種・絶滅危惧種", "② 日本最大のサンゴ礁", "③ 世界一の年間降水量", "④ 完全な無人島であること"],
        "answer": "① 固有種・絶滅危惧種",
        "explanation": "アマミノクロウサギなど高い固有種・絶滅危惧種の生息地であることが評価されました。",
        "tag": "登録年: 2021年 / 基準(x)",
        "trivia": "イリオモテヤマネコやヤンバルクイナなど、世界的にも貴重な固有種が生息しています。"
    },
    {
        "question": "原爆ドーム（広島平和記念碑）の設計を手掛けた建築家の出身国はどこか。",
        "options": ["① チェコ", "② ドイツ", "③ フランス", "④ イギリス"],
        "answer": "① チェコ",
        "explanation": "正解は「チェコ」です。チェコ人の建築家ヤン・レッツェルによって設計されました。",
        "tag": "登録年: 1996年 / 基準(vi)",
        "trivia": "原爆ドームは核兵器の惨禍を今に伝える負の歴史の象徴です。"
    },
    {
        "question": "琉球王国のグスク及び関連遺産群の中で、首里城跡とともに登録された城の名称はどれか。",
        "options": ["① 熊本城の跡地", "② 中城城跡", "③ 大阪城の石垣", "④ 名古屋城の天守"],
        "answer": "② 中城城跡",
        "explanation": "正解は「中城城跡」です。沖縄県にある幾つものグスク（城）や関連遺産が登録されています。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi)",
        "trivia": "琉球のグスクは独特の曲りくねった城壁や高度な石積み技術が見られます。"
    },
    {
        "question": "石見銀山遺跡（島根県）の世界遺産登録の決め手となった、特徴的な鉱石採掘・精錬法は何か。",
        "options": ["① 水銀圧搾法", "② 灰吹法", "③ アマルガム法", "④ 露天掘り手法"],
        "answer": "② 灰吹法",
        "explanation": "正解は「灰吹法（はいふきほう）」です。銀を効率よく抽出する高度な技術として評価されました。",
        "tag": "登録年: 2007年 / 基準(ii)(iii)",
        "trivia": "石見銀山で生産された銀は、16〜17世紀の世界的銀流通に大きな影響を与えました。"
    },
    {
        "question": "明治日本の産業革命遺産の構成資産として正しくないものはどれか。",
        "options": ["① 官営八幡製鉄所", "② 軍艦島（端島炭坑）", "③ 長崎グラバー住宅", "④ 萩反射炉"],
        "answer": "③ 長崎グラバー住宅",
        "explanation": "正解は「長崎グラバー住宅」です。グラバー園内の旧住宅は世界遺産の構成資産ではありません。",
        "tag": "登録年: 2015年 / 基準(ii)(iv)",
        "trivia": "重工業・造船・製鉄などの分野における日本および世界の産業発展の歴史を伝えています。"
    },
    {
        "question": "「神宿る島」宗像・沖ノ島と関連遺産群において、一般人の立ち入りが原則禁止されている島はどれか。",
        "options": ["① 沖ノ島", "② 大島", "③ 相島", "④ 宗像大島"],
        "answer": "① 沖ノ島",
        "explanation": "正解は「沖ノ島」です。島全体がご神体であり、今でも厳格な禁忌が守られています。",
        "tag": "登録年: 2017年 / 基準(ii)(iii)",
        "trivia": "古代の祭祀遺跡から多数の国家鎮護の宝物が発見され、「海の正倉院」とも呼ばれます。"
    },
    {
        "question": "長崎と天草地方の潜伏キリシタン関連遺産の構成資産に含まれないものはどれか。",
        "options": ["① 大浦天主堂", "② 原城跡", "③ 久賀島の集落", "④ 首里城跡"],
        "answer": "④ 首里城跡",
        "explanation": "正解は「首里城跡」です。首里城跡は沖縄県の世界遺産であり、潜伏キリシタン関連遺産には含まれません。",
        "tag": "登録年: 2018年 / 基準(iii)",
        "trivia": "禁教期に独自の信仰を密かに続けた人々の歴史と文化的伝統を伝えています。"
    },
    {
        "question": "北海道・北東北の縄文遺跡群の代表的な構成資産として正しくないものはどれか。",
        "options": ["① 三内丸山遺跡", "② 大湯環状列石", "③ 函館山要塞跡", "④ 小牧野遺跡"],
        "answer": "③ 函館山要塞跡",
        "explanation": "正解は「函館山要塞跡」です。近代の軍事遺跡であり、縄文遺跡群には含まれません。",
        "tag": "登録年: 2021年 / 基準(iii)(v)",
        "trivia": "採集・漁労・狩猟による定住生活の発展と精神文化を示す貴重な遺跡群です。"
    },
    {
        "question": "佐渡島の金山が新しく世界文化遺産に登録された年はいつか。",
        "options": ["① 2022年", "② 2023年", "③ 2024年", "④ 2025年"],
        "answer": "③ 2024年",
        "explanation": "正解は「2024年」です。インドのニューデリーで開催された世界遺産委員会で登録が決定しました。",
        "tag": "登録年: 2024年 / 基準(iv)",
        "trivia": "手作業による伝統的な採掘技術から近代的な機械化まで、長期間の生産システムが良好に残されています。"
    },
    {
        "question": "世界遺産条約が採択された年はいつか。",
        "options": ["① 1945年", "② 1972年", "③ 1992年", "④ 2003年"],
        "answer": "② 1972年",
        "explanation": "正解は「1972年」のユネスコ総会で採択されました。",
        "tag": "ユネスコ総会での採択年",
        "trivia": "正式名称は「世界の文化及び自然遺産の保護に関する条約」です。"
    },
    {
        "question": "ユネスコ（UNESCO）の本部が置かれている都市はどこか。",
        "options": ["① ジュネーブ", "② ニューヨーク", "③ パリ", "④ ローマ"],
        "answer": "③ パリ",
        "explanation": "正解は「パリ（フランス）」です。ユネスコの本部はパリに置かれています。",
        "tag": "国際機関の本部",
        "trivia": "ユネスコは教育・科学・文化の発展と協力を通じて平和に貢献することを目指しています。"
    },
    {
        "question": "世界遺産の登録基準において、文化遺産の基準の数はいくつあるか。",
        "options": ["① 4つ（(i)〜(iv)）", "② 6つ（(i)〜(vi)）", "③ 10つ（(i)〜(x)）", "④ 12つ"],
        "answer": "② 6つ（(i)〜(vi)）",
        "explanation": "正解は「6つ（(i)〜(vi)」です。自然遺産の基準は4つであり、合わせて10個の基準があります。",
        "tag": "検定頻出：登録基準の数",
        "trivia": "文化遺産は(i)〜(vi)、自然遺産は(vii)〜(x)の基準が設けられています。"
    },
    {
        "question": "次のうち、日本の「無形文化遺産」に登録されているものはどれか。",
        "options": ["① 法隆寺の金堂", "② 姫路城の大天守", "③ 和食（日本人の伝統食）", "④ 原爆ドームの遺構"],
        "answer": "③ 和食（日本人の伝統食）",
        "explanation": "正解は「和食」です。建造物などは世界遺産（文化遺産）、伝統技術や食文化などは無形文化遺産です。",
        "tag": "無形文化遺産と世界遺産の区別",
        "trivia": "無形文化遺産には、芸能や伝統工芸技術、食文化などが登録されています。"
    },
    {
        "question": "「北海道・北東北の縄文遺跡群」がユネスコ世界文化遺産に登録された年はいつか。",
        "options": ["① 2011年", "② 2019年", "③ 2021年", "④ 2024年"],
        "answer": "③ 2021年",
        "explanation": "正解は「2021年」です。2021年7月27日の第44回世界遺産委員会拡大会合にて世界文化遺産への記載が決議されました。",
        "tag": "登録年: 2021年 / 基準(iii)(v)",
        "trivia": "北海道6遺跡・青森県8遺跡・岩手県1遺跡・秋田県2遺跡の計17遺跡（および2関連資産）で構成されています。"
    },
    {
        "question": "「北海道・北東北の縄文遺跡群」が世界文化遺産に登録された際の登録基準の組み合わせとして正しいものはどれか。",
        "options": ["① 基準(i) と (iv)", "② 基準(ii) と (vi)", "③ 基準(iii) と (v)", "④ 基準(iv) と (vii)"],
        "answer": "③ 基準(iii) と (v)",
        "explanation": "正解は「基準(iii) と (v)」です。定住を伴う採集・漁労・狩猟社会が1万年以上続いた稀有な文化の証拠（基準(iii)）と、環境変化に適応しながら定住生活を発展させた伝統的土地利用の顕著な例（基準(v)）が評価されました。",
        "tag": "登録年: 2021年 / 基準(iii)(v)",
        "trivia": "農耕社会以前の定住社会の発展と精神文化の変遷をたどれる点が、国際的にも高く評価されました。"
    },
    {
        "question": "秋田県鹿角市にある「大湯環状列石」を構成する2つの代表的な環状列石の組み合わせとして正しいものはどれか。",
        "options": [
            "① 万座環状列石 と 野中堂環状列石",
            "② 亀ヶ岡環状列石 と 三内丸山環状列石",
            "③ 伊勢堂岱環状列石 と 大森勝山環状列石",
            "④ 垣ノ島環状列石 と 大船環状列石"
        ],
        "answer": "① 万座環状列石 と 野中堂環状列石",
        "explanation": "正解は「万座環状列石 と 野中堂環状列石」です。縄文時代後期（約4,000年前）につくられた大規模な配石遺構で、共同墓地や祭祀の場としての性格を持っています。",
        "tag": "登録年: 2021年 / 基準(iii)(v) / 大湯環状列石",
        "trivia": "各環状列石の中心と「日時計状組石」を結ぶ線や2つの環の中心を結ぶ線は、夏至の日没方向とほぼ一致するとされています。"
    },
    {
        "question": "平泉の構成資産「中尊寺」において、1124年に建立され内部に奥州藤原氏三代の遺体などが納められている堂宇はどれか。",
        "options": ["① 金色堂", "② 経蔵", "③ 鳳凰堂", "④ 大日堂"],
        "answer": "① 金色堂",
        "explanation": "正解は「金色堂」です。初代藤原清衡が1124年に建立した仏堂で、金箔や螺鈿などの工芸技術が集められ、奥州藤原氏三代の遺体と四代泰衡の首級が納められています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi) / 中尊寺",
        "trivia": "中尊寺は850年に円仁が開山したと伝わり、清衡が戦乱の犠牲者を敵味方なく供養する願いを込めて造営を進めました。"
    },
    {
        "question": "平泉の構成資産「毛越寺」において、現在の浄土庭園の中心となっている池の名称はどれか。",
        "options": ["① 舞鶴が池", "② 大泉が池", "③ 阿字ヶ池", "④ 厳島池"],
        "answer": "② 大泉が池",
        "explanation": "正解は「大泉が池」です。毛越寺浄土庭園は大泉が池を中心に、洲浜や立石、遣水などの平安時代の庭園技法が良好に残されています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi) / 毛越寺",
        "trivia": "毛越寺の浄土庭園は、国の特別史跡と特別名勝の二重指定を受けています。"
    },
    {
        "question": "平泉の構成資産「観自在王院跡」について、建立したと伝えられる人物と中心となる池の組み合わせとして正しいものはどれか。",
        "options": [
            "① 清衡の妻・大泉が池",
            "② 基衡の妻・舞鶴が池",
            "③ 秀衡の妻・中島池",
            "④ 泰衡の妻・鏡が池"
        ],
        "answer": "② 基衡の妻・舞鶴が池",
        "explanation": "正解は「基衡の妻・舞鶴が池」です。奥州藤原氏二代基衡の妻が建立したと伝えられ、舞鶴が池を中心とする浄土庭園が築かれていました。",
        "tag": "登録年: 2011年 / 基準(ii)(vi) / 観自在王院跡",
        "trivia": "堂宇は残っていませんが、発掘調査や整備によって庭園構成や女性の信仰文化への関わりを読み取ることができます。"
    },
    {
        "question": "平泉の構成資産「無量光院跡」が造営される際、手本としたとされる京都の寺院建築はどれか。",
        "options": ["① 銀閣寺", "② 平等院鳳凰堂", "③ 清水寺本堂", "④ 金閣寺"],
        "answer": "② 平等院鳳凰堂",
        "explanation": "正解は「平等院鳳凰堂」です。奥州藤原氏三代秀衡が宇治の平等院鳳凰堂を模して建立した寺院の遺跡で、背後の金鶏山と西方の夕日を意識した配置が特徴です。",
        "tag": "登録年: 2011年 / 基準(ii)(vi) / 無量光院跡",
        "trivia": "無量光院跡は、堂宇や池の配置と金鶏山、沈む夕日が一つの軸線上に重なるよう意識された空間構成が注目されています。"
    },
    {
        "question": "平泉の構成資産「金鶏山」について、特徴や位置づけとして正しいものはどれか。",
        "options": [
            "① 標高約300mの活火山",
            "② 平泉中心部の山・景観の基準",
            "③ 太平洋に浮かぶ孤島",
            "④ 江戸時代に築かれた山城"
        ],
        "answer": "② 平泉中心部の山・景観の基準",
        "explanation": "正解は「平泉中心部の山・景観の基準」です。平泉の中心部（標高約98.6m）に位置し、中尊寺と毛越寺のほぼ中間にあって寺院・庭園配置の基準や宗教的景観を支えています。",
        "tag": "登録年: 2011年 / 基準(ii)(vi) / 金鶏山",
        "trivia": "山頂に黄金の鶏が埋められているという伝説がありますが、これは伝承であり史実とは区別して理解されます。"
    },
    {
        "question": "日本の世界自然遺産「小笠原諸島」において、海洋島ならではの独自の進化を示し、高い固有率が注目される植物群はどれか。",
        "options": ["① 維管束植物", "② コケ植物", "③ 藻類", "④ 地衣類"],
        "answer": "① 維管束植物",
        "explanation": "正解は「維管束植物」です。小笠原諸島は一度も大陸と陸続きになったことがない海洋島であり、維管束植物をはじめとする生物が独自の進化を遂げました。",
        "tag": "登録年: 2011年 / 基準(ix) / 小笠原諸島",
        "trivia": "小笠原諸島は「東洋のガラパゴス」とも称され、固有種が多いことで知られています。"
    },
    {
        "question": "世界自然遺産「白神山地」などのブナ林に生息し、国の天然記念物にも指定されている大型のキツツキはどれか。",
        "options": ["① コゲラ", "② クマゲラ", "③ アオゲラ", "④ ヤマセミ"],
        "answer": "② クマゲラ",
        "explanation": "正解は「クマゲラ」です。広大な原生的なブナ林など豊かな森林環境を必要とする大型のキツツキで、日本の森林生態系を象徴する鳥の一つです。",
        "tag": "登録年: 1993年 / 基準(ix) / 白神山地",
        "trivia": "黒い体と頭頂部の赤い冠羽が特徴で、樹木の枯れ木や巨木に大きな営巣穴を掘ります。"
    },
    {
        "question": "世界自然遺産「知床」などで冬に見られることがあり、流氷と海の生態系とも関わりが深い大型の猛禽類はどれか。",
        "options": ["① トビ", "② オジロワシ", "③ ハヤブサ", "④ フクロウ"],
        "answer": "② オジロワシ",
        "explanation": "正解は「オジロワシ」です。尾羽が白いのが特徴の大型ワシで、知床などでは冬季に海氷や沿岸の魚類・海鳥などと結びついた生態が見られます。",
        "tag": "登録年: 2005年 / 基準(ix)(x) / 知床",
        "trivia": "知床は北半球における流氷の南限付近に位置し、海と陸のつながりが生態系を支えています。"
    },
    {
        "question": "「琉球王国のグスク及び関連遺産群」の背景として、琉球王国が東アジアや東南アジアの地域間で担った交易の形態は何か。",
        "options": ["① 中継貿易", "② 鎖国体制下の密貿易", "③ 朝貢のみの限定交易", "④ 近代的海運貿易"],
        "answer": "① 中継貿易",
        "explanation": "正解は「中継貿易」です。琉球王国は地理的な位置を生かし、中国や日本、朝鮮、東南アジア諸国を結ぶ中継貿易によって繁栄しました。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi) / 琉球王国",
        "trivia": "中継貿易で得た富や文物は、グスクの築造や首里の文化発展にもつながりました。"
    },
    {
        "question": "「琉球王国のグスク及び関連遺産群」の時代背景において、各地にグスクを築いて勢力を広げた地域の指導者層は何と呼ばれるか。",
        "options": ["① 按司", "② 庄屋", "③ 惣代", "④ 国司"],
        "answer": "① 按司",
        "explanation": "正解は「按司（あじ）」です。グスク時代（12世紀頃〜15世紀頃）に各地で台頭した豪族・領主層で、やがて統合が進み琉球王国の成立へとつながりました。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(vi) / グスク時代",
        "trivia": "グスクは単なる城塞だけでなく、聖域や集落・政治の拠点としての性格も持っていました。"
    },
    {
        "question": "「明治日本の産業革命遺産」の構成資産の一つである「端島炭坑（軍艦島）」と並び、長崎県で近代石炭産業を支えた炭坑はどれか。",
        "options": ["① 高島炭坑", "② 足尾銅山", "③ 生野銀山", "④ 別子銅山"],
        "answer": "① 高島炭坑",
        "explanation": "正解は「高島炭坑」です。長崎港沖の高島にあり、近代的な採炭技術や設備の導入が進められた明治日本の産業革命遺産の構成資産の一つです。",
        "tag": "登録年: 2015年 / 基準(ii)(iv) / 産業革命遺産",
        "trivia": "高島炭坑は日本の近代炭鉱の歩みを語るうえで重要な構成資産となっています。"
    },
    {
        "question": "スイスの世界文化遺産「ラヴォー地域のブドウ畑」において、11世紀頃から組織的なブドウ栽培や修道院運営に関わった修道会の一つはどれか。",
        "options": ["① シトー会", "② イエズス会", "③ フランシスコ会", "④ ドミニコ会"],
        "answer": "① シトー会",
        "explanation": "正解は「シトー会」です。11世紀頃にベネディクト会やシトー会の修道院がブドウ畑の運営・開拓に関わり、急斜面の段々畑とワインづくりの伝統が築かれました。",
        "tag": "登録年: 2007年 / 基準(iii)(iv)(v) / ラヴォー",
        "trivia": "レマン湖の直射日光、湖面の反射光、石垣の反射光の「3つの太陽」が良質なブドウを育てます。"
    },
    {
        "question": "キューバの世界文化遺産「ビニャーレス渓谷」において、谷底から島のようにそびえる特徴的な石灰岩の岩山は何と呼ばれるか。",
        "options": ["① モゴーテ", "② メサ", "③ ビュート", "④ カルスト台地"],
        "answer": "① モゴーテ",
        "explanation": "正解は「モゴーテ」です。ビニャーレス渓谷では、モゴーテと呼ばれる独特の岩山と伝統的な葉タバコ栽培などの農耕景観が調和しています。",
        "tag": "登録年: 1999年 / 基準(iv) / ビニャーレス渓谷",
        "trivia": "ビニャーレス渓谷は、自然の地形と伝統的な農耕や土着文化が結びついた文化的景観として登録されています。"
    },
    {
        "question": "2009年にキルギスで初めて世界文化遺産に登録された、中央アジアにおける崇拝の対象となってきた霊峰はどれか。",
        "options": ["① 聖山スレイマン・トー", "② 天山山脈", "③ パミール高原", "④ イシク・クル"],
        "answer": "① 聖山スレイマン・トー",
        "explanation": "正解は「聖山スレイマン・トー」です。2009年にキルギス初の世界遺産として登録され、長く信仰・崇拝の場となってきた文化的景観です。",
        "tag": "登録年: 2009年 / 基準(iii)(vi) / キルギス初",
        "trivia": "古来より巡礼や信仰の場として守られてきた歴史や精神的伝統が評価されています。"
    },
    {
        "question": "世界文化遺産「タウリカ半島の古代都市とチョーラ」における「チョーラ」の説明として正しいものはどれか。",
        "options": [
            "① 古代ギリシャの植民都市の農業区画",
            "② 南インドのチョーラ朝が建てた寺院",
            "③ クリミア半島北部の遊牧民の墓",
            "④ イスラム教のモスクと学院の複合体"
        ],
        "answer": "① 古代ギリシャの植民都市の農業区画",
        "explanation": "正解は「古代ギリシャの植民都市の農業区画」です。黒海に面するタウリカ（クリミア）半島の古代都市ケルソネソス周辺に広がる矩形などの農業領域（チョーラ）を指します（インドの大チョーラ朝寺院群とは別遺産です）。",
        "tag": "登録年: 2013年 / 基準(ii)(v) / チョーラ",
        "trivia": "古代ギリシャの植民都市遺跡と周辺のブドウ栽培などを含む農業領域の結びつきが良好に残っています。"
    },
    {
        "question": "1993年に文化遺産としての価値も認められて複合遺産となり、世界で初めて「文化的景観」の概念が適用された世界遺産はどこか。",
        "options": ["① トンガリロ国立公園", "② ウルル＝カタ・ジュタ", "③ カカドゥ国立公園", "④ ブルー・マウンテンズ"],
        "answer": "① トンガリロ国立公園",
        "explanation": "正解は「トンガリロ国立公園」です。ニュージーランドにあり、1990年に自然遺産として登録された後、1993年にマオリの聖地としての文化的価値が認められ、世界初の「文化的景観」となりました。",
        "tag": "登録年: 1990年（1993年拡大） / 基準(vi)(vii)(viii)",
        "trivia": "日本の世界遺産では「紀伊山地の霊場と参詣道」や「石見銀山遺跡とその文化的景観」などが文化的景観として評価されています。"
    },
    {
        "question": "日本の世界文化遺産「日光の社寺」が登録された年と、登録基準の組み合わせとして正しいものはどれか。",
        "options": [
            "① 1998年 / 基準(ii)(iv)(vi)",
            "② 1999年 / 基準(i)(iv)(vi)",
            "③ 2000年 / 基準(ii)(iii)(vi)",
            "④ 2004年 / 基準(ii)(iii)(iv)(vi)"
        ],
        "answer": "② 1999年 / 基準(i)(iv)(vi)",
        "explanation": "正解は「1999年 / 基準(i)(iv)(vi)」です。1999年に登録され、日本の伝統的建築技術と彫刻・彩色などの芸術的達成（基準(i)(iv)）や信仰との結びつき（基準(vi)）が評価されています。",
        "tag": "登録年: 1999年 / 基準(i)(iv)(vi) / 日本の遺産",
        "trivia": "「1998年・基準(ii)(iv)(vi)」は古都奈良の文化財、「2004年・基準(ii)(iii)(iv)(vi)」は紀伊山地の霊場と参詣道です。"
    },
    {
        "question": "日本の世界文化遺産「富岡製糸場と絹産業遺産群」の登録年と、登録基準の組み合わせとして正しいものはどれか。",
        "options": [
            "① 2013年 / 基準(iii)(vi)",
            "② 2014年 / 基準(ii)(iv)",
            "③ 2015年 / 基準(ii)(iv)",
            "④ 2019年 / 基準(iii)(iv)"
        ],
        "answer": "② 2014年 / 基準(ii)(iv)",
        "explanation": "正解は「2014年 / 基準(ii)(iv)」です。19世紀後半から20世紀初頭にかけて生糸の大量生産・品質向上をもたらした技術交流と産業遺産の価値が評価されました。",
        "tag": "登録年: 2014年 / 基準(ii)(iv) / 日本の遺産",
        "trivia": "同じ基準(ii)(iv)を持つ日本の産業系文化遺産には、2015年登録の「明治日本の産業革命遺産」もあります。"
    },
    {
        "question": "マリの複合遺産「バンディアガラの断崖（ドゴン人の地）」において、ドゴン族の創世神話で万物を創造したとされる最高神は何か。",
        "options": ["① アンマ", "② ノモ", "③ オゴ", "④ レベ"],
        "answer": "① アンマ",
        "explanation": "正解は「アンマ」です。ドゴン族の神話では、最高神アンマが宇宙や精霊ノモなどを創造したと伝えられ、断崖の集落空間や儀礼とも深く結びついています。",
        "tag": "登録年: 1989年 / 基準(v)(vii) / マリ",
        "trivia": "バンディアガラの断崖は、絶壁に築かれた集落や穀物倉、仮面舞踊などの伝統文化と壮大な地形が一体となった複合遺産です。"
    },
    {
        "question": "イスラエルの世界文化遺産「マサダ国立公園」において、紀元前1世紀に宮殿と要塞を築いた人物と、現代における象徴的意味の組み合わせはどれか。",
        "options": [
            "① ヘロデ王・ユダヤ人の結束のシンボル",
            "② ソロモン王・和平と交易のシンボル",
            "③ ダビデ王・王権統一のシンボル",
            "④ コンスタンティヌス帝・信仰の象徴"
        ],
        "answer": "① ヘロデ王・ユダヤ人の結束のシンボル",
        "explanation": "正解は「ヘロデ王・ユダヤ人の結束のシンボル」です。紀元前1世紀にヘロデ王が宮殿・要塞群を築き、後の第1次ユダヤ戦争でローマ軍に抗戦した歴史から、ユダヤ人の結束や自由への闘いのシンボルとされています。",
        "tag": "登録年: 2001年 / 基準(iii)(iv)(vi) / イスラエル",
        "trivia": "死海を見下ろす孤立した岩山の上に築かれており、ローマ軍が築いた包囲陣地や攻城用スロープの遺構も良好に残っています。"
    },
    {
        "question": "ジンバブエの世界文化遺産「大ジンバブエ遺跡」を11〜15世紀頃に繁栄させたとされるバントゥー系民族はどれか。",
        "options": ["① ショナ族", "② ズールー族", "③ マサイ族", "④ サン族"],
        "answer": "① ショナ族",
        "explanation": "正解は「ショナ族」です。ショナ族の祖先が築いた王国の首都として栄え、漆喰を使わず花崗岩を積み上げた大規模な石造建築群が残されています。",
        "tag": "登録年: 1986年 / 基準(i)(iii)(vi) / ジンバブエ",
        "trivia": "「ジンバブエ」はショナ語で「石の家」を意味し、現在の国名の由来にもなっています。"
    },
    {
        "question": "チリの世界文化遺産「ラパ・ニュイ国立公園（イースター島）」において、巨石像モアイの建造を担ったと伝承される支配階級の集団はどれか。",
        "options": ["① 長耳族", "② 短耳族", "③ ラパ族", "④ マオリ族"],
        "answer": "① 長耳族",
        "explanation": "正解は「長耳族（ハナウ・エエペ）」です。島の伝承では、耳たぶを長く伸ばす風習を持っていた支配階級の長耳族がモアイ建造を主導し、後に被支配層の短耳族（ハナウ・モモコ）との抗争が起きたと語られています。",
        "tag": "登録年: 1995年 / 基準(i)(iii)(v) / チリ",
        "trivia": "モアイは主に祖先の霊力（マナ）を宿し、集落を見守る守護像として建てられました。"
    },
    {
        "question": "アイスランドの「シングヴェトリル国立公園」において、930年頃に創設された世界最古の議会の一つとされる全島民会の名称は何か。",
        "options": ["① アルシング", "② ゲイシール", "③ ヴァイキング評議会", "④ レイキャビク会議"],
        "answer": "① アルシング",
        "explanation": "正解は「アルシング」です。大西洋中央海嶺の裂け目（ギャオ）が走る地形にあり、930年頃に野外議会アルシングが創設されました。なお、ゲイシール（間欠泉の語源）などと共にアイスランドの代表的な観光ルート「ゴールデン・サークル」を構成しています。",
        "tag": "登録年: 2004年 / 基準(iii)(vi) / アイスランド",
        "trivia": "プレートの境界（ユーラシアプレートと北米プレート）が地上で見られる地球科学的にも重要な場所です。"
    },
    {
        "question": "中国の世界文化遺産「麗江の旧市街」において、伝統的な街並みを築いた少数民族と、彼らが伝えてきた象形文字の組み合わせはどれか。",
        "options": [
            "① 納西族・東巴文字",
            "② 白族・彝文字",
            "③ 苗族・女書",
            "④ 蔵族・チベット文字"
        ],
        "answer": "① 納西族・東巴文字",
        "explanation": "正解は「納西族・東巴文字」です。納西（ナシ）族が玉龍雪山の雪解け水を引き込んだ水路網とともに街を築き、現在も使われる世界唯一の象形文字「東巴（トンパ）文字」などの独自文化を伝えています。",
        "tag": "登録年: 1997年 / 基準(ii)(iv)(v) / 中国",
        "trivia": "旧市街には城壁がなく、自然地形と調和した木造建築と石橋の景観が特徴です。"
    },
    {
        "question": "ハンガリーの世界文化遺産「ホローケーの伝統的集落と周辺環境」に見られる、白い漆喰壁と木造のベランダを持つ伝統的な建築様式は何か。",
        "options": ["① パローツ様式", "② マジャール様式", "③ ゴシック様式", "④ チュードル様式"],
        "answer": "① パローツ様式",
        "explanation": "正解は「パローツ様式」です。ハンガリー北部の山間部に暮らすパローツ人による伝統的農村集落で、大火後の1910年代に防火対策を採り入れつつ伝統的なパローツ様式で再建されました。",
        "tag": "登録年: 1987年 / 基準(v) / ハンガリー",
        "trivia": "ホローケーはハンガリー語で「カラスの石」を意味し、現在も住民が伝統衣装や生活文化を受け継いでいます。"
    },
    {
        "question": "ロシアの世界文化遺産「カザン・クレムリンの歴史的建造物群」に含まれる、イヴァン雷帝が建てた正教会の大聖堂と、傾いた姿で知られる塔の組み合わせはどれか。",
        "options": [
            "① ブラゴヴェシェンスキー大聖堂・シュユンベキ塔",
            "② 聖ワシリイ大聖堂・スパスカヤ塔",
            "③ ウスペンスキー大聖堂・イワン大帝の鐘楼",
            "④ 血の上の救世主教会・ペトロパヴロフスク要塞"
        ],
        "answer": "① ブラゴヴェシェンスキー大聖堂・シュユンベキ塔",
        "explanation": "正解は「ブラゴヴェシェンスキー大聖堂・シュユンベキ塔」です。ロシア正教とイスラム教（タタール文化）が融合するカザン・クレムリンには、ブラゴヴェシェンスキー大聖堂、象徴的なシュユンベキ塔、クル・シャリーフ・モスクなどが共存しています。",
        "tag": "登録年: 2000年 / 基準(ii)(iii)(iv) / ロシア",
        "trivia": "シュユンベキ塔は頂部が約2メートル傾いている「斜塔」としても有名です。"
    },
    {
        "question": "ポーランドの負の世界遺産「アウシュヴィッツ・ビルケナウ」が伝える、ナチス・ドイツによるユダヤ人などの組織的大量虐殺を指す言葉は何か。",
        "options": ["① ホロコースト", "② アパルトヘイト", "③ ポグロム", "④ ディアスポラ"],
        "answer": "① ホロコースト",
        "explanation": "正解は「ホロコースト」です。第二次世界大戦中にナチス・ドイツが推し進めた大量虐殺（ホロコースト）の象徴であり、二度と繰り返してはならない人類の悲劇として登録基準(vi)のみで登録されています。",
        "tag": "登録年: 1979年 / 基準(vi) / ポーランド",
        "trivia": "2007年に、誤解を避け歴史的事実を明確にするため登録名称が「アウシュヴィッツ・ビルケナウ：ナチス・ドイツの強制絶滅収容所（1940-1945）」に変更されました。"
    },
    {
        "question": "ベネズエラの世界自然遺産「カナイマ国立公園」にある、テーブルマウンテン（テプイ）の「アウヤンテプイ」から流れ落ちる世界最大落差（約979m）の滝は何か。",
        "options": ["① アンヘルの滝", "② イグアスの滝", "③ ヴィクトリアの滝", "④ ナイアガラの滝"],
        "answer": "① アンヘルの滝",
        "explanation": "正解は「アンヘルの滝」です。落差があまりに大きいため、水が滝壺に届く前に霧散してしまうことでも知られ、ギアナ高地特有のテーブルマウンテン（テプイ）の景観とともに自然遺産に登録されています。",
        "tag": "登録年: 1994年 / 基準(vii)(viii)(ix)(x) / ベネズエラ",
        "trivia": "名前の由来は、1937年に不時着した際にこの滝を世界に紹介したアメリカ人飛行士ジミー・エンジェルにちなみます。"
    },
    {
        "question": "同一国内の複数資産で構成される「シリアル・サイト」と、国境を越えて複数国にまたがる「トランスバウンダリー・サイト」の両方に該当する世界遺産はどれか。",
        "options": [
            "① ル・コルビュジエの建築作品群",
            "② 明治日本の産業革命遺産",
            "③ イグアス国立公園",
            "④ 古都京都の文化財"
        ],
        "answer": "① ル・コルビュジエの建築作品群",
        "explanation": "正解は「ル・コルビュジエの建築作品群」です。日本（国立西洋美術館）やフランスなど3大陸7カ国にある計17資産で構成されるため、シリアル（連続性）かつトランスバウンダリー（国境を越える）な遺産です。なお「明治日本の産業革命遺産」は日本国内のシリアル・サイトです。",
        "tag": "世界遺産の分類 / シリアル＆トランスバウンダリー",
        "trivia": "日本にあるもう一つのトランスバウンダリー・サイトは、アメリカ・イギリスなどと共同登録された「ル・コルビュジエの建築作品群」のみです。"
    },
    {
        "question": "悲劇や紛争などの歴史的出来事を風化させず「未来への教訓・記憶の場」として登録基準(vi)を中心に評価されている世界遺産の組み合わせとして正しいものはどれか。",
        "options": [
            "① 原爆ドーム と ロベン島",
            "② 姫路城 と モン・サン・ミシェル",
            "③ 厳島神社 と タージ・マハル",
            "④ 白神山地 と ガラパゴス諸島"
        ],
        "answer": "① 原爆ドーム と ロベン島",
        "explanation": "正解は「原爆ドーム と ロベン島」です。核兵器の惨禍を伝える「原爆ドーム」や、南アフリカのアパルトヘイト政策下でネルソン・マンデラらが収監された「ロベン島」は、人類が記憶し未来へ教訓を伝えるべき「記憶の場（負の遺産）」として基準(vi)で登録されています。",
        "tag": "登録基準(vi) / 記憶の場・負の世界遺産",
        "trivia": "ほかにアウシュヴィッツ・ビルケナウやゴレ島なども代表的な「記憶の場」として知られています。"
    },
    {
        "question": "エジプトの「アブ・シンベルからフィラエまでのヌビア遺跡群」において、アスワン・ハイ・ダムの建設による水没の危機から遺跡を救うために行われた歴史的取り組みは何か。",
        "options": [
            "① ユネスコによる国際救済キャンペーンと移築",
            "② 遺跡全体を覆う巨大水中ドームの建設",
            "③ ナイル川の上流を別ルートへ完全に付け替え",
            "④ 砂漠の地下シェルターへの永久封印保存"
        ],
        "answer": "① ユネスコによる国際救済キャンペーンと移築",
        "explanation": "正解は「ユネスコによる国際救済キャンペーンと移築」です。1960年代にアスワン・ハイ・ダム建設でナセル湖に沈む危機に直面した際、ユネスコが国際的な救済を呼びかけ、岩山ごと切り出して高台へ移築しました。この活動が1972年の「世界遺産条約」採択の直接のきっかけとなりました。",
        "tag": "登録年: 1979年 / 基準(i)(iii)(vi) / 世界遺産条約の原点",
        "trivia": "アブ・シンベル大神殿は、年2回（2月22日と10月22日頃）に奥の至聖所の神像に朝日が差し込む精密な設計まで再現して移築されました。"
    },
    {
        "question": "オーストラリアの複合遺産「ウィランドラ湖地域」において、約4万年前の人類の埋葬跡や火葬跡などが発見され、その初期の移動や文化の証拠として重要視されている人類種はどれか。",
        "options": [
            "① ホモ・サピエンス（現生人類）",
            "② ネアンデルタール人",
            "③ アウストラロピテクス",
            "④ 北京原人（ホモ・エレクトス）"
        ],
        "answer": "① ホモ・サピエンス（現生人類）",
        "explanation": "正解は「ホモ・サピエンス（現生人類）」です。ウィランドラ湖地域では、約4万年以上前のホモ・サピエンスの化石人骨（ムンゴマン・ムンゴレディ）や世界最古級の火葬・埋葬の痕跡が発見されており、アフリカを出た現生人類の移動と精神文化の証拠となっています。",
        "tag": "登録年: 1981年 / 基準(iii)(viii) / オーストラリア",
        "trivia": "最終氷期以降の気候変動で干上がった湖沼群の地層と、人類の適応の歴史が評価された複合遺産です。"
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

from html import escape
from typing import Dict, List, Tuple

import plotly.graph_objects as go
import streamlit as st


COLOR_BLUE = "#40C1E9"
COLOR_PINK = "#F17F9E"
COLOR_YELLOW = "#F9CE23"
COLOR_TEXT = "#243447"
COLOR_SUB = "#5B6675"
COLOR_BORDER = "#E6E8EC"
COLOR_BG = "#FFFFFF"
COLOR_SOFT = "#F8FAFC"
COLOR_MINT = "#EEF9FD"


st.set_page_config(
    page_title="個別専用キャリア設計図ロードマップ作成",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-family: 'Helvetica Neue', Helvetica, Arial, 'Hiragino Sans', sans-serif;
        color: {COLOR_TEXT};
    }}
    .stApp {{
        background-color: {COLOR_BG};
    }}
    h1, h2, h3 {{
        color: {COLOR_TEXT};
        letter-spacing: 0.2px;
    }}
    .lead {{
        font-size: 16px;
        line-height: 1.85;
        color: {COLOR_SUB};
    }}
    .card {{
        background: {COLOR_BG};
        border: 1px solid {COLOR_BORDER};
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(16, 24, 40, 0.04);
    }}
    .mini-card {{
        background: {COLOR_SOFT};
        border: 1px solid {COLOR_BORDER};
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }}
    .compare-wrap {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 10px;
    }}
    .compare-box {{
        background: {COLOR_SOFT};
        border: 1px solid {COLOR_BORDER};
        border-radius: 14px;
        padding: 14px;
    }}
    .compare-title {{
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
        color: {COLOR_TEXT};
    }}
    .section-title {{
        font-size: 24px;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-top: 10px;
        margin-bottom: 8px;
    }}
    .timeline {{
        position: relative;
        margin-top: 8px;
        padding-left: 18px;
    }}
    .timeline:before {{
        content: "";
        position: absolute;
        left: 8px;
        top: 8px;
        bottom: 8px;
        width: 3px;
        background: {COLOR_BLUE};
        opacity: 0.35;
    }}
    .timeline-item {{
        position: relative;
        background: {COLOR_BG};
        border: 1px solid {COLOR_BORDER};
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }}
    .timeline-item:before {{
        content: "";
        position: absolute;
        left: -17px;
        top: 18px;
        width: 12px;
        height: 12px;
        border-radius: 999px;
        background: {COLOR_PINK};
        border: 2px solid {COLOR_BG};
    }}
    .timeline-label {{
        display: inline-block;
        font-size: 13px;
        font-weight: 700;
        color: {COLOR_TEXT};
        background: {COLOR_MINT};
        padding: 4px 8px;
        border-radius: 999px;
        margin-bottom: 8px;
    }}
    .accent {{
        color: {COLOR_PINK};
        font-weight: 700;
    }}
    .accent-blue {{
        color: {COLOR_BLUE};
        font-weight: 700;
    }}
    .accent-yellow {{
        color: #C99A00;
        font-weight: 700;
    }}
    .center-button button {{
        width: 100%;
        border-radius: 12px;
        background: {COLOR_BLUE};
        color: white;
        font-weight: 700;
        border: none;
        padding: 0.82rem 1rem;
        font-size: 18px;
    }}
    .center-button button:hover {{
        background: #2CB2DB;
        color: white;
    }}
    .track-rank {{
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        color: white;
        background: {COLOR_PINK};
        padding: 4px 8px;
        border-radius: 999px;
        margin-bottom: 10px;
    }}
    .track-title {{
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        color: {COLOR_TEXT};
    }}
    .subtle-head {{
        font-size: 13px;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-top: 10px;
        margin-bottom: 6px;
    }}
    .lead ul {{
        margin-top: 6px;
        margin-bottom: 8px;
        padding-left: 20px;
    }}
    .lead li {{
        margin-bottom: 4px;
    }}
    @media (max-width: 768px) {{
        .compare-wrap {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


JOB_OPTIONS = [
    "会社員",
    "パート",
    "アルバイト",
    "主婦",
    "営業職",
    "事務職",
    "接客販売",
    "医療従事者",
    "介護福祉職",
    "工場勤務",
    "教育",
    "保育",
    "美容",
    "サロン",
    "ジム・フィットネス関連",
    "フリーランス",
    "自営業",
    "その他",
]

EXPERIENCE_OPTIONS = [
    "ブログ執筆",
    "記事作成",
    "SNS投稿",
    "SNS運用",
    "ライティング",
    "リライト",
    "要約",
    "情報整理",
    "リサーチ",
    "画像作成",
    "Canva",
    "デザイン",
    "チラシ作成",
    "資料作成",
    "マニュアル作成",
    "Excel・スプレッドシート",
    "データ入力",
    "会議メモ・議事録",
    "接客",
    "販売",
    "営業",
    "電話対応",
    "問い合わせ対応",
    "教える・指導する",
    "研修・教育",
    "医療知識の説明",
    "介護現場の説明",
    "子育て経験の発信",
    "美容・健康の情報発信",
    "写真撮影",
    "動画編集",
    "AI使用経験",
    "ChatGPT使用経験",
]

REASON_OPTIONS = [
    "独学の試行錯誤を終わらせたい",
    "自分に合うテーマや方向性を明確にしたい",
    "自分の経験がどんな仕事に変わるのか知りたい",
    "AI×Canva×ライティングを実務で使える形にしたい",
    "3ヶ月以内に収益の土台を作りたい",
    "企業案件で型を学びながら自分の資産にもつなげたい",
    "書くだけではなく設計・整理・改善側に回りたい",
    "体力勝負ではない働き方に切り替えたい",
    "将来の収入不安に備えたい",
    "家事・育児・仕事と両立できる別レールを作りたい",
    "自分一人で判断し続けるやり方を終わらせたい",
    "個別に設計されたロードマップで進みたい",
]

GOAL_OPTIONS = [
    "半年以内に月3〜5万円の副収入の土台を作りたい",
    "1年以内に月10万円以上を安定して目指したい",
    "会社以外の収入源を持ちたい",
    "在宅でも続けやすい働き方を作りたい",
    "自分のブログやSNSも資産化したい",
    "自分の経験を価値に変えられる働き方に移行したい",
    "将来的にフリーランスや独立も視野に入れたい",
    "子育てや家庭と両立しながら積み上げたい",
    "親の介護や将来の生活不安に備えたい",
    "今の仕事を続けながら次のレールを準備したい",
]

REGION_OPTIONS = [
    "北海道",
    "東北",
    "関東",
    "中部",
    "近畿",
    "中国",
    "四国",
    "九州",
    "沖縄",
    "海外",
    "その他",
]

AGE_OPTIONS = [
    "20代前半",
    "20代後半",
    "30代前半",
    "30代後半",
    "40代前半",
    "40代後半",
    "50代前半",
    "50代後半",
    "60代以上",
]

GENDER_OPTIONS = ["女性", "男性", "その他", "回答しない"]
MARITAL_OPTIONS = ["未婚", "既婚", "その他"]
CHILD_OPTIONS = ["いない", "いる"]
CHILD_COUNT_OPTIONS = ["0", "1", "2", "3", "4人以上"]

BLOG_HAVE_OPTIONS = ["持っている", "持っていない"]
BLOG_HISTORY_OPTIONS = [
    "まだ始めていない",
    "1ヶ月未満",
    "1〜3ヶ月",
    "3〜6ヶ月",
    "6ヶ月〜1年",
    "1〜2年",
    "2年以上",
]

SIDE_HISTORY_OPTIONS = [
    "まだ取り組んでいない",
    "1ヶ月未満",
    "1〜3ヶ月",
    "3〜6ヶ月",
    "6ヶ月〜1年",
    "1〜2年",
    "2年以上",
]

REVENUE_OPTIONS = [
    "0円",
    "1円〜5,000円",
    "5,001円〜1万円",
    "1万〜3万円",
    "3万〜5万円",
    "5万〜10万円",
    "10万〜30万円",
    "30万円以上",
]

ANNUAL_INCOME_OPTIONS = [
    "200万円未満",
    "200万〜300万円",
    "300万〜400万円",
    "400万〜500万円",
    "500万〜700万円",
    "700万〜1,000万円",
    "1,000万円以上",
    "回答しない",
]

HOUSEHOLD_INCOME_OPTIONS = [
    "300万円未満",
    "300万〜500万円",
    "500万〜700万円",
    "700万〜1,000万円",
    "1,000万円以上",
    "回答しない",
]

SAVINGS_OPTIONS = [
    "50万円未満",
    "50万〜100万円",
    "100万〜300万円",
    "300万〜500万円",
    "500万〜1,000万円",
    "1,000万円以上",
    "回答しない",
]

TARGET_INCOME_OPTIONS: Dict[str, int] = {
    "月3万円": 30000,
    "月5万円": 50000,
    "月10万円": 100000,
    "月15万円": 150000,
    "月20万円": 200000,
    "月25万円": 250000,
    "月30万円": 300000,
}

if "generated" not in st.session_state:
    st.session_state.generated = False


def unique_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def safe_text(value: str) -> str:
    return escape(value) if value else ""


def round_thousand(value: float) -> int:
    return int(round(value / 1000) * 1000)


def experience_score(experiences: List[str], side_history: str, current_revenue: str, best_revenue: str, blog_history: str) -> int:
    score = len(experiences)

    if side_history in ["3〜6ヶ月", "6ヶ月〜1年"]:
        score += 2
    elif side_history in ["1〜2年", "2年以上"]:
        score += 4

    if blog_history in ["3〜6ヶ月", "6ヶ月〜1年"]:
        score += 1
    elif blog_history in ["1〜2年", "2年以上"]:
        score += 2

    if current_revenue in ["1万〜3万円", "3万〜5万円"]:
        score += 2
    elif current_revenue in ["5万〜10万円", "10万〜30万円", "30万円以上"]:
        score += 4

    if best_revenue in ["1万〜3万円", "3万〜5万円"]:
        score += 1
    elif best_revenue in ["5万〜10万円", "10万〜30万円", "30万円以上"]:
        score += 3

    return score


def get_experience_multiplier(score: int) -> float:
    if score <= 3:
        return 0.92
    if score <= 7:
        return 1.00
    if score <= 12:
        return 1.10
    return 1.20


def get_ideal_multiplier(score: int) -> float:
    if score <= 3:
        return 1.18
    if score <= 8:
        return 1.22
    if score <= 13:
        return 1.25
    return 1.28


def hours_to_base_monthly(hours: float) -> int:
    base_map = {
        0.5: 15000,
        1.0: 30000,
        1.5: 50000,
        2.0: 70000,
        2.5: 95000,
        3.0: 120000,
        3.5: 145000,
        4.0: 175000,
        4.5: 205000,
        5.0: 235000,
    }
    return base_map.get(hours, 70000)


def build_income_lines(score: int) -> Tuple[List[float], List[int], List[int]]:
    hours_points = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    exp_multiplier = get_experience_multiplier(score)
    ideal_multiplier = get_ideal_multiplier(score)

    current_line: List[int] = []
    ideal_line: List[int] = []
    for hours in hours_points:
        current = round_thousand(hours_to_base_monthly(hours) * exp_multiplier)
        ideal = round_thousand(current * ideal_multiplier)
        if ideal <= current:
            ideal = current + 3000
        current_line.append(current)
        ideal_line.append(ideal)

    return hours_points, current_line, ideal_line


def selected_income_values(work_hours: float, hours_points: List[float], current_line: List[int], ideal_line: List[int]) -> Tuple[int, int]:
    idx = hours_points.index(work_hours)
    return current_line[idx], ideal_line[idx]


def build_long_term_projection(current_monthly: int, ideal_monthly: int, score: int, work_hours: float) -> Tuple[List[str], List[int], List[int]]:
    years = ["1年目", "2年目", "3年目", "4年目", "5年目"]

    base_monthly = round_thousand(current_monthly * 0.8 + ideal_monthly * 0.2)
    if work_hours <= 1.0:
        growth = [1.00, 1.14, 1.25, 1.34, 1.42]
    elif work_hours <= 2.0:
        growth = [1.00, 1.18, 1.34, 1.48, 1.60]
    else:
        growth = [1.00, 1.22, 1.42, 1.60, 1.76]

    score_bonus = 0.00
    if score >= 8:
        score_bonus = 0.04
    if score >= 13:
        score_bonus = 0.08

    annuals: List[int] = []
    for i, factor in enumerate(growth):
        monthly_run_rate = base_monthly * (factor + score_bonus)
        if i == 0:
            annual = round_thousand(monthly_run_rate * 10)
        else:
            annual = round_thousand(monthly_run_rate * 12)
        if annuals and annual <= annuals[-1]:
            annual = annuals[-1] + 120000
        annuals.append(annual)

    cumulative: List[int] = []
    running = 0
    for annual in annuals:
        running += annual
        cumulative.append(running)

    return years, annuals, cumulative


def build_income_outlook_text(target_label: str, target_income: int, current_monthly: int, ideal_monthly: int, work_hours: float) -> str:
    gap_current = target_income - current_monthly
    gap_ideal = target_income - ideal_monthly

    if target_income <= current_monthly:
        relation = f"いまの条件でも、1日{work_hours}時間なら<span class='accent-blue'>現実ラインで月{current_monthly:,}円前後</span>が見えています。"
    elif target_income <= ideal_monthly:
        relation = (
            f"いまの条件なら、1日{work_hours}時間で<span class='accent-blue'>現実ラインは月{current_monthly:,}円前後</span>、"
            f"<span class='accent'>理想ラインは月{ideal_monthly:,}円前後</span>です。"
            f" 目標の{target_label}は、型と順番を揃えることで十分に射程に入る位置です。"
        )
    else:
        relation = (
            f"いまの条件だと、1日{work_hours}時間で<span class='accent-blue'>現実ラインは月{current_monthly:,}円前後</span>、"
            f"<span class='accent'>理想ラインは月{ideal_monthly:,}円前後</span>です。"
            f" 目標の{target_label}までは現実ラインとの差が{gap_current:,}円、理想ラインとの差が{max(gap_ideal, 0):,}円あるため、"
            "作業時間を増やすより、単価が落ちにくい作業へ寄せる設計が重要です。"
        )

    lift = ideal_monthly - current_monthly
    return relation + f" 現実ラインと理想ラインの差は<span class='accent-yellow'>{lift:,}円前後</span>で、少し頑張り方を変えるだけでも数か月後の見え方は変わります。"


def pick_multiple_with_checkboxes(label: str, options: List[str], key_prefix: str, columns: int = 2) -> List[str]:
    st.markdown(f"<div class='section-subtitle'><b>{safe_text(label)}</b></div>", unsafe_allow_html=True)
    cols = st.columns(columns)
    selected: List[str] = []
    for idx, option in enumerate(options):
        with cols[idx % columns]:
            checked = st.checkbox(option, key=f"{key_prefix}_{idx}")
            if checked:
                selected.append(option)
    return selected


def build_priority_work_tracks(
    job: str,
    experiences: List[str],
    reasons: List[str],
    goals: List[str],
    career_text: str,
    hobbies: str,
) -> List[Dict[str, object]]:
    candidates = [
        {
            "key": "structure",
            "title": "情報を整理し、相手が判断しやすい形に直す仕事",
            "fit_jobs": ["会社員", "事務職", "営業職", "フリーランス", "自営業"],
            "fit_exps": ["情報整理", "資料作成", "Excel・スプレッドシート", "会議メモ・議事録", "マニュアル作成", "要約"],
            "fit_reasons": ["書くだけではなく設計・整理・改善側に回りたい", "自分一人で判断し続けるやり方を終わらせたい"],
            "fit_goals": ["自分の経験を価値に変えられる働き方に移行したい", "会社以外の収入源を持ちたい"],
            "why_high_value": "単に作る人ではなく、情報を『判断できる形』に変える役割なので、AIが進んでも単価が崩れにくい領域です。",
            "cases": [
                "会議内容を1枚の要点資料に整理する",
                "営業資料や提案書を、見ただけで理解できる構成に直す",
                "社内マニュアルや業務手順を、現場が迷わない順番に整える",
            ],
            "steps": [
                "既存の文章やメモを、見出し・比較・次アクション付きの1枚資料にまとめる",
                "Canvaで見た目を整え、読みにくい資料を『すぐ分かる資料』に変える",
                "完成物を2〜3本ためて、ポートフォリオ化する",
            ],
        },
        {
            "key": "visual",
            "title": "文章を図解・スライド・見せ方に変える仕事",
            "fit_jobs": ["主婦", "会社員", "営業職", "接客販売", "美容", "サロン"],
            "fit_exps": ["Canva", "デザイン", "画像作成", "チラシ作成", "資料作成", "写真撮影"],
            "fit_reasons": ["AI×Canva×ライティングを実務で使える形にしたい", "企業案件で型を学びながら自分の資産にもつなげたい"],
            "fit_goals": ["在宅でも続けやすい働き方を作りたい", "自分のブログやSNSも資産化したい"],
            "why_high_value": "『作る』だけでなく『伝わる形に直す』ところまで入れるので、単純なデザイン外注より価値を出しやすいです。",
            "cases": [
                "長い説明文を1枚図解に直す",
                "ブログ記事や営業資料をスライド形式に整える",
                "サービス案内や比較表を、初見でも理解できる見た目に変える",
            ],
            "steps": [
                "AIで下書きを作り、要点だけを抜いたラフを作る",
                "Canvaで1テーマ1枚の図解サンプルを2本作る",
                "文章だけの説明を『見た瞬間に伝わる形』へ置き換える練習をする",
            ],
        },
        {
            "key": "explain",
            "title": "難しいことを初心者向けにやさしく説明し直す仕事",
            "fit_jobs": ["医療従事者", "介護福祉職", "教育", "保育", "主婦"],
            "fit_exps": ["教える・指導する", "研修・教育", "医療知識の説明", "介護現場の説明", "子育て経験の発信", "要約"],
            "fit_reasons": ["自分の経験がどんな仕事に変わるのか知りたい", "体力勝負ではない働き方に切り替えたい"],
            "fit_goals": ["自分の経験を価値に変えられる働き方に移行したい", "親の介護や将来の生活不安に備えたい"],
            "why_high_value": "現場経験がある人しか作れない説明は、AIの一般論より価値が高く、企業の説明コンテンツや採用広報にもつながりやすいです。",
            "cases": [
                "専門用語の多い説明を、患者・家族・保護者向けにやさしく書き直す",
                "現場の流れを、初めての人でも分かる順番で整理する",
                "採用向けに『この仕事のリアル』を伝える文章や図解を作る",
            ],
            "steps": [
                "自分が普段説明している内容を、初心者向けの言葉に置き換える",
                "1テーマごとに『よくある質問→答え』の形で整理する",
                "文章だけでなく、箇条書きや図解でも伝えられる形に整える",
            ],
        },
        {
            "key": "research",
            "title": "比較・リサーチ・選ばれる理由を整理する仕事",
            "fit_jobs": ["営業職", "接客販売", "パート", "アルバイト", "美容", "サロン"],
            "fit_exps": ["リサーチ", "接客", "販売", "営業", "問い合わせ対応", "SNS運用"],
            "fit_reasons": ["自分に合うテーマや方向性を明確にしたい", "3ヶ月以内に収益の土台を作りたい"],
            "fit_goals": ["半年以内に月3〜5万円の副収入の土台を作りたい", "1年以内に月10万円以上を安定して目指したい"],
            "why_high_value": "『どれが良いのか分からない』を解消する仕事は、集客・販売・問い合わせ導線に直結するため、企業側の需要がはっきりしています。",
            "cases": [
                "サービスや商品の比較表を作る",
                "口コミ・レビューから選ばれる理由を抜き出して整理する",
                "お客様が迷うポイントを先回りして潰す説明コンテンツを作る",
            ],
            "steps": [
                "既存のサービスや競合を3〜5件並べて比較軸を作る",
                "レビューや問い合わせ内容を拾い、よくある不安を整理する",
                "比較表・FAQ・来店前案内のような成果物に落とす",
            ],
        },
        {
            "key": "writing",
            "title": "記事・導線・構成を整える実務ライティングの仕事",
            "fit_jobs": ["会社員", "主婦", "フリーランス", "自営業", "営業職"],
            "fit_exps": ["ブログ執筆", "記事作成", "ライティング", "リライト", "SNS投稿", "SNS運用"],
            "fit_reasons": ["企業案件で型を学びながら自分の資産にもつなげたい", "独学の試行錯誤を終わらせたい"],
            "fit_goals": ["自分のブログやSNSも資産化したい", "在宅でも続けやすい働き方を作りたい"],
            "why_high_value": "『書くだけ』では弱いですが、構成・導線・見せ方まで入ると、単なる執筆よりも企業成果に近い仕事になります。",
            "cases": [
                "記事の見出し構成を作る",
                "リライトで読みやすさと導線を改善する",
                "ブログ・SNS・資料で使い回せるコンテンツ骨子を作る",
            ],
            "steps": [
                "AIで構成案を作り、人が検索意図や伝える順番を整える",
                "1記事を『本文』『図解』『SNS要約』に分解して再利用する",
                "記事サンプルと改善前後の比較をポートフォリオ化する",
            ],
        },
    ]

    ranked: List[Dict[str, object]] = []
    for candidate in candidates:
        score = 0
        if job in candidate["fit_jobs"]:
            score += 5
        for exp in experiences:
            if exp in candidate["fit_exps"]:
                score += 2
        for reason in reasons:
            if reason in candidate["fit_reasons"]:
                score += 3
        for goal in goals:
            if goal in candidate["fit_goals"]:
                score += 2
        if career_text.strip() and candidate["key"] in ["structure", "explain", "writing"]:
            score += 1
        if hobbies.strip() and candidate["key"] in ["visual", "research", "writing"]:
            score += 1
        candidate_copy = dict(candidate)
        candidate_copy["score"] = score
        ranked.append(candidate_copy)

    ranked.sort(key=lambda x: (int(x["score"]), x["title"]), reverse=True)
    return ranked[:3]


def build_roadmap_detail(work_hours: float, blog_have: str, side_history: str) -> List[Tuple[str, str]]:
    if work_hours <= 1.0:
        pace_line = "毎日長時間やる設計ではなく、平日は短く、休日に少しまとめる前提で進めます。"
    elif work_hours <= 2.0:
        pace_line = "平日夜の1〜2時間を軸に、休日で整える前提で進めます。"
    else:
        pace_line = "平日にもある程度時間を取れるので、実務経験づくりとポートフォリオ整備を並行できます。"

    if side_history in ["まだ取り組んでいない", "1ヶ月未満"]:
        month2_first = "まずは小さな案件、模擬案件、または知人向けのサンプル対応で『最後まで出す経験』を作ります。"
    else:
        month2_first = "すでに動いた経験があるなら、自己流で散らばった実績を『企業向けに見せられる形』へ整えます。"

    if blog_have == "持っている":
        month4_first = "企業案件で覚えた型を、自分のブログやSNSにも移植し始めます。"
    else:
        month4_first = "最初は企業案件側で型を覚え、その後に自分のブログやSNSの立ち上げへ進みます。"

    month1 = (
        "1ヶ月目｜現在地の把握と、最初の型づくり",
        (
            f"<div class='lead'>{pace_line}</div>"
            "<div class='subtle-head'>この月にやること</div>"
            "<ul>"
            "<li>現在地の把握と、どの経験を価値に変えるかの整理</li>"
            "<li>受注するための基本準備（プロフィール、肩書き、簡単な自己紹介）</li>"
            "<li>AIで下書きを作り、Canvaや文章で見やすく整える型を1つ作る</li>"
            "<li>最初のサンプルを1〜2個作る</li>"
            "<li>案件応募の流れを知り、どこに出すかを決める</li>"
            "</ul>"
            "<div class='subtle-head'>この月のゴール</div>"
            "<div class='lead'>『何をやる人か』が一言で言える状態と、見せられるサンプルが最低1本ある状態を作ります。</div>"
        ),
    )

    month2 = (
        "2ヶ月目｜小さく受注しながら、実務の型に慣れる",
        (
            f"<div class='lead'>{month2_first}</div>"
            "<div class='subtle-head'>この月にやること</div>"
            "<ul>"
            "<li>お仕事の並行受注、または模擬案件で納品経験を増やす</li>"
            "<li>コンテンツ制作の慣れを作り、Canva操作や修正対応に慣れる</li>"
            "<li>継続受注につながるよう、成果物の見せ方を整える</li>"
            "<li>ポートフォリオを作り、提案時に見せられる状態にする</li>"
            "</ul>"
            "<div class='subtle-head'>この月のゴール</div>"
            "<div class='lead'>『作れる』ではなく『納品できる』に変わること。ここで実務の流れを体で覚えます。</div>"
        ),
    )

    month3 = (
        "3ヶ月目｜継続受注と、単価を上げる提案に進む",
        (
            "<div class='subtle-head'>この月にやること</div>"
            "<ul>"
            "<li>継続受注を狙い、単発作業から抜ける提案を入れる</li>"
            "<li>価値単価を上げるために、整理だけでなく改善提案まで含める</li>"
            "<li>デザインや見せ方の幅を広げ、対応可能コンテンツを増やす</li>"
            "<li>記事・図解・資料・導線改善など、関連する納品パターンを1つ増やす</li>"
            "</ul>"
            "<div class='subtle-head'>この月のゴール</div>"
            "<div class='lead'>『作業者』ではなく、『整えて成果につなげる人』として見てもらう段階に入ります。</div>"
        ),
    )

    month4 = (
        "90日以降｜企業案件の型を、自分の資産にも移す",
        (
            f"<div class='lead'>{month4_first}</div>"
            "<div class='subtle-head'>この先の伸ばし方</div>"
            "<ul>"
            "<li>企業案件で使った構成・導線・見せ方を、自分の発信にも流用する</li>"
            "<li>自分の強みが刺さるテーマを固定し、発信の軸をぶらさない</li>"
            "<li>自腹で手探りするのではなく、実務で学んだ型を自分資産へ移す</li>"
            "</ul>"
        ),
    )

    return [month1, month2, month3, month4]


def build_lifestyle_image(
    work_hours: float,
    holiday_text: str,
    marital: str,
    child_status: str,
    child_count: str,
    holiday_hours: str,
    reasons: List[str],
    goals: List[str],
) -> str:
    if work_hours <= 1.0:
        daily = "平日は30分〜1時間でも、『今日も何も進まなかった』ではなく、『少しでも前に進んだ』に変わる暮らしです。"
    elif work_hours <= 2.0:
        daily = "平日の夜1〜2時間が、ただ疲れて終わる時間ではなく、未来の収入源を育てる時間に変わる暮らしです。"
    else:
        daily = "平日にも時間を取りやすいぶん、納品・改善・自分の発信がつながり始め、『やった分だけ形になる』実感を持ちやすい暮らしです。"

    if marital == "既婚" and child_status == "いる":
        family = f"子ども{child_count}人の生活を崩さず、家族時間を全部削るのではなく、無理のない範囲で積み上がっていくのが前提です。"
    elif marital == "既婚":
        family = "家庭を守りながらでも、将来への不安をただ抱え続けるだけではない日常に変えていくイメージです。"
    else:
        family = "一気に人生を変えるというより、生活の土台を崩さずに、次のレールを静かに作っていくイメージです。"

    holiday = (
        f"休日は『{safe_text(holiday_hours)}』ほど確保しやすく、過ごし方が『{safe_text(holiday_text)}』なら、その時間を全部仕事に変えるのではなく、"
        "心の余白を残したまま続けられる設計に寄せます。"
        if holiday_text.strip()
        else f"休日は『{safe_text(holiday_hours)}』ほど確保しやすいので、全部を作業に使う前提ではなく、無理なく回る配分で進めます。"
    )

    reason_line = ""
    if reasons:
        reason_line = f"いま抱えている『{safe_text(reasons[0])}』という気持ちを、ただの不安で終わらせず、行動に変えていける状態を目指します。"

    goal_line = ""
    if goals:
        goal_line = f"ゴールは『{safe_text(goals[0])}』のような未来を、勢いではなく、再現できる順番で近づけていくことです。"

    return "<br><br>".join([daily, family, holiday, reason_line, goal_line]).strip("<br>")


def build_current_pattern(
    current_job: str,
    work_hours: float,
    reasons: List[str],
    goals: List[str],
    side_history: str,
    experiences: List[str],
) -> Tuple[str, str]:
    pattern1 = (
        f"いまの『{safe_text(current_job)}』だけで毎日が回る状態が続くと、経験は増えても、それが副収入や資産に変わらないまま終わりやすいです。"
        f" とくに1日{work_hours}時間を確保できるのに動かない状態が続くと、1年後も『不安はあったのに何も変わっていない』に戻りやすいです。"
    )

    reason_hint = f"『{safe_text(reasons[0])}』という悩みがあるのに、" if reasons else ""
    goal_hint = f"『{safe_text(goals[0])}』を目指していても、" if goals else ""

    if side_history in ["まだ取り組んでいない", "1ヶ月未満"]:
        pattern2 = (
            f"{reason_hint}{goal_hint}型も順番も持たずに始めると、頑張っているつもりでも、収益に繋がらない作業だけが増えやすいです。"
            " 調べる、投稿する、作るを繰り返しても、企業ニーズに合う形へ変換できないままだと、時間だけが先に消えていきます。"
        )
    else:
        exp_hint = safe_text("、".join(experiences[:3]) if experiences else "これまでの経験")
        pattern2 = (
            f"すでに『{exp_hint}』のような土台があっても、正しい順番や型を使わずに自己流で広げると、単発作業ばかり増えて継続収益に繋がりにくくなります。"
            " 少し頑張っているのに手応えが薄い人は、このズレで止まっているケースが多いです。"
        )

    return pattern1, pattern2


def build_success_route(
    display_name: str,
    current_job: str,
    work_hours: float,
    top_track: Dict[str, object],
    annual_projection: List[int],
    reasons: List[str],
    goals: List[str],
) -> str:
    first_case = top_track["cases"][0] if top_track.get("cases") else "整理・構成・図解の仕事"
    reason_hint = f"『{safe_text(reasons[0])}』という悩みがあるなら、" if reasons else ""
    goal_hint = f"『{safe_text(goals[0])}』を目指すなら、" if goals else ""

    return (
        f"{reason_hint}{goal_hint}{safe_text(display_name)}さんは、いきなり自分の発信だけで勝ちにいくより、"
        f"まずは『{safe_text(str(first_case))}』のような企業ニーズに近い仕事で型を覚え、"
        f"フィードバックを受け、その型を自分のブログやSNSにも移す順番が合っています。"
        f" 入口は、{safe_text(current_job)}として積み上げた経験を、企業が使いやすい成果物に変換することです。"
        f" 1日{work_hours}時間の作業でも、<span class='accent-blue'>1年目は{annual_projection[0]:,}円前後</span>、"
        f"<span class='accent'>{annual_projection[1]:,}円前後</span>が現実ラインとして見えやすく、"
        "その後は『作業を受ける人』から『改善を提案できる人』へ寄せていくと、伸び方が安定します。"
    )


def render_result_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <h3 style="margin-top:0;">{title}</h3>
            <div class="lead">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timeline_card(title: str, roadmap: List[Tuple[str, str]]) -> None:
    items_html = ""
    for phase_title, phase_desc in roadmap:
        items_html += f"""
        <div class="timeline-item">
            <div class="timeline-label">{phase_title}</div>
            <div class="lead">{phase_desc}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="card">
            <h3 style="margin-top:0;">{title}</h3>
            <div class="timeline">{items_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_compare_card(title: str, left_title: str, left_body: str, right_title: str, right_body: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <h3 style="margin-top:0;">{title}</h3>
            <div class="compare-wrap">
                <div class="compare-box">
                    <div class="compare-title">{left_title}</div>
                    <div class="lead">{left_body}</div>
                </div>
                <div class="compare-box">
                    <div class="compare-title">{right_title}</div>
                    <div class="lead">{right_body}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_priority_tracks(title: str, tracks: List[Dict[str, object]]) -> None:
    blocks = []
    for idx, track in enumerate(tracks, start=1):
        cases_html = "".join(f"<li>{safe_text(str(item))}</li>" for item in track.get("cases", []))
        steps_html = "".join(f"<li>{safe_text(str(item))}</li>" for item in track.get("steps", []))
        blocks.append(
            f"""
            <div class="mini-card">
                <div class="track-rank">優先順位 {idx}</div>
                <div class="track-title">{safe_text(str(track['title']))}</div>
                <div class="lead">{safe_text(str(track['why_high_value']))}</div>
                <div class="subtle-head">向きやすい案件</div>
                <div class="lead"><ul>{cases_html}</ul></div>
                <div class="subtle-head">初心者が最初にやる作業</div>
                <div class="lead"><ul>{steps_html}</ul></div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="card">
            <h3 style="margin-top:0;">{title}</h3>
            <div class="lead" style="margin-bottom:12px;">一番上から順に、単価が崩れにくく、今の経験を価値へ変えやすい順番で並べています。『自分にできるか』が一回で分かるように、案件内容と最初の作業まで具体化しています。</div>
            {''.join(blocks)}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.title("個別専用キャリア設計図ロードマップ作成")
st.markdown(
    "<p class='lead'>Zoomで画面共有しながら、その場のヒアリング内容をもとに『何をやると、どう価値になり、どの順番で進めるか』を整理するためのシミュレーターです。入力項目全体から現在地と伸ばし方を見立て、会話の中で未来を具体化するために使います。</p>",
    unsafe_allow_html=True,
)
st.divider()

st.markdown("<div class='section-title'>1. 基本プロフィール</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("お名前", placeholder="例：山田 花子")
    age = st.selectbox("年齢", AGE_OPTIONS, index=4)
    current_job = st.selectbox("現在の職業", JOB_OPTIONS, index=0)
    gender = st.selectbox("性別", GENDER_OPTIONS, index=0)
with col2:
    marital = st.selectbox("既婚・未婚", MARITAL_OPTIONS, index=0)
    child_status = st.selectbox("お子様の有無", CHILD_OPTIONS, index=0)
    child_count = st.selectbox("お子様の人数", CHILD_COUNT_OPTIONS, index=0)
    region = st.selectbox("お住まいの地域", REGION_OPTIONS, index=2)

career_text = st.text_area("これまでの経歴", height=100, placeholder="例：医療事務を7年、その後クリニック受付を3年。新人教育も担当。")

st.divider()
st.markdown("<div class='section-title'>2. 経験の棚卸し</div>", unsafe_allow_html=True)
experiences = st.multiselect(
    "経験のあること（仕事・副業・趣味で、少しでも触れたことがあれば選択してください）",
    EXPERIENCE_OPTIONS,
)

blog_col1, blog_col2 = st.columns(2)
with blog_col1:
    blog_have = st.selectbox("ブログはお持ちですか", BLOG_HAVE_OPTIONS, index=1)
with blog_col2:
    blog_history = st.selectbox("ブログ運用歴", BLOG_HISTORY_OPTIONS, index=0)

side_col1, side_col2 = st.columns(2)
with side_col1:
    side_history = st.selectbox("副業歴", SIDE_HISTORY_OPTIONS, index=0)
with side_col2:
    current_revenue = st.selectbox("現在の収益額", REVENUE_OPTIONS, index=0)

best_revenue = st.selectbox("これまでに副業へ取り組んだことがあれば、最高実績を教えてください", ["実績なし"] + REVENUE_OPTIONS, index=0)

st.divider()
st.markdown("<div class='section-title'>3. 現在地と作業条件</div>", unsafe_allow_html=True)
work_col1, work_col2 = st.columns(2)
with work_col1:
    work_hours = st.slider("1日に確保できる平均作業時間", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
with work_col2:
    holiday_hours = st.selectbox("休日に確保しやすい時間", ["ほぼ取れない", "1〜2時間", "3〜4時間", "5時間以上"], index=1)

holiday_style = st.text_area("休日の主な過ごし方", height=90, placeholder="例：家族と過ごす、買い物、子どもの習い事、家事をまとめる など")

income_col1, income_col2 = st.columns(2)
with income_col1:
    annual_income = st.selectbox("現在の年収", ANNUAL_INCOME_OPTIONS, index=3)
with income_col2:
    household_income = st.selectbox("世帯年収", HOUSEHOLD_INCOME_OPTIONS, index=3)

savings = st.selectbox("現在の貯金額（今後どのぐらい増えるかのお話もするためです）", SAVINGS_OPTIONS, index=2)

st.divider()
st.markdown("<div class='section-title'>4. 申し込み理由・今後の目標</div>", unsafe_allow_html=True)
reasons = pick_multiple_with_checkboxes("個別相談に申し込んだ理由", REASON_OPTIONS, "reason", columns=2)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
goals = pick_multiple_with_checkboxes("今後の目標・将来設計", GOAL_OPTIONS, "goal", columns=2)
why_now = st.text_area("なぜ、これから頑張ってみようと思いましたか？", height=90, placeholder="例：このまま今の働き方だけだと不安で、次の収入源を準備したい")
hobbies = st.text_area("趣味・特技・少しでも興味があること", height=90, placeholder="例：旅行、健康、美容、家計管理、子育て、料理、SNSを見ること など")

st.divider()
st.markdown("<div class='section-title'>5. 収益シミュレーター</div>", unsafe_allow_html=True)
target_label = st.select_slider("目標金額", options=list(TARGET_INCOME_OPTIONS.keys()), value="月5万円")
target_income = TARGET_INCOME_OPTIONS[target_label]

score = experience_score(experiences, side_history, current_revenue, best_revenue, blog_history)
hours_points, current_line, ideal_line = build_income_lines(score)
current_monthly, ideal_monthly = selected_income_values(work_hours, hours_points, current_line, ideal_line)
years, annual_projection, cumulative_projection = build_long_term_projection(current_monthly, ideal_monthly, score, work_hours)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=hours_points,
        y=current_line,
        mode="lines+markers",
        name="現実ライン",
        line=dict(color=COLOR_BLUE, width=4),
        marker=dict(size=8, color=COLOR_BLUE),
        hovertemplate="1日%{x}時間<br>現実ライン: <b>%{y:,.0f}円</b><extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=hours_points,
        y=ideal_line,
        mode="lines+markers",
        name="理想ライン",
        line=dict(color=COLOR_PINK, width=4),
        marker=dict(size=8, color=COLOR_PINK),
        hovertemplate="1日%{x}時間<br>理想ライン: <b>%{y:,.0f}円</b><extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=hours_points,
        y=[target_income] * len(hours_points),
        mode="lines",
        name="目標金額",
        line=dict(color=COLOR_YELLOW, width=3, dash="dash"),
        hovertemplate="目標: <b>%{y:,.0f}円</b><extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=[work_hours],
        y=[current_monthly],
        mode="markers",
        name="現在の作業時間での現実ライン",
        marker=dict(size=14, color=COLOR_BLUE, line=dict(color=COLOR_BG, width=2)),
        hovertemplate="選択中: 1日%{x}時間<br>現実ライン: <b>%{y:,.0f}円</b><extra></extra>",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[work_hours],
        y=[ideal_monthly],
        mode="markers",
        name="現在の作業時間での理想ライン",
        marker=dict(size=14, color=COLOR_PINK, line=dict(color=COLOR_BG, width=2)),
        hovertemplate="選択中: 1日%{x}時間<br>理想ライン: <b>%{y:,.0f}円</b><extra></extra>",
        showlegend=False,
    )
)
fig.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=30, b=20),
    plot_bgcolor=COLOR_BG,
    paper_bgcolor=COLOR_BG,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    hovermode="x unified",
)
fig.update_yaxes(title_text="月間収益額（円）", tickformat=",d", gridcolor="rgba(36,52,71,0.08)")
fig.update_xaxes(title_text="1日に確保できる平均作業時間", showgrid=False)
st.plotly_chart(fig, use_container_width=True)

income_comment = build_income_outlook_text(target_label, target_income, current_monthly, ideal_monthly, work_hours)
render_result_card("収益ラインの見通し", income_comment)

center_left, center_mid, center_right = st.columns([1, 1.6, 1])
with center_mid:
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("個別専用キャリア設計図を作成する"):
        st.session_state.generated = True
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.generated:
    display_name = name.strip() if name.strip() else "この方"
    priority_tracks = build_priority_work_tracks(current_job, experiences, reasons, goals, career_text, hobbies)
    top_track = priority_tracks[0] if priority_tracks else {
        "title": "情報整理・構成設計",
        "cases": ["既存情報を整理して見せ方を変える仕事"],
    }
    roadmap = build_roadmap_detail(work_hours, blog_have, side_history)
    lifestyle = build_lifestyle_image(work_hours, holiday_style, marital, child_status, child_count, holiday_hours, reasons, goals)
    risk_pattern_1, risk_pattern_2 = build_current_pattern(current_job, work_hours, reasons, goals, side_history, experiences)
    success_route = build_success_route(display_name, current_job, work_hours, top_track, annual_projection, reasons, goals)

    st.divider()
    st.markdown("<div class='section-title'>作成結果</div>", unsafe_allow_html=True)

    render_result_card("この働き方が日常に入った後の暮らし", lifestyle)
    render_result_card("この順番で進むと形になりやすいルート", success_route)
    render_compare_card(
        "このままだと起こりやすい停滞パターン",
        "何も変えないまま、時間だけが過ぎるパターン",
        risk_pattern_1,
        "少し動くが、自己流で遠回りするパターン",
        risk_pattern_2,
    )
    render_priority_tracks("あなたの経験が高単価な価値に変わる具体的な作業内容", priority_tracks)
    render_timeline_card("90日ロードマップ", roadmap)

    long_fig = go.Figure()
    long_fig.add_trace(
        go.Bar(
            x=years,
            y=annual_projection,
            name="年間収益",
            marker_color=COLOR_BLUE,
            hovertemplate="%{x}<br>年間収益: <b>%{y:,.0f}円</b><extra></extra>",
        )
    )
    long_fig.add_trace(
        go.Scatter(
            x=years,
            y=cumulative_projection,
            mode="lines+markers",
            name="累計収益",
            line=dict(color=COLOR_PINK, width=4),
            marker=dict(size=9, color=COLOR_YELLOW, line=dict(color=COLOR_PINK, width=1.5)),
            hovertemplate="%{x}<br>累計収益: <b>%{y:,.0f}円</b><extra></extra>",
        )
    )
    long_fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor=COLOR_BG,
        paper_bgcolor=COLOR_BG,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
    )
    long_fig.update_yaxes(title_text="収益額（円）", tickformat=",d", gridcolor="rgba(36,52,71,0.08)")
    long_fig.update_xaxes(showgrid=False)
    st.plotly_chart(long_fig, use_container_width=True)

    long_summary = (
        f"いまの条件なら、<span class='accent-blue'>1年目は{annual_projection[0]:,}円前後</span>を現実ラインとして見ながら、"
        f"<span class='accent'>2年目は{annual_projection[1]:,}円前後</span>、"
        f"5年累計では<span class='accent-yellow'>{cumulative_projection[-1]:,}円前後</span>まで積み上がる見立てです。"
        " ここで重要なのは、作業時間だけで伸ばすのではなく、整理・構成・図解・改善提案のように、単価が崩れにくい作業へ寄せることです。"
    )
    render_result_card("1〜5年の収益見通し", long_summary)

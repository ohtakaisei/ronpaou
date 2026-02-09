"""定数・UI文字列・設定値"""

# デフォルトモデル
DEFAULT_MODEL = "gemini-2.0-flash"

# モードID
MODE_FILTER_BUBBLE = "filter_bubble"
MODE_PROPOSAL_REVIEW = "proposal_review"
MODE_FREE_DEBATE = "free_debate"

# ペルソナID
PERSONA_CRITIC = "critic"
PERSONA_INVESTOR = "investor"
PERSONA_RISK_MANAGER = "risk_manager"

# モード設定（ラベル・説明文）
MODES = {
    MODE_FILTER_BUBBLE: {
        "label": "フィルターバブル破壊",
        "description": "あなたの意見に対し、Web検索で根拠を集めて反論します。",
        "icon": "🫧",
    },
    MODE_PROPOSAL_REVIEW: {
        "label": "企画書の穴埋め",
        "description": "企画書の弱点をQ&A形式で鋭く指摘します。",
        "icon": "📋",
    },
    MODE_FREE_DEBATE: {
        "label": "自由討論",
        "description": "あなたの意見に多角的な視点から反論します。",
        "icon": "💬",
    },
}

# ペルソナ設定（ラベル・説明文）
PERSONAS = {
    PERSONA_CRITIC: {
        "label": "辛口批評家",
        "description": "歯に衣着せぬ批評で、論理の甘さを容赦なく突く。",
        "icon": "🔥",
    },
    PERSONA_INVESTOR: {
        "label": "慎重派投資家",
        "description": "ROI・市場データ・競合分析の観点から冷静に評価する。",
        "icon": "💰",
    },
    PERSONA_RISK_MANAGER: {
        "label": "リスク管理専門家",
        "description": "最悪のシナリオを想定し、リスクを徹底的に洗い出す。",
        "icon": "🛡️",
    },
}

# UI文字列
APP_TITLE = "Devil's Advocate メーカー"
APP_SUBTITLE = "あなたの意見にあえて反論し、思考を深めるAIアシスタント"
SIDEBAR_TITLE = "⚙️ 設定"
API_KEY_LABEL = "Google AI Studio APIキー"
API_KEY_HELP = "Google AI Studioで取得したAPIキーを入力してください。"
MODE_LABEL = "モード選択"
PERSONA_LABEL = "ペルソナ選択"
RESET_BUTTON_LABEL = "🔄 会話をリセット"
THINKING_MESSAGE = "悪魔の代弁者が思考中..."
NO_API_KEY_WARNING = "⚠️ サイドバーからAPIキーを入力してください。"
CHAT_PLACEHOLDER = "あなたの意見を入力してください..."
PROPOSAL_PLACEHOLDER = "企画書の内容を貼り付けてください..."
PROPOSAL_SUBMIT_LABEL = "📝 企画書を送信"
PROCESS_EXPANDER_LABEL = "🔍 思考・検索プロセスを表示"

# エラーメッセージ
ERROR_INVALID_API_KEY = "❌ APIキーが無効です。Google AI Studioで正しいキーを確認してください。"
ERROR_RATE_LIMIT = "⏳ APIのレート制限に達しました。しばらく待ってから再試行してください。"
ERROR_SEARCH_FAILED = "🔍 Web検索中にエラーが発生しました。検索なしで回答を生成します。"
ERROR_GENERIC = "❌ エラーが発生しました: {error}"
ERROR_TIMEOUT = "⏰ 処理がタイムアウトしました。入力を短くするか、再試行してください。"

# エージェント設定
AGENT_MAX_ITERATIONS = 8
AGENT_MAX_EXECUTION_TIME = 120

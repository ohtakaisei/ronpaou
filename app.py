"""Streamlit UI（メインエントリポイント）"""

import streamlit as st

from config import (
    APP_TITLE,
    APP_SUBTITLE,
    SIDEBAR_TITLE,
    API_KEY_LABEL,
    API_KEY_HELP,
    MODE_LABEL,
    PERSONA_LABEL,
    RESET_BUTTON_LABEL,
    THINKING_MESSAGE,
    NO_API_KEY_WARNING,
    CHAT_PLACEHOLDER,
    PROPOSAL_PLACEHOLDER,
    PROPOSAL_SUBMIT_LABEL,
    PROCESS_EXPANDER_LABEL,
    ERROR_INVALID_API_KEY,
    ERROR_RATE_LIMIT,
    ERROR_GENERIC,
    ERROR_TIMEOUT,
    MODES,
    PERSONAS,
    MODE_PROPOSAL_REVIEW,
)
from agent import run_agent


# --- ページ設定 ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="😈",
    layout="centered",
)


def init_session_state():
    """セッションステートを初期化する。"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mode" not in st.session_state:
        st.session_state.mode = list(MODES.keys())[0]
    if "persona" not in st.session_state:
        st.session_state.persona = list(PERSONAS.keys())[0]


def render_sidebar():
    """サイドバーを描画し、APIキー・モード・ペルソナを返す。"""
    with st.sidebar:
        st.title(SIDEBAR_TITLE)

        # APIキー入力
        api_key = st.text_input(
            API_KEY_LABEL,
            type="password",
            help=API_KEY_HELP,
        )

        st.divider()

        # モード選択
        st.subheader(MODE_LABEL)
        mode_options = list(MODES.keys())
        mode_labels = [
            f"{MODES[m]['icon']} {MODES[m]['label']}" for m in mode_options
        ]
        selected_mode_label = st.radio(
            MODE_LABEL,
            options=mode_labels,
            label_visibility="collapsed",
        )
        selected_mode = mode_options[mode_labels.index(selected_mode_label)]

        # モード説明
        st.caption(MODES[selected_mode]["description"])

        st.divider()

        # ペルソナ選択
        st.subheader(PERSONA_LABEL)
        persona_options = list(PERSONAS.keys())
        persona_labels = [
            f"{PERSONAS[p]['icon']} {PERSONAS[p]['label']}" for p in persona_options
        ]
        selected_persona_label = st.radio(
            PERSONA_LABEL,
            options=persona_labels,
            label_visibility="collapsed",
        )
        selected_persona = persona_options[
            persona_labels.index(selected_persona_label)
        ]

        # ペルソナ説明
        st.caption(PERSONAS[selected_persona]["description"])

        st.divider()

        # リセットボタン
        if st.button(RESET_BUTTON_LABEL, use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return api_key, selected_mode, selected_persona


def display_chat_history():
    """チャット履歴を表示する。"""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar")):
            st.markdown(msg["content"])
            # 中間ステップがあれば表示
            if msg.get("steps"):
                with st.expander(PROCESS_EXPANDER_LABEL):
                    for i, step in enumerate(msg["steps"], 1):
                        action, observation = step
                        st.markdown(f"**ステップ {i}: {action.tool}**")
                        st.code(action.tool_input, language="text")
                        st.markdown(f"**結果:** {observation[:500]}...")
                        st.divider()


def format_intermediate_steps(steps: list) -> list[dict]:
    """中間ステップをシリアライズ可能な形式に変換する。"""
    formatted = []
    for action, observation in steps:
        formatted.append({
            "tool": action.tool,
            "tool_input": (
                action.tool_input
                if isinstance(action.tool_input, str)
                else str(action.tool_input)
            ),
            "observation": str(observation)[:500],
        })
    return formatted


def display_intermediate_steps(steps: list):
    """中間ステップをexpanderで表示する。"""
    if not steps:
        return
    with st.expander(PROCESS_EXPANDER_LABEL):
        for i, step in enumerate(steps, 1):
            action, observation = step
            st.markdown(f"**ステップ {i}: {action.tool}**")
            st.code(
                action.tool_input
                if isinstance(action.tool_input, str)
                else str(action.tool_input),
                language="text",
            )
            st.markdown(f"**結果:**")
            st.text(str(observation)[:500])
            st.divider()


def handle_error(e: Exception) -> str:
    """例外を日本語エラーメッセージに変換する。"""
    error_str = str(e).lower()
    if "api key" in error_str or "api_key" in error_str or "401" in error_str:
        return ERROR_INVALID_API_KEY
    if "429" in error_str or "rate" in error_str or "quota" in error_str:
        return ERROR_RATE_LIMIT
    if "timeout" in error_str or "timed out" in error_str:
        return ERROR_TIMEOUT
    return ERROR_GENERIC.format(error=str(e))


def process_input(api_key: str, mode: str, persona: str, user_input: str):
    """ユーザー入力を処理し、エージェントの回答を表示する。"""
    # ユーザーメッセージを履歴に追加
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # エージェント実行
    with st.chat_message("assistant", avatar="😈"):
        with st.spinner(THINKING_MESSAGE):
            try:
                result = run_agent(api_key, mode, persona, user_input)
                output = result["output"]
                steps = result["intermediate_steps"]

                st.markdown(output)
                display_intermediate_steps(steps)

                # 履歴に追加（中間ステップはシリアライズ可能な形式で保存）
                st.session_state.messages.append({
                    "role": "assistant",
                    "avatar": "😈",
                    "content": output,
                    "steps_formatted": format_intermediate_steps(steps),
                })

            except Exception as e:
                error_msg = handle_error(e)
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "avatar": "😈",
                    "content": error_msg,
                })


def display_saved_messages():
    """保存済みメッセージを表示する。"""
    for msg in st.session_state.messages:
        avatar = msg.get("avatar")
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            # 保存済みの中間ステップを表示
            if msg.get("steps_formatted"):
                with st.expander(PROCESS_EXPANDER_LABEL):
                    for i, step in enumerate(msg["steps_formatted"], 1):
                        st.markdown(f"**ステップ {i}: {step['tool']}**")
                        st.code(step["tool_input"], language="text")
                        st.markdown("**結果:**")
                        st.text(step["observation"])
                        st.divider()


def main():
    """メインアプリケーション。"""
    init_session_state()

    # ヘッダー
    st.title(f"😈 {APP_TITLE}")
    st.caption(APP_SUBTITLE)

    # サイドバー
    api_key, mode, persona = render_sidebar()

    # APIキーチェック
    if not api_key:
        st.info(NO_API_KEY_WARNING)
        display_saved_messages()
        return

    # チャット履歴表示
    display_saved_messages()

    # 入力フォーム（モードによって切り替え）
    if mode == MODE_PROPOSAL_REVIEW:
        # 企画書モード: text_areaで長文入力
        with st.form("proposal_form", clear_on_submit=True):
            user_input = st.text_area(
                PROPOSAL_PLACEHOLDER,
                height=200,
                label_visibility="collapsed",
                placeholder=PROPOSAL_PLACEHOLDER,
            )
            submitted = st.form_submit_button(
                PROPOSAL_SUBMIT_LABEL,
                use_container_width=True,
            )
        if submitted and user_input.strip():
            process_input(api_key, mode, persona, user_input.strip())

    else:
        # チャットモード: chat_input
        user_input = st.chat_input(CHAT_PLACEHOLDER)
        if user_input and user_input.strip():
            process_input(api_key, mode, persona, user_input.strip())


if __name__ == "__main__":
    main()

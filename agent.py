"""LangChain ReActエージェント構築・実行"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from config import DEFAULT_MODEL, AGENT_MAX_ITERATIONS, AGENT_MAX_EXECUTION_TIME
from tools import get_search_tool
from prompts import build_system_prompt

# ReActエージェント用プロンプトテンプレート
REACT_TEMPLATE = """{system_prompt}

あなたは以下のツールを使用できます:

{tools}

ツールを使用するには、以下のフォーマットに**正確に**従ってください。
「Action:」の直後にはツール名のみを書いてください（余計な言葉を入れないこと）。

使用可能なツール名: {tool_names}

```
Thought: （思考内容）
Action: web_search
Action Input: （検索クエリ）
```

Observationにツールの結果が返されます。これを繰り返せます。

最終回答の準備ができたら:

```
Thought: （まとめ）
Final Answer: （ユーザーへの最終回答）
```

さあ、始めましょう。

ユーザーの入力: {input}

{agent_scratchpad}"""


def run_agent(
    api_key: str,
    mode_id: str,
    persona_id: str,
    user_input: str,
) -> dict:
    """ReActエージェントを構築・実行し結果を返す。

    Returns:
        dict with keys:
            - output: 最終回答テキスト
            - intermediate_steps: 中間ステップ（思考・検索プロセス）
    """
    # LLMインスタンス化
    llm = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL,
        google_api_key=api_key,
        temperature=0.7,
        convert_system_message_to_human=True,
    )

    # ツール
    tools = [get_search_tool()]

    # システムプロンプト構築
    system_prompt = build_system_prompt(persona_id, mode_id)

    # ReActプロンプト
    prompt = PromptTemplate(
        template=REACT_TEMPLATE,
        input_variables=["input", "agent_scratchpad"],
        partial_variables={
            "system_prompt": system_prompt,
        },
    )

    # エージェント作成
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # AgentExecutor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=AGENT_MAX_ITERATIONS,
        max_execution_time=AGENT_MAX_EXECUTION_TIME,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        verbose=False,
    )

    # 実行
    result = executor.invoke({"input": user_input})

    return {
        "output": result.get("output", ""),
        "intermediate_steps": result.get("intermediate_steps", []),
    }

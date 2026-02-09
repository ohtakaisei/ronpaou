"""DuckDuckGo検索ツール設定"""

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


def get_search_tool():
    """日本語リージョン対応のDuckDuckGo検索ツールを返す。"""
    wrapper = DuckDuckGoSearchAPIWrapper(region="jp-jp", max_results=5)
    return DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        name="web_search",
        description=(
            "Web検索ツール。ユーザーの主張に反論するための根拠やデータを検索する。"
            "日本語・英語どちらのクエリにも対応。"
            "入力: 検索クエリ文字列"
        ),
    )

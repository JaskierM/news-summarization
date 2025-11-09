from typing import Literal, Optional
from pydantic import Field

from app.core.settings.base import BaseYamlSettings


class BaseDBToolSettings(BaseYamlSettings):
    _config_name = "tools"
    _config_section = "base_db"

    db_key: str = Field(...)


class BaseRetrieverToolSettings(BaseYamlSettings):
    _config_name = "tools"
    _config_section = "base_retriever"

    vector_db_key: str = Field(...)
    search_type: Literal["similarity", "mmr", "similarity_score_threshold"] = Field(
        "similarity"
    )
    k: Optional[int] = Field(4)
    score_threshold: Optional[float] = Field(0)
    fetch_k: Optional[int] = Field(20)
    lambda_mult: Optional[float] = Field(0.5)


class MyQuerySQLCheckerSettings(BaseDBToolSettings):
    _config_name = "tools"
    _config_section = "my_query_sql_checker_tool"

    llm_key: str = Field(...)


class CommonRulesRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "common_rules_retriever"

    model_config = {"extra": "ignore"}


class KPInfoRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "kp_info_retriever"


class ContextAnswererRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "context_answerer_retriever"


class TermsExplainerRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "terms_explainer_retriever"


class EntitiesExtractorRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "entities_extractor_retriever"


class TablesSelectorRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "tables_selector_retriever"


class SQLExamplesRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "sql_examples_retriever"


class ColumnsSelectorRetrieverToolSettings(BaseRetrieverToolSettings):
    _config_name = "tools"
    _config_section = "columns_selector_retriever"

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-6"
    llm_max_tokens: int = 1500
    llm_temperature: float = 0.2

    database_url: str = "postgresql+psycopg2://postgres:password@localhost:5432/college_copilot"

    chroma_persist_dir: str = "./data/chroma"
    policy_docs_dir: str = "./data/policies"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    rag_top_k: int = 4
    rag_chunk_size: int = 800
    rag_chunk_overlap: int = 100

    min_attendance_percent: float = 75
    min_internal_marks_percent: float = 50
    min_previous_gpa: float = 6.0
    max_allowed_backlogs: int = 1
    max_incomplete_assignments: int = 2
    min_indicators_for_alert: int = 2

    require_human_approval: bool = True
    audit_log_path: str = "./logs/audit.log"
    backend_url: str = "http://localhost:8000"


settings = Settings()

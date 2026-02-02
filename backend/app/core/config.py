from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DocQuery Enterprise"
    environment: str = "dev"
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:5173"]

    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    postgres_dsn: str = "postgresql+psycopg://postgres:postgres@db:5432/docquery"
    vector_dimension: int = 1536

    s3_bucket: str = "docquery-dev"
    s3_region: str = "us-east-1"
    s3_prefix: str = "documents"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    local_storage_path: str = "local_uploads"

    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    class Config:
        env_prefix = ""
        env_file = ".env"


settings = Settings()

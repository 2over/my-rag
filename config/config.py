import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = (
        os.getenv("DASHSCOPE_BASE_URL")
        or os.getenv("OPENAI_BASE_URL")
        or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "qwen-plus")

    # MySQL配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "rag")

    # Chroma配置
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "../core/chroma_db")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-large-zh-v1.5")

    # 其他配置
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K = int(os.getenv("TOP_K", 5))

    def require_llm_credentials(self):
        if not self.OPENAI_API_KEY:
            raise ValueError(
                "缺少大模型 API Key。请在项目根目录创建 .env，并设置 "
                "DASHSCOPE_API_KEY=你的百炼APIKey；如果使用 OpenAI 官方接口，"
                "也可以设置 OPENAI_API_KEY。"
            )

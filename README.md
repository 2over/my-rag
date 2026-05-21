# My RAG

这是一个基于 Streamlit + LangChain + Chroma + MySQL 的本地知识库问答项目。项目支持上传 PDF、Word、TXT 文档，将文档切分为父子 chunk 后写入向量库，并通过大模型完成普通对话和基于文档的 RAG 问答。

## 技术栈

### 前端界面

- **Streamlit**：构建 Web 交互界面，负责文档上传、知识库选择、聊天窗口和侧边栏管理。
- **自定义 CSS**：用于聊天气泡、文档卡片、按钮和响应式布局样式。

### RAG 与大模型

- **LangChain**：组织文档加载、文本切分、检索器、大模型调用和提示词模板。
- **langchain-openai / OpenAI 兼容接口**：通过 `ChatOpenAI` 调用大模型。当前配置默认适配阿里云百炼 DashScope 的 OpenAI 兼容接口。
- **ContextualCompressionRetriever + LLMChainExtractor**：对初步检索结果进行上下文压缩，提升回答相关性，但会增加一次额外的大模型调用。
- **PromptTemplate**：维护 RAG 问答提示词模板，将上下文、历史对话和用户问题组合后交给大模型生成回答。

### 向量检索

- **ChromaDB**：本地持久化向量数据库，用于存储和检索文档向量。
- **langchain-chroma**：LangChain 与 ChromaDB 的集成封装。
- **HuggingFaceEmbeddings**：使用 Sentence Transformers / HuggingFace embedding 模型生成文本向量。
- 默认 embedding 模型配置为：

```env
EMBEDDING_MODEL_NAME=BAAI/bge-large-zh-v1.5
```

也可以改成本地模型目录，例如：

```env
EMBEDDING_MODEL_NAME=D:\llm\Local_model\BAAI\bge-large-zh-v1.5
```

### 文档处理

- **PyPDFLoader**：加载 PDF 文档。
- **Docx2txtLoader**：加载 Word `.docx` 文档。
- **TextLoader**：加载 `.txt` 文本文档。
- **RecursiveCharacterTextSplitter**：将文档切分为父文档块和子文档块。子文档用于向量检索，父文档用于补充更完整的上下文。

### 数据存储

- **MySQL**：保存文档记录、父子 chunk 元数据、向量 ID 和聊天历史。
- **SQLAlchemy**：定义 ORM 模型并管理数据库连接。
- **PyMySQL**：作为 SQLAlchemy 连接 MySQL 的驱动。

### 配置管理

- **python-dotenv**：从项目根目录的 `.env` 文件读取配置。
- `.env.example`：提供环境变量模板，实际运行时需要创建 `.env` 文件。

常用配置项：

```env
DASHSCOPE_API_KEY=your_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus

EMBEDDING_MODEL_NAME=BAAI/bge-large-zh-v1.5

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=rag

CHROMA_PERSIST_DIR=../core/chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
```

## 项目结构

```text
my-rag/
├── app.py                  # Streamlit 应用入口
├── config/
│   └── config.py           # 环境变量和运行配置
├── core/
│   ├── database.py         # MySQL ORM 模型和数据库操作
│   ├── document_processor.py # 文档加载与父子 chunk 切分
│   ├── rag_system.py       # 普通对话与 RAG 问答逻辑
│   └── vector_store.py     # Chroma 向量库与检索器
├── .env.example            # 环境变量示例
└── README.md
```

## 核心流程

1. 用户通过 Streamlit 侧边栏上传文档。
2. `DocumentProcessor` 根据文件类型加载文档内容。
3. 文档被切分为父 chunk 和子 chunk。
4. `VectorStore` 使用 embedding 模型生成向量，并写入 ChromaDB。
5. `DatabaseManager` 将文档、chunk 元数据、向量 ID 保存到 MySQL。
6. 用户提问时，系统先从 ChromaDB 检索相关子 chunk。
7. 系统根据子 chunk 找到对应父 chunk，构造更完整的上下文。
8. `RAGSystem` 将上下文、历史对话、用户问题组合为 prompt，调用大模型生成回答。

## 运行方式

创建 `.env` 文件并填写真实配置后，运行：

```bash
streamlit run app.py
```

注意：`.env.example` 只是模板，程序实际读取的是 `.env`。

## 项目演示

<img width="2463" height="1260" alt="image" src="https://github.com/user-attachments/assets/16dd85fa-6467-438b-ac68-89f595d098da" />

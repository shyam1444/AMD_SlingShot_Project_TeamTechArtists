<img width="1919" height="867" alt="image" src="https://github.com/user-attachments/assets/c9a2eb82-757d-499f-ba66-adda25193995" /># 🤖🎓 EduBot

**EduBot** is a powerful RAG (Retrieval-Augmented Generation) chatbot that utilizes state-of-the-art LLMs to provide a seamless and interactive learning experience. It is designed to help students and teachers explore complex concepts, analyze course materials, and interact with academic data.

### Brief about the idea 💡
EduBot is an AI-powered personal teaching assistant designed to revolutionize the learning experience for students and educators alike. By leveraging state-of-the-art Large Language Models—including a high-performance integration with **Groq Llama 3.3** for lightning-fast responses—EduBot provides accurate, context-aware answers to complex academic queries. Its core strength lies in its advanced Retrieval-Augmented Generation (RAG) system, which combines **RAPTOR** tree-based retrieval, **SQL-RAG** for structured data analysis, and real-time **Web Scraping** to ensure information is always relevant and up-to-date. To prioritize user privacy and accessibility, the system now utilizes **local BGE embeddings**, removing the need for external Google API keys while maintaining high-quality search capabilities. Finally, EduBot adapts its teaching style through a personalized **User Profile** system, tailoring explanations to match each user's specific knowledge level and learning goals.

### Opportunities 🚀
- **Innovative Architecture**: Unlike conventional educational chatbots that rely on generic knowledge or basic document retrieval, EduBot distinguishes itself through a sophisticated **multi-engine architecture** that seamlessly orchestrates structured data via SQL, hierarchical knowledge trees with RAPTOR, and real-time live updates via web scraping.
- **Contextual Problem Solving**: It solves the core problem of information fragmentation and impersonal learning by synthesizing diverse data sources into coherent, contextually accurate explanations that are tailored specifically to an individual student’s progress and programming proficiency.
- **Industry-Leading USP**: The primary **Unique Selling Proposition (USP)** is the integration of high-speed Groq-powered inference with a 100% Google-independent, privacy-first local embedding system, delivering institutional-grade intelligence with unprecedented speed and data sovereignty.

## Features 🌟

- **Full English Localization**: All UI elements, AI prompts, and internal logic are now fully translated to English for global accessibility.
- **Multi-Engine RAG**: intelligent routing between RAPTOR (document trees), SQL-RAG (structured data), and Web-Scraping (live news).
- **Personalized Learning**: Answers are tailored based on the user's programming level and year of study.
- **High-Performance Groq Support**: Defaulting to Llama 3.3 70B via Groq for sub-second response times.
- **Privacy-First Local Embeddings**: Uses `BAAI/bge-small-en-v1.5` for all RAG tasks, removing the need for external Google/OpenAI API calls for vectors.
- **Comprehensive Document Support**: Handles Text, PDF, and **PowerPoint (.pptx)** files seamlessly.

> 🤖🎓 EduBot is built on the [LlamaIndex](https://www.llamaindex.ai/) framework and uses [Streamlit](https://streamlit.io/) for its modern, interactive interface.

## Modules 🎡

EduBot orchestrates three specialized RAG modules to provide the best possible answers:

1.  **SQL-RAG Module**: A text-to-SQL engine that queries structured academic data (SQLite), perfect for questions about grades, points, or student lists.
2.  **raptor_module.py**: This module, built specifically for EduBot, contains the [llamaindex implementation of RAPTOR](https://github.com/run-llama/llama_index/tree/main/llama-index-packs/llama-index-packs-raptor). It builds a hierarchical tree of summaries for ultra-accurate context retrieval. This implementation has been upgraded to use **local BGE embeddings** (`BAAI/bge-small-en-v1.5`), making the RAG pipeline 100% independent of external embedding providers and resolving all credential errors.
3.  **Web-Scraper Module**: Retrieves the latest news directly from the University of Pula's informatics portal.

### Intelligent Routing 🤔
EduBot uses an `LLMSingleSelector` to automatically analyze your question and pick the right tool:
- "Explain recursion in JS" ➡️ **RAPTOR** (Documents)
- "How many points does student X have?" ➡️ **SQL-RAG** (Database)
- "What's the latest news from FIPU?" ➡️ **Web-Scraper** (Live Scrape)

## Installation & Setup 🚀

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/shyam1444/AMD_SlingShot_Project_TeamTechArtists.git
    cd AMD_SlingShot_Project_TeamTechArtists
    ```

2.  **Environment Setup**:
    It is recommended to use Python 3.11+.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_key_here
    COOKIE_KEY=your_secure_random_string
    GOOGLE_API_KEY=your_optional_key_for_gemini_models
    ```
    *Note: The `COOKIE_KEY` should be a long random string for securing login sessions.*

4.  **Google Authentication**:
    Place your `google_credentials.json` in the root folder. This is required for the secure Google Login system.

5.  **Run the App**:
    ```bash
    streamlit run 🤖EduBot.py
    ```

## Recent Improvements ✅
- **PowerPoint Support**: Fixed dependencies for stable `.pptx` file processing.
- **Enhanced Security**: Added API key sanitization and forced `.env` overrides to prevent authentication errors.
- **Validation Stability**: Fixed Pydantic validation errors in the query engines for smoother operation.
- **Unified Language**: Standardized all AI instructions and UI text to English.

## Tools and Technologies 🛠
- **Framework**: LlamaIndex, Streamlit
- **LLMs**: Groq (Llama 3.3 70B), Gemini, Anthropic, Ollama (Local)
- **Embeddings**: Local BGE (BAAI/bge-small-en-v1.5)
- **Database**: SQLite
- **Technique**: RAPTOR (Recursive Tree Retrieval)

- <img width="1919" height="867" alt="image" src="https://github.com/user-attachments/assets/41b84c62-372f-48fa-b094-e20fc71250d2" />

- <img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/54946e9e-22aa-4931-bd61-062f418c8536" />

- <img width="1919" height="869" alt="image" src="https://github.com/user-attachments/assets/4be50990-d2fd-495e-ae63-09c33cd70d4c" />




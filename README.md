# 🤖🎓 EduBot

**EduBot** is a powerful RAG (Retrieval-Augmented Generation) chatbot that utilizes state-of-the-art LLMs to provide a seamless and interactive learning experience. It is designed to help students and teachers explore complex concepts, analyze course materials, and interact with academic data.

This app was originally developed for a [Master's thesis](https://repozitorij.unipu.hr/islandora/object/unipu:9219) at the [Faculty of Informatics Pula](https://fipu.unipu.hr/fipu/en), Croatia, and has been recently enhanced with full English localization and robust technical fixes.

## Features 🌟

- **Full English Localization**: All UI elements, AI prompts, and internal logic are now fully translated to English for global accessibility.
- **Multi-Engine RAG**: intelligent routing between RAPTOR (document trees), SQL-RAG (structured data), and Web-Scraping (live news).
- **Personalized Learning**: Answers are tailored based on the user's programming level and year of study.
- **SOTA Model Support**: Powered by GPT-4o, Claude 3, and local models via Ollama (Llama 3, Mistral, Gemma).
- **Comprehensive Document Support**: Handles Text, PDF, and **PowerPoint (.pptx)** files seamlessly.

> 🤖🎓 EduBot is built on the [LlamaIndex](https://www.llamaindex.ai/) framework and uses [Streamlit](https://streamlit.io/) for its modern, interactive interface.

## Modules 🎡

EduBot orchestrates three specialized RAG modules to provide the best possible answers:

1.  **RAPTOR Module**: Uses Recursive Abstractive Processing for Tree-Organized Retrieval. It clusters and summarizes your documents at multiple levels of abstraction, allowing for both detailed and high-level queries.
2.  **SQL-RAG Module**: A text-to-SQL engine that queries structured academic data (SQLite), perfect for questions about grades, points, or student lists.
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
    OPENAI_API_KEY=your_key_here
    COOKIE_KEY=your_secure_random_string
    ANTHROPIC_API_KEY=your_optional_key
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
- **LLMs**: OpenAI (GPT-4o), Anthropic (Claude 3), Ollama (Local)
- **Database**: SQLite
- **Technique**: RAPTOR (Recursive Tree Retrieval)

## License
MIT License - see the [LICENSE](LICENSE) file for details.

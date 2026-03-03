<<<<<<< HEAD
# 🤖 RAG Document Assistant

> An intelligent AI-powered document question-answering system using Multi-Agent Retrieval-Augmented Generation (RAG). Upload your documents and get instant, accurate answers with source citations.

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green.svg)](https://langchain.com/)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

---

## 🌟 Features

- 📄 **Multi-Format Support** - PDF, TXT, DOCX documents
- 🧠 **Semantic Search** - Find information by meaning, not just keywords
- 💬 **Natural Language Q&A** - Ask questions like you're talking to a human
- 📚 **Source Citations** - See exactly where each answer comes from
- 🎨 **Beautiful UI** - Clean, intuitive Streamlit interface
- 🆓 **100% Free Tier** - Uses free AI services (within generous limits)
- ⚡ **Fast & Local** - Embeddings run on your machine
- 🔒 **Privacy First** - Your documents stay local

---

## 🎯 What Problem Does This Solve?

Imagine having hundreds of documents and needing to find specific information quickly. Instead of:
- ❌ Manually searching through each file
- ❌ Using basic Ctrl+F keyword matching
- ❌ Reading pages and pages of text

**You can now:**
- ✅ Upload all your documents once
- ✅ Ask questions in plain English
- ✅ Get intelligent, contextual answers with sources
- ✅ Save hours of research time

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11.9 or 3.12.8
- Google AI Studio API Key (free from [ai.google.dev](https://ai.google.dev/))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rag-document-assistant.git
cd rag-document-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 💡 How It Works

```mermaid
graph LR
    A[Upload Document] --> B[Split into Chunks]
    B --> C[Create Embeddings]
    C --> D[Store in Vector DB]
    D --> E[Ask Question]
    E --> F[Search Similar Chunks]
    F --> G[Generate Answer]
    G --> H[Display with Sources]
```

1. **Document Processing**: Your document is split into manageable chunks
2. **Embedding Creation**: Each chunk is converted to a vector (semantic fingerprint)
3. **Vector Storage**: Stored in ChromaDB for fast similarity search
4. **Question Answering**: Your question is matched with relevant chunks
5. **AI Generation**: Google Gemini generates an accurate answer
6. **Source Citation**: Shows exactly which document sections were used

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | LangChain | Agent orchestration & RAG pipeline |
| **LLM** | Google Gemini Flash | Answer generation |
| **Embeddings** | Sentence Transformers | Local semantic search |
| **Vector DB** | ChromaDB | Similarity search |
| **Frontend** | Streamlit | Web interface |
| **Doc Processing** | PyPDF, python-docx | Multi-format support |

---

## 📁 Project Structure

```
rag-document-assistant/
│
├── app.py                  # Streamlit UI application
├── rag_engine.py          # Core RAG logic & functionality
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in git)
├── .gitignore            # Git ignore rules
│
├── data/                 # Your documents (optional)
├── chroma_db/           # Vector database (auto-created)
└── README.md            # This file
```

---

## 📖 Usage Examples

### Example 1: Academic Research
```
Upload: Research papers on machine learning
Ask: "What are the key differences between supervised and unsupervised learning mentioned in these papers?"
Result: Detailed comparison with citations from specific papers
```

### Example 2: Business Analysis
```
Upload: Company reports and financial statements
Ask: "What were the main challenges mentioned in Q3 2024 reports?"
Result: Summarized challenges with source references
```

### Example 3: Personal Knowledge Base
```
Upload: Your notes, articles, and study materials
Ask: "Summarize what I've learned about Python decorators"
Result: Personalized summary from your own notes
```

---

## 🎓 Learning Path

This project is structured as a progressive learning journey:

### ✅ Week 1-2: Basic RAG System (Current)
- Document loading and processing
- Vector embeddings and storage
- Simple question-answering
- Streamlit UI

### 🚧 Week 3-4: Multi-Agent System (Coming Soon)
- Specialized agents (Planner, Retriever, Analyzer)
- Agent orchestration
- Advanced RAG techniques

### 🔮 Week 5-6: Advanced Features (Planned)
- Conversation memory
- Multi-document queries
- Custom agent behaviors
- Performance optimization

### 🌐 Week 7-8: Production Deployment (Planned)
- API endpoints
- Cloud deployment
- Monitoring and logging
- User authentication

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# LLM Settings
LLM_MODEL = "gemini-1.5-flash"
LLM_TEMPERATURE = 0.3  # 0=focused, 1=creative

# Chunking Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K_RESULTS = 3  # Number of chunks to retrieve
```

---

## 🆓 Free Tier Limits

All services used are FREE within these limits:

- **Google Gemini Flash**: 1,500 requests/day
- **ChromaDB**: Unlimited (local storage)
- **Sentence Transformers**: Unlimited (runs locally)

Perfect for development, demos, and personal use!

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
# Ensure virtual environment is activated
# You should see (venv) in your terminal
pip install -r requirements.txt
```

### "API Key Not Found"
```bash
# Check your .env file
cat .env  # Mac/Linux
type .env  # Windows

# Should contain:
GOOGLE_API_KEY=your_actual_key
```

### Slow Processing
- First run downloads embedding model (~500MB)
- Large PDFs take longer (1-2 minutes)
- This is normal behavior

### "Vector store not found"
- Process a document first before asking questions
- Click "Process Document" button after upload

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 **Report bugs** - Open an issue
2. 💡 **Suggest features** - Open an issue with your idea
3. 🔧 **Submit PRs** - Fork, make changes, submit PR
4. 📖 **Improve docs** - Better explanations help everyone
5. ⭐ **Star the repo** - Show your support!

---

## 📊 Roadmap

- [x] Basic RAG system with document Q&A
- [x] Streamlit UI with file upload
- [x] Source citation in answers
- [ ] Multi-agent architecture
- [ ] Conversation memory
- [ ] Multi-document queries
- [ ] REST API endpoints
- [ ] Docker containerization
- [ ] Cloud deployment guide
- [ ] Advanced RAG techniques (HyDE, ReAct)
- [ ] Support for more file formats (Excel, CSV)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - For the amazing RAG framework
- [Google AI](https://ai.google.dev/) - For free Gemini API access
- [ChromaDB](https://www.trychroma.com/) - For the vector database
- [Streamlit](https://streamlit.io/) - For the beautiful UI framework
- [Hugging Face](https://huggingface.co/) - For sentence transformers

---

## 📞 Contact & Support

- 📧 **Email**: kushwahsuraj5367@gmail.com
- 💼 **LinkedIn**:[www.linkedin.com/in/abhishek-kushwah-215b89260]

---


## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/rag-document-assistant&type=Date)](https://star-history.com/#yourusername/rag-document-assistant&Date)

---

## 📈 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/rag-document-assistant)
![GitHub contributors](https://img.shields.io/github/contributors/yourusername/rag-document-assistant)
![GitHub stars](https://img.shields.io/github/stars/yourusername/rag-document-assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/rag-document-assistant?style=social)

---

<div align="center">

**Built with ❤️ for learning and experimentation**

[Report Bug](https://github.com/Abhishekkushwah232/rag-document-assistant/issues) · [Request Feature](https://github.com/Abhishekkushwah232/rag-document-assistant/issues) · [Documentation](https://github.com/Abhishekkushwah232/rag-document-assistant/wiki)

</div>    

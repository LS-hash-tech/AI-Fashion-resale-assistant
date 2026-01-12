# GrabyAI Platform Assistant

AI-powered chatbot providing comprehensive guidance for the GrabyAI designer fashion resale platform.

# Features

# Core Functionality
- **Advanced RAG System**: Comprehensive platform knowledge base with semantic search
- **5 Specialized Tools**:
  - Knowledge base search (platform guidance, best practices)
  - Profit calculator (with all marketplace fees)
  - Price range lookup (historical data by brand/item/condition)
  - Platform tutorial (step-by-step guides)
  - Authentication tips (brand-specific guidelines)

# Security & Performance
- Input validation and sanitization
- Rate limiting (10 requests/60 seconds)
- Comprehensive error handling
- Logging system for monitoring
- No data persistence (privacy-focused)

# Domain Specialization
Focused on GrabyAI platform:
- Platform navigation and features
- Authentication guidance (AI + professional authenticator system)
- Profit optimization strategies
- Market insights and pricing data
- Listing optimization tips

# Tech Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **Model**: OpenAI GPT-4o-mini
- **Vector Store**: InMemoryVectorStore
- **Embeddings**: OpenAI text-embedding-3-small

# Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/grabyai-assistant.git
cd grabyai-assistant
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run app.py
```

4. Enter your OpenAI API key in the sidebar

## Project Structure
```
.
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── grabyai_assistant.log      # Application logs (generated)
```

# Usage Examples

**Platform Guidance:**
- "How does GrabyAI work?"
- "Show me the complete tutorial"

**Authentication:**
- "How do I authenticate Margiela pieces?"
- "What are red flags when buying designer items?"

**Profit Calculations:**
- "Calculate profit: buy £150, sell £350 on Grailed"

**Market Insights:**
- "What do Rick Owens jackets sell for?"
- "Best categories for arbitrage?"

# Security Features

- API key validation (format checking)
- Input sanitization (prevents injection attacks)
- Rate limiting (prevents abuse)
- No conversation persistence (privacy protection)
- Comprehensive error handling
- Logging for monitoring

# Development

**Logging:**
Logs are written to `grabyai_assistant.log` for debugging and monitoring.

**Rate Limits:**
- 10 requests per 60-second window per session
- Configurable in `app.py` (RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW)

**Adding Knowledge:**
Update the `KNOWLEDGE_BASE` variable in `app.py` with new content. The RAG system will automatically index it.

# License

Educational project for Turing College AI Engineering course.

# Contact

For support: support@grabyai.com
```

## **Create `requirements.txt`:**
```
streamlit==1.31.0
langchain==0.3.19
langchain-openai==0.3.1
langchain-community==0.3.18
langchain-text-splitters==0.3.6
langchain-core==0.3.28
openai==1.59.3
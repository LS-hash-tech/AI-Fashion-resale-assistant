"""
Agent initialization and configuration
"""
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config.settings import (
    MODEL_NAME, 
    MODEL_TEMPERATURE, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP, 
    SIMILARITY_SEARCH_K
)
from data.knowledge_base import KNOWLEDGE_BASE
from tools import (
    calculate_profit, 
    get_price_range, 
    get_platform_tutorial, 
    check_authentication_tips
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

def initialize_agent(api_key: str):
    """
    Initialize the agent with knowledge base and tools
    
    Args:
        api_key: OpenAI API key
    
    Returns:
        Tuple of (agent, vectorstore)
    """
    
    try:
        logger.info("Initializing agent...")
        
        # Create documents from knowledge base
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        docs = [Document(
            page_content=KNOWLEDGE_BASE, 
            metadata={"source": "platform_guide"}
        )]
        splits = text_splitter.split_documents(docs)
        
        logger.info(f"Knowledge base split into {len(splits)} chunks")
        
        # Create vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits,
            embedding=embeddings
        )
        
        logger.info("Vector store created successfully")
        
        # Create knowledge base search tool
        @tool
        def search_knowledge_base(query: str) -> str:
            """Search the GrabyAI platform guide for information"""
            try:
                docs = vectorstore.similarity_search(query, k=SIMILARITY_SEARCH_K)
                context = "\n\n---\n\n".join([doc.page_content for doc in docs])
                logger.info(f"Knowledge base search successful")
                return context
            except Exception as e:
                logger.error(f"Error in knowledge base search: {str(e)}")
                return f"Error searching knowledge base: {str(e)}"
        
        # Initialize model
        model = ChatOpenAI(
            model=MODEL_NAME, 
            temperature=MODEL_TEMPERATURE
        )
        
        # Collect all tools
        tools = [
            search_knowledge_base,
            calculate_profit,
            get_price_range,
            get_platform_tutorial,
            check_authentication_tips
        ]
        
        # System prompt
        system_prompt = """You are the GrabyAI Platform Assistant.

Guide users on:
- Platform usage
- Authentication (AI + professional authenticator system)
- Profit calculations
- Market insights
- Listing optimization

Always recommend 30%+ profit margin and direct users to WhatsApp group for expert help.

Be helpful, specific, and encouraging!"""
        
        # Create agent
        agent = create_agent(model, tools, system_prompt=system_prompt)
        
        logger.info("Agent initialized successfully")
        return agent, vectorstore
        
    except Exception as e:
        logger.error(f"Fatal error initializing agent: {str(e)}")
        raise
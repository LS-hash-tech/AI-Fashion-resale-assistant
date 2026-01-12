"""
Platform tutorial tool
"""
from langchain.tools import tool
from utils.logger import setup_logger

logger = setup_logger(__name__)

@tool
def get_platform_tutorial(step: str = "overview") -> str:
    """
    Provide detailed platform tutorial.
    
    Args:
        step: Tutorial section ('overview', 'setup', 'browse', etc.)
    
    Returns:
        Tutorial content for requested section
    """
    
    tutorials = {
        "overview": """
📚 **GrabyAI Platform Tutorial - Overview**

Quick Start Steps:
1️⃣ Browse opportunities
2️⃣ Evaluate profit & authenticity
3️⃣ Purchase from eBay UK
4️⃣ Verify on arrival
5️⃣ List for resale
6️⃣ Ship & profit!

Ask about specific steps for detailed guidance!
""",
        # Add other tutorial sections...
    }
    
    return tutorials.get(step.lower(), tutorials["overview"])
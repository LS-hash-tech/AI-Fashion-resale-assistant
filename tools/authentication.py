"""
Authentication guidance tool
"""
from langchain.tools import tool
from utils.logger import setup_logger
from config.settings import WHATSAPP_GROUP_EMAIL

logger = setup_logger(__name__)

@tool
def check_authentication_tips(brand: str = "general") -> str:
    """
    Provide authentication guidelines for specific brands.
    
    Args:
        brand: Designer brand name or 'general'
    
    Returns:
        Authentication checklist
    """
    
    auth_guides = {
        "margiela": """
🔍 **Maison Margiela Authentication Guide**

**Key Details:**
✓ Four white stitches on back
✓ Blank fabric label with numbers
✓ Premium materials
✓ Quality construction

**Red Flags:**
❌ Missing white stitches
❌ Poor stitching quality
❌ Cheap materials

📧 **Need expert help?**
Email {email} to join our WhatsApp group for authentication support!
""".format(email=WHATSAPP_GROUP_EMAIL),
        
        "general": """
🔍 **Universal Authentication Checklist**

1. Check labels and tags
2. Verify construction quality
3. Review seller profile
4. Analyze description
5. Check seller location
6. Combine all factors

📧 **Email {email} to join our WhatsApp group** for expert authentication help!
""".format(email=WHATSAPP_GROUP_EMAIL)
    }
    
    brand_lower = brand.lower()
    
    for key, guide in auth_guides.items():
        if key in brand_lower:
            return guide
    
    return auth_guides["general"]
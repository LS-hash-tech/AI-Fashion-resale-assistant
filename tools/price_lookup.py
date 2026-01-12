"""
Price range lookup tool
"""
from langchain.tools import tool
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Price database
PRICE_DATA = {
    "margiela": {
        "sneakers": {"new": "£250-£400", "excellent": "£180-£350", "good": "£140-£280"},
        "boots": {"new": "£450-£700", "excellent": "£300-£600", "good": "£220-£480"},
        # ... rest of data
    },
    "rick owens": {
        "sneakers": {"new": "£350-£550", "excellent": "£200-£450", "good": "£150-£350"},
        # ... rest of data
    },
    # ... other brands
}

@tool
def get_price_range(brand: str, item_type: str, condition: str = "excellent") -> str:
    """
    Get typical resale price ranges for specific designer brands and item types.
    
    Args:
        brand: Designer brand name
        item_type: Type of item (e.g., 'jacket', 'sneakers')
        condition: Item condition ('new', 'excellent', 'good', 'fair')
    
    Returns:
        Historical price data with market insights
    """
    
    try:
        logger.info(f"Price lookup: brand={brand}, type={item_type}, condition={condition}")
        
        brand_lower = brand.lower()
        item_lower = item_type.lower()
        condition_lower = condition.lower()
        
        # Search for matching brand and item
        for brand_key in PRICE_DATA:
            if brand_key in brand_lower or brand_lower in brand_key:
                brand_data = PRICE_DATA[brand_key]
                
                for item_key, prices in brand_data.items():
                    if item_key in item_lower or item_lower in item_key:
                        price_range = prices.get(condition_lower, prices.get("excellent"))
                        
                        return f"""
📊 **{brand.title()} {item_type.title()} - Resale Price Data**

**Condition: {condition.title()}**
💰 **Price Range: {price_range}**

Based on recent sales from Grailed and Vestiaire Collective.

💡 **Factors Affecting Price:**
- Specific model/collection
- Colorway popularity
- Seasonal timing
- Original packaging included

🔍 Check GrabyAI feed for exact historical data on specific items.
"""
        
        # Generic response if not found
        return f"""
📊 **{brand.title()} {item_type.title()} - General Pricing**

Typical designer resale ranges:
- Entry-level: £80-£200
- Mid-tier: £200-£500
- Premium: £500-£1500+

Check GrabyAI feed for specific opportunities with exact pricing data.
"""
        
    except Exception as e:
        logger.error(f"Error in price lookup: {str(e)}")
        return f"❌ Error looking up prices: {str(e)}"
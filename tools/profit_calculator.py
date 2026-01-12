"""
Profit calculation tool
"""
from langchain.tools import tool
from utils.validation import validate_price
from utils.logger import setup_logger

logger = setup_logger(__name__)

@tool
def calculate_profit(
    purchase_price: float, 
    selling_price: float, 
    platform: str = "grailed", 
    shipping_cost: float = 8.0
) -> str:
    """
    Calculate detailed profit breakdown after all marketplace fees and costs.
    
    Args:
        purchase_price: Price paid on eBay UK in GBP
        selling_price: Expected selling price in GBP
        platform: Resale platform - 'grailed', 'ebay', or 'vestiaire'
        shipping_cost: Estimated shipping cost in GBP (default 8.0)
    
    Returns:
        Detailed profit breakdown with margin analysis and recommendations
    """
    
    try:
        # Validate inputs
        if not validate_price(purchase_price) or not validate_price(selling_price):
            return "❌ Error: Please enter valid prices between £1 and £100,000"
        
        if selling_price <= purchase_price:
            return "❌ Warning: Selling price must be higher than purchase price to make a profit!"
        
        logger.info(f"Calculating profit: buy={purchase_price}, sell={selling_price}, platform={platform}")
        
        # Platform fee structures
        fees = {
            "grailed": 0.12,
            "ebay": 0.15,
            "vestiaire": 0.15
        }
        
        platform_lower = platform.lower()
        platform_fee = fees.get(platform_lower, 0.12)
        
        # Calculate breakdown
        platform_fees = selling_price * platform_fee
        net_revenue = selling_price - platform_fees - shipping_cost
        profit = net_revenue - purchase_price
        profit_margin = (profit / purchase_price) * 100 if purchase_price > 0 else 0
        
        # Generate recommendation
        if profit_margin >= 50:
            recommendation = "🌟 Excellent margin! This is a strong opportunity."
        elif profit_margin >= 30:
            recommendation = "✅ Good margin. This meets our recommended minimum."
        elif profit_margin >= 20:
            recommendation = "⚠️ Acceptable margin but below our 30% recommendation."
        else:
            recommendation = "❌ Low margin. Consider looking for better opportunities."
        
        result = f"""
💰 **Profit Analysis for {platform.upper()}**

**Purchase Details:**
├─ eBay UK Price: £{purchase_price:.2f}
└─ Estimated Shipping: £{shipping_cost:.2f}
**Total Investment: £{purchase_price + shipping_cost:.2f}**

**Revenue Breakdown:**
├─ Selling Price: £{selling_price:.2f}
├─ Platform Fees ({platform_fee*100:.0f}%): -£{platform_fees:.2f}
└─ Shipping to Buyer: -£{shipping_cost:.2f}
**Net Revenue: £{net_revenue:.2f}**

**Profit Analysis:**
├─ **Gross Profit: £{profit:.2f}**
├─ **Profit Margin: {profit_margin:.1f}%**
└─ **ROI: {profit_margin:.1f}%**

{recommendation}

💡 **Tips:**
- Factor in 2-3 hours for listing, communication, and shipping
- Effective hourly rate: £{profit/2.5:.2f} - £{profit/2:.2f}
- Consider seasonality and current market demand

📧 Join our WhatsApp group for pricing strategy discussions!
"""
        
        logger.info(f"Profit calculation successful: margin={profit_margin:.1f}%")
        return result
        
    except Exception as e:
        logger.error(f"Error in profit calculation: {str(e)}")
        return f"❌ Error calculating profit: {str(e)}"
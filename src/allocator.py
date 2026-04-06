import math

def calculate_allocation(total_budget, ticker_data):
    """
    Calculates number of shares to buy for each ticker predicted "UP".
    :param total_budget: Total amount user wants to invest.
    :param ticker_data: List of dicts {'ticker': str, 'price': float, 'confidence': float}
    :return: (recommendations, total_cost)
    """
    if total_budget <= 0:
        return [], 0
    
    # Filter only stocks predicted as "UP" (probability > 0.5)
    up_stocks = [t for t in ticker_data if t['confidence'] > 0.5]
    
    if not up_stocks:
        return [], 0
    
    # Strategy: Confidence-weighted Allocation
    # More budget to stocks where the model is highly certain
    total_confidence = sum(t['confidence'] for t in up_stocks)
    
    recommendations = []
    total_cost = 0
    
    for stock in up_stocks:
        weight = stock['confidence'] / total_confidence
        allocated_sub_budget = total_budget * weight
        
        # Determine shares
        shares = math.floor(allocated_sub_budget / stock['price'])
        cost = shares * stock['price']
        
        if shares > 0:
            recommendations.append({
                "Ticker": stock['ticker'],
                "Price": stock['price'],
                "Confidence": f"{stock['confidence']:.1%}",
                "Shares": shares,
                "Cost": round(cost, 2)
            })
            total_cost += cost
            
    return recommendations, round(total_cost, 2)

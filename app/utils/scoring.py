from typing import List, Dict

def calculate_effective_cpm(bid_cents: int, relevance: float, quality_factor: float = 1.0) -> float:
    """
    Calculate effective Cost Per Mille (eCPM) for ranking bids.
    
    Args:
        bid_cents: The original bid in cents
        relevance: Relevance score (0.0 to 1.0)
        quality_factor: Additional quality multiplier
        
    Returns:
        Effective bid for ranking purposes
    """
    return float(bid_cents) * relevance * quality_factor

def normalize_score(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Clamps a value to be within the specified range [min_val, max_val].
    
    Args:
        value: The score to normalize
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Normalized score
    """
    return max(min_val, min(value, max_val))

def weighted_category_match(campaign_categories: List[str], detected_categories: List[Dict]) -> float:
    """
    Compute a weighted match score between campaign target categories and detected content categories.
    
    Args:
        campaign_categories: List of IAB category codes the campaign targets
        detected_categories: List of dictionaries containing 'code' and 'confidence'
        
    Returns:
        A score between 0.0 and 1.0 representing the match quality
    """
    if not campaign_categories or not detected_categories:
        return 0.0
        
    campaign_targets = set(campaign_categories)
    
    max_score = 0.0
    for cat in detected_categories:
        code = cat.get('code')
        confidence = cat.get('confidence', 0.0)
        if code in campaign_targets and confidence > max_score:
            max_score = confidence
            
    return normalize_score(max_score)

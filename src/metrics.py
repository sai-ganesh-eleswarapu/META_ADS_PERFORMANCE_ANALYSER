def calculate_metrics(impressions, clicks, spend, conversions):
    # Basic ad performance metrics

    ctr = (clicks / impressions) * 100 if impressions > 0 else 0  # Click Through Rate
    cpc = (spend / clicks) if clicks > 0 else 0  # Cost Per Click
    cvr = (conversions / clicks) * 100 if clicks > 0 else 0  # Conversion Rate

    return ctr, cpc, cvr
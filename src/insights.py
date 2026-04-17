def generate_insight(data, prediction):
    impressions = data["impressions"]
    clicks = data["clicks"]
    spend = data["spend"]
    conversions = data["conversions"]

    ctr = clicks / impressions
    conversion_rate = conversions / clicks if clicks != 0 else 0

    if prediction == "creative_issue":
        return "Low CTR detected. Your ad creative may not be engaging enough."

    elif prediction == "audience_issue":
        return "High impressions but low engagement. Target audience may not be relevant."

    elif prediction == "conversion_issue":
        return "Users are clicking but not converting. Problem likely in landing page or offer."

    elif prediction == "good":
        return "Campaign performing well. Consider scaling budget."

    else:
        return "Unable to determine issue."
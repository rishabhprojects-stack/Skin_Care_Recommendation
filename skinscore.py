# skinscore.py 
def add_skincare_score(daily_summary, skin_type="normal"):
    scores = []
    recommendations = []

    for _, row in daily_summary.iterrows():
        score = 0
        recs = []

        # Hydration Stress (weight varies by skin type)
        if row.get("avg_humidity") is not None:
            if skin_type.lower() == "dry":
                if row["avg_humidity"] < 40:
                    score += 40
                    recs.append("Low humidity – rich moisturizer essential")
                elif row["avg_humidity"] < 50:
                    score += 20
                    recs.append("Moderate humidity – hydration important")
            elif skin_type.lower() == "oily":
                if row["avg_humidity"] < 30:
                    score += 20
                    recs.append("Low humidity – hydration helpful")

        # Sun / UV Stress
        uvi = row.get("uvi", 0)
        if uvi >= 8:
            score += 30
            recs.append("High UV – SPF 50+ needed")
        elif uvi >= 5:
            score += 20
            recs.append("Moderate UV – SPF advised")
        else:
            score += 5
            recs.append("Low sun exposure")

        # Wind Stress
        if row.get("wind_speed", 0) > 7:
            score += 20
            recs.append("Strong wind – barrier cream advised")
        elif row.get("wind_speed", 0) > 5:
            score += 10
            recs.append("Moderate wind – extra protection helpful")

        # Cold Stress
        min_temp = row.get("min_temp", row.get("temp", 20))
        if min_temp < 5:
            score += 10
            recs.append("Cold weather – heavy cream recommended")
        elif min_temp < 10:
            score += 5
            recs.append("Cool weather – use richer moisturizer")

        # Rain/Snow Stress
        total_precip = row.get("total_rain", 0) + row.get("total_snow", 0)
        if total_precip > 3:
            score += 10
            recs.append("Rain/Snow – protective cream helpful")

        scores.append(min(score, 100))
        recommendations.append("; ".join(recs))

    daily_summary["skincare_score"] = scores
    daily_summary["skincare_recs"] = recommendations
    return daily_summary

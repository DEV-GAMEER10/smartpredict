"""
SmartPredict AI — Insight Generator

Converts raw ML outputs into plain English insights and actionable recommendations.
Domain-adaptive: auto-detects business, healthcare, or education context.
"""
import pandas as pd
import numpy as np
from typing import Optional


# Domain keyword mappings for context detection
DOMAIN_KEYWORDS = {
    "business": ["revenue", "sales", "profit", "cost", "price", "customer", "order", "inventory",
                  "marketing", "expense", "income", "budget", "roi", "growth", "margin", "quantity"],
    "healthcare": ["patient", "diagnosis", "treatment", "hospital", "medicine", "health",
                    "blood", "pressure", "heart", "bmi", "age", "weight", "symptom", "disease"],
    "education": ["student", "grade", "score", "attendance", "course", "teacher", "exam",
                   "gpa", "enrollment", "class", "subject", "performance", "pass", "fail"],
}


def detect_domain(columns: list[str]) -> str:
    """Detect the domain from column names."""
    col_text = " ".join(columns).lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        scores[domain] = sum(1 for kw in keywords if kw in col_text)
    
    best = max(scores, key=scores.get)
    return best if scores[best] >= 2 else "business"  # Default to business


def generate_kpis(df: pd.DataFrame, data_summary: dict) -> list[dict]:
    """Generate top KPI cards from data summary."""
    kpis = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        return kpis
    
    domain = detect_domain(list(df.columns))
    
    # KPI 1: Primary metric (largest total numeric column)
    totals = {col: df[col].sum() for col in numeric_cols}
    primary_col = max(totals, key=totals.get)
    primary_val = totals[primary_col]
    
    # Calculate trend
    series = df[primary_col].values
    if len(series) >= 4:
        recent = np.mean(series[-len(series)//4:])
        earlier = np.mean(series[:len(series)//4])
        change = ((recent - earlier) / abs(earlier) * 100) if earlier != 0 else 0
    else:
        change = 0
    
    kpis.append({
        "label": _friendly_kpi_name(primary_col, "total"),
        "value": _format_number(primary_val),
        "change": round(change, 1),
        "direction": "up" if change > 0 else "down" if change < 0 else "stable",
        "icon": "💰" if domain == "business" else "🏥" if domain == "healthcare" else "📚",
        "color": "emerald" if change >= 0 else "red",
    })
    
    # KPI 2: Average of second numeric column
    if len(numeric_cols) >= 2:
        second_col = numeric_cols[1] if numeric_cols[1] != primary_col else numeric_cols[0]
        avg_val = df[second_col].mean()
        
        kpis.append({
            "label": _friendly_kpi_name(second_col, "average"),
            "value": _format_number(avg_val),
            "change": None,
            "direction": "stable",
            "icon": "📊",
            "color": "blue",
        })
    
    # KPI 3: Record count
    kpis.append({
        "label": "Total Records",
        "value": _format_number(len(df)),
        "change": None,
        "direction": "stable",
        "icon": "📋",
        "color": "violet",
    })
    
    # KPI 4: Growth rate of primary metric
    if change != 0:
        kpis.append({
            "label": "Growth Rate",
            "value": f"{abs(change):.1f}%",
            "change": round(change, 1),
            "direction": "up" if change > 0 else "down",
            "icon": "📈" if change > 0 else "📉",
            "color": "emerald" if change >= 0 else "amber",
        })
    else:
        # Data quality metric
        missing_pct = round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 1)
        kpis.append({
            "label": "Data Quality",
            "value": f"{100 - missing_pct:.0f}%",
            "change": None,
            "direction": "stable",
            "icon": "✅",
            "color": "emerald" if missing_pct < 5 else "amber",
        })
    
    return kpis


def generate_whats_happening(df: pd.DataFrame, data_summary: dict) -> list[str]:
    """Generate plain English descriptions of current data state."""
    statements = []
    domain = detect_domain(list(df.columns))
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Data overview
    statements.append(
        f"You have {len(df):,} records across {len(df.columns)} data categories."
    )
    
    # Top metrics
    for col in numeric_cols[:3]:
        total = df[col].sum()
        avg = df[col].mean()
        max_val = df[col].max()
        friendly = col.replace("_", " ").title()
        
        statements.append(
            f"Total {friendly}: {_format_number(total)} (average: {_format_number(avg)}, highest: {_format_number(max_val)})"
        )
    
    # Data range
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    if datetime_cols:
        date_col = datetime_cols[0]
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        statements.append(
            f"Your data spans from {min_date.strftime('%B %Y')} to {max_date.strftime('%B %Y')}."
        )
    
    # Categorical highlights
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_cols[:2]:
        top_val = df[col].value_counts().head(1)
        if len(top_val) > 0:
            friendly = col.replace("_", " ").title()
            statements.append(
                f"Most common {friendly}: \"{top_val.index[0]}\" ({top_val.values[0]:,} occurrences)"
            )
    
    return statements


def generate_recommendations(trends: list, patterns: list, risks: list, domain: str) -> list[dict]:
    """Generate actionable recommendations based on ML insights."""
    recommendations = []
    priority = 0
    
    # Recommendations from trends
    for trend in trends:
        priority += 1
        col = trend["friendly_name"]
        direction = trend["direction"]
        change = trend["change_percent"]
        
        if direction == "up" and change > 10:
            recommendations.append({
                "title": f"Capitalize on growing {col}",
                "description": f"{col} is projected to increase by {abs(change):.0f}%. Consider investing more resources in this area to maximize returns.",
                "impact": "high",
                "category": "opportunity",
                "icon": "🚀",
                "priority": priority,
            })
        elif direction == "up" and change > 0:
            recommendations.append({
                "title": f"Maintain momentum on {col}",
                "description": f"{col} shows steady growth of about {abs(change):.0f}%. Keep current strategies to sustain this positive trend.",
                "impact": "medium",
                "category": "action",
                "icon": "✨",
                "priority": priority,
            })
        elif direction == "down" and change > 10:
            recommendations.append({
                "title": f"Take action on declining {col}",
                "description": f"{col} is projected to decrease by {abs(change):.0f}%. Review your strategy and consider adjustments to reverse this trend.",
                "impact": "high",
                "category": "warning",
                "icon": "⚠️",
                "priority": priority,
            })
        elif direction == "down":
            recommendations.append({
                "title": f"Monitor {col} closely",
                "description": f"{col} shows a slight decline of about {abs(change):.0f}%. Keep an eye on this metric over the coming periods.",
                "impact": "medium",
                "category": "action",
                "icon": "👁️",
                "priority": priority,
            })
    
    # Recommendations from patterns
    for pattern in patterns:
        priority += 1
        if pattern["pattern_type"] == "correlation":
            cols = pattern["data"].get("columns", [])
            if len(cols) == 2:
                recommendations.append({
                    "title": f"Leverage the {cols[0].replace('_', ' ').title()} — {cols[1].replace('_', ' ').title()} connection",
                    "description": f"These two metrics move together. Changes in one will likely affect the other. Use this relationship for planning.",
                    "impact": "medium",
                    "category": "opportunity",
                    "icon": "🔗",
                    "priority": priority,
                })
        elif pattern["pattern_type"] == "cluster":
            recommendations.append({
                "title": "Consider segment-specific strategies",
                "description": pattern["description"] + " Tailoring your approach to each group could improve results.",
                "impact": "high",
                "category": "opportunity",
                "icon": "🎯",
                "priority": priority,
            })
    
    # Recommendations from risks
    for risk in risks:
        priority += 1
        if risk["severity"] in ["high", "critical"]:
            recommendations.append({
                "title": f"Address: {risk['title']}",
                "description": risk["description"] + " This needs immediate attention.",
                "impact": "high",
                "category": "warning",
                "icon": "🔴",
                "priority": priority,
            })
        elif risk["severity"] == "medium":
            recommendations.append({
                "title": f"Review: {risk['title']}",
                "description": risk["description"],
                "impact": "medium",
                "category": "action",
                "icon": "🟡",
                "priority": priority,
            })
    
    # Sort by impact priority
    impact_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda r: impact_order.get(r["impact"], 2))
    
    return recommendations


def generate_summary(df: pd.DataFrame, trends: list, patterns: list, risks: list) -> str:
    """Generate a one-paragraph executive summary."""
    parts = []
    domain = detect_domain(list(df.columns))
    
    parts.append(f"Based on your {len(df):,} records")
    
    # Trend summary
    up_trends = [t for t in trends if t["direction"] == "up"]
    down_trends = [t for t in trends if t["direction"] == "down"]
    
    if up_trends:
        top_up = max(up_trends, key=lambda t: t["change_percent"])
        parts.append(f"{top_up['friendly_name']} is trending upward (+{top_up['change_percent']:.0f}%)")
    
    if down_trends:
        top_down = max(down_trends, key=lambda t: t["change_percent"])
        parts.append(f"{top_down['friendly_name']} shows a decline (-{top_down['change_percent']:.0f}%)")
    
    # Risk summary
    high_risks = [r for r in risks if r["severity"] in ["high", "critical"]]
    if high_risks:
        parts.append(f"there {'are' if len(high_risks) > 1 else 'is'} {len(high_risks)} area{'s' if len(high_risks) > 1 else ''} needing attention")
    
    # Pattern summary
    if patterns:
        parts.append(f"{len(patterns)} interesting pattern{'s' if len(patterns) > 1 else ''} {'were' if len(patterns) > 1 else 'was'} found in your data")
    
    summary = ", ".join(parts) + "."
    return summary


def _friendly_kpi_name(col_name: str, metric_type: str) -> str:
    """Convert column name to a friendly KPI label."""
    friendly = col_name.replace("_", " ").title()
    
    if metric_type == "total":
        return f"Total {friendly}"
    elif metric_type == "average":
        return f"Avg {friendly}"
    else:
        return friendly


def _format_number(value) -> str:
    """Format a number for display."""
    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if abs(value) >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"
    elif abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"
    elif abs(value) < 1 and value != 0:
        return f"{value:.2f}"
    else:
        return f"{value:,.0f}"

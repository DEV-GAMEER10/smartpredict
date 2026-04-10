"""
SmartPredict AI — NLP Service

Handles natural language chat about data using OpenAI API.
Falls back to rule-based responses when no API key is available.
"""
import json
from typing import Optional
from app.config import settings


async def chat_with_data(
    question: str,
    data_summary: dict,
    columns_info: list[dict],
    recent_insights: Optional[dict] = None,
) -> dict:
    """
    Answer a natural language question about the uploaded data.
    
    Returns:
        dict with 'reply' and 'suggestions'
    """
    # Try OpenAI first
    if settings.OPENAI_API_KEY:
        try:
            return await _openai_chat(question, data_summary, columns_info, recent_insights)
        except Exception as e:
            print(f"OpenAI error, falling back to rule-based: {e}")
    
    # Fallback to rule-based
    return _rule_based_chat(question, data_summary, columns_info, recent_insights)


async def _openai_chat(
    question: str,
    data_summary: dict,
    columns_info: list[dict],
    recent_insights: Optional[dict],
) -> dict:
    """Use OpenAI API to answer data questions."""
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Build context
        context = _build_context(data_summary, columns_info, recent_insights)
        
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SmartPredict AI, a friendly business assistant that helps "
                        "non-technical users understand their data. You speak in plain English, "
                        "avoid technical jargon, and give actionable advice. "
                        "Keep responses concise (2-4 sentences). "
                        "Use simple language — you're talking to a business manager, not a data scientist. "
                        "If you don't have enough data to answer, say so honestly."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Here's the data context:\n{context}\n\nUser question: {question}",
                },
            ],
            max_tokens=300,
            temperature=0.7,
        )
        
        reply = response.choices[0].message.content.strip()
        
        return {
            "reply": reply,
            "suggestions": _generate_suggestions(data_summary, columns_info),
        }
    except ImportError:
        return _rule_based_chat(question, data_summary, columns_info, recent_insights)


def _rule_based_chat(
    question: str,
    data_summary: dict,
    columns_info: list[dict],
    recent_insights: Optional[dict],
) -> dict:
    """Rule-based fallback for when OpenAI is not available."""
    q_lower = question.lower()
    
    numeric_summary = data_summary.get("numeric_summary", {})
    columns = [c["name"] for c in columns_info]
    
    reply = ""
    
    # Pattern matching for common questions
    if any(word in q_lower for word in ["total", "sum", "how much", "overall"]):
        if numeric_summary:
            parts = []
            for col, stats in list(numeric_summary.items())[:3]:
                friendly = col.replace("_", " ").title()
                parts.append(f"Total {friendly}: {_format_num(stats.get('total', 0))}")
            reply = "Here are your totals: " + ". ".join(parts) + "."
    
    elif any(word in q_lower for word in ["average", "mean", "typical"]):
        if numeric_summary:
            parts = []
            for col, stats in list(numeric_summary.items())[:3]:
                friendly = col.replace("_", " ").title()
                parts.append(f"Average {friendly}: {_format_num(stats.get('average', 0))}")
            reply = "Here are the averages: " + ". ".join(parts) + "."
    
    elif any(word in q_lower for word in ["highest", "maximum", "best", "top", "most"]):
        if numeric_summary:
            parts = []
            for col, stats in list(numeric_summary.items())[:3]:
                friendly = col.replace("_", " ").title()
                parts.append(f"Highest {friendly}: {_format_num(stats.get('max', 0))}")
            reply = "Here are the peak values: " + ". ".join(parts) + "."
    
    elif any(word in q_lower for word in ["lowest", "minimum", "worst", "bottom", "least"]):
        if numeric_summary:
            parts = []
            for col, stats in list(numeric_summary.items())[:3]:
                friendly = col.replace("_", " ").title()
                parts.append(f"Lowest {friendly}: {_format_num(stats.get('min', 0))}")
            reply = "Here are the lowest values: " + ". ".join(parts) + "."
    
    elif any(word in q_lower for word in ["column", "fields", "data", "what do i have", "what's in"]):
        reply = f"Your dataset has {len(columns)} columns: {', '.join(col.replace('_', ' ').title() for col in columns[:8])}."
        if len(columns) > 8:
            reply += f" ...and {len(columns) - 8} more."
    
    elif any(word in q_lower for word in ["rows", "records", "entries", "how many"]):
        total = data_summary.get("total_rows", 0)
        reply = f"Your dataset contains {total:,} records."
    
    elif any(word in q_lower for word in ["trend", "predict", "future", "forecast", "next"]):
        if recent_insights and recent_insights.get("trends"):
            trend = recent_insights["trends"][0]
            reply = trend.get("summary", "I can see some trends in your data. Check the 'What Will Happen Next?' section of your dashboard for detailed predictions.")
        else:
            reply = "I've analyzed your data for trends. Check the 'What Will Happen Next?' section of your dashboard for detailed predictions."
    
    elif any(word in q_lower for word in ["risk", "problem", "issue", "concern", "worry"]):
        if recent_insights and recent_insights.get("risks"):
            risk = recent_insights["risks"][0]
            reply = f"I found this concern: {risk.get('title', 'Potential risk detected')}. {risk.get('description', 'Check the dashboard for details.')}"
        else:
            reply = "I haven't detected any major risks in your data. Things look stable for now."
    
    elif any(word in q_lower for word in ["recommend", "suggest", "should", "what to do", "advice"]):
        if recent_insights and recent_insights.get("recommendations"):
            rec = recent_insights["recommendations"][0]
            reply = f"My top recommendation: {rec.get('title', 'Review your data')}. {rec.get('description', '')}"
        else:
            reply = "Based on your data, I'd recommend reviewing the trends and patterns sections of your dashboard for actionable insights."
    
    elif any(word in q_lower for word in ["hello", "hi", "hey", "help"]):
        reply = (
            "Hi there! I'm your SmartPredict assistant. You can ask me things like:\n"
            "• 'What are my total sales?'\n"
            "• 'What trends do you see?'\n"
            "• 'Are there any risks?'\n"
            "• 'What should I do next?'"
        )
    
    else:
        reply = (
            "I understand you're asking about your data. Here's a quick overview: "
            f"You have {data_summary.get('total_rows', 0):,} records with "
            f"{data_summary.get('total_columns', 0)} data categories. "
            "Try asking about totals, averages, trends, or risks for more specific answers."
        )
    
    return {
        "reply": reply,
        "suggestions": _generate_suggestions(data_summary, columns_info),
    }


def _build_context(data_summary: dict, columns_info: list[dict], recent_insights: Optional[dict]) -> str:
    """Build context string for OpenAI."""
    parts = [
        f"Dataset: {data_summary.get('total_rows', 0)} rows, {data_summary.get('total_columns', 0)} columns",
        f"Columns: {', '.join(c['name'] for c in columns_info[:10])}",
    ]
    
    numeric_summary = data_summary.get("numeric_summary", {})
    if numeric_summary:
        for col, stats in list(numeric_summary.items())[:5]:
            parts.append(f"{col}: total={stats.get('total')}, avg={stats.get('average')}, min={stats.get('min')}, max={stats.get('max')}")
    
    if recent_insights:
        if recent_insights.get("trends"):
            for t in recent_insights["trends"][:3]:
                parts.append(f"Trend: {t.get('summary', '')}")
        if recent_insights.get("risks"):
            for r in recent_insights["risks"][:2]:
                parts.append(f"Risk: {r.get('title', '')} - {r.get('description', '')}")
    
    return "\n".join(parts)


def _generate_suggestions(data_summary: dict, columns_info: list[dict]) -> list[str]:
    """Generate suggested follow-up questions."""
    suggestions = [
        "What are the main trends?",
        "Are there any risks I should know about?",
        "What should I focus on next?",
    ]
    
    numeric_cols = [c["name"] for c in columns_info if "int" in c["dtype"] or "float" in c["dtype"]]
    if numeric_cols:
        suggestions.insert(0, f"What's the total {numeric_cols[0].replace('_', ' ')}?")
    
    return suggestions[:4]


def _format_num(value) -> str:
    """Format number for display."""
    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:,.1f}"

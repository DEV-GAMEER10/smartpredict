"""
SmartPredict AI — Insights Routes
"""
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.api.routes.upload import get_dataset_store
from app.services.ml_engine import MLEngine
from app.services.insight_generator import (
    generate_kpis,
    generate_whats_happening,
    generate_recommendations,
    generate_summary,
    detect_domain,
)

router = APIRouter(prefix="/api", tags=["insights"])

# Cache for generated insights
insights_cache = {}


@router.get("/insights/{dataset_id}")
async def get_insights(dataset_id: int):
    """Generate full AI insights for a dataset."""
    
    datasets_store = get_dataset_store()
    
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Check cache
    if dataset_id in insights_cache:
        return insights_cache[dataset_id]
    
    dataset = datasets_store[dataset_id]
    
    try:
        # Load cleaned data
        df = pd.read_csv(dataset["cleaned_filepath"])
        
        # Auto-detect date columns
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    converted = pd.to_datetime(df[col], infer_datetime_format=True)
                    if converted.notna().sum() > len(df) * 0.5:
                        df[col] = converted
                except (ValueError, TypeError):
                    pass
        
        data_summary = dataset["data_summary"]
        
        # Run ML Engine
        engine = MLEngine(df)
        trends = engine.predict_trends(periods=6)
        patterns = engine.detect_patterns()
        risks = engine.analyze_risks()
        
        # Generate insights
        domain = detect_domain(list(df.columns))
        kpis = generate_kpis(df, data_summary)
        whats_happening = generate_whats_happening(df, data_summary)
        recommendations = generate_recommendations(trends, patterns, risks, domain)
        summary = generate_summary(df, trends, patterns, risks)
        
        response = {
            "dataset_id": dataset_id,
            "dataset_name": dataset["original_filename"],
            "kpis": kpis,
            "whats_happening": whats_happening,
            "trends": trends,
            "patterns": patterns,
            "risks": risks,
            "recommendations": recommendations,
            "summary": summary,
            "generated_at": datetime.utcnow().isoformat(),
        }
        
        # Cache results
        insights_cache[dataset_id] = response
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@router.get("/insights/{dataset_id}/refresh")
async def refresh_insights(dataset_id: int):
    """Force regenerate insights for a dataset."""
    if dataset_id in insights_cache:
        del insights_cache[dataset_id]
    return await get_insights(dataset_id)


def get_insights_cache():
    """Expose insights cache to other modules."""
    return insights_cache

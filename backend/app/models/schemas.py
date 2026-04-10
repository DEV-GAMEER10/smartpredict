"""
SmartPredict AI — Pydantic Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Dataset Schemas ──────────────────────────────────────────

class ColumnInfo(BaseModel):
    name: str
    dtype: str
    non_null_count: int = 0
    sample_values: list = []
    unique_count: int = 0


class DatasetMeta(BaseModel):
    id: int
    filename: str
    original_filename: str
    upload_date: Optional[str] = None
    row_count: int = 0
    column_count: int = 0
    columns_info: list[ColumnInfo] = []
    file_size_bytes: int = 0
    status: str = "uploaded"
    cleaning_report: dict = {}
    data_summary: dict = {}


class DatasetListItem(BaseModel):
    id: int
    original_filename: str
    upload_date: Optional[str] = None
    row_count: int
    column_count: int
    status: str


# ── Insight Schemas ──────────────────────────────────────────

class KPI(BaseModel):
    label: str
    value: str
    change: Optional[float] = None  # Percentage change
    direction: Optional[str] = None  # up, down, stable
    icon: str = "📊"
    color: str = "blue"


class TrendPoint(BaseModel):
    label: str
    actual: Optional[float] = None
    predicted: Optional[float] = None
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None


class TrendPrediction(BaseModel):
    column_name: str
    friendly_name: str
    direction: str  # up, down, stable
    change_percent: float
    summary: str
    chart_data: list[TrendPoint] = []
    confidence: float = 0.0


class PatternInfo(BaseModel):
    title: str
    description: str
    pattern_type: str  # correlation, cluster, seasonal
    strength: str  # weak, moderate, strong
    data: dict = {}


class RiskAlert(BaseModel):
    title: str
    description: str
    severity: str  # low, medium, high, critical
    affected_metric: str
    data: dict = {}


class Recommendation(BaseModel):
    title: str
    description: str
    impact: str  # low, medium, high
    category: str  # action, warning, opportunity
    icon: str = "💡"
    priority: int = 0


class InsightResponse(BaseModel):
    dataset_id: int
    dataset_name: str
    kpis: list[KPI] = []
    whats_happening: list[str] = []
    trends: list[TrendPrediction] = []
    patterns: list[PatternInfo] = []
    risks: list[RiskAlert] = []
    recommendations: list[Recommendation] = []
    summary: str = ""
    generated_at: Optional[str] = None


# ── Chat Schemas ─────────────────────────────────────────────

class ChatRequest(BaseModel):
    dataset_id: int
    message: str


class ChatResponse(BaseModel):
    reply: str
    suggestions: list[str] = []


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    created_at: Optional[str] = None


# ── Upload Schemas ───────────────────────────────────────────

class UploadResponse(BaseModel):
    dataset_id: int
    filename: str
    row_count: int
    column_count: int
    columns: list[str]
    status: str
    message: str


class CleaningReport(BaseModel):
    rows_removed: int = 0
    duplicates_removed: int = 0
    missing_values_filled: dict = {}
    columns_normalized: list[str] = []
    type_conversions: dict = {}

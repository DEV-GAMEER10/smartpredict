"""
SmartPredict AI — Database Models
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float
from app.db.database import Base


class Dataset(Base):
    """Uploaded dataset record."""
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    columns_info = Column(JSON, default=list)  # [{name, dtype, sample_values}]
    file_size_bytes = Column(Integer, default=0)
    status = Column(String(50), default="uploaded")  # uploaded, cleaning, ready, error
    cleaning_report = Column(JSON, default=dict)
    data_summary = Column(JSON, default=dict)  # Basic stats per column


class Insight(Base):
    """Generated insight for a dataset."""
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, nullable=False)
    insight_type = Column(String(50), nullable=False)  # trend, pattern, risk, recommendation
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    data = Column(JSON, default=dict)  # Chart data, metrics, etc.
    confidence = Column(Float, default=0.0)
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ChatMessage(Base):
    """Chat message history."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

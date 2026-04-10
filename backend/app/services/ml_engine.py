"""
SmartPredict AI — ML Engine

Machine learning models for trend prediction, pattern detection, and risk analysis.
All models auto-select features based on data types.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score
from typing import Optional
import warnings

warnings.filterwarnings("ignore")


class MLEngine:
    """Core ML engine for SmartPredict predictions."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
        self.scaler = StandardScaler()
    
    def predict_trends(self, periods: int = 6) -> list[dict]:
        """
        Predict future trends for numeric columns.
        Uses Linear Regression and Random Forest.
        Returns predictions with chart data.
        """
        trends = []
        
        if not self.numeric_cols:
            return trends
        
        for col in self.numeric_cols[:5]:  # Limit to top 5 numeric columns
            try:
                series = self.df[col].dropna().values
                if len(series) < 5:
                    continue
                
                # Create time index
                X = np.arange(len(series)).reshape(-1, 1)
                y = series
                
                # Linear Regression for trend direction
                lr = LinearRegression()
                lr.fit(X, y)
                lr_score = max(0, lr.score(X, y))
                
                # Random Forest for better predictions
                rf = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
                rf.fit(X, y)
                
                # Predict future periods
                future_X = np.arange(len(series), len(series) + periods).reshape(-1, 1)
                rf_predictions = rf.predict(future_X)
                lr_predictions = lr.predict(future_X)
                
                # Blend predictions (70% RF, 30% LR for smoothness)
                predictions = 0.7 * rf_predictions + 0.3 * lr_predictions
                
                # Calculate prediction bounds (±1 std of residuals)
                residuals = y - rf.predict(X)
                std_residual = np.std(residuals)
                
                # Calculate trend direction and percentage
                recent_avg = np.mean(series[-3:]) if len(series) >= 3 else series[-1]
                predicted_avg = np.mean(predictions[:3])
                
                if recent_avg != 0:
                    change_pct = ((predicted_avg - recent_avg) / abs(recent_avg)) * 100
                else:
                    change_pct = 0
                
                if change_pct > 2:
                    direction = "up"
                elif change_pct < -2:
                    direction = "down"
                else:
                    direction = "stable"
                
                # Build chart data
                chart_data = []
                
                # Historical data points
                step = max(1, len(series) // 20)  # Limit to ~20 points for chart
                for i in range(0, len(series), step):
                    chart_data.append({
                        "label": f"Period {i+1}",
                        "actual": round(float(series[i]), 2),
                        "predicted": None,
                    })
                
                # Predicted data points
                for i in range(periods):
                    chart_data.append({
                        "label": f"Future {i+1}",
                        "actual": None,
                        "predicted": round(float(predictions[i]), 2),
                        "lower_bound": round(float(predictions[i] - 1.5 * std_residual), 2),
                        "upper_bound": round(float(predictions[i] + 1.5 * std_residual), 2),
                    })
                
                trends.append({
                    "column_name": col,
                    "friendly_name": col.replace("_", " ").title(),
                    "direction": direction,
                    "change_percent": round(change_pct, 1),
                    "summary": _trend_summary(col, direction, abs(change_pct)),
                    "chart_data": chart_data,
                    "confidence": round(lr_score * 100, 1),
                })
            except Exception as e:
                continue
        
        return trends
    
    def detect_patterns(self) -> list[dict]:
        """
        Detect patterns in the data using correlation analysis and clustering.
        """
        patterns = []
        
        if len(self.numeric_cols) < 2:
            return patterns
        
        # Correlation analysis
        try:
            corr_matrix = self.df[self.numeric_cols].corr()
            
            for i, col1 in enumerate(self.numeric_cols):
                for j, col2 in enumerate(self.numeric_cols):
                    if i >= j:
                        continue
                    corr_val = corr_matrix.loc[col1, col2]
                    if abs(corr_val) > 0.5:  # Significant correlation
                        strength = "strong" if abs(corr_val) > 0.7 else "moderate"
                        direction = "increase together" if corr_val > 0 else "move in opposite directions"
                        
                        patterns.append({
                            "title": f"{col1.replace('_', ' ').title()} ↔ {col2.replace('_', ' ').title()}",
                            "description": f"When {col1.replace('_', ' ')} goes up, {col2.replace('_', ' ')} tends to {direction.split()[0]}. This is a {strength} relationship.",
                            "pattern_type": "correlation",
                            "strength": strength,
                            "data": {
                                "correlation": round(float(corr_val), 3),
                                "columns": [col1, col2],
                            },
                        })
        except Exception:
            pass
        
        # Clustering (segment detection)
        try:
            if len(self.numeric_cols) >= 2 and len(self.df) >= 10:
                cluster_cols = self.numeric_cols[:5]
                cluster_data = self.df[cluster_cols].dropna()
                
                if len(cluster_data) >= 10:
                    scaled = self.scaler.fit_transform(cluster_data)
                    
                    n_clusters = min(3, len(cluster_data) // 5)
                    if n_clusters >= 2:
                        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                        labels = kmeans.fit_predict(scaled)
                        
                        # Describe clusters
                        cluster_data_with_labels = cluster_data.copy()
                        cluster_data_with_labels["_cluster"] = labels
                        
                        cluster_descriptions = []
                        for c in range(n_clusters):
                            cluster_subset = cluster_data_with_labels[cluster_data_with_labels["_cluster"] == c]
                            size = len(cluster_subset)
                            pct = round(size / len(cluster_data) * 100, 1)
                            
                            # Find the defining characteristic
                            means = cluster_subset[cluster_cols].mean()
                            overall_means = cluster_data[cluster_cols].mean()
                            diff = ((means - overall_means) / overall_means.replace(0, 1) * 100).round(1)
                            
                            top_feature = diff.abs().idxmax()
                            top_diff = diff[top_feature]
                            
                            direction_word = "higher" if top_diff > 0 else "lower"
                            cluster_descriptions.append({
                                "group": c + 1,
                                "size": size,
                                "percentage": pct,
                                "defining_feature": f"{abs(top_diff):.0f}% {direction_word} {top_feature.replace('_', ' ')}",
                            })
                        
                        patterns.append({
                            "title": f"Data has {n_clusters} distinct groups",
                            "description": f"Your data naturally splits into {n_clusters} segments. " + 
                                "; ".join([f"Group {d['group']} ({d['percentage']}% of data) has {d['defining_feature']}" for d in cluster_descriptions]),
                            "pattern_type": "cluster",
                            "strength": "moderate",
                            "data": {
                                "clusters": cluster_descriptions,
                                "features_used": cluster_cols,
                            },
                        })
        except Exception:
            pass
        
        # Seasonal / periodic pattern detection
        try:
            for col in self.numeric_cols[:3]:
                series = self.df[col].dropna().values
                if len(series) >= 12:
                    # Simple periodicity check via autocorrelation
                    mean = np.mean(series)
                    if np.std(series) > 0:
                        autocorr = np.correlate(series - mean, series - mean, mode='full')
                        autocorr = autocorr[len(autocorr)//2:]
                        autocorr = autocorr / autocorr[0]
                        
                        # Find peaks in autocorrelation
                        peaks = []
                        for i in range(2, len(autocorr) - 1):
                            if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and autocorr[i] > 0.3:
                                peaks.append(i)
                                break
                        
                        if peaks:
                            period = peaks[0]
                            patterns.append({
                                "title": f"Repeating pattern in {col.replace('_', ' ').title()}",
                                "description": f"{col.replace('_', ' ').title()} shows a repeating pattern every {period} periods. This could indicate seasonal or cyclical behavior.",
                                "pattern_type": "seasonal",
                                "strength": "moderate",
                                "data": {"period": period, "column": col},
                            })
        except Exception:
            pass
        
        return patterns
    
    def analyze_risks(self) -> list[dict]:
        """
        Detect anomalies and risks using Isolation Forest and statistical methods.
        """
        risks = []
        
        if not self.numeric_cols:
            return risks
        
        # Isolation Forest anomaly detection
        try:
            risk_cols = self.numeric_cols[:5]
            risk_data = self.df[risk_cols].dropna()
            
            if len(risk_data) >= 10:
                scaled = self.scaler.fit_transform(risk_data)
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                anomaly_labels = iso_forest.fit_predict(scaled)
                
                anomaly_count = (anomaly_labels == -1).sum()
                anomaly_pct = round(anomaly_count / len(risk_data) * 100, 1)
                
                if anomaly_count > 0:
                    severity = "high" if anomaly_pct > 15 else "medium" if anomaly_pct > 5 else "low"
                    risks.append({
                        "title": f"{anomaly_count} unusual data points detected",
                        "description": f"About {anomaly_pct}% of your data contains unusual patterns that don't fit the norm. These could be errors, outliers, or important events worth investigating.",
                        "severity": severity,
                        "affected_metric": "Overall data",
                        "data": {"anomaly_count": int(anomaly_count), "anomaly_percentage": anomaly_pct},
                    })
        except Exception:
            pass
        
        # Statistical risk analysis per column
        for col in self.numeric_cols[:5]:
            try:
                series = self.df[col].dropna()
                if len(series) < 5:
                    continue
                
                mean = series.mean()
                std = series.std()
                
                if std == 0:
                    continue
                
                # Check for high volatility
                cv = (std / abs(mean)) * 100 if mean != 0 else 0
                if cv > 50:
                    risks.append({
                        "title": f"High volatility in {col.replace('_', ' ').title()}",
                        "description": f"{col.replace('_', ' ').title()} varies a lot (coefficient of variation: {cv:.0f}%). This means it's unpredictable and may need closer monitoring.",
                        "severity": "medium" if cv < 100 else "high",
                        "affected_metric": col.replace("_", " ").title(),
                        "data": {"cv": round(cv, 1), "mean": round(float(mean), 2), "std": round(float(std), 2)},
                    })
                
                # Check for declining trend (last 30% vs first 30%)
                n = len(series)
                first_third = series.iloc[:n//3].mean()
                last_third = series.iloc[-n//3:].mean()
                
                if first_third != 0:
                    decline_pct = ((last_third - first_third) / abs(first_third)) * 100
                    if decline_pct < -15:
                        risks.append({
                            "title": f"Declining trend in {col.replace('_', ' ').title()}",
                            "description": f"{col.replace('_', ' ').title()} has dropped by about {abs(decline_pct):.0f}% from earlier periods. This downward trend may need attention.",
                            "severity": "high" if decline_pct < -30 else "medium",
                            "affected_metric": col.replace("_", " ").title(),
                            "data": {"decline_percent": round(decline_pct, 1)},
                        })
            except Exception:
                continue
        
        return risks


def _trend_summary(col_name: str, direction: str, change_pct: float) -> str:
    """Generate a plain English trend summary."""
    friendly_name = col_name.replace("_", " ").title()
    
    if direction == "up":
        if change_pct > 20:
            return f"{friendly_name} is expected to grow significantly — up about {change_pct:.0f}% in the coming periods."
        elif change_pct > 5:
            return f"{friendly_name} is trending upward, with a projected increase of about {change_pct:.0f}%."
        else:
            return f"{friendly_name} shows a slight upward trend — expect modest growth around {change_pct:.0f}%."
    
    elif direction == "down":
        if change_pct > 20:
            return f"{friendly_name} is projected to drop significantly — down about {change_pct:.0f}%. Action may be needed."
        elif change_pct > 5:
            return f"{friendly_name} is trending downward, with a projected decline of about {change_pct:.0f}%."
        else:
            return f"{friendly_name} shows a slight downward trend — a small decline of about {change_pct:.0f}% is expected."
    
    else:
        return f"{friendly_name} is expected to remain relatively stable in the near future."

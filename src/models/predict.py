"""Prediction and confidence helpers for persisted sklearn pipelines."""
from __future__ import annotations
import numpy as np
from src.features.feature_schema import NUMERIC_FEATURES, CATEGORICAL_FEATURES

def predict_one(pipeline, record: dict) -> dict:
    import pandas as pd
    frame=pd.DataFrame([record])
    for field in NUMERIC_FEATURES + CATEGORICAL_FEATURES:
        if field not in frame: frame[field]=None
    model=pipeline; pred=model.predict(frame)[0]
    probs=model.predict_proba(frame)[0] if hasattr(model,"predict_proba") else None
    classes=list(model.classes_) if hasattr(model,"classes_") else []
    confidence=float(np.max(probs)) if probs is not None else 0.0
    return {"label":str(pred),"confidence":confidence,"probabilities":{str(c):float(p) for c,p in zip(classes,probs)} if probs is not None else {},"top_factors":top_factors(pipeline,str(pred))}

def top_factors(pipeline, predicted_label: str, limit: int = 5) -> list[str]:
    """Return model-ranked signals without implying causality."""
    try:
        estimator=pipeline.named_steps["model"]
        transformer=pipeline.named_steps["features"].named_steps["features"]
        names=transformer.get_feature_names_out()
        if hasattr(estimator,"feature_importances_"):
            weights=np.asarray(estimator.feature_importances_)
        elif hasattr(estimator,"coef_"):
            classes=list(estimator.classes_)
            class_index=classes.index(predicted_label)
            if len(classes)>2: weights=np.asarray(estimator.coef_[class_index]).ravel()
            else:
                weights=np.asarray(estimator.coef_[0]).ravel()
                if class_index==0: weights=-weights
        else: return []
        order=np.argsort(np.abs(weights))[::-1][:limit]
        return [f"{names[i]} (model weight {weights[i]:.3f})" for i in order if i<len(names)]
    except (AttributeError,KeyError,ValueError,IndexError): return []

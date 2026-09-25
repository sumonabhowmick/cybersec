"""Fair train/validation/test comparison for threat and severity targets."""
from __future__ import annotations
import json, logging, time
import importlib.util
from pathlib import Path
import joblib, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.config.settings import DATA_PROCESSED, DATA_REPORTS, MODEL_DIR, RANDOM_SEED, MLFLOW_TRACKING_URI
from src.features.feature_pipeline import build_feature_transformer
from src.features.feature_schema import schema, write_schema
from src.models.baseline import build_baseline
from src.models.random_forest import build_random_forest
from src.models.evaluate import evaluate_model
from src.models.model_registry import save_artifact

logging.basicConfig(level=logging.INFO)
def _splits(df, target):
    train, remainder = train_test_split(df, test_size=.30, random_state=RANDOM_SEED, stratify=df[target])
    valid, test = train_test_split(remainder, test_size=.50, random_state=RANDOM_SEED, stratify=remainder[target])
    return train, valid, test

def _tracking():
    try:
        import mlflow
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI); mlflow.set_experiment("cybersecurity-incident-classification"); return mlflow
    except ImportError:
        logging.warning("MLflow is unavailable; comparison runs will be saved locally only."); return None

def train_all(dataset=DATA_PROCESSED / "cleaned_incidents.csv", max_features=20000, include_optional=True):
    df=pd.read_csv(dataset,low_memory=False)
    metrics={}; mlflow=_tracking()
    for target in ["threat_category","severity_level"]:
        train, valid, test = _splits(df,target)
        Xtr,ytr=train,train[target].astype(str); Xv,yv=valid,valid[target].astype(str); Xt,yt=test,test[target].astype(str)
        candidates={"logistic_regression_unigram":(build_baseline(),(1,1)),
            "logistic_regression_unigram_bigram":(build_baseline(),(1,2)),
            "random_forest_unigram_bigram":(build_random_forest(),(1,2))}
        if importlib.util.find_spec("tensorflow"):
            from src.models.neural_network import KerasMLPClassifier
            candidates["keras_mlp_unigram_bigram"]=(KerasMLPClassifier(max_features=max_features,ngram_range=(1,2),seed=RANDOM_SEED,model_path=str(MODEL_DIR/f"{target}_keras.keras")),(1,2))
        else: logging.warning("TensorFlow unavailable; Keras MLP omitted for %s",target)
        if include_optional:
            try:
                from src.models.xgboost_model import build_xgboost
                candidates["xgboost_unigram_bigram"]=(build_xgboost(),(1,2))
            except RuntimeError as e: logging.warning("%s",e)
        target_runs=[]; fitted=[]
        for name, (estimator, ngram_range) in candidates.items():
            if estimator.__class__.__name__=="KerasMLPClassifier":
                pipeline=estimator
            else:
                pipeline=Pipeline([("features",build_feature_transformer(max_features=max_features,ngram_range=ngram_range)),("model",estimator)])
            started=time.perf_counter()
            try:
                if estimator.__class__.__name__=="KerasMLPClassifier": pipeline.fit(Xtr,ytr,validation_data=(Xv,yv))
                else: pipeline.fit(Xtr,ytr)
                train_time=time.perf_counter()-started
                val_metrics=evaluate_model(pipeline,Xv,yv)
                row={"model":name,"target":target,"training_time_seconds":train_time,"validation":val_metrics}
                target_runs.append(row); fitted.append((name,pipeline,val_metrics,train_time))
                if mlflow:
                    try:
                        with mlflow.start_run(run_name=f"{target}-{name}"):
                            mlflow.log_params({"target":target,"model":name,"seed":RANDOM_SEED,"max_features":max_features,"ngram_range":str(ngram_range)})
                            mlflow.log_metrics({"training_time_seconds":train_time,**{f"validation_{k}":v for k,v in val_metrics.items() if isinstance(v,(int,float))}})
                            mlflow.log_dict({"labels":val_metrics["labels"],"matrix":val_metrics["confusion_matrix"]},f"confusion_matrices/{target}_{name}_validation.json")
                            mlflow.sklearn.log_model(pipeline,name="model",serialization_format="cloudpickle")
                    except Exception as exc: logging.warning("MLflow logging failed for %s/%s: %s",target,name,exc)
            except Exception as exc: logging.exception("Candidate failed: %s/%s",target,name); target_runs.append({"model":name,"target":target,"error":str(exc)})
        if not fitted: raise RuntimeError(f"All candidate models failed for {target}")
        # Selection is strictly on validation macro F1 then weighted F1, recall, precision, accuracy.
        name, winner, val, train_time=max(fitted,key=lambda x:(x[2]["macro_f1"],x[2]["weighted_f1"],x[2]["recall_macro"],x[2]["precision_macro"],x[2]["accuracy"],-x[3]))
        # Evaluate the selected model on the held-out test set only after selection.
        final_test=evaluate_model(winner,Xt,yt)
        if mlflow:
            try:
                with mlflow.start_run(run_name=f"{target}-{name}-final-test"):
                    mlflow.log_params({"target":target,"selected_model":name,"evaluation":"held-out test after validation selection"})
                    mlflow.log_metrics({f"test_{k}":v for k,v in final_test.items() if isinstance(v,(int,float))})
                    mlflow.log_dict({"labels":final_test["labels"],"matrix":final_test["confusion_matrix"]},f"confusion_matrices/{target}_{name}_test.json")
            except Exception as exc: logging.warning("Could not log final test metrics: %s",exc)
        save_artifact(winner,{"target":target,"selected_model":name,"selection_metric":"validation macro_f1","validation":val,"test":final_test,"training_rows":len(train),"validation_rows":len(valid),"test_rows":len(test),"seed":RANDOM_SEED,"feature_policy":schema()},target,MODEL_DIR)
        metrics[target]={"candidates":target_runs,"selected_model":name,"selected_validation":val,"final_test":final_test}
    write_schema(DATA_PROCESSED/"feature_schema.json")
    (DATA_REPORTS/"model_comparison.json").write_text(json.dumps(metrics,indent=2,default=str),encoding="utf-8")
    return metrics

if __name__=="__main__":
    from src.data.cleaning import clean_csv
    clean_csv(); result=train_all(); print(json.dumps({k:v["selected_model"] for k,v in result.items()},indent=2))

"""Lightweight Keras MLP comparison candidate; never required for the baseline API."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
from src.features.feature_pipeline import build_feature_transformer

def build_mlp(input_dim: int, class_count: int, seed: int = 42):
    try:
        import tensorflow as tf
        from tensorflow import keras
    except ImportError as exc: raise RuntimeError("TensorFlow is not installed. Install requirements.txt to enable the MLP.") from exc
    tf.keras.utils.set_random_seed(seed)
    inputs=keras.Input(shape=(input_dim,)); x=keras.layers.Dense(256)(inputs); x=keras.layers.BatchNormalization()(x); x=keras.layers.ReLU()(x); x=keras.layers.Dropout(.30)(x); x=keras.layers.Dense(128,activation="relu")(x); x=keras.layers.Dropout(.20)(x); outputs=keras.layers.Dense(class_count,activation="softmax")(x)
    model=keras.Model(inputs,outputs); model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"]); return model

def fit_mlp(model, X_train, y_train, X_validation, y_validation, checkpoint_path, epochs=50, batch_size=64):
    """Fit with early stopping, best-weight checkpointing, and balanced class weights."""
    try:
        import numpy as np
        import tensorflow as tf
        from sklearn.utils.class_weight import compute_class_weight
    except ImportError as exc: raise RuntimeError("TensorFlow and scikit-learn are required for MLP training") from exc
    classes=np.unique(y_train)
    weights=compute_class_weight(class_weight="balanced",classes=classes,y=y_train)
    class_weight={int(k):float(v) for k,v in zip(classes,weights)}
    callbacks=[tf.keras.callbacks.EarlyStopping(monitor="val_loss",patience=5,restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(str(checkpoint_path),monitor="val_loss",save_best_only=True)]
    return model.fit(X_train,y_train,validation_data=(X_validation,y_validation),epochs=epochs,batch_size=batch_size,
        class_weight=class_weight,callbacks=callbacks,verbose=0)

class KerasMLPClassifier(BaseEstimator, ClassifierMixin):
    """Sparse text + structured transformer, truncated projection, and small Keras MLP."""
    def __init__(self, max_features=20000, ngram_range=(1,2), seed=42, model_path=None):
        self.max_features=max_features; self.ngram_range=ngram_range; self.seed=seed; self.model_path=model_path
    def fit(self, X, y, validation_data=None):
        try: import tensorflow as tf
        except ImportError as exc: raise RuntimeError("TensorFlow is not installed. Install requirements.txt to enable the MLP.") from exc
        from sklearn.model_selection import train_test_split
        self.encoder_=LabelEncoder().fit(y); encoded=self.encoder_.transform(y); self.classes_=self.encoder_.classes_
        self.features_=build_feature_transformer(self.max_features,self.ngram_range)
        sparse_train=self.features_.fit_transform(X,y)
        self.svd_=TruncatedSVD(n_components=min(128,max(1,sparse_train.shape[1]-1)),random_state=self.seed)
        dense_train=self.svd_.fit_transform(sparse_train).astype("float32")
        if validation_data is None:
            indices=np.arange(len(encoded))
            train_i,val_i=train_test_split(indices,test_size=.1,random_state=self.seed,stratify=encoded)
            x_train,x_val=dense_train[train_i],dense_train[val_i]; y_train,y_val=encoded[train_i],encoded[val_i]
        else:
            x_train=dense_train; y_train=encoded
            X_val,y_val_raw=validation_data
            y_val=self.encoder_.transform(y_val_raw)
            dense_val=self.svd_.transform(self.features_.transform(X_val)).astype("float32")
            x_val=dense_val
        self.model_=build_mlp(dense_train.shape[1],len(self.classes_),self.seed)
        base=Path(self.model_path) if self.model_path else Path("models/artifacts/keras_mlp.keras")
        base.parent.mkdir(parents=True,exist_ok=True)
        checkpoint=base.with_name(base.stem+".best.keras")
        fit_mlp(self.model_,x_train,y_train,x_val,y_val,checkpoint)
        self.model_.save(str(base)); self.model_path_=str(base)
        return self
    def _load(self):
        if getattr(self,"model_",None) is None:
            import tensorflow as tf
            self.model_=tf.keras.models.load_model(self.model_path_)
        return self.model_
    def predict_proba(self,X):
        sparse=self.features_.transform(X); dense=self.svd_.transform(sparse).astype("float32")
        return self._load().predict(dense,verbose=0)
    def predict(self,X): return self.classes_[np.argmax(self.predict_proba(X),axis=1)]
    def __getstate__(self):
        state=self.__dict__.copy()
        if state.get("model_") is not None:
            state["model_"].save(state["model_path_"]); state["model_"]=None
        return state

import os
import argparse
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "tmp"
TEMP_DIR.mkdir(exist_ok=True)
os.environ["TMP"] = str(TEMP_DIR)
os.environ["TEMP"] = str(TEMP_DIR)

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score


MLRUNS_DIR = BASE_DIR / "mlruns"
EXPERIMENT_NAME = "Customer Segmentation - Basic"


def load_dataset(data_path: str) -> pd.DataFrame:
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Dataset preprocessing tidak ditemukan: {data_path}")
    return pd.read_csv(data_path)


def train_model(df: pd.DataFrame, n_clusters: int, random_state: int) -> tuple[KMeans, dict[str, float]]:
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(df)

    metrics = {
        "inertia": model.inertia_,
        "silhouette_score": silhouette_score(df, labels),
        "calinski_harabasz_score": calinski_harabasz_score(df, labels),
        "davies_bouldin_score": davies_bouldin_score(df, labels),
    }

    return model, metrics


def save_clustered_dataset(df: pd.DataFrame, labels) -> Path:
    output_path = BASE_DIR / "Customer-Segmentation_clustered_basic.csv"
    result = df.copy()
    result["Cluster"] = labels
    result.to_csv(output_path, index=False)
    return output_path


def save_pca_projection(df: pd.DataFrame, labels, random_state: int) -> Path:
    pca = PCA(n_components=2, random_state=random_state)
    projection = pca.fit_transform(df)

    output_path = BASE_DIR / "pca_projection_basic.csv"
    pca_df = pd.DataFrame(
        {
            "PCA1": projection[:, 0],
            "PCA2": projection[:, 1],
            "Cluster": labels,
        }
    )
    pca_df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=True)
    parser.add_argument("--n_clusters", type=int, default=3)
    parser.add_argument("--random_state", type=int, default=42)
    args = parser.parse_args()

    mlflow.set_tracking_uri(MLRUNS_DIR.as_uri())
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.sklearn.autolog()

    df = load_dataset(args.dataset_path)

    with mlflow.start_run(run_name="kmeans_basic_autolog"):
        model, metrics = train_model(df, args.n_clusters, args.random_state)
        mlflow.sklearn.autolog(disable=True)
        labels = model.labels_

        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(save_clustered_dataset(df, labels)))
        mlflow.log_artifact(str(save_pca_projection(df, labels, args.random_state)))

        print("Model Basic selesai dilatih.")
        print(f"Tracking URI: {MLRUNS_DIR}")
        print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()

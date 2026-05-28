# Customer Segmentation MLflow Pipeline

Project ini melatih model clustering untuk segmentasi pelanggan menggunakan KMeans, MLflow Tracking, GitHub Actions, dan Docker Hub. Pipeline dibuat supaya proses training, pencatatan metrik, penyimpanan artefak, dan pembuatan image model bisa dijalankan ulang secara konsisten dari repository.

## Ringkasan

- Model: KMeans clustering
- Tracking: MLflow local file store di folder `MLProject/mlruns`
- Dataset utama: `MLProject/Customer-Segmentation_preprocessing.csv`
- Artefak training: hasil cluster, PCA projection, MLflow run, dan model artifact
- CI: GitHub Actions untuk training otomatis dan penyimpanan artefak
- Docker: image dibuat dari model MLflow menggunakan `mlflow models build-docker`

## Struktur Project

```text
.
|-- .github/workflows/
|   |-- mlflow-training.yml
|   `-- mlflow-docker.yml
|-- MLProject/
|   |-- MLProject
|   |-- Customer-Segmentation_preprocessing.csv
|   |-- conda.yaml
|   |-- modelling.py
|   `-- requirements.txt
|-- github-artifacts/
|   `-- mlflow-training/
|-- data/
|-- Dockerfile
`-- README.md
```

## Menjalankan Training Lokal

Install dependency:

```bash
pip install -r MLProject/requirements.txt
```

Jalankan training:

```bash
cd MLProject
python modelling.py \
  --dataset_path Customer-Segmentation_preprocessing.csv \
  --n_clusters 3 \
  --random_state 42
```

Output lokal yang dihasilkan:

- `MLProject/mlruns/`
- `MLProject/Customer-Segmentation_clustered_basic.csv`
- `MLProject/pca_projection_basic.csv`

File output lokal tersebut di-ignore dari Git karena artefak resmi disimpan melalui workflow ke `github-artifacts/`.

## CI Training

Workflow training ada di `.github/workflows/mlflow-training.yml`.

Workflow ini berjalan saat:

- push ke `main` atau `develop` untuk perubahan di `MLProject/`, `data/`, atau workflow training
- pull request ke `main`
- jadwal mingguan
- manual run dari tab GitHub Actions

Yang dilakukan workflow:

- setup Python
- install dependency MLflow dan scikit-learn
- validasi dataset
- menjalankan `MLProject/modelling.py`
- menyimpan MLflow artifacts sebagai GitHub Actions artifact
- commit snapshot artefak ke `github-artifacts/mlflow-training/`

Artefak terbaru dapat dilihat di repository pada folder:

```text
github-artifacts/mlflow-training/
```

## Docker Image

Workflow Docker ada di `.github/workflows/mlflow-docker.yml`.

Alurnya:

1. menjalankan training
2. mengambil MLflow run terbaru
3. build image dengan:

```bash
mlflow models build-docker -m "runs:/<RUN_ID>/model" -n "tjutee/customer-segmentation:latest"
```

4. push image ke Docker Hub dengan tag:

- `latest`
- nomor run GitHub Actions, misalnya `12`

### Setup Docker Hub Paling Mudah

Gunakan Docker Hub access token, bukan password akun utama.

1. Buka Docker Hub.
2. Masuk ke `Account settings > Security`.
3. Buat access token baru.
4. Di GitHub repository, buka `Settings > Secrets and variables > Actions`.
5. Tambahkan repository secrets:

```text
DOCKERHUB_TOKEN = access token Docker Hub
```

Workflow sudah memakai username Docker Hub `tjutee`. Secret `DOCKER_PASSWORD` masih didukung sebagai fallback, tetapi `DOCKERHUB_TOKEN` lebih disarankan.

Setelah secrets ditambahkan, jalankan manual:

```text
GitHub > Actions > MLflow Training with Docker Build > Run workflow
```

Jika berhasil, image akan tersedia di:

```text
https://hub.docker.com/r/tjutee/customer-segmentation
```

## Menjalankan Image

Setelah image tersedia di Docker Hub:

```bash
docker pull tjutee/customer-segmentation:latest
```

MLflow model image biasanya berjalan sebagai model serving container. Contoh:

```bash
docker run --rm -p 8080:8080 tjutee/customer-segmentation:latest
```

Endpoint prediksi dapat dipanggil dari `http://localhost:8080/invocations`.

## Metrik

Training mencatat metrik berikut ke MLflow:

- inertia
- silhouette_score
- calinski_harabasz_score
- davies_bouldin_score

## Troubleshooting

**Docker workflow gagal di validasi credentials**

Tambahkan secret `DOCKERHUB_TOKEN` di GitHub Actions secrets. Error ini berarti workflow belum menerima token Docker Hub.

**Docker login gagal**

Pastikan token masih aktif, dibuat dari akun `tjutee`, dan memiliki izin read/write.

**Image tidak muncul di Docker Hub**

Cek step `Build and push Docker image using MLflow` di GitHub Actions. Jika login sukses tetapi push gagal, pastikan repository `customer-segmentation` bisa dibuat otomatis oleh akun tersebut atau buat manual lebih dulu di Docker Hub.

**Training gagal karena dataset tidak ditemukan**

Pastikan file berikut ada:

```text
MLProject/Customer-Segmentation_preprocessing.csv
```

**Artefak tidak berubah di repository**

Workflow hanya melakukan commit artefak jika training sukses dan event bukan pull request.

## Link

- Repository: https://github.com/tjutee/Workflow-CI
- GitHub Actions: https://github.com/tjutee/Workflow-CI/actions
- MLflow documentation: https://mlflow.org/docs/latest/

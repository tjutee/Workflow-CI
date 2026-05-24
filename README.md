# Workflow-CI: Customer Segmentation MLflow Project

MLflow Project dengan CI/CD Pipeline menggunakan GitHub Actions untuk automated model training.

## 📋 Project Structure

```
Workflow-CI/
├── .github/workflows/
│   ├── mlflow-training.yml      # Skilled Level (3 pts)
│   └── mlflow-docker.yml        # Advanced Level (4 pts)
├── MLProject/
│   ├── MLProject                # MLflow configuration
│   ├── conda.yaml               # Environment definition  
│   ├── modelling.py             # Training script
│   └── requirements.txt          # Python dependencies
├── Dockerfile                   # Docker configuration
└── data/                        # Dataset folder (create manually)
```

## 🚀 Setup dalam 3 Langkah

### 1️⃣ Persiapan Dataset

```bash
cd Workflow-CI
mkdir -p data
# Copy dataset dari folder preprocessing
cp "../Eksperimen_SML_Teja Endra Eng Tju/preprocessing/Customer-Segmentation_preprocessing.csv" data/
```

### 2️⃣ Push ke GitHub

```bash
git init
git add .
git commit -m "Initial MLflow CI/CD project"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 3️⃣ Setup Secrets (Untuk Advanced Level)

**GitHub Settings → Secrets and variables → Actions**

Tambahkan:
```
DOCKER_USERNAME = docker_hub_username
DOCKER_PASSWORD = docker_hub_access_token
```

---

## 📊 Workflow Levels

### ✅ Level: Skilled (3 pts)
**File:** `.github/workflows/mlflow-training.yml`

**Tahapan Workflow:**
1. Checkout code dari repository
2. Setup Python 3.10 environment
3. Install dependencies (mlflow, scikit-learn, pandas, numpy)
4. Verify dataset exists
5. Run MLflow Project Training dengan parameters
6. Log metrics & parameters ke MLflow
7. Save artifacts (clustered data, PCA projection)
8. **Upload artifacts ke GitHub** (retention 30 hari)
9. Create run summary

**Trigger:** Push, PR, Schedule (weekly), Manual dispatch

---

### ✅ Level: Advanced (4 pts)  
**File:** `.github/workflows/mlflow-docker.yml`

**Tahapan Workflow:**
1. Checkout code dari repository
2. Setup Python 3.10 environment
3. Install dependencies
4. Verify dataset exists
5. Run MLflow Project Training
6. Setup Docker Buildx untuk multi-platform builds
7. Login ke Docker Hub (menggunakan secrets)
8. **Build Docker image** dari Dockerfile
9. **Push image ke Docker Hub** dengan versioning:
   - Tag: `latest` (selalu latest)
   - Tag: `<github-run-number>` (untuk versioning)

**Trigger:** Push ke main, Manual dispatch

---

## 🔧 Cara Kerja Workflow

### Automatic Trigger
Workflow akan otomatis berjalan ketika:
- ✅ Push code ke branch `main`
- ✅ Create/update Pull Request ke `main`
- ✅ Schedule trigger (setiap Senin)
- ✅ Manual trigger dari GitHub Actions UI

### Manual Trigger
```
GitHub → Actions → MLflow CI Pipeline/Docker Build → Run workflow
```

### Monitoring
1. Go to repository `Actions` tab
2. See workflow running in real-time
3. Click workflow name untuk lihat details
4. Download artifacts setelah selesai

---

## 📦 Output & Artifacts

### Metrics yang di-log:
- Inertia
- Silhouette Score
- Calinski-Harabasz Score
- Davies-Bouldin Score

### Artifacts yang disimpan:
- `Customer-Segmentation_clustered.csv` (data dengan cluster labels)
- `pca_projection.csv` (2D PCA projection)
- `mlruns/` folder (MLflow tracking data)

### Download artifacts:
- **Skilled:** GitHub Actions → Completed Workflow → Artifacts (30 hari)
- **Advanced:** Docker Hub → Image layers (persistent)

---

## 🔑 MLflow Project Parameters

Ubah di file `MLProject/MLProject`:

```yaml
dataset_path:      Path ke dataset CSV
n_clusters:        Jumlah cluster untuk KMeans (default: 3)
random_state:      Random seed untuk reproducibility (default: 42)
```

Contoh custom parameters:
```bash
mlflow run ./MLProject \
  -P n_clusters=5 \
  -P random_state=123 \
  -P dataset_path="data/Customer-Segmentation_preprocessing.csv"
```

---

## 🧪 Test Lokal (Optional)

```bash
# Install dependencies
pip install mlflow scikit-learn pandas matplotlib numpy

# Run training locally
mlflow run ./MLProject

# View results
mlflow ui
# Akses: http://localhost:5000
```

---

## 🐳 Docker Hub Setup (Advanced Level)

### 1. Create Docker Hub Account
https://hub.docker.com → Sign up

### 2. Create Repository  
Dashboard → Repositories → Create → Name: `customer-segmentation`

### 3. Generate Access Token
Account Settings → Security → New Access Token

### 4. Add GitHub Secrets
Repo Settings → Secrets and variables → Actions:
- `DOCKER_USERNAME` = your_docker_username
- `DOCKER_PASSWORD` = dckr_pat_XXXXXXXXXXX

### 5. Trigger Workflow
Actions tab → MLflow Training with Docker Build → Run workflow

### 6. Verify
Docker Hub → Repositories → customer-segmentation → Tags

---

## ✅ Checklist Penyelesaian

- [ ] Repository dibuat di GitHub (Public visibility)
- [ ] Dataset di-copy ke folder `data/`
- [ ] Code di-push ke GitHub branch `main`
- [ ] GitHub Actions enabled dan workflow terdeteksi
- [ ] Test: Push code → Workflow berjalan → Download artifacts
- [ ] (Advanced) Docker Hub account created
- [ ] (Advanced) Repository created di Docker Hub
- [ ] (Advanced) Secrets ditambahkan: DOCKER_USERNAME & DOCKER_PASSWORD
- [ ] (Advanced) Test: Workflow berjalan → Image pushed to Docker Hub

---

## 🆘 Troubleshooting

| Error | Solusi |
|-------|--------|
| Dataset tidak ditemukan | Pastikan file ada di `data/Customer-Segmentation_preprocessing.csv` |
| Workflow tidak trigger | Check: Code di-push ke `main` branch, file path sesuai di workflow |
| Docker login gagal | Verify secrets DOCKER_USERNAME & DOCKER_PASSWORD |
| Artifacts tidak upload | Check disk space, verify permissions |

---

## 📚 Documentation

- [MLflow Docs](https://mlflow.org/docs/latest/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com/)

---

**Achievement Level:** ✅ Advanced (4 pts)

Example:
```bash
mlflow run ./MLProject -P n_clusters=5 -P random_state=123
```

## GitHub Actions

Workflows trigger automatically on:
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly schedule (Monday 00:00 UTC)
- Manual trigger via UI

## Docker Hub Setup (Optional)

For Advanced level with Docker images:

1. Create Docker Hub account and repository
2. Add GitHub secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
3. Trigger `mlflow-docker.yml` workflow

## Links

- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [GitHub Actions](https://docs.github.com/en/actions)

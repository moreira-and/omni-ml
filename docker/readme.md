❌ Antes
mlflow:
  image: ghcr.io/mlflow/mlflow:${MLFLOW_VERSION}

✅ Depois
mlflow:
  build:
    context: .
    dockerfile: Dockerfile
  image: mlflow-server:${MLFLOW_VERSION}

  ```bash
  
  docker compose up -d

  ```
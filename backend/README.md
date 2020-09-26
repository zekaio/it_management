# backend

后端

## 配置文件

修改配置文件`app/config/config.sample.py`并重命名为`config.py`

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
pip install gunicorn -i https://mirrors.cloud.tencent.com/pypi/simple
```

## Deploy

### Run in development mode

```bash
chmod +x run_dev.sh
./run_dev.sh
```

### Run in production mode

```bash
chmod +x run_prod.sh
./run_prod.sh
```

### Running with docker

```bash
# build the image
docker build -t backend .
# run the container on the host network
docker run -d --name backend --network="host" backend
```


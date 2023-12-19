# k8s-companion
Simple kubernetes companion

# python setup

```
python -m venv k8s-companion
source k8s-companion/bin/activate
```

# Nice GUI System

Based on https://nicegui.io ... a nice python gui framework

A simple project to navigate in current cluster

## config

create a venv

```bash
python3 -m venv $PWD/.k8s-companion
source $PWD/.k8s-companion/bin/activate
```

store a .config.yaml on base path

```yaml
gui:
  base_uri: http://localhost:8080
  login_uri: http://localhost:8080/login
  redirect_uri: http://localhost:8080/redirect
  secret: jCT6pBEZAQDSDQSDQQSDQd
  links:
  - name: Home page
    route: /
```

then run

```bash
pip3 install -r requirements.txt
python3 src/main.py
```

## docker

```
docker build -t <your-registry>/k8s-companion:1.0 .
```

```
docker run --rm --name k8s-companion -p8080:8080 <your-registry>/k8s-companion:1.0
```

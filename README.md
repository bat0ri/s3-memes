# s3-memes

### Install
``` Shell
cd docker-compose && docker-compose up -d
```
+ And go to ```http://localhost:5000/docs``` or testing on Postman for ```localhost:5000```

### Test (mock repository)
- go to ```/src``` and create ```venv```
```
python -m venv venv && . ./venv/bin/activate
```
- upgrade pip and install poetry
```
pip install poetry
```
- req install from ```pyproject.toml```
```
poetry install
```
- GO TEST
```
pytest -s
```

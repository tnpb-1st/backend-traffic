# Como rodar
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python3 main.py`

# Teste a API
`curl -G http://localhost:35000/get --data-urlencode "id=1"  (pode ser qualquer id entre 1 e 5. Olhar o cameras.json)`

# Teste cada arquivo
`python3 vehicles_detector.py`
`python3 video_downloader.py`

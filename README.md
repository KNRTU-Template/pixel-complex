# pixel-complex

## Установка и запуск

1. Сбор и запуск контейнера
   ```bash
   docker compose up -d --build
   ```
   
## Роуты

1. Коррекция изображения
   ```python
   import requests
   
   files = {'file': ('filename.tif', open('crop_0_1_0000.tif', 'rb'))}
   response = requests.post('http://localhost:8000/api', files=files)
   print(response.json())
   ```
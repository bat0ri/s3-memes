import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Доступные типы изображений для загрузки
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]

# 5 MB максимум для загрузки мемов
MAX_FILE_SIZE = 5 * 1024 * 1024


HOST = "0.0.0.0"
PORT = 8000

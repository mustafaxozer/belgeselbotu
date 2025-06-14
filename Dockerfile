# Base image: resmi python 3.10
FROM python:3.10-slim

# Çalışma dizini oluştur
WORKDIR /app

# Bağımlılık dosyasını kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# Botu çalıştır
CMD ["python", "main.py"]

# Usa imagem base leve com Python 3.11
FROM python:3.11-slim

# Instala dependências do sistema necessárias para WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    shared-mime-info \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    fonts-dejavu \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto local para o container
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do Render
EXPOSE 10000

# Comando para iniciar o app com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
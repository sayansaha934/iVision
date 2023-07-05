FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        git \
        ffmpeg \
        libsm6 \
        libxext6
COPY requirements.txt requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN python3.8 -m pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--forwarded-allow-ips=*"]
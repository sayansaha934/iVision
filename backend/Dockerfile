FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install git -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install build-essential -y
COPY requirements.txt requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install cmake
RUN git clone https://github.com/davisking/dlib.git && cd dlib && mkdir build && cd build && cmake .. && cmake --build . && cd .. && python3 setup.py install
RUN python3.8 -m pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--forwarded-allow-ips=*"]
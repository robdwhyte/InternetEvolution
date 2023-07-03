FROM python:3.10.6

RUN apt-get update -y && apt-get install -y \
    software-properties-common \
    build-essential \
    python3-dev \
    python3-pip \
    git

RUN apt-get update -y && apt-get install -y zsh tmux htop vim nano

RUN pip3 install -U pip
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /src
COPY . .

RUN pip install -r requirements.txt
RUN apt-get autoremove -y && apt-get autoclean -y

CMD python index.py
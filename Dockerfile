FROM debian:buster-slim
RUN apt update -y
RUN apt install -y libboost-python-dev libqt4-dev python-pip cmake python git python-numpy
RUN pip install --no-input pydub
RUN git clone https://github.com/ManaZeak/pymoodbar
WORKDIR /pymoodbar
RUN mkdir build
WORKDIR /pymoodbar/build
RUN cmake ../
RUN make
WORKDIR /pymoodbar
COPY moodbarGenerator.py .
CMD ["python3", "-u", "/pymoodbar/moodbarGenerator.py"]

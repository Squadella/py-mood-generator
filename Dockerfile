FROM debian:buster-slim
RUN apt update -y
RUN apt install -y libboost-python-dev libqt4-dev cmake python3 git python3-pip ffmpeg
RUN pip3 install --no-input pydub numpy
RUN git clone https://github.com/ManaZeak/pymoodbar
WORKDIR /pymoodbar
RUN mkdir build
WORKDIR /pymoodbar/build
RUN cmake ../
RUN make
WORKDIR /pymoodbar
COPY moodbarGenerator.py .
CMD ["python3", "-u", "/pymoodbar/moodbarGenerator.py"]

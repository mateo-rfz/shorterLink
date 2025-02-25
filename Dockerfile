FROM ubuntu 


RUN apt update && apt install python3 -y
RUN apt install python3-pip -y

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt --break-system-packages

CMD ["python3" , "app.py"]
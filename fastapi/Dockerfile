FROM python:3.7
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port" ," 8000"]
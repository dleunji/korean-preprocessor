FROM python:3.7
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8501
CMD ["streamlit" ,"run", "ui.py"]
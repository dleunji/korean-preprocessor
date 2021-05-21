FROM python:3.7
RUN apt-get update
RUN apt-get install -y supervisor
RUN apt-get install -y vim
RUN mkdir /app
WORKDIR /app
COPY fastapi/ .
COPY streamlit .
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /etc/supervisor/conf.d
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8000
EXPOSE 8501
CMD ["supervisord"]
#CMD ["/bin/bash"]
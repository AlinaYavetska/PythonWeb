FROM python:3.12

RUN adduser -q myuser 
USER myuser
ENV PATH="/home/myuser/.local/bin:${PATH}"
WORKDIR /app

COPY requirements/base.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src ./src
COPY ./static ./static
COPY ./templates ./templates
CMD ["uvicorn", "src.main:app",  "--host", "0.0.0.0" , "--port", "8000"]
FROM python:3.9.7

WORKDIR usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "8000"]
FROM python:3.10

WORKDIR .

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN python create_data.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
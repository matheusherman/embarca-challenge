import json
from datetime import datetime
import boto3
import requests
import pandas as pd
from io import BytesIO


BUCKET_NAME = "herman-embarca-challenge"

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")

def download_csv(csv_url):
    """Baixa o arquivo CSV da URL fornecida e retorna os dados em formato DataFrame."""
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        return pd.read_csv(BytesIO(response.content), encoding='ISO-8859-1', delimiter=';', quotechar='"')
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao baixar o CSV: {e}")

def upload_to_s3(data, bucket, s3_key):
    """Faz o upload dos dados para o S3."""
    try:
        s3.put_object(Bucket=bucket, Key=s3_key, Body=data)
    except Exception as e:
        raise Exception(f"Erro ao fazer upload para o S3: {e}")

def invoke_lambda_2(csv_string):
    """Chama a Lambda 2 passando o CSV como string"""
    payload = {
        "csv_data": csv_string
    }

    lambda_client.invoke(
        FunctionName="Lambda2",
        InvocationType="Event",
        Payload=json.dumps(payload)
    )

def lambda_handler(event, context):
    """Função principal para processar o evento"""
    csv_url = event.get("csv_url")
    if not csv_url:
        return {"status": "error", "message": "CSV URL não fornecido"}

    s3_key = f"input/inp_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv"

    try:
        # Baixar o CSV
        df = download_csv(csv_url)

        # Enviar o arquivo para o S3
        upload_to_s3(df.to_csv(index=False), BUCKET_NAME, s3_key)

        # Enviar para a lambda 2
        invoke_lambda_2(df)

        return {"status": "success", "s3_key": s3_key, "bucket": BUCKET_NAME}

    except Exception as e:
        return {"status": "error", "message": str(e)}

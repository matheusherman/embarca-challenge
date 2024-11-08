import pandas as pd
import json
import boto3
import pymysql
from io import StringIO

secrets_client = boto3.client('secretsmanager')


def get_db_credentials(secret_name):
    """Recupera as credenciais do banco de dados a partir do Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        return json.loads(secret)
    except Exception as e:
        raise Exception(f"Erro ao acessar o Secrets Manager: {str(e)}")

def connect_to_db(secret_name):
    """Conecta ao banco de dados MySQL usando as credenciais do Secrets Manager"""
    credentials = get_db_credentials(secret_name)
    try:
        rds_host = credentials["host"]
        db_user = credentials["username"]
        db_password = credentials["password"]
        db_name = credentials["dbname"]

        connection = pymysql.connect(
            host=rds_host,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")


def save_to_database(data):
    """Salva os dados no banco de dados MySQL"""
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            for entry in data:
                query = """
                INSERT INTO accidents (created_at, road_name, vehicle, number_deaths)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query,
                               (entry['created_at'], entry['road_name'], entry['vehicle'], entry['number_deaths']))

            connection.commit()
    except Exception as e:
        connection.rollback()
        raise Exception(f"Erro ao inserir no banco de dados: {str(e)}")
    finally:
        connection.close()


def calculate_deaths(df):
    """Calcula o número de mortes por tipo de veículo"""
    vehicles_of_interest = ['automovel', 'bicicleta', 'caminhao', 'moto', 'onibus']
    filtered_df = df[df['veiculo'].isin(vehicles_of_interest)]

    result = []
    for (vehicle, road_name), deaths in filtered_df.groupby(['veiculo', 'trecho'])['num_obitos'].sum().items():
        result.append({
            'created_at': pd.Timestamp.now(),
            'road_name': road_name,
            'vehicle': vehicle,
            'number_deaths': deaths
        })
    return result


def lambda_handler(event, context):
    """Função principal para processar o CSV recebido da Lambda 1 e  calcular o número de mortos por tipo de veículo"""

    csv_string = event.get("csv_data")

    if not csv_string:
        return {"status": "error", "message": "CSV data não fornecido"}

    try:
        # Carregar CSV na forma de DataFrame
        df = pd.read_csv(StringIO(csv_string), delimiter=",")

        # Calcular número de mortos por tipo de veículo
        deaths_data = calculate_deaths(df)

        # Salvar no banco de dados
        save_to_database(deaths_data)

        return {
            "status": "success",
            "deaths_data": deaths_data
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

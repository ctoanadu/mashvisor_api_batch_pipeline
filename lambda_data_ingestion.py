"""import library dependencies"""
import requests
import json
import boto3
from cities import cities
import os

headers = {
    "X-RapidAPI-Key": os.getenv('X_RapidAPI_Key'),
    "X-RapidAPI-Host": os.getenv('X_RapidAPI_Hos')
}

url = "https://mashvisor-api.p.rapidapi.com/data"

def fetch_data(url, query):
    try:
        response = requests.get(url, headers=headers, params=query)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Request failed with status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def lambda_handler(events,context):
    aws_access_key=os.getenv('aws_access_key')
    aws_secret_key=os.getenv('aws_secret_key')
    aws_region = 'eu-west-2' 
    
    session =boto3.Session(aws_access_key,aws_secret_key,  region_name=aws_region)
    s3_client=session.client('s3')
    
    final_result = []

    for city, zip_code in cities:
        query = {"state": "CA", "source": "airbnb", "city": city, "zip_code": zip_code}
        data = fetch_data(url, query)

        if data:
            final_result.append(data)

    if final_result:
        bucket_name='s3ingestionbucket'
        file_name='data.json'
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(final_result))

    return {
        'statusCode':200,
        'body':'Lambda function executed successfully'
    }




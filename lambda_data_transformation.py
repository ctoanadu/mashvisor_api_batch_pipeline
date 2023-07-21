"""import library dependencies"""
import io
import os
import boto3
import pandas as pd

def process_data(filepath):
    dataframe=pd.read_json(filepath)
    content_df = pd.json_normalize(dataframe['content'])
    content_df['city_id'] = content_df.reset_index().index + 1
    
    detailed_df = content_df.explode('detailed').reset_index(drop=True)
    detailed_df['detailed_id'] = detailed_df.reset_index().index + 1

    detailed_num_df = pd.json_normalize(detailed_df['detailed'])
    detailed_num_df.drop('neighborhood', axis=1)

    detailed_num_df['detailed_id'] = detailed_df['detailed_id']
    expanded_table = pd.merge(detailed_df, detailed_num_df, on='detailed_id')
    expanded_table=expanded_table.drop('neighborhood',axis=1)
    expanded_table=expanded_table.drop('detailed',axis=1)
    
    # Convert cells in 'beds' column to numeric (integer or float) and replace non-convertible values with NaN
    expanded_table['beds'] = pd.to_numeric(expanded_table['beds'], errors='coerce')

    # Convert 'beds' column to integer
    expanded_table['beds'] = expanded_table['beds'].astype('Int64')
    
    expanded_table=expanded_table.dropna()
    return expanded_table


def lambda_handler(event, context):
    aws_access_key=os.getenv('aws_access_key')
    aws_secret_key=os.getenv('aws_secret_key')
    aws_region = 'eu-west-2' 
    
    session =boto3.Session(aws_access_key,aws_secret_key, region_name=aws_region)
    s3_client=session.client('s3')
    
    #Extract Data from S3
    bucket_name='s3ingestionbucket'
    file_name='data.json'
    obj=s3_client.get_object(Bucket=bucket_name,Key=file_name)
    
    #Read data into a pandas dataframe
    df=process_data(obj['Body'])
    
    # Convert Dataframe to CSV format 
    csv_buffer=io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content=csv_buffer.getvalue()

    #Upload CSV file into S3 bucket
    bucket_name='s3processedbucket'
    file_name='data.csv'
    s3_client.put_object(Bucket=bucket_name,Key=file_name, Body=csv_content)

    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }

    
    
   

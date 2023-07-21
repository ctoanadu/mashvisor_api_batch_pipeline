import os
import boto3
import psycopg2

def lambda_handler(event, context):
    aws_acces_key=os.getenv('aws_access_key')
    aws_secret_key=os.getenv('aws_secret_key')
    aws_region='eu-west-2'
    session=boto3.Session(aws_acces_key,aws_secret_key,aws_region)
    
    
    #S3 configuration
    s3_client=session.client('s3')
    s3_bucket_name='s3processedbucket'
    file_name='data.csv'

    #Redshift configuration
    dbname=os.getenv('dbname')
    host=os.getenv('host')
    user=os.getenv('user')
    password=os.getenv('password')
    table_name='rental_data'
    connection=psycopg2.connect(dbname=dbname, host=host,port=5439,user=user,password=password)

    curs=connection.cursor()

    #Generate the Copy command
    copy_command=f""" COPY  {table_name} FROM 's3://{s3_bucket_name}/{file_name}'
    CREDENTIALS 'aws_access_key_id={aws_acces_key};aws_secret_access_key={aws_secret_key}' IGNOREHEADER 1 CSV;
    """

    curs.execute(copy_command)
    connection.commit()

    curs.close

    connection.close()

    return {
        'statuscode':200,
        'message':'Successfully imported CSV into redshift'
    }

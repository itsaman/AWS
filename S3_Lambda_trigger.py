import json
import boto3
import logging

#Logging basic info to Cloudwatch
logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    print('event', event)

    #Bucket name and object name from the event 
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        resposnse = s3.head_object(Bucket=bucket_name, Key=object_key)
        file_size_bytes = resposnse['ContentLength']
        file_size_mb = file_size_bytes / (1024 * 1024)

        #Checking the file size
        if file_size_mb < 100:
            logging.info('File size is smaller than 100MB')
            return {
                'statusCode': 200,
                'body': json.dumps('Hello from Lambda!')
            }
        else:
            logging.warning('File Size is more than 100 MB')
            return {
                'body': json.dumps('File greater than 100 MB')
            }

    #If File not get reterived
    except Exception as e:
        logging.error("Error in reteriving the file")
        return {
            'statusCode': 500,
            'body': f"Error retrieving file size: {str(e)}"
        }

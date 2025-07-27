import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'filesharing-thisside'

def lambda_handler(event, context):
    try:
        # Parse fileKey from POST body
        body = json.loads(event.get('body', '{}'))
        file_key = body.get('fileKey')
        
        if not file_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing fileKey field in request body.'}),
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            }
        
        # Extract filename from file_key to use in Content-Disposition header
        filename = file_key.split('/')[-1]
        
        # Generate presigned GET URL (valid for 10 minutes) with forced download header
        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_key,
                'ResponseContentDisposition': f'attachment; filename="{filename}"'
            },
            ExpiresIn=600
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'downloadUrl': presigned_url}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

# Example Python serverless function in api/hello.py

def handler(request, response):
    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello from Vercel Python serverless function!'
        }
    }
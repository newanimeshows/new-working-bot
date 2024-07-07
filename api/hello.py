# Example Python serverless function in api/hello.py
from bot import Bot


def handler(request, response):
    Bot().run()
    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello from Vercel Python serverless function!'
        }
    }

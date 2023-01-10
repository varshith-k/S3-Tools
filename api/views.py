import boto3
from django.conf import settings
from django.http import JsonResponse

from rest_framework.views import APIView


class CreateBucket(APIView):
    def post(self, request):
        # s3 = boto3.resource('s3')
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        s3.create_bucket(
            Bucket=bucket_name,
        )
        return JsonResponse({
            'message': 'Bucket created successfully',
            'status': '200'
        })


class DeleteBucket(APIView):
    def delete(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        try:
            s3.delete_bucket(
                Bucket=bucket_name,
            )
            return JsonResponse({
                'message': 'Bucket deleted successfully',
                'status': '200'
            })
        # Have to handle no such bucket exception and bucket not empty exception
        except Exception as e:
            return JsonResponse({
                'message': str(e),

            })


class CheckBucket(APIView):
    def post(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        try:
            s3.head_bucket(Bucket=bucket_name)
            return JsonResponse({
                'message': 'Bucket exists',
                'status': '200'
            })
        except:
            return JsonResponse({
                'message': 'Bucket does not exist',
                'status': '404'
            })


class ListBuckets(APIView):
    def get(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        buckets = s3.list_buckets()
        bucket_list = []
        for bucket in buckets['Buckets']:
            bucket_list.append(bucket['Name'])
        return JsonResponse({
            'message': 'Bucket list retrieved successfully',
            'status': '200',
            'buckets': bucket_list
        })


class UploadFile(APIView):
    def post(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        # file_name = request.data['file_name']
        file = request.data['file']
        s3.upload_fileobj(
            file,
            bucket_name,
            file.name,
        )
        return JsonResponse({
            'message': 'File uploaded successfully',
            'status': '200'
        })


class DeleteFile(APIView):
    def delete(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        file_name = request.data['file_name']
        s3.delete_object(
            Bucket=bucket_name,
            Key=file_name,
        )
        return JsonResponse({
            'message': 'File deleted successfully',
            'status': '200'
        })


class FileDownload(APIView):
    def post(self, request):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        # bucket_name = request.data['bucket_name']
        file_name = request.data['file_name']
        # file = request.data['file']
        bucket_name = request.data['bucket_name']
        destination = request.data['destination']
        s3.download_file(
            bucket_name,
            file_name,
            destination,
        )
        return JsonResponse({
            'message': 'File downloaded successfully',
            'status': '200'
        })


class ListFiles(APIView):
    def post(self, request):
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_REGION)
        bucket_name = request.data['bucket_name']
        # response = s3.list_objects_v2(Bucket=bucket_name)
        # files = []
        try:
            current_bucket = s3.Bucket(bucket_name)
            files = [file.key for file in current_bucket.objects.all()]
            # for content in response['Contents']:
            #     files.append(content['Key'])
            return JsonResponse({
                'message': 'File list retrieved successfully',
                'status': '200',
                'files': files
            })
        except Exception as e:
            return JsonResponse({
                'message': str(e),
                'status': '400', })

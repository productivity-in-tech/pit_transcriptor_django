from storages.backends.s3boto3 import S3Boto3Storage

# Create the ability to upload files to Amazon S3
class S3_Storage(S3Boto3Storage):
    location = 'pit-transcriptions'
    file_overwrite = False
    default_acl = 'public-read'

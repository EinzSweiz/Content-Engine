from dataclasses import dataclass
import boto3


@dataclass
class S3Client:
    aws_access_key_id: str
    aws_secret_access_key: str
    default_bucket_name: str
    region_name: str = 'eu-north-1'


    def __post_init__(self):
        self.client = self.create_s3_client()
    
    def create_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            
        )
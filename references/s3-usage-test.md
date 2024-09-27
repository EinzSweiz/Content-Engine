

```
python manage.py shell

```

```python

import s3
from cfehome.env import config

AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID', cast=str)
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY', cast=str)
AWS_BUCKET_NAME=config('AWS_BUCKET_NAME', cast=str)


client = s3.S3Client(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    default_bucket_name=AWS_BUCKET_NAME,
).client

paginator = client.get_paginator('list_objects_v2')
pag_gen = paginator.paginate(
    Bucket=AWS_BUCKET_NAME,
)
for page in pag_gen:
    print(page.get('Contents'))

```
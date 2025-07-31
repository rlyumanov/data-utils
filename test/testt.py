from s3 import S3Uploader
import os
from parquet_loader import ParquetUploader
import pandas as pd

from dotenv import load_dotenv

load_dotenv(override=True)

BUCKET_NAME = os.environ.get("POSTGRES_USER")
S3_ENDPOINT= os.environ.get("S3_ENDPOINT")
S3_ACCESS_KEY= os.environ.get("S3_ACCESS_KEY")
S3_SECRET_KEY= os.environ.get("S3_SECRET_KEY")

s3 = S3Uploader(S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT, default_bucket='dwhdata', debug=True)

# s3.upload_file('requirements.txt', 
#                'test/requirements.txt', 
#                skip_if_exists=True)

# s3.upload_directory('raw_data', 
#                     'revenue_uploader', 
#                     skip_if_exists=True)

df = pd.DataFrame({
    'id': [1,2,3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

parquet_uploader = ParquetUploader(s3)

# parquet_uploader.upload_dataframe(
#     df=df,
#     s3_key='test_data/employees.parquet',
#     skip_if_exists=True
# )

# Новые данные с upsert
new_data = pd.DataFrame({
    'id': [2, 4],  # id=2 обновляется, id=4 добавляется
    'name': ['Bob Updated', 'David'],
    'age': [31, 28]
})

# Выполняем upsert по колонке 'id'
result_df = parquet_uploader.upsert_dataframe(
    new_df=new_data,
    s3_key='test_data/employees.parquet',
    key_columns=['id']
)

print(result_df)
import os

from google.cloud import translate_v2 as translate
from google.cloud import storage

BUCKET_TRANSLATED = os.environ['BUCKET_TRANSLATED']


def read_gcs_object(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    if not blob:
        raise RuntimeError(f'{blob_name!r} does not exist in bucket {bucket_name!r}')
    content = blob.download_as_text()
    return content


def translate_text(text, target_language='en', source_language=None):
    translate_client = translate.Client()
    return translate_client.translate(text, target_language=target_language, 
        source_language=source_language)


def save_gcs_object(bucket_name, blob_name, content):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with blob.open('w') as file:
        bytes_writen = file.write(content)
    return bytes_writen


def main(event, context):
    bucket = event['bucket']
    file_name = event['name']
    
    print(f'Translating {file_name!r} in bucket {bucket!r}')

    text = read_gcs_object(bucket, file_name)
    text_translated = translate_text(text, target_language='pl')['translatedText']

    save_gcs_object(BUCKET_TRANSLATED, file_name, text_translated)
    
    print(f'Saving {file_name!r} in bucket {BUCKET_TRANSLATED!r}')

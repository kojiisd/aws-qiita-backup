import json
import sys
import os
import boto3
import botocore

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))

import requests

QIITA_BASE_URL = os.environ['QIITA_BASE_URL']
S3_BUCKET = os.environ['S3_BUCKET']
SETTING_FILE_NAME = os.environ['SETTING_FILE_NAME']
BACKUP_FILE_NAME = os.environ['BACKUP_FILE_NAME']

s3_client = boto3.client('s3')


def run(event, context):
    result = "No need to update."
    response_json = get_qiita_post(event['name'])
    org_topics = get_topics()

    if len(org_topics) > 0:
        target_array = extract_keys_as_array(response_json, 'url')
        org_array = extract_keys_as_array(org_topics, 'url')

        if not is_same_topics(org_array, target_array):
            put_data_to_s3(response_json, BACKUP_FILE_NAME)
            put_data_to_s3(extract_keys_as_json(response_json, 'url'), SETTING_FILE_NAME)
            result = "Update finished."

    return result

def get_qiita_post(name):
    page = 1

    result = []
    response_json = []
    is_loop = True

    while is_loop:
        url = QIITA_BASE_URL.format(user_id = name, page = page)
        result = requests.get(url)
        result_json = json.loads(result.text)
        response_json.extend(result_json)
        page+=1
        if len(result_json) == 0:
            is_loop = False

    return response_json

def is_same_topics(org_topics_array, target_array):
    is_same = True

    for org in org_topics_array:
        if org in target_array:
            target_array.remove(org)
        else:
            is_same = False
            break

    return is_same

def get_topics():
    json_file = SETTING_FILE_NAME + ".json"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=json_file)
        response_data = json.loads(response['Body'].read())
    except botocore.exceptions.ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            print("No Objects.")
            response_data = []
    

    return response_data

def extract_keys_as_array(target_json_array, key):
    result_array = []
    for target in target_json_array:
        result_array.append(target[key])
    
    return result_array

def extract_keys_as_json(target_json_array, key):
    result_array = []
    for target in target_json_array:
        result_array.append({
            key: target[key]
        })
    
    return result_array

def put_data_to_s3(contents, file_name):
    
    tmp_dir = "/tmp/"
    tmp_file = file_name + ".json"

    with open(tmp_dir + tmp_file, 'w') as file:
        file.write(json.dumps(contents, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))

    s3_client.upload_file(tmp_dir + tmp_file, S3_BUCKET, tmp_file)

    return True
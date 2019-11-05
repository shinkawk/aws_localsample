
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging
import boto3
from botocore.exceptions import ClientError

"""
Todo: 
1. aws --endpoint-url=http://localhost:4572 s3 mb s3://demo-bucket バケットの作成
2. aws --endpoint-url=http://localhost:4572 s3api put-bucket-acl --bucket demo-bucket --acl public-read バケットの公開設定（やらなくてもいけそう？
3. boto3をローカルS3設定に向けてやる（後はAWS上でやるのと全部同じ）
"""
s3 = boto3.resource('s3', endpoint_url='http://localhost:4572/',  aws_access_key_id="hogehoge",aws_secret_access_key="foobar" , region_name='ap-northeast-1' )


def put_object(dest_bucket_name, dest_object_name, src_data):
    """Add an object to an Amazon S3 bucket

    The src_data argument must be of type bytes or a string that references
    a file specification.

    :param dest_bucket_name: string
    :param dest_object_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: True if src_data was added to dest_bucket/dest_object, otherwise
    False
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            logging.error(e)
            return False
    else:
        logging.error('Type of ' + str(type(src_data)) +
                      ' for the argument \'src_data\' is not supported.')
        return False

    # Put the object
    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(e)
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True


def main():
    """Exercise put_object()"""

    # Assign these values before running the program
    test_bucket_name = 'demo-bucket'
    test_object_name = 'a_new_cat.jpg'
    filename = 'resource/cat.jpg'
    # Alternatively, specify object contents using bytes.
    # filename = b'This is the data to store in the S3 object.'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Put the object into the bucket
    success = put_object(test_bucket_name, test_object_name, filename)
    if success:
        logging.info(f'Added {test_object_name} to {test_bucket_name}')

    # Get the same object we just uploaded
    s3.download_file(test_bucket_name, test_object_name, "resource/new_cat_is_here.jpg")


if __name__ == '__main__':
    main()

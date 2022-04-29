import boto3


class AWSBase(object):
    @property
    def aws_settings(self):
        return {
            'aws_access_key_id': self.settings.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': self.settings.get('AWS_SECRET_ACCESS_KEY'),
            'region_name': self.settings.get('AWS_REGION')
        }

    def get_aws_lambda(self):
        return boto3.client('lambda', **self.aws_settings)

    def get_aws_s3(self):
        return boto3.resource('s3', **self.aws_settings)

    def get_aws_sqs(self):
        return boto3.resource('sqs', **self.aws_settings)

"""Private local and S3-compatible object storage for CMS uploads."""

import os
import re
from pathlib import Path


class StorageConfigurationError(RuntimeError):
    pass


def _storage_key_ok(key):
    return bool(re.fullmatch(r'[0-9a-f-]{36}', key))


class MediaStorage:
    def __init__(self, backend, directory, *, bucket='', region='', endpoint='',
                 access_key='', secret_key=''):
        self.backend = backend
        self.directory = Path(directory).expanduser().resolve()
        self.bucket = bucket
        self.region = region or None
        self.endpoint = endpoint or None
        self.access_key = access_key or None
        self.secret_key = secret_key or None
        if backend not in {'local', 's3'}:
            raise StorageConfigurationError('MEDIA_STORAGE_BACKEND must be local or s3.')

    def _s3(self):
        if not self.bucket:
            raise StorageConfigurationError(
                'Configure MEDIA_S3_BUCKET before using object storage.'
            )
        try:
            import boto3
        except ImportError as error:
            raise StorageConfigurationError(
                'Install the project dependencies to enable S3-compatible storage.'
            ) from error
        options = {'service_name': 's3', 'region_name': self.region}
        if self.endpoint:
            options['endpoint_url'] = self.endpoint
        if self.access_key and self.secret_key:
            options['aws_access_key_id'] = self.access_key
            options['aws_secret_access_key'] = self.secret_key
        return boto3.client(**options)

    def put(self, key, data, mime_type):
        if not _storage_key_ok(key):
            raise ValueError('Invalid generated storage key.')
        if self.backend == 's3':
            self._s3().put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType=mime_type,
                ContentDisposition='attachment',
            )
            return
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        target = (self.directory / key).resolve()
        if target.parent != self.directory:
            raise ValueError('Storage key escapes the media directory.')
        with target.open('xb') as stream:
            stream.write(data)
        target.chmod(0o600)

    def get(self, key):
        if not _storage_key_ok(key):
            raise ValueError('Invalid storage key.')
        if self.backend == 's3':
            result = self._s3().get_object(Bucket=self.bucket, Key=key)
            return result['Body'].read()
        target = (self.directory / key).resolve()
        if target.parent != self.directory:
            raise ValueError('Storage key escapes the media directory.')
        return target.read_bytes()

    def delete(self, key):
        if not _storage_key_ok(key):
            raise ValueError('Invalid storage key.')
        if self.backend == 's3':
            self._s3().delete_object(Bucket=self.bucket, Key=key)
            return
        target = (self.directory / key).resolve()
        if target.parent != self.directory:
            raise ValueError('Storage key escapes the media directory.')
        target.unlink(missing_ok=True)


def storage_from_environment(vardir):
    env = os.environ.get('YHTTP_ENV', 'development')
    backend = os.environ.get(
        'MEDIA_STORAGE_BACKEND', 'local' if env == 'development' else 's3',
    ).lower()
    return MediaStorage(
        backend=backend,
        directory=os.environ.get('MEDIA_STORAGE_DIR', os.path.join(vardir, 'media-private')),
        bucket=os.environ.get('MEDIA_S3_BUCKET', ''),
        region=os.environ.get('MEDIA_S3_REGION', ''),
        endpoint=os.environ.get('MEDIA_S3_ENDPOINT', ''),
        access_key=os.environ.get('MEDIA_S3_ACCESS_KEY_ID', ''),
        secret_key=os.environ.get('MEDIA_S3_SECRET_ACCESS_KEY', ''),
    )

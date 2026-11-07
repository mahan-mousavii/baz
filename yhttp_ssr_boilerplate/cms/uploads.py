"""Strict allowlist and content validation for image and resource uploads."""

from pathlib import PurePath
import re
import zipfile


MAX_UPLOAD_BYTES = 10 * 1024 * 1024
IMAGE_TYPES = {
    '.jpg': ('image/jpeg', 'JPEG'),
    '.jpeg': ('image/jpeg', 'JPEG'),
    '.png': ('image/png', 'PNG'),
    '.webp': ('image/webp', 'WEBP'),
}
RESOURCE_TYPES = {
    '.pdf': ('application/pdf', 'PDF'),
    '.docx': (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'DOCX',
    ),
    '.xlsx': (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'XLSX',
    ),
    '.csv': ('text/csv', 'CSV'),
}


class InvalidUpload(ValueError):
    pass


def _safe_filename(value):
    name = PurePath((value or '').replace('\\', '/')).name
    name = re.sub(r'[^A-Za-z0-9._ -]', '_', name).strip(' .')
    if not name or name in {'.', '..'}:
        raise InvalidUpload('Choose a file with a valid filename.')
    return name[:255]


def inspect_upload(field):
    filename = _safe_filename(field.filename)
    extension = PurePath(filename).suffix.lower()
    allowed = IMAGE_TYPES | RESOURCE_TYPES
    if extension not in allowed:
        raise InvalidUpload('Allowed files: JPG, PNG, WEBP, PDF, DOCX, XLSX, and CSV.')

    data = field.file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise InvalidUpload('The selected file is empty.')
    if len(data) > MAX_UPLOAD_BYTES:
        raise InvalidUpload('Files must be 10 MB or smaller.')

    mime_type, file_type = allowed[extension]
    width = height = None
    if extension in IMAGE_TYPES:
        try:
            from PIL import Image, UnidentifiedImageError
            from PIL.Image import DecompressionBombError, DecompressionBombWarning
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter('error', DecompressionBombWarning)
                image = Image.open(__import__('io').BytesIO(data))
                if image.format != file_type:
                    raise InvalidUpload('The image content does not match its file extension.')
                width, height = image.size
                if width * height > 30_000_000:
                    raise InvalidUpload('Images must be 30 megapixels or smaller.')
                image.verify()
        except ImportError as error:
            raise InvalidUpload(
                'Image validation is unavailable; install the project dependencies.'
            ) from error
        except InvalidUpload:
            raise
        except (OSError, ValueError, DecompressionBombError, DecompressionBombWarning,
                UnidentifiedImageError) as error:
            raise InvalidUpload('The uploaded file is not a valid supported image.') from error
    elif extension == '.pdf':
        if not data.startswith(b'%PDF-'):
            raise InvalidUpload('The uploaded file is not a valid PDF.')
    elif extension in {'.docx', '.xlsx'}:
        required_member = (
            'word/document.xml' if extension == '.docx' else 'xl/workbook.xml'
        )
        try:
            with zipfile.ZipFile(__import__('io').BytesIO(data)) as archive:
                names = set(archive.namelist())
                if '[Content_Types].xml' not in names or required_member not in names:
                    raise InvalidUpload('The uploaded Office file has invalid contents.')
        except (OSError, zipfile.BadZipFile) as error:
            raise InvalidUpload('The uploaded file is not a valid Office document.') from error
    else:
        try:
            decoded = data.decode('utf-8-sig')
        except UnicodeDecodeError as error:
            raise InvalidUpload('CSV files must use UTF-8 text encoding.') from error
        if '\x00' in decoded:
            raise InvalidUpload('The CSV file contains invalid binary data.')

    return {
        'filename': filename,
        'mime_type': mime_type,
        'extension': extension,
        'data': data,
        'width': width,
        'height': height,
    }

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageBytesSizeValidator:
    def __init__(self, max_image_size_bytes):
        self.max_image_size = max_image_size_bytes

    def __call__(self, image):
        if image.size > self.max_image_size:
            raise ValidationError(_(f'File size exceeded (currently {image.size}).'))


class ImageDimensionValidator:
    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height

    def __call__(self, image_object):
        try:
            from PIL import Image

            image = Image.open(image_object.file)
        except (ImportError, OSError):
            raise ValidationError(_('Please upload a valid image.'))
        else:
            if image.width > self.max_width or image.height > self.max_height:
                raise ValidationError(
                    _(
                        'Image dimensions exceeded '
                        f'(currently {image.width} * {image.height}).',
                    ),
                )


class ImageContentTypeValidator:
    def __init__(self, allowed_types: tuple[str, ...]):
        self.allowed_types = allowed_types

    def __call__(self, image_object):
        try:
            from PIL import Image

            image = Image.open(image_object.file)
        except (ImportError, OSError):
            raise ValidationError(_('Please upload a valid image.'))
        else:
            if image.format.lower() not in self.allowed_types:
                raise ValidationError(
                    _(f'Type disallowed (currently {image.format}).'),
                )

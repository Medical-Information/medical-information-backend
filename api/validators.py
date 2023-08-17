from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageBytesSizeValidator:
    def __init__(self, image_size_bytes=settings.BASE64_IMAGE_MAX_SIZE_BYTES):
        """Initialize image max size in bytes."""
        self.max_image_size = image_size_bytes

    def __call__(self, image):
        if image.size > self.max_image_size:
            raise ValidationError(_(f'File size exceeded (currently {image.size}).'))


class ImageDimensionValidator:
    def __init__(
        self,
        width=settings.BASE64_AVATAR_MAX_WIDTH,
        height=settings.BASE64_AVATAR_MAX_HEIGHT,
    ):
        """Initialize image max size in bytes."""
        self.width = width
        self.height = height

    def __call__(self, image_object):
        try:
            from PIL import Image

            image = Image.open(image_object.file)
        except (ImportError, OSError):
            raise ValidationError(_('Please upload a valid image.'))
        else:
            if image.width > self.width or image.height > self.height:
                raise ValidationError(
                    _(
                        'Image dimensions exceeded '
                        f'(currently {image.width} * {image.height}).',
                    ),
                )


class ImageContentTypeValidator:
    def __init__(
        self,
        allowed_types: tuple[str] = settings.ALLOWED_B64ENCODED_IMAGE_FORMATS,
    ):
        """Initialize image max size in bytes."""
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

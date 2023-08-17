import pytest
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.validators import (
    ImageBytesSizeValidator,
    ImageContentTypeValidator,
    ImageDimensionValidator,
)


def get_bytes_length(file_string):
    return int(len(file_string) * 3 / 4 - file_string[-2:].count('='))


class ImageSizeRestrictedSerializer(serializers.Serializer):
    image = Base64ImageField(validators=(ImageBytesSizeValidator(5000),))


class ImageDimensionsRestrictedSerializer(serializers.Serializer):
    image = Base64ImageField(validators=(ImageDimensionValidator(200, 200),))


class ImageTypeRestrictedSerializer(serializers.Serializer):
    image = Base64ImageField(validators=(ImageContentTypeValidator(),))


def test_image_size_exceeded(settings):
    with open(
        settings.BASE_DIR
        / 'tests'
        / 'fixtures'
        / 'snapshots'
        / 'image_snapshot_jpg_5203_bytes.txt',
    ) as source:
        image_b64string = source.read()

    serializer = ImageSizeRestrictedSerializer(data={'image': image_b64string})

    assert serializer.is_valid() is False

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.data is not None
    assert serializer.data['image'] is not None
    assert serializer.validated_data == {}


def test_image_size_not_exceeded(settings):
    with open(
        settings.BASE_DIR
        / 'tests'
        / 'fixtures'
        / 'snapshots'
        / 'image_snapshot_jpg_4233_bytes.txt',
    ) as source:
        image_b64string = source.read()

    serializer = ImageSizeRestrictedSerializer(data={'image': image_b64string})

    assert serializer.is_valid(raise_exception=True) is True
    assert serializer.validated_data is not None
    assert serializer.validated_data['image'] is not None
    assert serializer.validated_data['image'].size == get_bytes_length(image_b64string)


def test_image_dimensions_exceeded(settings):
    with open(
        settings.BASE_DIR
        / 'tests'
        / 'fixtures'
        / 'snapshots'
        / 'image_snapshot_jpg_225_225.txt',
    ) as source:
        image_b64string = source.read()

    serializer = ImageDimensionsRestrictedSerializer(data={'image': image_b64string})

    assert serializer.is_valid() is False

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.data is not None
    assert serializer.data['image'] is not None
    assert serializer.validated_data == {}


def test_image_dimensions_not_exceeded(settings):
    with open(
        settings.BASE_DIR
        / 'tests'
        / 'fixtures'
        / 'snapshots'
        / 'image_snapshot_jpeg_100_100.txt',
    ) as source:
        image_b64string = source.read()

    serializer = ImageDimensionsRestrictedSerializer(data={'image': image_b64string})

    assert serializer.is_valid() is True
    assert serializer.data is not None
    assert serializer.validated_data['image'].size == get_bytes_length(image_b64string)


def test_image_type_incorrect(settings):
    with open(
        settings.BASE_DIR
        / 'tests'
        / 'fixtures'
        / 'snapshots'
        / 'image_snapshot_gif.txt',
    ) as source:
        image_b64string = source.read()

    serializer = ImageTypeRestrictedSerializer(data={'image': image_b64string})

    assert serializer.is_valid() is False

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    assert serializer.data is not None
    assert serializer.data['image'] is not None
    assert serializer.validated_data == {}

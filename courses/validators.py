import re

from rest_framework.exceptions import ValidationError


def validate_url(value):
    if not re.match(r'^https://www\.youtube\.com/', value):
        raise ValidationError("Can't use another url addresses except - YouTube")

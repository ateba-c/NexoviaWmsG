from django.core.exceptions import ValidationError


def validate_barcode(value: str) -> str:
    if not value or len(value.strip()) < 4:
        raise ValidationError("Barcode must contain at least 4 characters.")
    return value


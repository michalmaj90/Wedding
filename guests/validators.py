from django.core.exceptions import ValidationError

def validate_email(email):
    if "@" not in email or email[-3:] != "com":
        raise ValidationError("Nieprawidłowy adres email")

def validate_number(number):
    if 15 < len(str(number)) < 9:
        raise ValidationError("Nieprawidłowa długość numeru")

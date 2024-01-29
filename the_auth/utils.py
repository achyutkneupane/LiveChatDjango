from rest_framework import serializers


def required_validators(**required_fields):
    validators = dict()
    for field, value in required_fields.items():
        if not value:
            validators[field] = 'This field is required'

    if validators:
        raise serializers.ValidationError(validators)

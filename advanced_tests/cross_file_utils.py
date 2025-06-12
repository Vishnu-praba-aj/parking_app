def validate_age(age):
    if age < 0:
        raise ValueError("Age must be non-negative")
    return age
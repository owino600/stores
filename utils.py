#!/usr/bin/python3
def validate_positive(value: int):
    if value <= 0:
        raise ValueError("Value must be positive")
    return value
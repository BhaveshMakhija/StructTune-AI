import json

def is_valid_json(text):
    """
    Check if the response string is a valid JSON.
    Returns 1.0 for valid, 0.0 for invalid.
    """
    try:
        json.loads(text)
        return 1.0
    except (ValueError, TypeError):
        return 0.0

def exact_match(prediction, target):
    """
    Check if the prediction exactly matches the target string (ignoring simple whitespace).
    Returns 1.0 for match, 0.0 otherwise.
    """
    return 1.0 if prediction.strip() == target.strip() else 0.0

if __name__ == "__main__":
    # Test valid
    print(f"Valid result (expected 1.0): {is_valid_json('{\"name\": \"John\"}')}")
    # Test invalid
    print(f"Invalid result (expected 0.0): {is_valid_json('invalid json text')}")

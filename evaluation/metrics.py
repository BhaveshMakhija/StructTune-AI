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

def field_accuracy(prediction, target):
    """
    Calculate accuracy at the JSON field level.
    Compares keys and values in both objects.
    Returns 1.0 if all fields match, otherwise (matching fields / total fields).
    """
    try:
        pred_obj = json.loads(prediction)
        tgt_obj = json.loads(target)
    except:
        return 0.0
    
    if not isinstance(pred_obj, dict) or not isinstance(tgt_obj, dict):
        return 1.0 if pred_obj == tgt_obj else 0.0
    
    all_keys = set(pred_obj.keys()).union(set(tgt_obj.keys()))
    if not all_keys:
        return 1.0
    
    matches = 0
    for key in all_keys:
        if key in pred_obj and key in tgt_obj and pred_obj[key] == tgt_obj[key]:
            matches += 1
            
    return matches / len(all_keys)

if __name__ == "__main__":
    # Test valid
    test_json = '{"name": "John"}'
    print(f"Valid result (expected 1.0): {is_valid_json(test_json)}")
    # Test invalid
    print(f"Invalid result (expected 0.0): {is_valid_json('invalid json text')}")


import os
import re

def normalize_dart_code(code):
    return code.strip()

def sanitize_filename(name, max_length=50):
    # Replace non-alphanumeric characters with underscores
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return cleaned[:max_length]

def save_flutter_feature(*, project, feature_name, screen_code, test_code):
    base_path = f"../projects/{project}"
    os.makedirs(f"{base_path}/lib/components", exist_ok=True)
    os.makedirs(f"{base_path}/test", exist_ok=True)

    safe_name = sanitize_filename(feature_name)
    screen_file = f"{base_path}/lib/components/{safe_name}.dart"
    test_file = f"{base_path}/test/{safe_name}_test.dart"

    with open(screen_file, "w", encoding="utf-8") as f:
        f.write(normalize_dart_code(screen_code))

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(normalize_dart_code(test_code))

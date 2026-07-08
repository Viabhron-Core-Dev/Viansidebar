import re

def replace_alert_dialog(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # We need to replace AlertDialog with a custom Box overlay
    # This is a bit tricky with regex, so we'll do string replacements.
    # We will just write a custom script for each since they are slightly different.


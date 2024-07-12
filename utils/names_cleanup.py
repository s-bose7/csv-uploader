import re
import json

def org_cleaner(text):
    if not isinstance(text, str):
        # Return the original text if it's not a string
        return text

    path = 'text_correction.json'
    with open(path, 'r') as f:
        abbr_dict = json.load(f)

    words = text.split()
    l = len(words)
    for idx in range(l-1, -1, -1):
        wd = words[idx]
        full_form = abbr_dict.get(wd, None)
        if full_form:
            words[idx] = full_form
        else:
            break

    clean_text = " ".join(words)

    if re.search("(high|middle)$", clean_text.lower()):
        clean_text += " School"

    additional_dict = {
        'Parent Teacher Organization': 'PTO',
        'Parent-Teacher Organization': 'PTO',
        'Parent Teacher Association': 'PTA',
        'Parent-Teacher Association': 'PTA',
        'Ptsa': 'PTSA',
        'Sr.': 'Senior',
        'Sr': 'Senior',
        'Pcs': 'Public Charter School',
        'Chtr': 'Charter',
        'Jr': 'Junior'
    }

    for phrase, abbr in additional_dict.items():
        clean_text = clean_text.replace(phrase, abbr)

    return clean_text

    
def remove_special_chr(text):
    if not isinstance(text, str):
        # Return the original text if it's not a string
        return text

    clean_text = text.replace("?", "").replace("@", "").replace("#", "")
    clean_text = " ".join(clean_text.split())
    return clean_text
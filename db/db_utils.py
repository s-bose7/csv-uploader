import re


def generate_slug(organization_name:str, address: str)->str:
    combined = organization_name + address
    slug = re.sub(r'[^a-z0-9]+', '-', combined.replace(" ", "").lower()).strip('-')
    return slug

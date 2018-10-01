import re


def camel_case_to_url(name):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name)
    return "-".join([m.group(0).lower() for m in matches])


def camel_case_to_underscore(name):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name)
    return "_".join([m.group(0).lower() for m in matches])


def underscore_to_dash(name: str):
    return name.replace('_', '-')

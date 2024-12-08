from flask import Flask, request
from tinydb import TinyDB
import re

app = Flask(__name__)
db = TinyDB('templates.json')

types = {
    'email': re.compile(r'^\S+@\S+\.\S+$'),
    'phone': re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$'),
    'date': re.compile(r'^(\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})$')
}


def parse_query(query: str) -> dict[str, str]:
    query_str = query.split('&')
    pairs = [tuple(s.split('=')) for s in query_str]
    return {field: value for field, value in pairs}


def get_type(value: str) -> str:
    for tp in ['date', 'phone', 'email']:
        if types[tp].match(value):
            return tp
    return 'text'


def check_template(template: dict[str, str], query: dict[str, str]) -> int | None:
    diff = len(template)
    for field, value in query.items():
        if field not in template:
            return None
        if template[field] != 'text' and template[field] != get_type(value):
            return None
        diff -= 1
    return diff


@app.post('/get_form')
def get_form():
    try:
        cur_template = None
        cur_diff = None
        query = parse_query(request.data.decode())
        for template in db:
            diff = check_template(template, query)
            if diff is None:
                continue
            print(template['name'], diff)
            if cur_diff is None or diff < cur_diff:
                cur_diff = diff
                cur_template = template
        if cur_template is not None:
            return cur_template['name']
        else:
            return {field: get_type(value) for field, value in query.items()}
    except RuntimeError:
        return 'Internal server error', 500
    except ValueError:
        return 'Invalid query', 400

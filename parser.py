import requests

def parse_link(link):
    try:
        html = requests.get(link).text
        result = True
    except Exception as a:
        result = a
        html = None
    response = {'html': html, 'result': result, "link": link}
    return response
from application import parsing
url = 'https://spb.hh.ru/search/vacancy'
params = {
    'area': (1, 2),
    'text': 'python',
    'page': 0
}

if __name__ == '__main__':
    parsed_db = []
    filename, path = 'db.json', 'db/'
    parsing.parsed_hh(url, params, parsed_db)
    parsing.load_json(path, filename, parsed_db)
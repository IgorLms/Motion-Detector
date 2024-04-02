import json


def get_json(path_json: str) -> json:
    """
    Чтение JSON файла
    :path_json путь до json файла
    :return данные с json файла
    """

    return json.load(open(path_json))


def set_json(data_json, name: str, data: str, path_json: str) -> json:
    """
    Запись в JSON файл
    :data_json данные с json файла
    :name имя ключа
    :data значение
    :path_json путь до json файла
    """

    data_json.update({name: data, })
    json.dump(data_json, open(path_json, 'w'), sort_keys=True, indent=2, ensure_ascii=False)

    return data_json

import json


def get_json(path_json: str) -> dict:
    """
    Чтение JSON файла
    :path_json путь до json файла
    :return данные с json файла
    """

    with open(path_json) as f:
        data = json.load(f)

    return data


def set_json(data_json: dict, name: str, data: str, path_json: str) -> dict:
    """
    Запись в JSON файл
    :data_json данные с json файла
    :name имя ключа
    :data значение
    :path_json путь до json файла
    """

    data_json.update({name: data, })
    with open(path_json, 'w') as f:
        json.dump(data_json, f, sort_keys=True, indent=2, ensure_ascii=False)

    return data_json

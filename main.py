import csv
from datetime import datetime
import math
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator
from prettytable import PrettyTable
from unittest import TestCase


formatted_russian_columns = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_description": "Оклад",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии",
}

filter_criterias = [
    "Название",
    "Описание",
    "Навыки",
    "Опыт работы",
    "Премиум-вакансия",
    "Компания",
    "Оклад",
    "Название региона",
    "Дата публикации вакансии",
    "Идентификатор валюты оклада"
]

job_experience = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

job_experience_priority = {
    "Нет опыта": 0,
    "От 1 года до 3 лет": 1,
    "От 3 до 6 лет": 2,
    "Более 6 лет": 3
}

currencies = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
}

currencies_exchanges = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}

class DataSet:
    """
    Класс для преобразования данных CSV-файла в список обьектов Vacancy

    Attributes:
        file_name (str): Имя CSV-файла
        vacancies_objects (object): Список вакансий-объектов
    """
    def __init__(self, file_name):
        """
        Инициализирует внутреннее состояние обьекта в соответствии с переданным именем файла
        Args:
            file_name (str): Имя CSV-файла
        """
        self.__file_name = file_name
        self.__vacancies_objects = DataSet.csv_reader(file_name)

    @property
    def file_name(self):
        """
        Геттер для получения имени файла

        Returns:
            str: Имя CSV-файла
        """
        return self.__file_name

    @property
    def vacancies_objects(self):
        """
        Геттер для получения списка вакансий-обьектов
        Returns:
            list: Список вакансий-объектов
        """
        return self.__vacancies_objects

    @staticmethod
    def get_filtered_vacancy_info(input, columns):
        """
        Очищает поданную на вход информацию о вакансии от HTML-тегов
        Args:
            input (list) - Информация о вакансии, которую необходимо очистить от HTML-тегов
            columns (list) - Названия столбцов, необходимые для правильной обработки
        Returns:
            list: Список очищенных от HTML-тегов строк
        """
        return [DataSet.remove_html(input[i], columns[i]) for i in range(len(input))]

    @staticmethod
    def remove_html(input, column_name):
        """
        Очищает поданную на вход строку от HTML тегов
        Args:
            input (str): Строка, которую нужно очистить от тегов
            column_name (str): Название столбца, необходимое для правильной обработки строки
        Returns:
            str: Очищенная от HTML-тегов строка

        >>> DataSet.remove_html('<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>', "Test")
        'Обязанности: компьютерное моделирование деталей настройки параметров обработки деталей установка материала и съем готовой детали контроль и измерение деталей на соответствие размеров техническому заданию Требования: Образование Средне-специальное Умение пользоваться инструментом Умение читать чертежи Технический склад ума Примечание: Питание предоставляется. Возможно проживание'

        """
        if column_name == "key_skills":
            return "\n".join(re.sub(r"<[^>]+>", "", input).splitlines())
        else:
            return " ".join(re.sub(r"<[^>]+>", "", input).split())

    @staticmethod
    def get_formatted_number(number_str):
        """
        Разделяет поданное на вход число по разрядам

        Args:
            number_str (str or float or int): число с плавающей точкой

        Returns:
            str: Разделенное по разрядам число

        >> DataSet.get_formatted_number("1500003")
        '1 500 003'

        >>> DataSet.get_formatted_number("1000")
        '1 000'

        >>> DataSet.get_formatted_number("13849204839")
        '13 849 204 839'

        >>> DataSet.get_formatted_number("0")
        '0'

        >>> DataSet.get_formatted_number(150)
        '150'

        >>> DataSet.get_formatted_number(123012321)
        '123 012 321'

        >>> DataSet.get_formatted_number(150.3)
        '150'

        >>> DataSet.get_formatted_number(12839.3291839)
        '12 839'
        """
        return '{0:,}'.format(int(number_str)).replace(',', ' ')

    @staticmethod
    def formatter(row):
        """
        Форматирует поданную на вход информацию о вакансии

        Args:
            row (dict): Словарь с информацией о вакансии, которую необходимо обработать

        Returns:
            dict: Обработанная информация о вакансии

        """
        formatted_vacancy_data = dict()
        for key, value in formatted_russian_columns.items():
            if key == "salary_description":
                data = f"{DataSet.get_formatted_number(float(row['salary_from']))} - {DataSet.get_formatted_number(float(row['salary_to']))} ({currencies[row['salary_currency']]}) ({'Без вычета налогов' if row['salary_gross'] == 'True' else 'С вычетом налогов'})"
                formatted_vacancy_data.update({value: data})
            elif key == "experience_id":
                formatted_vacancy_data.update({value: job_experience[row[key]]})
            elif key == "premium":
                formatted_vacancy_data.update({value: "Да" if row[key] == "True" else "Нет"})
            else:
                formatted_vacancy_data.update({value: row[key]})
        return formatted_vacancy_data

    @staticmethod
    def csv_reader(file_name):
        """
        Считывает данные из CSV-файла
        :param file_name: Имя CSV-файла
        :return: Считанные из CSV-файла данные
        """
        reader = csv.reader(open(file_name, encoding="utf_8_sig"))
        columns = []
        try:
            columns = next(reader)
        except StopIteration:
            print("Пустой файл")
            exit()
        data = [DataSet.formatter(dict(zip(columns, DataSet.get_filtered_vacancy_info(row, columns)))) for row in reader if len(row) == len(columns) and row.count("") == 0]
        if len(data) == 0:
            print("Нет данных")
            exit()
        return data


class InputConnect:
    """
    Класс для хранения введенной пользователем информации и результата ее обработки
    """
    def __init__(self):
        """
        Инициализирует внутреннее состояние объекта в соответствии с переданными параметрами
        """
        self.__input = InputConnect.get_user_input()
        self.__parsed_input = self.get_parsed_input(self.__input)

    @property
    def parsed_input(self):
        """
        Getter для получения обработанной информации, которую ввел пользователь
        :return:
        """
        return self.__parsed_input

    @staticmethod
    def get_user_input():
        """
        Считывает информацию, введенную в консоль пользователем
        :return: Считанная информация, введенная пользователем
        """
        rows = [
            "Введите название файла",
            "Введите параметр фильтрации",
            "Введите параметр сортировки",
            "Обратный порядок сортировки (Да / Нет)",
            "Введите диапазон вывода",
            "Введите требуемые столбцы"
        ]
        return [input(f"{rows[i]}: ") for i in range(6)]

    @staticmethod
    def get_parsed_input(raw_input):
        """
        Обрабатывает введенную в консоль пользователем информацию
        :param raw_input: Введенные пользователем "грязные" данные
        :return: Обработанные данные
        """
        parsed_input = {
            "Название файла": raw_input[0],
            "Параметр фильтрации": InputConnect.parse_filter_criteria(raw_input[1]),
            "Параметр сортировки": InputConnect.parse_sort_criteria(raw_input[2]),
            "Порядок сортировки": InputConnect.parse_sort_order(raw_input[3]),
            "Диапазон вывода": InputConnect.parse_vacancies_range(raw_input[4]),
            "Требуемые столбцы": InputConnect.parse_to_print_columns(raw_input[5])
        }
        return parsed_input

    @staticmethod
    def parse_vacancies_range(input):
        """
        Обрабатывает данные о диапазоне номеров вакансий в таблице
        :param input: "Грязные" данные о диапазоне
        :return: Обработанные данные о диапазоне
        """
        splitted_input = list(map(int, input.split()))
        splitted_input_len = len(splitted_input)
        if splitted_input_len == 2:
            return [splitted_input[0] - 1, splitted_input[1] - 1]
        elif splitted_input_len == 1:
            return [splitted_input[0] - 1, None]
        return [None]

    @staticmethod
    def parse_to_print_columns(input):
        """
        Обрабатывает данные о столбцах в таблице, которые нужно напечатать
        :param input: "Грязные" данные о столбцах
        :return: Обработанные данные о столбцах
        """
        to_print_columns = input.strip().split(", ")
        if to_print_columns[0] == "":
            return list(formatted_russian_columns.values())
        return to_print_columns

    @staticmethod
    def parse_filter_criteria(input):
        """
        Обрабатывает данные о критерии фильтрации
        Args:
            input (str): "Грязные" данные о критерии фильтрации
        Returns:
            list: Обработанные данные о критерии фильтрации
        """
        if input.strip() == "":
            return []
        if ":" not in input:
            print("Формат ввода некорректен")
            exit()
        splitted_input = input.split(": ")
        column_name = splitted_input[0]
        if column_name not in filter_criterias:
            print("Параметр поиска некорректен")
            exit()
        if column_name == "Навыки":
            splitted_input = splitted_input[1].split(", ")
        return [splitted_input[0], splitted_input[1]]

    @staticmethod
    def parse_sort_criteria(input):
        """
        Обрабатывает данные о критерии сортировки
        Args:
            input (str): "Грязные" данные о критерии сортировки
        Returns:
            str: Обработанные данные о критерии сортировки
        """
        if input not in formatted_russian_columns.values() and input.strip() != "":
            print("Параметр сортировки некорректен")
            exit()
        return input


    @staticmethod
    def parse_sort_order(input):
        """
        Обрабатывает данные о порядке сортировки
        Args:
            input (str): "Грязные" данные о порядке сортировки
        Returns:
            boolean: True, если порядок сортировки обратный, False, если прямой
        """
        if input not in ["Да", "Нет", ""]:
            print("Порядок сортировки задан некорректно")
            exit()
        return input == "Да"

    @staticmethod
    def make_string_length_limit(input):
        """
        Обрезает введенную строку длиной > 100 символов до длины 100 или возвращает исходную, если длина < 100
        Args:
            input (str): Исходная строка
        Returns:
            str: Обработанная строка
        """
        if len(input) > 100:
            return f"{input[:100]}..."
        return input

    @staticmethod
    def get_filtered_vacancies(vacancies_info, criteria):
        """
        Фильтрует поданные на вход вакансии в соответствии с критерием
        Args:
        vacancies_info (list): Список данных о вакансиях, который нужно обработать
        criteria (str): Строка, содержащая критерий фильтрации

        Returns:
             list: Отфильтрованные вакансии
        """
        if len(criteria) == 0:
            return vacancies_info
        filtered_vacancies_info = []
        for vacancy_info in vacancies_info:
            if InputConnect.compare_vacancy_info_with_criteria(vacancy_info, criteria):
                filtered_vacancies_info.append(vacancy_info)
        if len(filtered_vacancies_info) == 0:
            print("Ничего не найдено")
            exit()

        return filtered_vacancies_info

    @staticmethod
    def compare_vacancy_info_with_criteria(vacancy_info, criteria):
        """
        Проверяет, удовлетворяет ли поданная на вход вакансия критерию фильтрации

        Args:
            vacancy_info (dict): Словарь с информацией о вакансии
            criteria (list): Критерий фильтрации
        Returns:
            boolean: True, если вакансия удовлетворяет критерию, False, если нет.
        """
        if criteria[0] == "Навыки":
            skills = vacancy_info[criteria[0]].split("\n")
            for skill in criteria[1]:
                if skill not in skills:
                    return False
            return True
        elif criteria[0] == "Оклад":
            salary_criteria = float(criteria[1])
            temp = re.sub('(?<=\d) (?=\d)', "", vacancy_info[criteria[0]]).split()
            return float(temp[0]) <= salary_criteria <= float(temp[2])
        elif criteria[0] == "Идентификатор валюты оклада":
            salary_currency = re.search('\((.*?)\)', vacancy_info["Оклад"]).group(1)
            return salary_currency == criteria[1]
        elif criteria[0] == "Дата публикации вакансии":
            date = InputConnect.get_normalized_date(vacancy_info["Дата публикации вакансии"])
            return date == criteria[1]
        return vacancy_info[criteria[0]] == criteria[1]

    @staticmethod
    def get_rouble_medium_salary(vacancy_info):
        """
        Возвращает среднюю зарплату вакансии в рублях
        Args:
            vacancy_info (dict): Информация о вакансии
        Returns:
            float: Средняя зарплата вакансии в рублях
        """
        temp = re.sub('(?<=\d) (?=\d)', "", vacancy_info["Оклад"]).split(" ", 3)
        salary_currency = re.search('\((.*?)\)', temp[3]).group(1)
        return currencies_exchanges[salary_currency] * (float(temp[0]) + float(temp[2])) / 2

    @staticmethod
    def get_vacancy_skills_count(vacancy_info):
        """
        Возвращает количество навыков данной вакансии
        Args:
            vacancy_info (dict): Информация о вакансии
        Returns:
            int: Количество навыков данной вакансии
        """
        temp = vacancy_info["Навыки"]
        return len(temp.split("\n"))

    @staticmethod
    def get_lambda(criteria):
        """
        Возвращает подходящую лямбда-функцию для сортировки
        Args:
            criteria (str): Критерий сортировки
        Returns:
            lambda: Лямбда-функция для сортировки
        """

        if criteria == "Оклад":
            return lambda d: InputConnect.get_rouble_medium_salary(d)
        elif criteria == "Навыки":
            return lambda d: InputConnect.get_vacancy_skills_count(d)
        elif criteria == "Дата публикации вакансии":
            return lambda d: datetime.strptime(d["Дата публикации вакансии"], '%Y-%m-%dT%H:%M:%S%z')
        elif criteria == "Опыт работы":
            return lambda d: job_experience_priority[d["Опыт работы"]]
        return lambda d: d[criteria]

    @staticmethod
    def get_sorted_vacancies(vacancies_info, sort_criteria, reversed):
        """
        Сортирует вакансии по критерию
        Args:
            vacancies_info (list): Список вакансии

        Returns:
            list: отсортированный по указанному критерию список вакансий
        """
        if len(sort_criteria) == 0:
            return vacancies_info
        proper_lambda = InputConnect.get_lambda(sort_criteria)
        return sorted(vacancies_info, key=proper_lambda, reverse=reversed)

    @staticmethod
    def get_normalized_date(input):
        """
        Преобразует объект datetime в строку вида "Число.Месяц.Год"
        Args:
            input (datetime): Объект, который нужно преобразовать в строку
        Returns:
            str: Преобразованная в строку вида "Число.Месяц.Год" дата
        """
        return f"{input[8:10]}.{input[5:7]}.{input[:4]}"

    @staticmethod
    def get_date_normalized_vacancies(vacancies_info):
        """
        Заменяет в вакансиях дату, представленную объектом datetime, на строку вида "Число.Месяц.Год"
        Args:
            vacancies_info (list): Список вакансий с датой публикации вида datetime
        Returns:
            list: Список вакансий с замененной на строку вида "Число.Месяц.Год" датой.
        """
        normalized_date_vacancies = []
        for i in range(len(vacancies_info)):
            current_vacancy = vacancies_info[i]
            current_vacancy["Дата публикации вакансии"] = InputConnect.get_normalized_date(vacancies_info[i]["Дата публикации вакансии"])
            normalized_date_vacancies.append(current_vacancy)
        return normalized_date_vacancies


    def prepare_vacancies_info(self, vacancies_info):
        """
        Обрабатывает поданный на вход список вакансий: фильтрует и сортирует по поданным на вход критериям фильтрации и сортировки, преобразует дату
        """
        filtered_vacancies = InputConnect.get_filtered_vacancies(vacancies_info, self.parsed_input["Параметр фильтрации"])
        sorted_vacancies = InputConnect.get_sorted_vacancies(filtered_vacancies, self.parsed_input["Параметр сортировки"], self.parsed_input["Порядок сортировки"])
        normalized_date_sorted_vacancies = InputConnect.get_date_normalized_vacancies(sorted_vacancies)
        return normalized_date_sorted_vacancies


    def get_filled_table(self, vacancies_info):
        """
        Заполняет таблицу, представленную объектом PrettyTable, данными, поданными на вход.
        Args:
            vacancies_info (list): Список вакансий, которыми будет заполнена таблица.
        Returns:
            PrettyTable: таблица, заполненная данными.
        """
        vacancies_info = self.prepare_vacancies_info(vacancies_info)
        table = PrettyTable(align="l", hrules=1)
        field_names = []
        field_names.append("№")
        for element in formatted_russian_columns.values():
            table.max_width[element] = 20
            field_names.append(element)
        table.field_names = field_names
        for i in range(len(vacancies_info)):
            table.add_row([i + 1] + [InputConnect.make_string_length_limit(x) for x in vacancies_info[i].values()])
        return table

    def print_table(self, vacancies_info):
        """
        Печатает в консоль таблицу, которая будет заполненая поданными на вход данными
        Args:
            vacancies_info (list): Данные, которыми нужно заполнить таблицу для печати
        Returns:
            None
        """
        table = self.get_filled_table(vacancies_info)
        vacancies_range = self.parsed_input["Диапазон вывода"]
        vacancies_count = len(vacancies_info)
        to_print_columns = self.parsed_input["Требуемые столбцы"]
        print(table.get_string(start=0 if len(vacancies_range) == 1 else vacancies_range[0],
                               end=vacancies_range[1] if None not in vacancies_range else vacancies_count,
                               fields=["№"] + to_print_columns))


class FileHandler:
    """
    Класс для хранения данных о пользовательском вводе, а также для обработки данных из CSV-файла
    """
    @staticmethod
    def get_user_input():
        """
        Отдает данные, введенные пользователем
        Args:
             None
        Returns:
            list: Пользовательский ввод
        """
        rows = [
            "Введите название файла",
            "Введите название профессии"
        ]
        return [input(f"{rows[i]}: ") for i in range(len(rows))]

    @staticmethod
    def csv_reader(file_name):
        """
        Обрабатывает данные из CSV-файла
        Args:
            file_name (str): имя CSV-файла
        Returns:
            list: Список обьектов-вакансий, полученных при обработке CSV-файла
        """
        reader = csv.reader(open(file_name, encoding="utf_8_sig"))
        data = [Vacancy(row) for row in list(filter(lambda x: "" not in x, reader))[1:]]
        return data


class Vacancy:
    """
    Класс для хранения данных об отдельной вакансии

    Attributes:
        __currentcies_exchanges (dict): Словарь с курсами валют, соответствующих разным странам
        name (str): Название вакансии
        salary (int): Средняя зарплата вакансии
        city (str): Город вакансии
        year (int): Год публикации вакансии

    """
    def __init__(self, vacancy_info):
        """
        Инициализирует внутреннее состояние обьекта в соответствии с переданными данными
        Args:
            vacancy_info (list): список с данными о вакансии
        """
        self.__currencies_exchanges = {
            "AZN": 35.68,
            "BYR": 23.91,
            "EUR": 59.90,
            "GEL": 21.74,
            "KGS": 0.76,
            "KZT": 0.13,
            "RUR": 1,
            "UAH": 1.64,
            "USD": 60.66,
            "UZS": 0.0055
        }
        if len(vacancy_info) > 6:
            vacancy_info = [vacancy_info[0], vacancy_info[6], vacancy_info[7], vacancy_info[9], vacancy_info[10],
                            vacancy_info[11]]
        self.name = vacancy_info[0]
        self.salary = int(0.5 * self.__currencies_exchanges[vacancy_info[3]] * (
                float(vacancy_info[1]) + float(vacancy_info[2])))
        self.city = vacancy_info[4]
        self.year = int(datetime.strptime(vacancy_info[5], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y'))

class Statistics:
    """
    Класс предназначенный, для обработки статистических данных и последующей их печати

    Attributes:
        years_salaries (dict): Словарь с динамикой уровня зарплат по годам
        job_years_salaries (dict): Словарь с динамикой уровня зарплат по годам для выбранной профессии
        years_vacancies_counts (dict): Словарь с динамикой количества вакансий по годам
        job_years_vacancies (dict): Словарь с динамикой количества вакансий по годам для выбранной профессии
        cities_salaries (dict): Словарь с динамикой уровня зарплат в порядке убывания по городам
        cities_vacancies_ratios (dict): Словарь с долями вакансий в порядке убывания по городам
    """
    def __init__(self):
        """
        Инициализирует внутреннее состояние обьекта в соответствии с переданными параметрами
        """
        self.years_salaries = None
        self.years_vacancies_counts = None
        self.job_years_salaries = None
        self.job_years_vacancies = None
        self.cities_salaries = None
        self.cities_vacancies_ratios = None

    def get_empty_dict_with_keys(self, keys):
        """
        Возвращает словарь с нулевыми значениями и ключами, поданными на вход

        Args:
            keys (set or list): ключи, с которыми нужно вернуть словарь

        Returns:
            dict: словарь с нулевыми значениями и ключами, поданными на вход
        """
        return {x: y for x in keys for y in [0]}

    def prepare(self, vacancies_info, name):
        """
        Подготавливает статистические данные из списка информации о вакансиях
        """
        years = set()
        cities = list()
        for vacancy_info in vacancies_info:
            years.add(vacancy_info.year)
            if vacancy_info.city not in cities:
                cities.append(vacancy_info.city)
        years = sorted(years)
        years_salaries = self.get_empty_dict_with_keys(years)
        job_years_salaries = self.get_empty_dict_with_keys(years)
        years_vacancies_counts = self.get_empty_dict_with_keys(years)
        job_years_vacancies = self.get_empty_dict_with_keys(years)
        cities_salaries = self.get_empty_dict_with_keys(cities)
        cities_vacancies = self.get_empty_dict_with_keys(cities)

        for vacancy_info in vacancies_info:
            years_salaries[vacancy_info.year] += vacancy_info.salary
            years_vacancies_counts[vacancy_info.year] += 1
            cities_salaries[vacancy_info.city] += vacancy_info.salary
            cities_vacancies[vacancy_info.city] += 1
            if name in vacancy_info.name:
                job_years_vacancies[vacancy_info.year] += 1
                job_years_salaries[vacancy_info.year] += vacancy_info.salary

        for year in years:
            if years_vacancies_counts[year] > 0:
                years_salaries[year] = years_salaries[year] // years_vacancies_counts[year]
            if job_years_vacancies[year] > 0:
                job_years_salaries[year] = job_years_salaries[year] // job_years_vacancies[year]
        for city in cities:
            cities_salaries[city] = cities_salaries[city] // cities_vacancies[city]

        vacancies_count = len(vacancies_info)

        proper_cities_salaries = dict()
        for city_salary in cities_salaries.items():
            if math.floor(100 * cities_vacancies[city_salary[0]] / vacancies_count) >= 1:
                proper_cities_salaries.update({city_salary[0]: city_salary[1]})

        cities_vacancies_ratios = dict()
        for city_vacancy in cities_vacancies.items():
            if math.floor(100 * city_vacancy[1] / vacancies_count) >= 1:
                cities_vacancies_ratios.update(
                    {city_vacancy[0]: round(city_vacancy[1] / vacancies_count, 4)})

        self.years_salaries = years_salaries
        self.years_vacancies_counts = years_vacancies_counts
        self.job_years_salaries = job_years_salaries
        self.job_years_vacancies = job_years_vacancies
        slice_end = 10 if len(proper_cities_salaries.items()) > 10 else len(proper_cities_salaries.items())
        self.cities_salaries = dict(
            sorted(proper_cities_salaries.items(), key=lambda x: x[1], reverse=True)[:slice_end])
        slice_end = 10 if len(cities_vacancies_ratios.items()) > 10 else len(cities_vacancies_ratios.items())
        self.cities_vacancies_ratios = dict(
            sorted(cities_vacancies_ratios.items(), key=lambda x: x[1], reverse=True)[:slice_end])
        if len(cities_vacancies_ratios.items()) > 10:
            self.cities_vacancies_ratios.update({"Другие": round(1 - sum(self.cities_vacancies_ratios.values()), 4)})

    def print(self):
        """
        Печатает статистические данные в консоль
        """
        print(f"Динамика уровня зарплат по годам: {self.years_salaries}")
        print(f"Динамика количества вакансий по годам: {self.years_vacancies_counts}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.job_years_salaries}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.job_years_vacancies}")
        print(f"Уровень зарплат по городам (в порядке убывания): {self.cities_salaries}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.cities_vacancies_ratios}")

    def get_prepared_statistics(self):
        """
        Возвращает статистические данные, подсчитанные внутри класса

        Returns:
            dict: Словарь с динамикой уровня зарплат по годам
            dict: Словарь с динамикой уровня зарплат по годам для выбранной профессии
            dict: Словарь с динамикой количества вакансий по годам
            dict: Словарь с динамикой количества вакансий по годам для выбранной профессии
            dict: Словарь с динамикой уровня зарплат в порядке убывания по городам
            dict: Словарь с долями вакансий в порядке убывания по городам
        """
        return self.years_salaries, \
               self.job_years_salaries, \
               self.years_vacancies_counts, \
               self.job_years_vacancies, \
               self.cities_salaries, \
               self.cities_vacancies_ratios

class Report:
    """
    Класс, отвечающий за отрисовку графиков и дальнейшее сохранение их в файл формата PNG.

    Attribues:
        job_name (str): Название профессии, данные для которой необходимо вывести
        years_salaries (dict): Словарь с динамикой уровня зарплат по годам
        job_years_salaries (dict): Словарь с динамикой уровня зарплат по годам для выбранной профессии
        years_vacancies_counts (dict): Словарь с динамикой количества вакансий по годам
        job_years_vacancies (dict): Словарь с динамикой количества вакансий по годам для выбранной профессии
        cities_salaries (dict): Словарь с динамикой уровня зарплат в порядке убывания по городам
        cities_vacancies_ratios (dict): Словарь с долями вакансий в порядке убывания по городам
    """
    def __init__(self,
            job_name,
            years_salaries,
            job_years_salaries,
            years_vacancies_counts,
            job_years_vacancies,
            cities_salaries,
            cities_vacancies_ratios):

        """
        Инициализирует внутреннее состояние обьекта в соответствии с переданными параметрами
            job_name (str): Название профессии, данные для которой необходимо вывести
            years_salaries (dict): Словарь с динамикой уровня зарплат по годам
            job_years_salaries (dict): Словарь с динамикой уровня зарплат по годам для выбранной профессии
            years_vacancies_counts (dict): Словарь с динамикой количества вакансий по годам
            job_years_vacancies (dict): Словарь с динамикой количества вакансий по годам для выбранной профессии
            cities_salaries (dict): Словарь с динамикой уровня зарплат в порядке убывания по городам
            cities_vacancies_ratios (dict): Словарь с долями вакансий в порядке убывания по городам
        """
        self.job_name = job_name
        self.years_salaries = years_salaries
        self.job_years_salaries = job_years_salaries
        self.years_vacancies_counts = years_vacancies_counts
        self.job_years_vacancies = job_years_vacancies
        self.cities_salaries = cities_salaries
        self.cities_vacancies_ratios = cities_vacancies_ratios

    def render_graph(self):
        """
        Отрисовывает все 4 графика
        """
        fig, ax = plt.subplots(2, 2)
        self.render_years_salaries_graph(ax[0, 0])
        self.render_years_vacancies_graph(ax[0, 1])
        self.render_cities_salaries_graph(ax[1, 0])
        self.render_cities_vacancies_ratios_graph(ax[1, 1])
        plt.tight_layout()
        plt.savefig("graph.png")
        plt.show()

    def render_years_salaries_graph(self, ax):
        ax.set_title("Уровень зарплат по годам")
        width = 0.4
        years = self.years_salaries.keys()
        salaries = self.years_salaries.values()
        ax.bar([i - width / 2 for i in range(len(years))],
               salaries,
               width=width,
               label="средняя з/п")

        job_salaries = self.job_years_salaries.values()
        ax.bar([i + width / 2 for i in range(len(years))],
               job_salaries,
               width=width,
               label=f"з/п {self.job_name}")
        ax.set_xticks(range(len(years)), years, rotation="vertical")
        ax.tick_params(axis="both", labelsize=8)
        ax.legend(fontsize=8)
        ax.yaxis.set_major_locator(IndexLocator(base=10000, offset=0))

    def render_years_vacancies_graph(self, ax):
        ax.set_title("Количество вакансий по годам")
        width = 0.4
        years = self.years_vacancies_counts.keys()
        vacancies = self.years_vacancies_counts.values()
        ax.bar([i - width / 2 for i in range(len(years))],
               vacancies,
               width=width,
               label="Количество вакансий")
        job_vacancies = self.job_years_vacancies.values()
        ax.bar([i + width / 2 for i in range(len(years))],
               job_vacancies,
               width=width,
               label=f"Количество вакансий\n{self.job_name}")
        ax.set_xticks(range(len(years)),
                      years,
                      rotation="vertical")
        ax.tick_params(axis="both", labelsize=8)
        ax.legend(fontsize=8, loc='upper left')

    def render_cities_salaries_graph(self, ax):
        ax.set_title("Уровень зарплат по городам")
        cities_salaries = self.cities_salaries
        cities = cities_salaries.keys()
        salaries = cities_salaries.values()
        y_pos = range(len(self.cities_salaries))
        cities = [re.sub(r"[- ]", "\n", city) for city in cities]
        ax.barh(y_pos, salaries)
        ax.set_yticks(y_pos, cities)
        ax.invert_yaxis()
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=6)

    def render_cities_vacancies_ratios_graph(self, ax):
        ax.set_title("Доля вакансий по городам")
        reversed_cities_vacancies_ratios = dict(sorted(self.cities_vacancies_ratios.items(), key=lambda item: item[1], reverse=True))
        cities = reversed_cities_vacancies_ratios.keys()
        ratios = reversed_cities_vacancies_ratios.values()
        ax.pie(ratios, labels=cities, textprops={'fontsize': 6})





# functionality_choice = input("Выберите интересующую функциональность (таблица с вакансиями - 1 / статистика по вакансиям - 2): ")
# if functionality_choice == "1":
#     input_connect = InputConnect()
#     dataset = DataSet(input_connect.parsed_input["Название файла"])
#     input_connect.print_table(dataset.vacancies_objects)
# elif functionality_choice == "2":
#     user_input = FileHandler.get_user_input()
#     file_name = user_input[0]
#     vacancy_name = user_input[1]
#     vacancies_info = FileHandler.csv_reader(file_name)
#     statistics = Statistics()
#     statistics.prepare(vacancies_info, vacancy_name)
#     statistics.print()
#     report = Report(vacancy_name, *statistics.get_prepared_statistics())
#     report.render_graph()

import csv
from datetime import datetime
import math
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator
from prettytable import PrettyTable

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
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__vacancies_objects = DataSet.__csv_reader(file_name)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def vacancies_objects(self):
        return self.__vacancies_objects

    @staticmethod
    def __remove_html(input, column_name):
        if column_name == "key_skills":
            return "\n".join(re.sub(r"<[^>]+>", "", input).splitlines())
        else:
            return " ".join(re.sub(r"<[^>]+>", "", input).split())

    @staticmethod
    def __get_filtered_vacancy_info(input, columns):
        return [DataSet.__remove_html(input[i], columns[i]) for i in range(len(input))]

    @staticmethod
    def __get_formatted_number(input):
        return '{0:,}'.format(int(input)).replace(',', ' ')

    @staticmethod
    def __formatter(row):
        formatted_vacancy_data = dict()
        for key, value in formatted_russian_columns.items():
            if key == "salary_description":
                data = f"{DataSet.__get_formatted_number(float(row['salary_from']))} - {DataSet.__get_formatted_number(float(row['salary_to']))} ({currencies[row['salary_currency']]}) ({'Без вычета налогов' if row['salary_gross'] == 'True' else 'С вычетом налогов'})"
                formatted_vacancy_data.update({value: data})
            elif key == "experience_id":
                formatted_vacancy_data.update({value: job_experience[row[key]]})
            elif key == "premium":
                formatted_vacancy_data.update({value: "Да" if row[key] == "True" else "Нет"})
            else:
                formatted_vacancy_data.update({value: row[key]})
        return formatted_vacancy_data

    @staticmethod
    def __csv_reader(file_name):
        reader = csv.reader(open(file_name, encoding="utf_8_sig"))
        columns = []
        try:
            columns = next(reader)
        except StopIteration:
            print("Пустой файл")
            exit()
        #
        data = [DataSet.__formatter(dict(zip(columns, DataSet.__get_filtered_vacancy_info(row, columns)))) for row in reader if len(row) == len(columns) and row.count("") == 0]
        if len(data) == 0:
            print("Нет данных")
            exit()
        return data


class InputConnect:
    def __init__(self):
        self.__input = InputConnect.__get_user_input()
        self.__parsed_input = self.__get_parsed_input(self.__input)

    @property
    def parsed_input(self):
        return self.__parsed_input

    @staticmethod
    def __get_user_input():
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
    def __get_parsed_input(raw_input):
        parsed_input = {
            "Название файла": raw_input[0],
            "Параметр фильтрации": InputConnect.__parse_filter_criteria(raw_input[1]),
            "Параметр сортировки": InputConnect.__parse_sort_criteria(raw_input[2]),
            "Порядок сортировки": InputConnect.__parse_sort_order(raw_input[3]),
            "Диапазон вывода": InputConnect.__parse_vacancies_range(raw_input[4]),
            "Требуемые столбцы": InputConnect.__parse_to_print_columns(raw_input[5])
        }
        return parsed_input

    @staticmethod
    def __parse_vacancies_range(input):
        splitted_input = list(map(int, input.split()))
        splitted_input_len = len(splitted_input)
        if splitted_input_len == 2:
            return [splitted_input[0] - 1, splitted_input[1] - 1]
        elif splitted_input_len == 1:
            return [splitted_input[0] - 1, None]
        return [None]

    @staticmethod
    def __parse_to_print_columns(input):
        to_print_columns = input.strip().split(", ")
        if to_print_columns[0] == "":
            return list(formatted_russian_columns.values())
        return to_print_columns

    @staticmethod
    def __parse_filter_criteria(input):
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
            splitted_input[1] = splitted_input[1].split(", ")
        return [splitted_input[0], splitted_input[1]]

    @staticmethod
    def __parse_sort_criteria(input):
        if input not in formatted_russian_columns.values() and input.strip() != "":
            print("Параметр сортировки некорректен")
            exit()
        return input


    @staticmethod
    def __parse_sort_order(input):
        if input not in ["Да", "Нет", ""]:
            print("Порядок сортировки задан некорректно")
            exit()
        return input == "Да"

    @staticmethod
    def __make_string_length_limit(input):
        if len(input) > 100:
            return f"{input[:100]}..."
        return input

    @staticmethod
    def __get_filtered_vacancies(vacancies_info, criteria):
        if len(criteria) == 0:
            return vacancies_info
        filtered_vacancies_info = []
        for vacancy_info in vacancies_info:
            if InputConnect.__compare_vacancy_info_with_criteria(vacancy_info, criteria):
                filtered_vacancies_info.append(vacancy_info)
        if len(filtered_vacancies_info) == 0:
            print("Ничего не найдено")
            exit()

        return filtered_vacancies_info

    @staticmethod
    def __compare_vacancy_info_with_criteria(vacancy_info, criteria):
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
            date = InputConnect.__get_normalized_date(vacancy_info["Дата публикации вакансии"])
            return date == criteria[1]
        return vacancy_info[criteria[0]] == criteria[1]

    @staticmethod
    def __get_rouble_medium_salary(input):
        temp = re.sub('(?<=\d) (?=\d)', "", input["Оклад"]).split(" ", 3)
        salary_currency = re.search('\((.*?)\)', temp[3]).group(1)
        return currencies_exchanges[salary_currency] * (float(temp[0]) + float(temp[2])) / 2

    @staticmethod
    def __get_vacancy_skills_count(input):
        temp = input["Навыки"]
        return len(temp.split("\n"))

    @staticmethod
    def __get_lambda(input):
        if input == "Оклад":
            return lambda d: InputConnect.__get_rouble_medium_salary(d)
        elif input == "Навыки":
            return lambda d: InputConnect.__get_vacancy_skills_count(d)
        elif input == "Дата публикации вакансии":
            return lambda d: datetime.strptime(d["Дата публикации вакансии"], '%Y-%m-%dT%H:%M:%S%z')
        elif input == "Опыт работы":
            return lambda d: job_experience_priority[d["Опыт работы"]]
        return lambda d: d[input]

    @staticmethod
    def __get_sorted_vacancies(vacancies_info, sort_criteria, reversed):
        if len(sort_criteria) == 0:
            return vacancies_info
        proper_lambda = InputConnect.__get_lambda(sort_criteria)
        return sorted(vacancies_info, key=proper_lambda, reverse=reversed)

    @staticmethod
    def __get_normalized_date(input):
        return f"{input[8:10]}.{input[5:7]}.{input[:4]}"

    @staticmethod
    def __get_date_normalized_vacancies(vacancies_info):
        normalized_date_vacancies = []
        for i in range(len(vacancies_info)):
            current_vacancy = vacancies_info[i]
            current_vacancy["Дата публикации вакансии"] = InputConnect.__get_normalized_date(vacancies_info[i]["Дата публикации вакансии"])
            normalized_date_vacancies.append(current_vacancy)
        return normalized_date_vacancies


    def __prepare_vacancies_info(self, vacancies_info):
        filtered_vacancies = InputConnect.__get_filtered_vacancies(vacancies_info, self.parsed_input["Параметр фильтрации"])
        sorted_vacancies = InputConnect.__get_sorted_vacancies(filtered_vacancies, self.parsed_input["Параметр сортировки"], self.parsed_input["Порядок сортировки"])
        normalized_date_sorted_vacancies = InputConnect.__get_date_normalized_vacancies(sorted_vacancies)
        return normalized_date_sorted_vacancies


    def __get_filled_table(self, raw_vacancies_info):
        vacancies_info = self.__prepare_vacancies_info(raw_vacancies_info)
        table = PrettyTable(align="l", hrules=1)
        field_names = []
        field_names.append("№")
        for element in formatted_russian_columns.values():
            table.max_width[element] = 20
            field_names.append(element)
        table.field_names = field_names
        for i in range(len(vacancies_info)):
            table.add_row([i + 1] + [InputConnect.__make_string_length_limit(x) for x in vacancies_info[i].values()])
        return table

    def print_table(self, vacancies_info):
        table = self.__get_filled_table(vacancies_info)
        vacancies_range = self.parsed_input["Диапазон вывода"]
        vacancies_count = len(vacancies_info)
        to_print_columns = self.parsed_input["Требуемые столбцы"]
        print(table.get_string(start=0 if len(vacancies_range) == 1 else vacancies_range[0],
                               end=vacancies_range[1] if None not in vacancies_range else vacancies_count,
                               fields=["№"] + to_print_columns))


class FileHandler:
    @staticmethod
    def get_user_input():
        rows = [
            "Введите название файла",
            "Введите название профессии"
        ]
        return [input(f"{rows[i]}: ") for i in range(len(rows))]

    @staticmethod
    def csv_reader(file_name):
        reader = csv.reader(open(file_name, encoding="utf_8_sig"))
        data = [Vacancy(row) for row in list(filter(lambda x: "" not in x, reader))[1:]]
        return data


class Vacancy:
    def __init__(self, vacancy_info):
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
    def __init__(self):
        self.years_salaries = None
        self.years_vacancies_counts = None
        self.job_years_salaries = None
        self.job_years_vacancies = None
        self.cities_salaries = None
        self.cities_vacancies_ratios = None

    def __get_empty_dict_with_keys(self, keys):
        return {x: y for x in keys for y in [0]}

    def prepare(self, vacancies_info, name):
        years = set()
        cities = list()
        for vacancy_info in vacancies_info:
            years.add(vacancy_info.year)
            if vacancy_info.city not in cities:
                cities.append(vacancy_info.city)
        years = sorted(years)
        years_salaries = self.__get_empty_dict_with_keys(years)
        job_years_salaries = self.__get_empty_dict_with_keys(years)
        years_vacancies_counts = self.__get_empty_dict_with_keys(years)
        job_years_vacancies = self.__get_empty_dict_with_keys(years)
        cities_salaries = self.__get_empty_dict_with_keys(cities)
        cities_vacancies = self.__get_empty_dict_with_keys(cities)

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
        print(f"Динамика уровня зарплат по годам: {self.years_salaries}")
        print(f"Динамика количества вакансий по годам: {self.years_vacancies_counts}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.job_years_salaries}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.job_years_vacancies}")
        print(f"Уровень зарплат по городам (в порядке убывания): {self.cities_salaries}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.cities_vacancies_ratios}")

    def get_prepared_statistics(self):
        return self.years_salaries, \
               self.job_years_salaries, \
               self.years_vacancies_counts, \
               self.job_years_vacancies, \
               self.cities_salaries, \
               self.cities_vacancies_ratios

class Report:
    def __init__(self,
            job_name,
            years_salaries,
            job_years_salaries,
            years_vacancies_counts,
            job_years_vacancies,
            cities_salaries,
            cities_vacancies_ratios):

        self.job_name = job_name
        self.years_salaries = years_salaries
        self.job_years_salaries = job_years_salaries
        self.years_vacancies_counts = years_vacancies_counts
        self.job_years_vacancies = job_years_vacancies
        self.cities_salaries = cities_salaries
        self.cities_vacancies_ratios = cities_vacancies_ratios

    def render_graph(self):
        fig, ax = plt.subplots(2, 2)
        self.__render_years_salaries_graph(ax[0, 0])
        self.__render_years_vacancies_graph(ax[0, 1])
        self.__render_cities_salaries_graph(ax[1, 0])
        self.__render_cities_vacancies_ratios_graph(ax[1, 1])
        plt.tight_layout()
        plt.savefig("graph.png")
        plt.show()

    def __render_years_salaries_graph(self, ax):
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

    def __render_years_vacancies_graph(self, ax):
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

    def __render_cities_salaries_graph(self, ax):
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

    def __render_cities_vacancies_ratios_graph(self, ax):
        ax.set_title("Доля вакансий по городам")
        reversed_cities_vacancies_ratios = dict(sorted(self.cities_vacancies_ratios.items(), key=lambda item: item[1], reverse=True))
        cities = reversed_cities_vacancies_ratios.keys()
        ratios = reversed_cities_vacancies_ratios.values()
        ax.pie(ratios, labels=cities, textprops={'fontsize': 6})





functionality_choice = input("Выберите интересующую функциональность (таблица с вакансиями/статистика по вакансиям): ")
if functionality_choice == "Таблица":
    input_connect = InputConnect()
    dataset = DataSet(input_connect.parsed_input["Название файла"])
    input_connect.print_table(dataset.vacancies_objects)
elif functionality_choice == "Графики":
    user_input = FileHandler.get_user_input()
    file_name = user_input[0]
    vacancy_name = user_input[1]
    vacancies_info = FileHandler.csv_reader(file_name)
    statistics = Statistics()
    statistics.prepare(vacancies_info, vacancy_name)
    statistics.print()
    report = Report(vacancy_name, *statistics.get_prepared_statistics())
    report.render_graph()


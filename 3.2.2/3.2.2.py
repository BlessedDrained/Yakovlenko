import multiprocessing
import os
import pandas as pd
import math


def get_year_statistics(file_name, job_name, queue):
    year = file_name[-8:-4]
    df = pd.read_csv(file_name)
    df["mean_salary"] = 0.5 * (df["salary_from"] + df["salary_to"])
    salaries_year = int(df["mean_salary"].mean())
    vacancies_count_year = df.shape[0]

    job_dataframe = df[df["name"].str.contains(job_name)]
    job_salary_years = int(job_dataframe["mean_salary"].mean())
    job_vacancies_count_year = job_dataframe.shape[0]
    queue.put([year, salaries_year, vacancies_count_year, job_salary_years, job_vacancies_count_year])


def separate_csv(file_name):
    df = pd.read_csv(file_name)
    df["years"] = df["published_at"].apply(lambda s: s[0:4])
    years = df["years"].unique()

    if not os.path.exists("csv_files"):
        os.mkdir("csv_files")
    for year in years:
        data = df[df["years"] == year]
        data.iloc[:, :6].to_csv(rf"csv_files\part_{year}.csv", index=False)


def get_multiprocess_statistics(job_name):
    queue = multiprocessing.Queue()
    processes = []
    for file_name in os.listdir("csv_files"):
        csv_file = os.path.join("csv_files", file_name)
        process = multiprocessing.Process(target=get_year_statistics, args=(csv_file, job_name, queue))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

    result = [{} for x in range(4)]
    while not queue.empty():
        year_data = queue.get()
        for i in range(4):
            result[i][year_data[0]] = year_data[i + 1]

    for i in range(len(result)):
        result[i] = dict(sorted(result[i].items(), key=lambda x: x[0]))
    return result


def get_singleprocess_statistics(file_name):
    df = pd.read_csv(file_name)
    df["mean_salary"] = 0.5 * (df["salary_from"] + df["salary_to"])
    cities = df["area_name"].unique()
    cities_vacancies_count = {city: 0 for city in cities}
    cities_salaries = {city: 0 for city in cities}
    for index, row in df.iterrows():
        city = row["area_name"]
        salary = row["mean_salary"]
        cities_vacancies_count[city] += 1
        cities_salaries[city] += salary

    vacancies_count = df.shape[0]

    for city in cities:
        cities_salaries[city] = cities_salaries[city] // cities_vacancies_count[city]

    proper_cities_salaries = {}
    for city_salary in cities_salaries.items():
        if math.floor(100 * cities_vacancies_count[city_salary[0]] / vacancies_count) >= 1:
            proper_cities_salaries.update({city_salary[0]: int(city_salary[1])})

    cities_vacancies_ratios = {}
    for city_vacancy in cities_vacancies_count.items():
        if math.floor(100 * city_vacancy[1] / vacancies_count) >= 1:
            cities_vacancies_ratios.update({city_vacancy[0]: round(city_vacancy[1] / vacancies_count, 4)})

    slice_end = 10 if len(proper_cities_salaries.items()) > 10 else len(proper_cities_salaries.items())
    cities_salaries = dict(sorted(proper_cities_salaries.items(), key=lambda x: x[1], reverse=True)[:slice_end])
    slice_end = 10 if len(cities_vacancies_ratios.items()) > 10 else len(cities_vacancies_ratios.items())
    cities_vacancies_ratios = dict(
        sorted(cities_vacancies_ratios.items(), key=lambda x: x[1], reverse=True)[:slice_end])
    return [cities_salaries, cities_vacancies_ratios]


def get_user_input():
    rows = [
        "Введите название файла",
        "Введите название профессии"
    ]
    return [input(f"{row}: ") for row in rows]


if __name__ == "__main__":
    #user_input = get_user_input()

    print("Работаем")
    user_input = [
        "vacancies_by_year.csv",
        "Программист"
    ]
    separate_csv(user_input[0])
    multiproc_result = get_multiprocess_statistics(user_input[1])
    singleproc_result = get_singleprocess_statistics(user_input[0])
    print(f"Динамика уровня зарплат по годам: {multiproc_result[0]}")
    print(f"Динамика количества вакансий по годам: {multiproc_result[1]}")
    print(f"Динамика уровня зарплат по годам для выбранной профессии: {multiproc_result[2]}")
    print(f"Динамика количества вакансий по годам для выбранной профессии: {multiproc_result[3]}")
    print(f"Уровень зарплат по городам (в порядке убывания): {singleproc_result[0]}")
    print(f"Доля вакансий по городам (в порядке убывания): {singleproc_result[1]}")
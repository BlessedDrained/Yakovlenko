import pandas as pd
import sqlite3

pd.set_option("expand_frame_repr", False)

if __name__ == "__main__":
    con = sqlite3.connect("vacancies.db")
    cur = con.cursor()
    vacancies_count = pd.read_sql("select count(*) from vacancies", con).to_dict()["count(*)"][0]

    # Динамика уровня зарплат по годам
    years_salaries_raw = pd.\
        read_sql("select substr(published_at, 0, 5), round(avg(salary)) from vacancies group by substr(published_at, 0, 5)", con).\
        to_dict()
    years_salaries = dict(
        zip(
            years_salaries_raw["substr(published_at, 0, 5)"].values(), years_salaries_raw["round(avg(salary))"].values()))

    # Динамика количества вакансий по годам
    years_vacancies_raw = pd.\
        read_sql("select substr(published_at, 0, 5), count(*) from vacancies group by substr(published_at, 0, 5)", con).\
        to_dict()
    years_vacancies = dict(
        zip(
            years_vacancies_raw["substr(published_at, 0, 5)"].values(), years_vacancies_raw["count(*)"].values()))

    # Динамика уровня зарплат по годам для выбранной профессии
    job_name = "Программист"
    db_job_name = f"%{job_name}%"
    job_years_salaries_raw = pd.\
        read_sql("select substr(published_at, 0, 5), round(avg(salary)) from vacancies where name like :db_job_name group by substr(published_at, 0, 5)", con, params=[db_job_name])\
        .to_dict()
    job_years_salaries = dict(
        zip(
            job_years_salaries_raw["substr(published_at, 0, 5)"].values(), job_years_salaries_raw["round(avg(salary))"].values()))

    # Динамика количества вакансий по годам для выбранной профессии
    job_name = "Программист"
    db_job_name = f"%{job_name}%"
    job_years_vacancies = pd\
        .read_sql("select substr(published_at, 0, 5), count(substr(published_at, 0, 5)) from vacancies where name like :db_job_name group by substr(published_at, 0, 5)", con, params=[db_job_name])\
        .to_dict()
    job_years_vacancies = dict(
        zip(
            job_years_vacancies["substr(published_at, 0, 5)"].values(), job_years_vacancies["count(substr(published_at, 0, 5))"].values()))

    # Уровень зарплат по городам (в порядке убывания) - только первые 10 значений
    cities_salaries_raw = pd.read_sql("select area_name, round(avg(salary)), count(area_name) from vacancies group by area_name", con)
    cities_salaries_raw = cities_salaries_raw[cities_salaries_raw["count(area_name)"] >= 0.01 * vacancies_count].to_dict()

    cities_salaries = dict(
        sorted(
            zip(cities_salaries_raw["area_name"].values(), cities_salaries_raw["round(avg(salary))"].values()),
            key=lambda x: x[1],
            reverse=True)[:10])

    # Доля вакансий по городам (в порядке убывания) - только первые 10 значений
    cities_vacancies_ratios_raw = pd.read_sql("select area_name, count(area_name) from vacancies group by area_name", con)
    cities_vacancies_ratios_raw = cities_vacancies_ratios_raw[cities_vacancies_ratios_raw["count(area_name)"] >= 0.01 * vacancies_count].to_dict()

    cities_vacancies_ratios = dict(
        sorted(
            zip(cities_vacancies_ratios_raw["area_name"].values(), cities_vacancies_ratios_raw["count(area_name)"].values()),
            key=lambda x: x[1],
            reverse=True)[:10])
    for city in cities_vacancies_ratios.keys():
        cities_vacancies_ratios[city] = round(cities_vacancies_ratios[city] / vacancies_count, 4)

    print(f"Динамика уровня зарплат по годам: {years_salaries}")
    print(f"Динамика количества вакансий по годам: {years_vacancies}")
    print(f"Динамика уровня зарплат по годам для выбранной профессии: {job_years_salaries}")
    print(f"Динамика количества вакансий по годам для выбранной профессии: {job_years_vacancies}")
    print(f"Уровень зарплат по городам (в порядке убывания): {cities_salaries}")
    print(f"Доля вакансий по городам (в порядке убывания): {cities_vacancies_ratios}")




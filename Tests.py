from unittest import TestCase
from main import Vacancy
from main import DataSet
from main import InputConnect
from main import Statistics


test_vacancy_info = ['Оператор ЧПУ',
                             '<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>',
                             'Работа с чертежами\nMS Dos',
                             'between1And3',
                             'FALSE',
                             'ЗСК Глобал',
                             '70000',
                             '80000',
                             'TRUE',
                             'RUR',
                             'Артем',
                             '2022-07-06T02:03:11+0300']


test_vacancy_info_eur = ['Senior Python Developer (Crypto)',
                         '<p>With over 1,500 employees of more than 88 nationalities, Exness is the place for global teamwork, incredible leadership, a learning culture, and constant development. Unlimited by time zones, Exnessians from around the world have worked seamlessly together since 2008 to provide our traders with the best possible trading experience. Today, we stand proud with over 300,000 active traders and 2.5 trillion USD in monthly trading volume.</p> <p><em><strong>Your role at Exness:</strong></em></p> <p>We are looking for an experienced Python Engineer to join our Exness Technology team. The role will be focused on the implementation of complex business logic inside web stack in the area of financial and crypto markets. Working side-by-side with Product Managers, connecting ideas to the customers in the most optimal way. We&#39;re looking for a person who will extend, optimize, and support the production of the existing software solutions, ensuring we capture as much value from the market as possible. You will research and innovate new ideas in high reliable, low-latency, and high-load computing in financial markets.</p> <p><em><strong>What You will do:</strong></em></p> <ul> <li>Software development;</li> <li>Highload and high available web stack services to support various customer journeys (Payments management);</li> <li>Supporting and back-office interfaces (Personal Area, Payment Solutions, Back Office);</li> <li>Blockchain and cryptocurrencies integration and development</li> <li>Internal auxiliary libraries, tools, integrations, interfaces, and frameworks supporting all components and services.</li> </ul> <p><em><strong>What you need to succeed:</strong></em></p> <ul> <li>You’re passionate about building a trading product that brings the world together;</li> <li>You have 5 years of commercial software development using Python and have excellent knowledge of its stack;</li> <li>You have a solid knowledge of general Computer Science and working experience with various system designs and integrational patterns,</li> <li>You have solid experience with ORM, DBMS, including database architecting;</li> <li>You cultivate DevOps culture and usage of relevant tools. You have solid experience with Operating Systems, Networking Models, virtualization, and containerization;</li> <li>You cover your software by unit tests, have experience in integrational and load tests;</li> <li>You can successfully interact with business functions using the English language.</li> </ul> <p><em><strong>Nice to have:</strong></em></p> <ul> <li>Knowledge and experience in cryptocurrencies integration (Ethereum/Bitcoin)</li> <li>Commercial experience with Go;</li> <li>Experience acting as a code reviewer;</li> <li>Experience in debugging, profiling, and code optimizations;</li> <li>Highload, concurrency &amp; multithreading backend systems development;</li> <li>Microservice development experience.</li> </ul> <p><em><strong>What we offer:</strong></em></p> <ul> <li>A fairly estimated and attractive package (competitive salary based on your expectations and internal benchmark) with the ability to start working remotely anywhere in the world;</li> <li>Company Car - the company will provide Exness-branded cars to those who relocated, parking near the office or a bus tickets;</li> <li>We’ll pay school or kindergarten fees (Annual Registration or Tuition Fees, Regular term fees, Half day service to kindergartens) for your children between 0 years - 18 years, up to three (3) children;</li> <li>L&amp;D - support your need to replenish your knowledge and acquire new skills to do your job better via: Continuous product education, Professional training &amp; Certifications, Soft skill training, Language classes, and our very own Exness library;</li> <li>Sports Benefits - Our very own Sports Club with dedicated coaches doing group and individual training, on-site and online, sharing healthy recipes and life hacks + Free Sanctum Club Membership for you and your spouse. Jet Skis (if you have a speed boat operator license);</li> <li>Medical - in addition to having a Corporate Doctor, we cooperate with one of the biggest international insurance companies in order to provide medical insurance for you and your families. Coverage is provided for you, your spouse, and your children up to 18 years old. It includes Inpatient, Outpatient, and international support.<br /><br /><em>Sounds like you? Apply and we will arrange a video call:)</em></li> </ul> <div> <div> <div> </div> </div> </div>',
                         'Development\nPython\nAgile\nBlockchain\nInformation Technology',
                         'moreThan6',
                         'FALSE',
                         'EXNESS Global Limited',
                         '4500',
                         '5500',
                         'FALSE',
                         'EUR',
                         'Москва',
                         '2022-07-05T18:23:15+0300']


test_vacancies_info = [
    Vacancy(test_vacancy_info),
    Vacancy(test_vacancy_info_eur)
]

class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy(test_vacancy_info)).__name__, "Vacancy")

    def test_vacancy_name(self):
        self.assertEqual(Vacancy(test_vacancy_info).name, "Оператор ЧПУ")

    def test_vacancy_average_salary(self):
        self.assertEqual(Vacancy(test_vacancy_info).salary, 75000)

    def test_vacancy_city(self):
        self.assertEqual(Vacancy(test_vacancy_info).city, "Артем")

    def test_vacancy_average_salary_eur(self):
        self.assertEqual(Vacancy(test_vacancy_info_eur).salary, 299500)

class DataSetTest(TestCase):
    def test_remove_html_non_key_skills(self):
        to_remove_html_string = '<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>'
        reference_string = 'Обязанности: компьютерное моделирование деталей настройки параметров обработки деталей установка материала и съем готовой детали контроль и измерение деталей на соответствие размеров техническому заданию Требования: Образование Средне-специальное Умение пользоваться инструментом Умение читать чертежи Технический склад ума Примечание: Питание предоставляется. Возможно проживание'
        self.assertEqual(DataSet.remove_html(to_remove_html_string, "Test"), reference_string)

    def test_remove_html_key_skills(self):
        to_remove_html_string = '<strong>Работа<li> с чертежами<div>\n</strong>MS Dos'
        reference_string = 'Работа с чертежами\nMS Dos'
        self.assertEqual(DataSet.remove_html(to_remove_html_string, "key_skills"), reference_string)

    def test_get_formatted_number(self):
        test_value = "1500003"
        self.assertEqual(DataSet.get_formatted_number(test_value), "1 500 003")


    def test_formatter(self):
        vacancy_info_dict = dict(zip(['name',
                  'description',
                  'key_skills',
                  'experience_id',
                  'premium',
                  'employer_name',
                  'salary_from',
                  'salary_to',
                  'salary_gross',
                  'salary_currency',
                  'area_name', 'published_at'],
                 ['Оператор ЧПУ',
                  '<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>',
                  'Работа с чертежами\nMS DOS',
                  'between1And3',
                  'FALSE',
                  'ЗСК Глобал',
                  '70000',
                  '80000',
                  'TRUE',
                  'RUR',
                  'Артем',
                  '2022-07-06T02:03:11+0300']))
        formatted_vacancy_info = list(DataSet.formatter(vacancy_info_dict).values())
        reference_formatted_vacancy_info = [
            "Оператор ЧПУ",
            '<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>',
            "Работа с чертежами\nMS DOS",
            "От 1 года до 3 лет",
            "Нет",
            "ЗСК Глобал",
            "70 000 - 80 000 (Рубли) (С вычетом налогов)",
            "Артем",
            "2022-07-06T02:03:11+0300"
        ]
        self.assertEqual(formatted_vacancy_info, reference_formatted_vacancy_info)


class InputConnectTests(TestCase):
    def test_compare_vacancy_with_criteria(self):
        vacancy_info_dict = dict(zip(['name',
                                      'description',
                                      'key_skills',
                                      'experience_id',
                                      'premium',
                                      'employer_name',
                                      'salary_from',
                                      'salary_to',
                                      'salary_gross',
                                      'salary_currency',
                                      'area_name', 'published_at'],
                                     ['Оператор ЧПУ',
                                      '<strong>Обязанности:</strong> <ul> <li>компьютерное моделирование деталей</li> <li>настройки параметров обработки деталей</li> <li>установка материала и съем готовой детали</li> <li>контроль и измерение деталей на соответствие размеров техническому заданию</li> </ul> <strong>Требования:</strong> <ul> <li>Образование Средне-специальное</li> <li>Умение пользоваться инструментом</li> <li>Умение читать чертежи</li> <li>Технический склад ума</li> </ul> <strong>Примечание:</strong> <ul> <li>Питание предоставляется. Возможно проживание</li> </ul>',
                                      'Работа с чертежами\nMS DOS',
                                      'between1And3',
                                      'FALSE',
                                      'ЗСК Глобал',
                                      '70000',
                                      '80000',
                                      'TRUE',
                                      'RUR',
                                      'Артем',
                                      '2022-07-06T02:03:11+0300']))
        formatted_vacancy_info = DataSet.formatter(vacancy_info_dict)
        self.assertFalse(InputConnect.compare_vacancy_info_with_criteria(formatted_vacancy_info, ["Оклад", "150000"]))

class StatisticsTests(TestCase):
    def test_prepare_statistic(self):
        statistics = Statistics()
        statistics.prepare(test_vacancies_info, "Программист")

        result = [
            statistics.cities_salaries,
            statistics.cities_vacancies_ratios,
            statistics.job_years_salaries,
            statistics.job_years_vacancies,
            statistics.years_salaries,
            statistics.years_vacancies_counts
        ]

        reference_cities_salaries = {
            "Москва": 299500,
            "Артем": 75000
        }

        reference_cities_vacancies_ratios = {
            "Артем": 0.5,
            "Москва": 0.5
        }

        reference_job_years_salaries = {
            2022: 0
        }

        reference_job_years_vacancies = {
            2022: 0
        }

        reference_years_salaries = {
            2022: 187250
        }

        reference_years_vacancies_counts = {
            2022: 2
        }

        reference_values = [
            reference_cities_salaries,
            reference_cities_vacancies_ratios,
            reference_job_years_salaries,
            reference_job_years_vacancies,
            reference_years_salaries,
            reference_years_vacancies_counts
        ]
        self.assertEqual(result, reference_values)

# SMIT INSURANCE TEST API

# [ENG]
This project was build as part of job application testing for SMIT.

### Run with DOCKER
1. First pull the project from Hub:
> docker pull kubanemil/smit_api

2. Next, create and run the container:
> docker run --name smit_container -p 0.0.0.0:80:80 smit_api

3. Go to http://127.0.0.1/ to see API documentation.
4. Go to http://127.0.0.1/get_insurance endpoint,

If you running API with docker, there is <b>no need to create data, 
as it will be created automatically</b>.

### Run manually
1. Clone the repository:
> git clone https://github.com/kubanemil/SMIT_insurance_project
2. Create and activate a virtual environment (recommended):
> python3 -m venv venv

> source venv/bin/activate
3. Install requirements:
> pip install -r requirements.txt
4. Initiate the database and populate it with dataset:
> python3 create_data.py
5. Run the API:
> uvicorn main:app --reload
6. Go to http://127.0.0.1/get_insurance endpoint


## About API
For this project, the API gets Tariff from the API itself, but in case that 
you need to retrieve Tariff from external API, you just need to set it as 
an environmental variable TARIFF_URL.
(for example: TARIFF_URL='http://example.com/get_tariff').

To test the insurance estimator, go to <b>/get_insurance</b> endpoint and 
specify the <b>cargo's name</b> and <b>cargo's cost</b>.
It will return <b>insurance amount</b> for <b>all dates</b> in the tariff.
If you want to get insurance for a <b>specific date</b>, you can use <b>/get_insurance/by_date</b>
endpoint.

Insurance is calculated by: <b>cargo_cost*cargo_rate</b>

## Endpoints' descriptions:

You can add more data with **POST /data/cargo** and **POST /data/tariff**. But before adding more data, I 
recommend you to delete previous data with **DELETE /data/cargo** and **DELETE /data/tariff**

**/cargos** - lists all existing Cargo instances from database.

**/tariff** - returns tariff rates for each cargo by date.

**/get_insurance** - Given the cargo's name and price, calculates the insurance 
for each date according to tariff.

**/get_insurance/by_date** - Given the cargo's name and price, calculates 
the insurance according to tariff for specific date.


# [RUS]

Этот проект был создан в рамках тестирования при приеме на работу в SMIT.

### Запуск с помощью DOCKER
1. Сначала загрузите проект из Хаба:
> docker pull kubanemil/smit_api

2. Затем запустите контейнер:
> docker run --name smit_container -p 0.0.0.0:80:80 smit_api

3. Документация API в: http://127.0.0.1/
4. Перейдите в http://127.0.0.1/get_insurance, чтобы увидеть страховочный endpoint


Если вы запускаете API с помощью Docker, то <b>не нужно создавать данные, так как они будут созданы автоматически</b>.

### Ручной запуск
1. Отклонируйте репу:
> git clone https://github.com/kubanemil/SMIT_insurance_project
2. Создайте и активруйте venv:
> python3 -m venv venv

> source venv/bin/activate
3. Установите requirements:
> pip install -r requirements.txt
4. Создайте базу данных и сами данные с этим скриптом:
> python3 create_data.py
5. Запустите API:
> uvicorn main:app --reload
6. Перейдите в http://127.0.0.1/get_insurance, чтобы увидеть страховочный endpoint


## Описание API
Для этого проекта API получает Тариф из самого себя, 
но если вам нужно получить Тариф из внешнего API, 
вам просто нужно установить его в качестве переменной среды TARIFF_URL.
(например: TARIFF_URL='http://example.com/get_tariff').

Для тестирования перейдите по адресу <b>/get_insurance</b> и укажите 
<b>название груза</b> и <b>стоимость груза</b>.
Он вернет <b>сумму страхования</b> для <b>всех дат</b> в тарифе.
Если вы хотите получить страхование на <b>определенную дату</b>, 
вы можете использовать <b>/get_insurance/by_date</b>.

Страховая сумма рассчитывается по формуле: <b>стоимость_груза * тариф_груза</b>

## Описание endpoint-ов:
Вы можете создать больше данных с помощью POST /data/cargo и POST /data/tariff. 
Но перед добавлением новых данных,
рекомендую удалить предыдущие записи с помощью DELETE /data/cargo и DELETE /data/tariff

/cargos - выводит список существующих грузов из базы данных.

/tariff - возвращает Актуальный Тариф для каждого груза по датам.

/get_insurance - Для указанного названия и цены груза рассчитывается страхование 
для каждой даты в соответствии с тарифом.

/get_insurance/by_date - Для указанного названия и цены груза рассчитывается 
страхование согласно тарифу для указанной даты.
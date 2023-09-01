## Запуск на Linux/MacOs

- Положить файл в папку src/data, либо в параметрах скрипта указать путь до файла
- Определить параметры - название файла, интервал графика и параметр для скользящей средней
- `cd src && chmod +x run.sh`
- запустить скрипт с указанием парметров `source run.sh --data_path {} --time_inter {} --EMA_inter {}`
- пример: `source run.sh --data_path ./data/prices.csv --time_inter 3600 --EMA_inter 1`

## Запуск в Windows

- Активировать виртуальное окружение или установить библиотеки в системное `pip install -r ../requirements.txt`
- Запустить python файл main.py с параметрами
- пример: `python main.py --data_path ./data/prices.csv --time_inter 3600 --EMA_inter 1`

## Запуск в Docker

In progress...

## Результат

В результате в браузере по умолчанию откроется график 
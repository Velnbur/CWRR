#!/usr/bin/python
"""
Variant 34
Description:
 
    Обробляються дані спостережень за погодою.
    Записи основного файлу містять поля: середня денна температура, кількість опадів, код метеостанції,
    сила вітру, рік, день, місяць, відносна вологість, максимальна денна температура, мінімальна денна температура.
    У допоміжному файлі наявні ключі: кількість метеостанцій, середнє значення середньоденної температури.
    Знайти метеостанції, по яких фіксувалася кількість опадів у два рази менша за середню по всіх даних. Вивести по кожному з них інформацію:
    — на першому рядку:
    найбільша кількість опадів, кількість спостережень, середня мінімальна температура, метеостанція;
    — на наступних рядках, починаючи з табуляції, вивести для них агреговані дані (по одному на рядок):
    день, середня вологість (за цей день року по всіх місяцях по цій метеостанції), рік у такому сортуванні: день, рік.
"""
from records import Records
from load import load, load_ini
from sys import argv


def _print_author():
    print("Kyrylo Baibula. Group K-11")


def _print_doc():
    print(__doc__)


def process(path_to_ini: str):
    """ Program main function """
    input_paths, output_path = load_ini(path_to_ini)
    records = Records()
    load(records, input_paths["csv"],
         input_paths["json"], input_paths["encoding"])
    records.output(output_path["fname"], output_path["encoding"])

if __name__ == "__main__":
    try:
        if len(argv) < 2:
            raise Exception("Not enough arguments")
        _print_author()
        _print_doc()
        print("*****")
        process(path_to_ini=argv[1])
    except BaseException as e:
        print("\n***** program aborted *****")
        print(e)

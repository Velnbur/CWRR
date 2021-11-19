import json
from records import Records
from builder import Builder


def check_ini(d: dict) -> bool:
    """ Check correctness of ini file """
    result = True
    if "input" in d.keys():
        input_keys = d["input"].keys()
        if not ("csv" in input_keys
                or "json" in input_keys
                or "encoding" in input_keys):
            result = False
    else:
        result = False

    if "output" in d.keys():
        output_keys = d["output"].keys()
        if not ("fname" in output_keys or "encoding" in output_keys):
            result = False
    else:
        result = False
    return result


def check_addit(json: dict) -> bool:
    """ Check correctness of json file """
    stations_count = "кількість метеостанцій"
    middle_middle_temp = "середнє значення середньоденної температурти"

    keys = json.keys()
    if stations_count in keys and middle_middle_temp in keys:
        return True
    return False


def fit(records: Records, station_count: int, mid_mid_temp: float) -> bool:
    """check if data from json file is right"""
    stat1 = records.mid_mid_temp == mid_mid_temp
    stat2 = records.count_of_stations == station_count
    return stat1 and stat2


def load_ini(path: str) -> tuple:
    print("ini", path, ":", end="")
    with open(path, "r") as f:
        data = json.load(f)

    if not check_ini(data):
        raise Exception("ini doesn't have enough information")
    print(" OK")
    return data["input"], data["output"]


def load_stat(path: str, encoding: str) -> tuple:
    print("input-json ", path, ": ", end="", sep="")    
    with open(path, "r", encoding=encoding) as f:
        data = json.load(f)
    if check_addit(data):
        print("OK")
        return data.values()
    return None


def load(
    records: Records,
    path_to_csv: str,
    path_to_json: str,
    encoding: str
):
    load_data(records, path_to_csv, encoding)    
    station_count, mid_mid_temp = load_stat(path_to_json, encoding)

    print("json?=csv: ", end="")
    if fit(records, station_count, mid_mid_temp):
        print("OK")
    else:
        print("UPS")


def load_data(records: Records, path: str, encoding: str):
    print("input-csv ", path, ": ", end="", sep="")
    records.clear()
    try:
        with open(path, "r", encoding=encoding) as f:
            b = Builder()
            b.load(records, f)
    except BaseException as error:
        records.clear()
        raise error
    print("OK")
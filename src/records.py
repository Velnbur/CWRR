from datetime import date
import re


class _Temperatures:
    """
    Private 'data' class for representing
    temperatures in MeteorologicalData
    """
    _minimal: float
    _middle: float
    _maximum: float

    def __init__(self, min_temp, mid_temp, max_temp):
        if (
            not isinstance(mid_temp, (int, float))
            or not isinstance(max_temp, (int, float))
            or not isinstance(min_temp, (int, float))
        ):
            raise TypeError("Temperature must be float")

        self._minimal = float(min_temp)
        self._maximum = float(max_temp)
        self._middle = float(mid_temp)

    @property
    def minimal(self):
        return self._minimal

    @property
    def middle(self):
        return self._middle

    @property
    def maximum(self):
        return self._maximum


class _MeteorologicalData:
    """
    'Data' class for representing
    all recorded data from stations
    """
    _precipitation: float
    _relative_humidity: float
    _temps: _Temperatures
    _wind_force: int

    def __init__(self,
                 prec: float,
                 rel_hum: float,
                 wind_force: int,
                 min_temp: float,
                 mid_temp: float,
                 max_temp: float):
        if not isinstance(rel_hum, float):
            raise TypeError()

        if not isinstance(prec, float):
            raise TypeError("precipitation must be float")

        if not isinstance(wind_force, int):
            raise TypeError(" wind_force must be int")

        self._precipitation = prec
        self._relative_humidity = rel_hum
        self._wind_force = wind_force
        self._temps = _Temperatures(min_temp, mid_temp, max_temp)

    @property
    def precipitation(self):
        return self._precipitation

    @property
    def relative_humidity(self) -> float:
        return self._relative_humidity

    @property
    def min_temp(self) -> float:
        return self._temps.minimal

    @property
    def mid_temp(self) -> float:
        return self._temps.middle

    @property
    def max_temp(self) -> float:
        return self._temps.maximum

    @property
    def wind_force(self) -> int:
        return self._wind_force

    def __repr__(self) -> str:
        return f"|{self.precipitation}, {self.relative_humidity}" \
            f"{self.wind_force}, {self.temps}|"


class DailyRecord:
    """
    Daily records from  Meteorological Stations
    The  of classes:
        datetime.date, _MeteorologicalData
    """
    rec_date: date
    _data: _MeteorologicalData

    def __init__(
        self,
        mid_temp: float,
        precip: float,
        wind_force: int,
        year: int,
        month: int,
        day: int,
        rel_hum: float,
        max_temp: float,
        min_temp: float,
    ):
        if (
            not isinstance(year, int)
            or year < 1000
        ):
            raise Exception("Date format is invalid")
        self.rec_date = date(year, month, day)
        self._data = _MeteorologicalData(
            precip, rel_hum, wind_force, min_temp, mid_temp, max_temp)

    @property
    def data(self):
        return self._data

    @property
    def day(self):
        return self.rec_date.day

    @property
    def year(self):
        return self.rec_date.year


class Records:
    """
    Main Information class
    """
    __count_of_stations: int = 0
    __count_of_records: int = 0
    __mid_mid_temp: float = .0
    __mid_precipitation: float = .0
    __stations: dict = {}
    __date_relhum: dict = {}

    def __init__(self):
        self.__stations = {}

    @property
    def count_of_stations(self) -> int:
        if not self.__count_of_stations:
            self.__count_of_stations = self._count_stations()
        return self.__count_of_stations

    @property
    def mid_mid_temp(self) -> float:
        if not self.__mid_mid_temp:
            self.__mid_mid_temp = self._get_middle_middle_temp()
        return self.__mid_mid_temp

    @property
    def mid_precipitation(self) -> float:
        if not self.__mid_precipitation:
            self.__mid_precipitation = self._calc_mid_precip()
        return self.__mid_precipitation

    @property
    def count_of_records(self) -> int:
        if not self.__count_of_records:
            self.__count_of_records = self._count_records()
        return self.__count_of_records

    def clear(self):
        self.__mid_mid_temp = .0
        self.__count_of_stations = 0
        self.__mid_precipitation = .0
        self.__count_of_records = 0
        self.__count_of_stations = 0
        self.__stations.clear()
        self.__date_relhum.clear()


    def output(self, path: str, encoding: str):
        print("output ", path, ": ", sep="", end="")
        with open(path, "w", encoding=encoding) as f:
            for station_id, records in self.__stations.items():
                if self.__check_precip(records):
                    self._output(f, station_id)
        print("OK")

    def _output(self, f, station_id: str):
        """ Function for creating a message and writing it ot file 
        Parameters:
            f - opened file stream
            station_id - id of the station
        """
        max_precip, mid_min_temp = self.__find_maxprecip_avemintemp(station_id)
        message = f"{max_precip:.1f}\t" \
            f"{len(self.__stations[station_id])}\t" \
            f"{mid_min_temp:.1f}\t" \
            f"{station_id}"

        self.__stations[station_id].sort(key=lambda r: (r.day, r.year))

        l_day = 0
        l_year = 0
        for rec in self.__stations[station_id]:
            if l_year == rec.year and l_day == rec.day:
                continue

            rel_hum, count = self.__date_relhum[station_id][rec.year][rec.day]
            message += f"\n\t{rec.day}" \
                f"\t{rel_hum/count:.1f}" \
                f"\t{rec.year}"
            l_year = rec.year
            l_day = rec.day
        message += "\n"
        f.write(message)

    def __check_precip(self, records: list[DailyRecord]) -> bool:
        """
        Check if list of records has record that
        with precipitation two times less then mid precipitation
        """
        flag = False
        for record in records:
            if record.data.precipitation < (self.mid_precipitation / 2):
                flag = True
                break
        return flag

    def __find_maxprecip_avemintemp(self, station_id) -> float and float:
        """
        Return max precipitation and
        average value of min temps
        """
        max_precip = .0
        mid_min_temp = 0
        records_count = len(self.__stations[station_id])
        for record in self.__stations[station_id]:
            if max_precip < record.data.precipitation:
                max_precip = record.data.precipitation
            mid_min_temp += record.data.mid_temp
        return max_precip, mid_min_temp / records_count

    def _calc_mid_precip(self):
        """
        Calculate middle precipitation from all records
        """
        sum_precip = sum([sum([record.data.precipitation for record in records])
                        for records in self.__stations.values()])
        return sum_precip / self.count_of_records

    def _count_stations(self) -> int:
        return len(self.__stations.keys())

    def _count_records(self) -> int:
        return sum([len(records) for records in self.__stations.values()])

    def _get_middle_middle_temp(self) -> float:
        """Calculate average temp between middle temps"""
        sum_temps = .0
        for records in self.__stations.values():
            for record in records:
                sum_temps += record.data.mid_temp
        return sum_temps / self.count_of_records

    def append_record(
        self,
        mid_temp: float,
        precip: float,
        station_id: str,
        wind_force: int,
        year: int,
        month: int,
        day: int,
        rel_hum: float,
        max_temp: float,
        min_temp: float,
    ):
        """ Appends new daily record """
        if not re.fullmatch(r"\w{3,9}", station_id):
            raise Exception("Station id is invalid")
        if station_id not in self.__stations.keys():
            self.__stations[station_id] = []
        self.__stations[station_id].append(DailyRecord(
            mid_temp, precip, wind_force,
            year, month, day, rel_hum, max_temp, min_temp))
        self._append_date_relhum(station_id, day, year, rel_hum)

    def _append_date_relhum(self, station_id, day, year, rel_hum):
        """
        append to dict 
        """
        if station_id not in self.__date_relhum:
            self.__date_relhum[station_id] = {}
        if year not in self.__date_relhum[station_id].keys():
            self.__date_relhum[station_id][year] = {}
        if day not in self.__date_relhum[station_id][year].keys():
            self.__date_relhum[station_id][year][day] = (.0, 0)
        rel, count = self.__date_relhum[station_id][year][day]
        self.__date_relhum[station_id][year][day] = (rel+rel_hum, count+1)

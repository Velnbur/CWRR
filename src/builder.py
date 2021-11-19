from records import Records
import csv


class Builder:
    __mid_temp: float
    __precipitation: float
    __station_id: str
    __wind_force: int
    __year: int
    __month: int
    __day: int
    __rel_hum: float
    __max_temp: float
    __min_temp: float

    def _clear(self):
        self.__mid_temp = .0
        self.__precipitation = .0
        self.__station_id = ""
        self.__wind_force = 0
        self.__year = 0
        self.__month = 0
        self.__day = 0
        self.__rel_hum = .0
        self.__max_temp = .0
        self.__min_temp = .0

    def load(self, records: Records,  f):
        self._clear()
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            line_len = len(line)
            if not line_len:
                continue
            if line_len != 10:
                raise Exception("There is not enough or too much columns")

            self.__mid_temp = line[0]
            self.__precipitation = line[1]
            self.__station_id = line[2]
            self.__wind_force = line[3]
            self.__year = line[4]
            self.__month = line[5]
            self.__day = line[6]
            self.__rel_hum = line[7]
            self.__max_temp = line[8]
            self.__min_temp = line[9]
            self._convert_line()
            records.append_record(mid_temp=self.__mid_temp,
                                  precip=self.__precipitation,
                                  station_id=self.__station_id,
                                  wind_force=self.__wind_force,
                                  year=self.__year, 
                                  month=self.__month,
                                  day=self.__day,
                                  rel_hum=self.__rel_hum,
                                  max_temp=self.__max_temp,
                                  min_temp=self.__min_temp)

    def _convert_line(self):
        try:
            self.__mid_temp = float(self.__mid_temp)
            self.__precipitation = float(self.__precipitation)
            self.__wind_force = int(self.__wind_force)
            self.__year = int(self.__year)
            self.__month = int(self.__month)
            self.__day = int(self.__day)
            self.__rel_hum = float(self.__rel_hum)
            self.__max_temp = float(self.__max_temp)
            self.__min_temp = float(self.__min_temp)
        except ValueError:
            raise Exception("wrong data in csv file")

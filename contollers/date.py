import datetime


class DateController:
    @staticmethod
    def check_date_validity(date) -> bool:
        date = date.split('/')
        if len(date) == 3:
            if date[2].isnumeric() and date[1].isnumeric() and date[0].isnumeric():
                try:
                    datetime.date(int(date[2]), int(date[1]), int(date[0]))
                    return True
                except ValueError:
                    return False
        return False

    @staticmethod
    def str_date_to_date(date: str) -> datetime.date:
        date_list = date.split('/')
        return datetime.date(
            year=int(date_list[2]),
            month=int(date_list[1]),
            day=int(date_list[0])
        )

    def str_list_of_date_to_list_of_date(self, dates_str: str) -> list:
        list_date_str = [[date for date in dates.split('-')]for dates in dates_str.split(',')]
        date_list = [[self.str_date_to_date(date) for date in dates] for dates in list_date_str]
        dates_list_timestamp = [[datetime.datetime(
            date.timetuple()[0],
            date.timetuple()[1],
            date.timetuple()[2]
        ).timestamp() for date in dates] for dates in date_list]
        dates_betweens = []
        for dates in dates_list_timestamp:
            cursor = dates[0]+24*60*60
            date_between = [dates[0]]
            while cursor <= dates[-1]:
                date_between.append(cursor)
                cursor += 24*60*60
            dates_betweens.append([datetime.datetime.fromtimestamp(d).date() for d in date_between])
        date_list_result = []
        for dates in dates_betweens:
            date_list_result += dates
        return date_list_result

    @staticmethod
    def list_of_date_to_str_list_of_date(list_dates: list) -> str:
        list_dates.sort()
        list_dates_timestamp = [datetime.datetime(
            date.timetuple()[0],
            date.timetuple()[1],
            date.timetuple()[2]
        ).timestamp() for date in list_dates]
        cursor = 0
        clean_date_list = []
        for loop_cursor in range(len(list_dates_timestamp)):
            if loop_cursor != len(list_dates_timestamp)-1:
                if int(list_dates_timestamp[loop_cursor])+24*60*60 < int(list_dates_timestamp[loop_cursor+1]):
                    clean_date_list.append(list_dates[cursor:loop_cursor+1])
                    cursor = loop_cursor+1
            else:
                clean_date_list.append(list_dates[cursor:loop_cursor+1])
        result_date_list_str = ''
        for dates in clean_date_list:
            if len(dates) == 1:
                result_date_list_str += f' le {dates[0].strftime("%d/%m/%Y")} et'
            else:
                result_date_list_str += f' du {dates[0].strftime("%d/%m/%Y")} au {dates[-1].strftime("%d/%m/%Y")} et'
        return result_date_list_str[1:-3]

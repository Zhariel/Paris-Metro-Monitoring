import random
import datetime
from datetime import datetime, timedelta

_START_YEAR = 2012
_END_YEAR = 2022

class DisruptionGenerator:
    def __init__(self):
        self.flatten = lambda lis: [x for l in lis for x in l]
        self.priority = [['bloquant', [75, 0, 0, 15, 0, 10, 0, 0, 0, 0], [720, 1440]],
                         ['perturbation', [15, 15, 5, 10, 10, 5, 5, 0, 25, 10], [20, 180]],
                        ['information', [0, 0, 10, 0, 0, 20, 0, 70, 0, 0], [0, 0]]]
        self.prio_weights = self.flatten([['bloquant']*5, ['perturbation']*14, ['information']])
        self.years = [x for x in range(_START_YEAR, _END_YEAR)]
        # self.months = range(1, 13)
        self.months = range(1, 13)
        self.months_max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.cause = [
            "Travaux",
            "Panne d'ascenseur",
            "Déplacement d'une personnalité",
            "Incident technique",
            "Difficultés d'exploitation",
            "Incidents d'exploitation",
            "Actionnement d'une alarme",
            "Concerts",
            "Baggage abandonné",
            "Malaise voyageur",
        ]
        self.codes = range(1, 15)
        self.lines = zip(self.codes, [2, 3, 5, 5, 2, 2, 4, 5, 3, 4, 2, 4, 6, 3])
        weighted_lines = [[x[0]]*x[1] for x in self.lines]
        self.weighted_lines = self.flatten(weighted_lines)

    def __weighted_cause_per_line(self, prio_idx):
        weights = self.priority[prio_idx][1]
        weighted_causes = [[self.cause[idx]]*w for idx, w in enumerate(weights)]
        return self.flatten(weighted_causes)


    def __create_datetime(self, year, month, day):
        return datetime(
            year=year,
            month=month,
            day=day,
            hour=random.randint(0, 23),
            minute=random.randint(0, 59)
        )

    def generate_disruptions(self):
        headers = ['is_disrupted', 'line', 'start_date', 'duration', 'cause', 'priority']
        prio_idx = lambda x: 0 if x == 'bloquant' else 1 if x == 'perturbation' else 2
        res = []

        for year in self.years:
            for month in self.months:
                for day in range(1, self.months_max_days[month-1]+1):
                    disrupted = True if random.random() < 0.5 else False
                    line_code = random.choice(self.weighted_lines)
                    date = self.__create_datetime(year, month, day)

                    if disrupted:
                        prio = random.choice(self.prio_weights)
                        idx = prio_idx(prio)
                        cause = random.choice(self.__weighted_cause_per_line(idx))

                        res.append([True,
                                line_code,
                                date,
                                random.randint(self.priority[idx][2][0], self.priority[idx][2][1]),
                                cause,
                                prio,
                                ])
                    else:
                        res.append([False, line_code, date, 0, "", ""])

        return headers, res

    def gen_xy_predict_disruption(self, disruptions):
        # x: start_time, line
        # y: disruption
        keys = ['is_disrupted', 'year', 'month', 'day', 'hour', 'minute'] + [str(x) for x in range(1, 15)]

        entries = []
        for dis in disruptions:
            entry = [dis[0], dis[2].year, dis[2].month, dis[2].day, dis[2].hour, dis[2].minute] + \
                [1 if x == dis[1] else 0 for x in range(1, 15)]

            entries.append(dict(zip(keys, entry)))

        return keys, entries

    def gen_xy_predict_duration(self, disruptions):
        # x: start_time, line
        # y: duration
        keys = ['year', 'month', 'day', 'hour', 'minute', 'duration'] + [str(x) for x in range(1, 15)]

        entries = []
        for dis in disruptions:
            if not dis[0]:
                continue
            entry = [dis[2].year, dis[2].month, dis[2].day, dis[2].hour, dis[2].minute, dis[3]] + \
                [1 if x == dis[1] else 0 for x in range(1, 15)]

            if dict[0]:
                entries.append(dict(zip(keys, entry)))

        return keys, entries

    def gen_xy_predict_priority(self, disruptions):
        # x: start_time, line
        # y: priority
        keys = ['year', 'month', 'day', 'hour', 'minute', 'duration'] + \
               [str(x) for x in range(1, 15)] + \
               ['priority']

        entries = []
        for dis in disruptions:
            if not dis[0]:
                continue
            entry = [dis[2].year, dis[2].month, dis[2].day, dis[2].hour, dis[2].minute, dis[3]] + \
                [1 if x == dis[1] else 0 for x in range(1, 15)] + \
                [dis[5]]

            if dict[0]:
                entries.append(dict(zip(keys, entry)))

        return keys, entries

    def gen_xy_predict_cause(self, disruptions):
        # x: start_time, line, priority
        # y: cause
        prio_list = ['bloquant', 'perturbation', 'information']
        keys = ['year', 'month', 'day', 'hour', 'minute', 'duration'] + \
               [str(x) for x in range(1, 15)] + \
                prio_list + \
                ['cause']

        entries = []
        for dis in disruptions:
            if not dis[0]:
                continue
            entry = [dis[2].year, dis[2].month, dis[2].day, dis[2].hour, dis[2].minute, dis[3]] + \
                [1 if x == dis[1] else 0 for x in range(1, 15)] + \
                [1 if x == dis[5] else 0 for x in prio_list] + \
                [dis[4]]

            if dict[0]:
                entries.append(dict(zip(keys, entry)))

        return keys, entries


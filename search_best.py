#!/usr/bin/env python

import csv
import os

from datetime import datetime, timedelta

results_dir = os.path.join('results', 'runs')


def main():
    mini = 0
    min_string = ""
    start_date = datetime.strptime("2013-01-01", '%Y-%m-%d').date()
    for l in [1, 2, 4, 5, 6, 7, 8]:
        for d in range(0, 365):
            load = "load" + str(l)
            day = "day" + dayify(d + 1)
            date = start_date + timedelta(d)
            bay_reg = "{0}-{1}-{2}-bay_reg_all_feat_90_days.csv".format(date,
                                                                        load,
                                                                        day)
            svr = "{0}-{1}-{2}-lin_svr_c1e3_all_feat_90_days.csv".format(date,
                                                                         load,
                                                                         day)

            f1_location = os.path.join(results_dir, bay_reg)
            f2_location = os.path.join(results_dir, svr)

            with open(f1_location, 'r') as f1:
                with open(f2_location, 'r') as f2:
                    bay_reg_data = list(csv.reader(f1, delimiter=','))
                    svr_data = list(csv.reader(f2, delimiter=','))
                    bay_regret = bay_reg_data[4]
                    svr_regret = svr_data[4]

                    difference = bay_regret - svr_regret

                    if difference < mini:
                        mini = difference
                        min_string = "{0}-{1}-{2}".format(date, load, day)
    print min_string


def dayify(d):
    if d > 99:
        return str(d)
    elif d > 9:
        return '0' + str(d)
    else:
        return '00' + str(d)


if __name__ == '__main__':
    main()

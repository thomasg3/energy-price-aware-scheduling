#!/usr/bin/env python

# make a visualisation of the results, filtered and with the optimal added to the plot or not.

import os
import argparse
import cPickle as pickle
import matplotlib.pyplot as plt


def main(filter, optimal_too):

    run_location = os.path.join("results", "runs")
    image_location = os.path.join("results", "img")
    if not os.path.isdir(image_location):
        os.makedirs(image_location)
    files = [f for f in os.listdir(run_location) if f.split('.')[-1] == 'p' and filter in f]
    for index, file_name in enumerate(files):
        with open(os.path.join(run_location, file_name), 'r') as stream:
            result = pickle.load(stream)

        time_slots = range(len(result.prediction.actual_values))
        time_slot_names = ["{:02d}:{:02d}".format(t / 2, (t % 2) * 30) for t in time_slots]
        time_slot_names = [t if i % 4 == 0 else "" for i, t in enumerate(time_slot_names)]

        power_usage = result.forecasted_schedule.power_usage()
        if optimal_too:
            optimal_usage = result.optimal_schedule.power_usage()

        fig, ax1 = plt.subplots()
        ax1.set_title(file_name.split('.')[0])
        ax1.plot(time_slots, result.prediction.actual_values, 'g', label="actual")
        ax1.plot(time_slots, result.prediction.prediction_values, 'r', label="prediction")

        ax2 = ax1.twinx()
        ax2.bar(time_slots, power_usage, alpha=0.2)
        if optimal_too:
            ax2.bar(time_slots, optimal_usage, color="g", alpha=0.2)

        image_name = file_name.split('.')[0]+'.png'
        image_full_name = os.path.join(image_location, image_name)
        if not os.path.isfile(image_full_name):
            open(image_full_name, 'a').close()
        plt.savefig(image_full_name)
        plt.close()
        print "{}/{} Saved {}".format(index+1, len(files), image_full_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Plot experiment results")

    parser.add_argument("-r", "--result", help="filter the results to plot", default="")
    parser.add_argument("-o", help="plot optimal schedule in graph", action="store_true")

    args = parser.parse_args()

    main(args.result, args.o)

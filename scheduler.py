#!/usr/bin/env python

from gurobipy import *
import scripts.instance2dzn as i2dzn


def schedule(instance, price):
    return _schedule(instance.time_step, instance.nbMachines, instance.nbTasks, instance.nbRes, instance.m_res,
              instance.j_earl, instance.j_late, instance.j_dur, instance.j_power, instance.j_res, price)


def _schedule(time_step, nb_machines, nb_tasks, nb_res, m_res, j_earl, j_late, j_dur, j_power, j_res, price):
    machines = range(nb_machines)
    tasks = range(nb_tasks)
    res = range(nb_res)

    time_step = float(time_step)
    t = int(24.0 * 60.0 / time_step)
    times = range(t)

    model = Model("schedule")
    model.params.logToConsole = 0

    x_jmt = [(j, m, t) for j in tasks for m in machines for t in times]

    x = model.addVars(x_jmt, vtype=GRB.BINARY, name="x")

    model.setObjective(quicksum(x[j, m, t] * quicksum(
        (j_power[j] * price[t2] * time_step) / 60.0 for t2 in range(t, min(t + j_dur[j], len(price))))
                                for j in tasks for m in machines for t in times), GRB.MINIMIZE)

    model.addConstrs(x.sum(j, "*", "*") == 1 for j in tasks)
    model.addConstrs(x[j, m, t] == 0 for j in tasks for m in machines for t in times if t < j_earl[j])
    model.addConstrs(x[j, m, t] == 0 for j in tasks for m in machines for t in times if t + j_dur[j] > j_late[j])
    model.addConstrs(
        sum([x[j, m, t2] * j_res[j][r] for j in tasks for t2 in times if t - j_dur[j] < t2 <= t]) <= m_res[m][r]
        for m in machines for r in res for t in times)

    model.optimize()

    result_schedule = [[[x[j, m, t].x for t in times] for m in machines] for j in tasks]
    return Schedule(time_step, result_schedule, model.objVal, j_dur, j_power)


class Schedule:
    def __init__(self, time_step, schedule_values, forecasted_price, task_durations, task_power):
        self.time_step = time_step
        self.values = schedule_values
        self.forecasted_price = forecasted_price
        self.task_durations = task_durations
        self.task_power = task_power

    def cost(self, actual_prices):
        cost = 0.0
        for (j, task) in enumerate(self.values):
            for machine in task:
                start = [t for t in range(len(machine)) if machine[t] == 1]
                if start:
                    start = start[0]
                    for t in range(start, start + self.task_durations[j]):
                        cost += (self.task_power[j] * actual_prices[t] * self.time_step) / 60.0
        return cost

    def power_usage(self):
        usage = [0] * ((24 * 60) / int(self.time_step))
        for j, task in enumerate(self.values):
            for machine in task:
                start = [t for t in range(len(machine)) if machine[t] == 1]
                if start:
                    start = start[0]
                    for t in range(start, start+self.task_durations[j]):
                        usage[t] += (self.task_power[j] * self.time_step) / 60.0
        return usage


def read_instance(file_name):
    data = i2dzn.read_instance(file_name)
    return Instance(data)


class Instance:
    def __init__(self, data):
        self.time_step = data['time_step']
        self.nbMachines = len(data['machines'])
        self.nbTasks = len(data['tasks'])
        self.nbRes = data['nr_res']
        self.m_res = [m['res'] for m in data['machines']]
        self.j_earl = [j['earl'] for j in data['tasks']]
        self.j_late = [j['late'] for j in data['tasks']]
        self.j_dur = [j['dur'] for j in data['tasks']]
        self.j_power = [j['power'] for j in data['tasks']]
        self.j_res = [j['usage'] for j in data['tasks']]

    def nr_of_periods(self):
        time_step = float(self.time_step)
        return int(24.0 * 60.0 / time_step)

    def analyse(self):
        analysis = InstanceAnalysis(
            [0 for _ in range(self.nr_of_periods())],
            [0 for _ in range(self.nr_of_periods())],
            [0 for _ in range(self.nr_of_periods())])
        for j in range(self.nbTasks):
            duration = self.j_dur[j]
            earliest_start = self.j_earl[j]
            earliest_end = earliest_start + duration
            latest_end = self.j_late[j]
            latest_start = latest_end - duration

            for t in range(self.nr_of_periods()):
                if earliest_start <= t < latest_end:
                    analysis.max_load[t] += self.j_power[j]
                    if latest_start <= t < earliest_end:
                        analysis.min_load[t] += self.j_power[j]

            # expected load
            number_of_pos = latest_end - earliest_start - duration + 1
            expected_load = [0 for _ in range(latest_end - earliest_start)]
            for p in range(number_of_pos):
                for t in range(duration):
                    expected_load[p+t] += 1
            expected_load = [(float(exp) / number_of_pos) * self.j_power[j] for exp in expected_load]
            for index, exp in enumerate(expected_load):
                analysis.exp_load[earliest_start+index] += exp
        return analysis


class InstanceAnalysis:
    def __init__(self, min_load, max_load, exp_load):
        self.min_load = min_load
        self.max_load = max_load
        self.exp_load = exp_load

    def normalize(self):
        sum_min_load = sum(self.min_load)
        sum_max_load = sum(self.max_load)
        sum_exp_load = sum(self.exp_load)
        return InstanceAnalysis(
            [m / sum_min_load for m in self.min_load],
            [m / sum_max_load for m in self.max_load],
            [e / sum_exp_load for e in self.exp_load])


if __name__ == '__main__':
    test_time_step = 30.0

    test_nbMachines = 1
    test_nbTasks = 1
    test_nbRes = 1

    test_m_res = [[2000]]

    test_j_earl = [0]
    test_j_late = [48]
    test_j_dur = [14]
    test_j_power = [155.8]
    test_j_res = [[1668]]

    test_price = [0.2922, 0.28758, 0.28758, 0.28512, 0.28512, 0.264, 0.28512, 0.28512, 0.24612, 0.246, 0.20766, 0.20766,
                  0.18834, 0.24384, 0.24606, 0.28656, 0.28656, 0.28644, 0.20868, 0.28656, 0.24384, 0.24384, 0.28644,
                  0.28656, 0.28656, 0.28656, 0.28656, 0.28656, 0.28656, 0.28656, 0.28656, 0.2922, 0.2922, 0.2922,
                  0.29466, 1.64598, 1.64598, 0.30048, 0.29466, 0.2922, 0.2922, 0.2922, 0.2922, 0.2922, 0.28908, 0.28656,
                  0.2922, 0.2922]

    test_result = _schedule(test_time_step, test_nbMachines, test_nbTasks, test_nbRes, test_m_res, test_j_earl,
                            test_j_late, test_j_dur, test_j_power, test_j_res, test_price)

    print test_result.forecasted_price

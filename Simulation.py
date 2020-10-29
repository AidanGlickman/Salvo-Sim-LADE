import numpy as np
from matplotlib import pyplot as plt
import copy
import random
import itertools


class Force:
    units = 0
    power = 0.0
    defense = 0.0
    staying = 0.0
    accuracy = 0.0

    history = []

    def __init__(self, units, power, defense, staying, accuracy):
        self.units = units
        self.power = power
        self.defense = defense
        self.staying = staying
        self.accuracy = accuracy
        self.history = []
        self.history.append(units)

    def advance(self, opponent):
        diff1 = self.units - (opponent.power * opponent.accuracy *
                              opponent.units - self.defense*self.units) / self.staying
        self.units = min(max(0, diff1), self.units)
        self.history.append(self.units)
        return self.units

    def __str__(self):
        return 'UNITS: ' + str(self.units) + '\nPOWER: ' + str(self.power) + '\nDEFENSE: ' + str(self.defense) + '\nSTAYING: ' + str(self.staying) + '\nACCURACY: ' + str(self.accuracy) + '\nHISTORY: ' + str(self.history)


class Engagement:
    force1 = None
    force2 = None
    maxSalvos = 0
    simulated = False
    winner = 0

    def __init__(self, force1, force2, maxSalvos=5):
        self.force1 = force1
        self.force2 = force2
        self.maxSalvos = maxSalvos

    def advance(self):
        temp1 = copy.deepcopy(self.force1)
        self.force1.advance(self.force2)
        self.force2.advance(temp1)
        # print('Force1\n' + str(self.force1))
        # print('Force2\n' + str(self.force2))

    def checkEnded(self):
        if len(self.force1.history) >= self.maxSalvos or self.force1.units == self.force2.units == 0:
            # print('maxed')
            # print(self.force1.history)
            if self.force1.units > self.force2.units:
                self.winner = -1
            elif self.force1.units < self.force2.units:
                self.winner = -2
            return True
        elif self.force1.units == 0:
            # print('force1 depleted')
            self.winner = 2
            return True
        elif self.force2.units == 0:
            # print('force2 depleted')
            self.winner = 1
            return True
        return False

    def simulate(self):
        while not self.checkEnded():
            self.advance()


class StatTab:
    log = None
    wins1 = 0
    wins2 = 0
    partWins1 = 0
    partWins2 = 0
    avgScore = 0

    def __init__(self, engagementLog):
        self.log = engagementLog
        self.wins1 = sum(
            1 for engagement in self.log if engagement.winner == 1)
        self.wins2 = sum(
            1 for engagement in self.log if engagement.winner == 2)
        self.partWins1 = sum(
            1 for engagement in self.log if engagement.winner == -1)
        self.partWins2 = sum(
            1 for engagement in self.log if engagement.winner == -2)

    def plot(self):
        for i in self.log:
            log1 = i.force1.history
            log2 = i.force2.history

            def propfunc(x):
                try:
                    return (((log1[x] / (log1[x]+log2[x]))-0.5)*2)
                except:
                    return 0
            # proportionLog holds numbers from -1 to 1 where 1 indicates total win for force1 and -1 indicates total win for force2
            proportionLog = [propfunc(x) for x in range(len(log1))]
            self.avgScore = sum(proportionLog)/len(proportionLog)
            # print(proportionLog)
            plt.plot(proportionLog)


class Simulation:
    engagements = []
    log = []
    title = "Simulation"
    run = False

    def __init__(self, title, force_units, force_power, force_defense, force_staying, force_accuracy, diff1_units=0, diff1_power=0, diff1_defense=0, diff1_staying=0, diff1_accuracy=0, diff2_units=0, diff2_power=0, diff2_defense=0, diff2_staying=0, diff2_accuracy=0):
        combos = itertools.product(force_units, force_power, force_defense, force_staying,
                                   force_accuracy, force_units, force_power, force_defense, force_staying,
                                   force_accuracy)
        self.title = title
        for combo in combos:
            force1 = Force(combo[0]+diff1_units, combo[1]+diff1_power, combo[2] +
                           diff1_defense, combo[3]+diff1_staying, combo[4]+diff1_accuracy)
            force2 = Force(combo[5]+diff2_units, combo[6]+diff2_power, combo[7] +
                           diff2_defense, combo[8]+diff2_staying, combo[9]+diff2_accuracy)
            self.engagements.append(Engagement(force1, force2))

    def genTab(self):
        if not self.run:
            raise Exception("Please run the simulate() function first.")
        else:
            tab = StatTab(self.log)
            tab.plot()
            plt.title(self.title)
            plt.ylim(-1, 1)
            plt.ylabel("Outcome")
            plt.xlabel("Salvos")
            print(f"Engagements Simulated: {len(self.log)}\nForce1 Total Victories: {tab.wins1}\nForce2 Total Victories: {tab.wins2}\nForce1 Partial Victories: {tab.partWins1}\nForce2 Partial Victories: {tab.partWins2}\nAverage Score: {tab.avgScore}")

    def simulate(self):
        for engagement in self.engagements:
            engagement.simulate()
            self.log.append(engagement)
        self.run = True


def equalBattle():
    return Simulation("Equal Forces", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1))


def unitAdv(num):
    return Simulation(f"{num} Unit Advantage", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_units=num)


def powerAdv(num):
    return Simulation(f"{num} Power Level Advantage", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_power=num)


def defenseAdv(num):
    return Simulation(f"{num} Defense Level Advantage", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_defense=num)


def stayingAdv(num):
    return Simulation(f"{num} Staying Power Level Advantage", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_staying=num)


def accuracyAdv(num):
    return Simulation(f"{num} Accuracy Level Advantage", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_accuracy=num/10)


def turtlingAdv(defe, atta):
    return Simulation(f"Turtling vs Blitzing", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_defense=defe, diff2_power=atta)


def intelfireAdv(acc, att):
    return Simulation(f"Intel vs Firepower", range(2, 6), range(1, 4), range(
        1, 3), range(1, 2), np.arange(0.5, 1, 0.1), diff1_accuracy=acc/10, diff2_power=att)


def main():
    # sim = equalBattle()
    # sim = accuracyAdv(1)
    sim = intelfireAdv(1, 1)
    sim.simulate()
    sim.genTab()
    plt.show()
    # force1 = Force(6, 6, 6, 6, 1)
    # force2 = Force(5, 5, 5, 5, 1)
    # eng = Engagement(force1, force2)
    # eng.simulate()


main()

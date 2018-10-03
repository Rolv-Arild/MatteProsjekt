import numpy as np
import math as m
import sys
import time


class RungeKuttaFehlberg54:
    A = np.array(
        [[0, 0, 0, 0, 0, 0],
         [1 / 4, 0, 0, 0, 0, 0],
         [3 / 32, 9 / 32, 0, 0, 0, 0],
         [1932 / 2197, -7200 / 2197, 7296 / 2197, 0, 0, 0],
         [439 / 216, -8, 3680 / 513, -845 / 4104, 0, 0],
         [-8 / 27, 2, -3544 / 2565, 1859 / 4104, -11 / 40, 0]])

    B = np.array(
        [[25 / 216, 0, 1408 / 2565, 2197 / 4104, -1 / 5, 0],
         [16 / 135, 0, 6656 / 12825, 28561 / 56430, -9 / 50, 2 / 55]])

    def __init__(self,
                 function,
                 dimension,
                 stepsize,
                 tolerance):
        self.F = function
        self.dim = dimension
        self.h = stepsize
        self.tol = tolerance

    def step(self,
             Win):
        s = np.zeros((6, self.dim))

        for i in range(0, 6):
            s[i, :] = self.F(Win + self.h * self.A[i, 0:i].dot(s[0:i, :]))

        Zout = Win + self.h * (self.B[0, :].dot(s))
        Wout = Win + self.h * (self.B[1, :].dot(s))

        E = np.linalg.norm(Wout - Zout, 2) / np.linalg.norm(Wout, 2)
        return Wout, E

    def safeStep(self,
                 Win):
        Wout, E = self.step(Win)
        # Check if the error is tolerable
        if not self.isErrorTolerated(E):
            # Try to adjust the optimal step length
            self.adjustStep(E)
            Wout, E = self.step(Win)
        # If the error is still not tolerable
        counter = 0
        while not self.isErrorTolerated(E):
            # Try if dividing the steplength with 2 helps.
            self.divideStepByTwo()
            Wout, E = self.step(Win)
            counter = counter + 1
            if counter > 10:
                sys.exit(-1)

        self.adjustStep(E)

        return Wout, E

    def isErrorTolerated(self, E):
        return E < self.tol

    def adjustStep(self, E):
        if E == 0:
            s = 2
        else:
            s = m.pow(self.tol * self.h / (2 * E), 0.25)
        self.h = s * self.h

    def divideStepByTwo(self):
        self.h = self.h / 2

    def setStepLength(self, stepLength):
        self.h = stepLength


def F(Y):
    M = np.array([[-1, -1],
                  [1, -1]])
    res = np.ones(3)
    res[1:3] = M.dot(Y[1:3])
    return res


def current_time_seconds():
    return time.time()


    #Gjennomfører RungeKuttaFehlberg54 for en gitt toleranse og slutt-t
    #Returnerer tiden det tok å beregne
def main(tol, tEnd):
    print("tol: ", tol)

    W = np.array([0, 1, 0])
    h = 0.1
    rkf54 = RungeKuttaFehlberg54(F, 3, h, tol)
    accumulated_error = 0

    start_in = current_time_seconds()
    while W[0] < tEnd:
        W, E = rkf54.safeStep(W)
        accumulated_error += E

    rkf54.setStepLength(tEnd - W[0])
    W, E = rkf54.step(W)
    tid_in = current_time_seconds() - start_in
    #global_trunc = W[1:3] - [np.exp(10) * np.cos(10), -np.exp(10) * np.sin(10)]
    global_trunc = W[1:3] - [np.exp(-tEnd)*np.cos(tEnd), np.exp(-tEnd)*np.sin(tEnd)]

    print("Global feil: ", global_trunc)
    print("Akkumulert lokal feil: ", accumulated_error)
    print("\n")
    return tid_in

    #Kjører main() for toleranse = 10^0, ..., 10^-35
    #tEnd kan endres ved å endre t her
if __name__ == "__main__":
    # execute only if run as a script
    e_mach = 7./3 - 4./3 - 1
    print(e_mach)
    forhold = []
    t = 1.0
    optimal = (0.0, 0.0)
    forrige_forhold = 0
    for i in range(0, 35):
        tid = main(np.power(10.0, -i), t)
        forholdet = tid / t
        forhold.append(forhold)
        if (forholdet > forrige_forhold) and (forholdet < 1):
            optimal = (np.power(10.0, -i), forholdet)

        forrige_forhold = forholdet
    print(optimal)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 20:26:05 2018

@author: rivertz
"""

import numpy as np
import math as m
import sys


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
                 func,
                 dimension,
                 step_size,
                 tolerance):
        self.F = func
        self.dim = dimension
        self.h = step_size
        self.tol = tolerance

    def step(self,
             w_in):
        s = np.zeros((6, self.dim))

        for i in range(0, 6):
            s[i, :] = self.F(w_in + self.h * self.A[i, 0:i].dot(s[0:i, :]))

        z_out = w_in + self.h * (self.B[0, :].dot(s))
        w_out = w_in + self.h * (self.B[1, :].dot(s))

        E = np.linalg.norm(w_out - z_out, 2) / np.linalg.norm(w_out, 2)
        return w_out, E

    def safe_step(self,
                  w_in):
        w_out, E = self.step(w_in)
        # Check if the error is tolerable
        if not self.is_error_tolerated(E):
            # Try to adjust the optimal step length
            self.adjust_step(E)
            w_out, E = self.step(w_in)
        # If the error is still not tolerable
        counter = 0
        while not self.is_error_tolerated(E):
            # Try if dividing the steplength with 2 helps. 
            self.divide_step_by_two()
            w_out, E = self.step(w_in)
            counter = counter + 1
            if counter > 10:
                sys.exit(-1)

        self.adjust_step(E)

        return w_out, E

    def is_error_tolerated(self, E):
        return E < self.tol

    def adjust_step(self, E):
        if E == 0:
            s = 2
        else:
            s = m.pow(self.tol * self.h / (2 * E), 0.25)
        self.h = s * self.h

    def divide_step_by_two(self):
        self.h = self.h / 2

    def set_step_length(self, step_length):
        self.h = step_length


def F(Y):
    M = np.array([[0.49119653, 0.32513304, 0.98057799],
                  [0.20768544, 0.97699416, 0.18220559],
                  [0.96407071, 0.18373237, 0.95307793]])
    res = np.ones(4)
    res[1:4] = M.dot(Y[1:4])
    return res


def main():
    W = np.array([0, 1, 1, 1])
    h = 0.1
    tol = 05e-14
    t_end = 2.0
    rkf54 = RungeKuttaFehlberg54(F, 4, h, tol)

    while W[0] < t_end:
        W, E = rkf54.safe_step(W)

    rkf54.set_step_length(t_end - W[0])
    W, E = rkf54.step(W)

    print(W, E)


if __name__ == "__main__":
    # execute only if run as a script
    main()

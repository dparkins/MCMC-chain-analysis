#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, gaussian_kde, scoreatpercentile
from scipy.integrate import quad
from scipy import constants as const
from matplotlib.pylab import uniform
from matplotlib.mlab import griddata
import random
import csv
import emcee
import math
import time

def ln_prob(params):
    """Gaussian likelihood function"""
    x = params[0]
    y = params[1]

    chi2_value = (x-0.762)**2/(0.12523**2) + (y+0.438556)**2/(0.56687**2)
    return -0.5*chi2_value


if __name__ == "__main__":
    time0 = time.time()
    ndim = 2
    cov_in = np.matrix('1.0, 0.0; 0., 1.0')
    multiple_logical = raw_input("Multiple chains (y/n)?")
    if (multiple_logical == 'Y' or multiple_logical == 'y'):
        num_chains = 4
    elif (multiple_logical == 'N' or multiple_logical == 'n'):
        num_chains = 1
    else:
        print('Input not recognised')
        stop

    for ichain in range(0,num_chains):
        sampler = emcee.MHSampler(cov_in, ndim, ln_prob)

        if num_chains > 1:
            file_name = "chain_{0:4d}.dat".format(ichain)
            random_x = random.uniform(-500.0,500.0)
            random_y = random.uniform(-500.0,500.0)
            p0 = (random_x,random_y)
        else:
            file_name = "chain_long.dat"
            p0 = (-100.0,100.0)

        f = open(file_name, "w")
        f.close()
        for result in sampler.sample(p0, iterations=200000, storechain=False):
            position = result[0]
            chi2_out = result[1]
            f = open(file_name, "a")
            f.write("{0:s}\n".format(" ".join(map(str,position))))
            f.close()

#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, gaussian_kde, scoreatpercentile
from scipy.integrate import quad
from scipy import constants as const
from matplotlib.pylab import uniform
from matplotlib.mlab import griddata
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
    sampler = emcee.MHSampler(cov_in, ndim, ln_prob)
    p0 = (-100.0,100.0)
    f = open("chain.dat", "w")
    f.close()
    for result in sampler.sample(p0, iterations=20000, storechain=False):
        position = result[0]
        chi2_out = result[1]
        f = open("chain.dat", "a")
        f.write("{0:s}\n".format(" ".join(map(str,position))))
        f.close()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pytest
import time


from dgtd.maxwellDriver import *
from dgtd.mesh1d import *
from dgtd.maxwell1d import *
from fdtd.fdtd1d import *


from nodepy import runge_kutta_method as rk

#······················································

def plot(sp, driver):
    for _ in range(1000):
        driver.step()
        plt.plot(sp.x, driver['E'],'b')
        plt.plot(sp.xH, driver['H'],'r')
        plt.ylim(-1, 1)
        plt.title(driver.timeIntegrator.time)
        plt.grid(which='both')
        plt.pause(0.01)
        plt.cla()
        
#······················································


def test_fdtd_pec():
    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="PEC"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2', CFL=1.0)

    s0 = 0.25
    initialFieldE = np.exp(-(sp.x)**2/(2*s0**2))
    driver['E'][:] = initialFieldE[:]

    #plot(sp, driver)

    driver.run_until(2.0)

    finalFieldE = driver['E'][:]
    R = np.corrcoef(initialFieldE, -finalFieldE)
    assert R[0, 1] > 0.9999


def test_fdtd_periodic():
    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="Periodic"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2')

    s0 = 0.25
    initialFieldE = np.exp(-(sp.x)**2/(2*s0**2))
    driver['E'][:] = initialFieldE[:]

    #plot(sp, driver)

    driver.run_until(6.0)

    finalFieldE = driver['E'][:]
    R = np.corrcoef(initialFieldE, finalFieldE)
    assert R[0, 1] > 0.9999


def test_fdtd_pmc():

    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="PMC"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2')

    s0 = 0.25
    initialFieldH = np.exp(-(sp.xH)**2/(2*s0**2))
    driver['H'][:] = initialFieldH[:]

    #plot(sp, driver)

    driver.run_until(2.0)

    finalFieldH = driver['H'][:]
    R = np.corrcoef(initialFieldH.ravel(), -finalFieldH.ravel())
    assert R[0, 1] > 0.9999


def test_fdtd_pmc_cfl_equals_half():
    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="PMC"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2', CFL=0.5)

    s0 = 0.25
    initialFieldH = np.exp(-(sp.xH)**2/(2*s0**2))
    driver['H'][:] = initialFieldH[:]

    #plot(sp, driver)

    driver.run_until(2.0)

    finalFieldH = driver['H'][:]

    R = np.corrcoef(initialFieldH, -finalFieldH)
    assert R[0, 1] > 0.9999


def test_fdtd_mur():
    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="Mur"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2')

    s0 = 0.25
    initialFieldE = np.exp(-(sp.x)**2/(2*s0**2))
    driver['E'][:] = initialFieldE[:]

    #plot(sp, driver)

    driver.run_until(8.0)

    finalFieldE = driver['E'][:]
    assert np.allclose(finalFieldE, 0.0, atol=1e-3)


def test_fdtd_mur_right_only():

    t_final = 8.0

    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="Mur"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2', CFL=1.0)

    s0 = 0.25
    driver['E'][:] = np.exp(-(sp.x)**2/(2*s0**2))
    driver['H'][:] = np.exp(-(sp.xH - driver.dt/2)**2/(2*s0**2))

    # plot(sp, driver)

    driver.run_until(t_final)

    finalFieldE = driver['E'][:]
    assert np.allclose(finalFieldE, 0.0, atol=1e-3)


def test_fdtd_right_only_mur_and_pec():

    bdrs = {
        "LEFT": "Mur",
        "RIGHT": "PEC",
    }

    t_final = 8.0

    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label = bdrs))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2', CFL=1.0)

    s0 = 0.25
    driver['E'][:] = np.exp(-(sp.x)**2/(2*s0**2))
    initialFieldE =  driver['E'][:]
    driver['H'][:] = np.exp(-(sp.xH - driver.dt/2)**2/(2*s0**2))

    #plot(sp, driver)
        
    driver.run_until(8.0)

    finalFieldE = driver['E'][:]
    assert np.allclose(finalFieldE, 0.0, atol=1e-3)


def test_fdtd_check_initial_conditions_GW_right():

    x_min = -4.0
    x_max = 4.0
    k_elements = 400
    t_final = 1.0

    sp = FDTD1D(mesh=Mesh1D(x_min, x_max, k_elements, boundary_label="PEC"))
    driver = MaxwellDriver(sp, timeIntegratorType='LF2', CFL=1.0)
    c0 = 1.0

    s0 = 0.25
    driver['E'][:] = np.exp(-(sp.x)**2/(2*s0**2))
    driver['H'][:] = np.exp(-(sp.xH - driver.dt/2)**2/(2*s0**2))
    
    #plot(sp, driver)

    driver.run_until(t_final)

    evolvedE = driver['E'][:]

    expectedE = np.exp(-(sp.x - c0*t_final)**2/(2*s0**2))

    R1 = np.corrcoef(expectedE, evolvedE)
    assert R1[0, 1] > 0.995


def test_fdtd_periodic_lserk():
    sp = FDTD1D(mesh=Mesh1D(-1.0, 1.0, 100, boundary_label="Periodic"))
    driver = MaxwellDriver(sp, CFL=1.5)

    s0 = 0.25
    initialFieldE = np.exp(-(sp.x)**2/(2*s0**2))
    driver['E'][:] = initialFieldE[:]

    #plot(sp, driver)

    driver.run_until(2.0)

    finalFieldE = driver['E'][:]
    R = np.corrcoef(initialFieldE, finalFieldE)
    assert R[0, 1] > 0.9999

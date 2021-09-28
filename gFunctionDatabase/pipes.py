# Jack C. Cook
# Sunday, September 26, 2021

import os
import json
import pygfunction as gt
import numpy as np


class HDPEDimensions:
    def __init__(self, standard='SDR-11'):
        self.standard = standard
        self.HDPEPipeDimensions = self.access_pipe_dimensions()

    def index_pipe(self, idx):
        # get the specific pipe
        pipe = self.HDPEPipeDimensions[self.standard]
        # get the index of the nominal pipe in the nominal pipe list
        nominal_size = pipe['Nominal Size (in)'][idx]
        r_in = pipe['Inside Diameter (mm)'][idx] / 2000.
        r_out = pipe['Outer Diameter (mm)'][idx] / 2000.
        return nominal_size, r_in, r_out

    def access_pipe_dimensions(self):
        path_to_hdpe = os.path.dirname(os.path.abspath(__file__))
        file_name = 'HDPEPipeDimensions.json'
        try:
            HDPEPipeDimensions = self.js_r(path_to_hdpe + r'/' + file_name)
        except:
            HDPEPipeDimensions = self.js_r(path_to_hdpe + r'\\' + file_name)
        return HDPEPipeDimensions

    @staticmethod
    def js_r(filename):
        with open(filename) as f_in:
            return json.load(f_in)


def pipe_selection(height: float, m_flow_borehole: float, fluid, epsilon,
                   HDPE: HDPEDimensions):
    global nominal_size, r_in, r_out, h_l, Re, f
    length = height * 2.  # Pipe length goes down and then up
    # Find pipe that is below 15 ft of head loss
    count = -1
    above_fifteen = True
    # Loop through HDPE SDR-11 pipe indices until the head loss is below
    # 15 ft
    while above_fifteen:
        count += 1
        nominal_size, r_in, r_out = HDPE.index_pipe(count)
        h_l, Re, f = pipe_dp(length, r_in, m_flow_borehole, fluid, epsilon)
        h_l /= 0.3048  # Head loss in feet

        if h_l <= 15.0:
            above_fifteen = False

    return nominal_size, r_in, r_out, h_l, Re, f


def shank_spacing(config, rb, rp_out):
    # This gives the shank spacing given a configuration A, B or C as defined
    # in Paul's thesis
    if config == 'A':
        shank = 0.
    elif config == 'B':
        total_distance = rb * 2.
        pipe_coverage = rp_out * 2. * 2.
        empty_space = total_distance - pipe_coverage
        shank = empty_space / 3.
    elif config == 'C':
        total_distance = rb * 2.
        pipe_coverage = rp_out * 2. * 2.
        shank = total_distance - pipe_coverage
    else:
        raise ValueError('Only A, B, or C configurations allowed.')

    return shank


def place_pipes(s, r_out, n_pipes):
    """ Positions pipes in an axisymetric configuration."""
    D_s = s / 2 + r_out
    pi = np.pi
    dt = pi / float(n_pipes)
    pos = [(0., 0.) for i in range(2 * n_pipes)]
    for i in range(n_pipes):
        pos[2 * i] = (
            D_s * np.cos(2.0 * i * dt + pi),
            D_s * np.sin(2.0 * i * dt + pi))
        pos[2 * i + 1] = (D_s * np.cos(2.0 * i * dt + pi + dt),
                          D_s * np.sin(2.0 * i * dt + pi + dt))
    return pos


def pipe_dp(length: float, r_in: float, m_flow_borehole: float,
            fluid: gt.media.Fluid, epsilon: float):
    # Computes the head loss in SI units (in meters)
    m_flow_pipe = m_flow_borehole
    # Darcy Weisbach friction factor
    f = gt.pipes.fluid_friction_factor_circular_pipe(
        m_flow_pipe, r_in, fluid.mu, fluid.rho, epsilon)
    # Fluid velocity
    V_flow = m_flow_pipe / fluid.rho
    A_cs = np.pi * r_in**2
    V = V_flow / A_cs
    # Reynolds number
    Re = fluid.rho * V * (r_in * 2.) / fluid.mu
    # gravitational constant gc is 1 in SI units
    g = 1.

    h_l = f * length / (r_in * 2.) * (V ** 2) / (2. * g)

    return h_l, Re, f

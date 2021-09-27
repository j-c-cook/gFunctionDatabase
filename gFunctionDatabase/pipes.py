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

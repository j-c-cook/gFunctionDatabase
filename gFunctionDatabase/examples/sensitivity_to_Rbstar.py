# Jack C. Cook
# Friday, September 24, 2021

"""
Sensitivity to effective borehole thermal resistance for the g-function computed
with the UIFT boundary condition
"""
import numpy as np
import pygfunction as gt
import PLAT
import gFunctionDatabase as gfdb
import matplotlib.pyplot as plt

log_time = [-8.5, -7.8, -7.2, -6.5, -5.9, -5.2, -4.5,
            -3.963, -3.27, -2.864, -2.577, -2.171, -1.884,
            -1.191, -0.497, -0.274, -0.051, 0.196, 0.419,
            0.642, 0.873, 1.112, 1.335, 1.679, 2.028, 2.275, 3.003]


def main():
    # Borehole dimensions
    H_values = [96.]                   # Borehole length (m)
    D = 2.                      # Borehole buried depth (m)
    B = 5.                  # Uniform borehole spacing (m)
    r_b_values = [150./1000./2.]       # Borehole radius (m)

    # Mass flow rate
    # For 2.5 GPM/ton and 250 ft/ton, the flow rate for pure water is 0.2 kg/s
    # flow rate of kg/s per 100 m of drilling to each borehole
    m_flow_borehole_per_100m = 0.2 / 100.
    # Find the mass flow rates at each height
    m_flow_borehole_design = [m_flow_borehole_per_100m * H_values[i]
                              for i in range(len(H_values))]

    # Fluid properties
    fluid = gt.media.Fluid(mixer='Water', percent=0)

    # Pipe properties
    epsilon = 2.0e-05  # HDPE Pipe roughness (m)

    # Pipe dimensions
    HDPE = gfdb.pipes.HDPEDimensions(standard='SDR-11')

    # Create BHEs with low Rb (A configuration), average Rb (B configuration)
    # and high Rb (C configuration)

    # Grout Thermal conductivity (W/m.K)
    k_g_a = 0.64  # Thermal conductivity to encourage low Rb
    k_g_b = 1.0  # Average thermal conductivity
    k_g_c = 2.77  # Thermal conductivity to encourage high Rb
    k_g_values = [k_g_a, k_g_b, k_g_c]

    # Grout properties
    # k_g = k_g_values[c]
    # grout = PLAT.media.ThermalProperty(k=k_g)

    # Ground properties
    k_s = 2.0  # Ground thermal conductivity (W/m.K)
    alpha = 1.0e-06  # Ground thermal diffusivity (m2/s)
    soil = PLAT.media.ThermalProperty(k=k_s)

    # Pipe properties
    k_p = 0.4       # Pipe thermal conductivity (W/m.K)

    # g-Function calculation options
    nSegments = 24
    options = {'nSegments': nSegments, 'disp': False}

    # Field of 7x10 (n=70) boreholes
    N_1 = 7
    N_2 = 10
    nBoreholes = N_1 * N_2

    H = H_values[0]
    r_b = r_b_values[0]
    boreField = gt.boreholes.rectangle_field(N_1, N_2, B, B, H, D, r_b)

    flow_rate = m_flow_borehole_design[0]
    nominal_size, r_in, r_out, h_l, Re, f = \
        gfdb.pipes.pipe_selection(H, flow_rate, fluid, epsilon, HDPE)

    # Time vector is based off of Hellstrom's 27 points
    ts = H ** 2 / (9. * alpha)  # Bore field characteristic time
    time_arr = np.exp(np.array(log_time)) * ts

    UIFT_gfunctions = []
    effective_borehole_resistances = []
    shank_spacings = []

    borehole_configurations = ['A', 'B', 'C']
    m_flow_borehole = m_flow_borehole_design[0]

    for c, config in enumerate(borehole_configurations):

        k_g = k_g_values[c]
        grout = PLAT.media.ThermalProperty(k=k_g)

        # Pipe positioning
        shank = gfdb.pipes.shank_spacing(config, r_b, r_out)
        shank_spacings.append(shank)
        pos = PLAT.media.Pipe.place_pipes(shank, r_out, 1)
        pipe = PLAT.media.Pipe(pos, r_in, r_out, shank, epsilon, k_p)

        UTubes = []
        for borehole in boreField:
            single_u_tube = PLAT.borehole_heat_exchangers.SingleUTube(
                m_flow_borehole, fluid, borehole, soil, grout, pipe)
            UTubes.append(single_u_tube)
        m_flow_network = m_flow_borehole * nBoreholes
        network = gt.networks.Network(
            boreField, UTubes, m_flow_network=m_flow_network, cp_f=fluid.cp,
            nSegments=nSegments)

        Rb = UTubes[0].compute_effective_borehole_resistance()
        effective_borehole_resistances.append(Rb)

        print('{0} configuration Rb: {1:.4f}'.format(config, Rb))

        # Calculate the g-function for equal inlet fluid temperature
        gfunc_equal_Tf_in_i = gt.gfunction.gFunction(
            network, alpha, time=time_arr, boundary_condition='MIFT',
            options=options)
        UIFT_gfunctions.append(gfunc_equal_Tf_in_i)

    # -------------------------------------------------------------------------
    # Evaluate the g-functions for the borefield
    # -------------------------------------------------------------------------

    # Calculate the g-function for uniform heat extraction rate
    gfunc_uniform_Q = gt.gfunction.gFunction(
        boreField, alpha, time=time_arr, boundary_condition='UHTR',
        options=options)

    # Calculate the g-function for uniform borehole wall temperature
    gfunc_uniform_T = gt.gfunction.gFunction(
        boreField, alpha, time=time_arr, boundary_condition='UBWT',
        options=options)

    # Create table providing variation of parameters to change effective
    # borehole thermal resistance
    print('\tHigh $R_b^*$\tAverage $R_b^*$\tLow $R_b^*$')

    grout_string = 'Grout conductivity, $k_g$ (W/m.K)'
    for i in range(len(k_g_values)):
        grout_string += '\t' + str(k_g_values[i])
    print(grout_string)

    shank_string = 'Shank spacing, $s$ (m)'
    for i in range(len(shank_spacings)):
        shank_string += '\t' + str(round(shank_spacings[i], 3))
    print(shank_string)

    Rb_string = 'Eff. Borehole Resistance, $R_b^*$ (m.K/W)'
    for i in range(len(effective_borehole_resistances)):
        Rb_string += '\t' + str(round(effective_borehole_resistances[i], 4))
    print(Rb_string)

    # -------------------------------------------------------------------------
    # Plot g-functions
    # -------------------------------------------------------------------------

    fig = gt.gfunction._initialize_figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'ln$(t/t_s)$')
    ax.set_ylabel(r'$g$-function')
    gt.gfunction._format_axes(ax)

    ax.plot(log_time, gfunc_uniform_Q.gFunc, label='UHF')
    ax.plot(log_time, gfunc_uniform_T.gFunc, '--', label='UBHWT')

    for i in range(len(UIFT_gfunctions)):
        ax.plot(
            log_time, UIFT_gfunctions[i].gFunc,
            label='UIFT (Configuration ' + borehole_configurations[i] +
                  ', $R_b^*$='+str(round(effective_borehole_resistances[i], 2)))

    fig.legend(loc=2)
    fig.tight_layout()

    fig.savefig('g-function_variation.png')

    return


if __name__ == '__main__':
    main()

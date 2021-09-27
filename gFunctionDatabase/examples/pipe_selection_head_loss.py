# Jack C. Cook
# Saturday, September 25, 2021

import pygfunction as gt
import gFunctionDatabase as gfdb


def main():
    # For 2.5 GPM/ton and 250 ft/ton, the flow rate for pure water is 0.2 kg/s
    m_flow_borehole = 0.2 / 100.  # kg/s per 100 m of flow to each borehole
    # The borehole lengths selected for the library
    borehole_lengths = [24, 48, 96, 192, 384]

    # Roughness of HDPE pipe
    epsilon = 2.0e-05

    # Find the mass flow rates at each height
    m_flow_borehole_design = [m_flow_borehole * borehole_lengths[i]
                              for i in range(len(borehole_lengths))]
    print('Mass flow rates based on height (kg/s):')
    print(list(zip(borehole_lengths, m_flow_borehole_design)))

    # Access to HDPE pipe dimensions
    HDPE = gfdb.pipes.HDPEDimensions(standard='SDR-11')

    # Fluid properties
    fluid = gt.media.Fluid(mixer='Water', percent=0)

    print(50 * '-')
    # Create table providing information about pipe design
    print('$H$ (m)\tNominal Size (in)\t $D_i$ (mm)\t'
          '$D_o$ (mm)\t$f$\t$Re$\t$h_L$ (ft)\t$\dot{m_b}$ (kg/s)')

    for i in range(len(borehole_lengths)):
        length = borehole_lengths[i] * 2.  # Pipe length goes down and then up
        # Find pipe that is below 15 ft of head loss
        count = -1
        above_fifteen = True
        # Loop through HDPE SDR-11 pipe indices until the head loss is below
        # 15 ft
        while above_fifteen:
            count += 1
            nominal_size, r_in, r_out = HDPE.index_pipe(count)
            _m_flow_borehole = m_flow_borehole_design[i]
            h_l, Re, f = gfdb.pipes.pipe_dp(length, r_in, _m_flow_borehole,
                                            fluid, epsilon)
            h_l /= 0.3048  # Head loss in feet

            if h_l <= 15.0:
                above_fifteen = False

        ID = round((r_in * 2000.), 2)
        OD = round((r_out * 2000.), 2)

        print('{0}\t{1}\t{2}\t{3}\t{4:.3f}\t{5:.0f}\t{6:.2f}\t{7}'.
              format(borehole_lengths[i], nominal_size, ID, OD, f, Re, h_l,
                     _m_flow_borehole))


if __name__ == '__main__':
    main()

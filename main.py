import json
import numpy as np
import os.path 

from ImportSXSSimulation import ImportSimulation
from FundamentalFit import FundamentalFit
from ComputeOmegas import ComputeOmegas
from Plots import Plots
from FitOvertone import FitOvertone
from SaveParameters import SaveParameters
class ComputeQNMParameters():
    """Compute QNMs parameters by fitting the fundamental mode
        and the first overtone to the waveform data.
    """

    def __init__(
        self,
        file_path,
        lm_modes,
        lmn_modes,
        lm_dominant,
        ):
        self._create_folders(file_path)
        
        # import simulation info
        with open(file_path+'/metadata.json') as f:
            par_simu = json.load(f)

        par_simu['final_spin'] = np.sqrt(sum(x**2 for x in par_simu['remnant_dimensionless_spin']))
        # import SXS simulation data and save waveform to data/waveforms
        ImportSimulation(file_path, lm_modes, lmn_modes, lm_dominant)
        # compute the QNM frequencies of this simulation and save to data/omegas
        compute_omegas = ComputeOmegas() 
        omegas_sim = compute_omegas.compute_omega(par_simu['final_spin'], lmn_modes, 'sim', file_path)

        fit_fundamental = FundamentalFit(file_path, lm_modes, lm_dominant)

        omegas_spin = compute_omegas.compute_omega(fit_fundamental.a_M, lmn_modes, 'fit', file_path)

        plots = Plots()

        # plot derivative of the phase and fundamental modes of fitting and simulation
        label_dominant = f'l{lm_dominant[0]}m{lm_dominant[1]}'
        for mode in lm_modes:
            key = f'l{mode[0]}m{mode[1]}'
            mode = f'({mode[0]},{mode[1]},0)'
            plots.plot_d_theta(label_dominant, key, omegas_spin[mode]['omega_r'], omegas_sim[mode]['omega_r'], file_path)

        FitOvertone(file_path, omegas_sim, lm_dominant, lm_dominant)
        SaveParameters(file_path, lm_modes, lm_dominant)

    def _create_folders(self, file_path):
        # create folders for figures and data
        if not os.path.exists('figs' + file_path[-4:]):
            os.makedirs('figs' + file_path[-4:])

        if not os.path.exists('data' + file_path[-4:]):
            os.makedirs('data' + file_path[-4:])

events = [

          ]

for event in events:
    if __name__ == '__main__':
        lm_modes = ((2,2), (2,1), (3,3), (4,4))
        lmn_modes = ((2,2,0), (2,2,1), (3,3,0), (4,4,0), (2,1,0), (2,2,2))
        lm_dominant = (2,2)
        file_path = 'import_data' + event
        ComputeQNMParameters(file_path, lm_modes, lmn_modes, lm_dominant)

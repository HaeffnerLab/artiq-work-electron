from pulse_sequence import PulseSequence
from subsequences.noisy_phase_rabi_excitation import NoisyPhaseRabiExcitation
from subsequences.state_preparation import StatePreparation
from artiq.experiment import *
# import numpy as np


class QRM(PulseSequence):
    PulseSequence.accessed_params = {
        "QRM.line_selection",
        "QRM.amplitude_729",
        "QRM.att_729",
        "QRM.channel_729",
        "QRM.duration",
        "QRM.selection_sideband",
        "QRM.order",
        "QRM.delta",
        "QRM.noise_parameter"
    }

    PulseSequence.scan_params = dict(
        QRM=[
            ("QRM", ("QRM.duration", 0., 100e-6, 20, "us")),
            ("QRM", ("QRM.att_729", 0*dB, 32*dB, 1*dB, "dB"))
        ])

    def run_initially(self):
        self.stateprep = self.add_subsequence(StatePreparation)
        self.qrm = self.add_subsequence(NoisyPhaseRabiExcitation)
        self.qrm.channel_729 = self.p.QRM.channel_729
        self.set_subsequence["QRM"] = self.set_subsequence_QRM

    @kernel
    def set_subsequence_rabiflopping(self):
        self.qrm.duration = self.get_variable_parameter("QRM_duration")
        self.qrm.amp_729 = self.RabiFlopping_amplitude_729
        self.qrm.att_729 = self.get_variable_parameter("QRM_att_729")
        self.qrm.freq_729 = self.calc_frequency(
            self.qrm_line_selection, 
            detuning=self.qrm_detuning,
            sideband=self.qrm_selection_sideband,
            order=self.qrm_order, 
            dds=self.qrm_channel_729
        )
        self.qrm.noise_list

    @kernel
    def QRM(self):
        self.qrm.phase_ref_time = now_mu()
        self.stateprep.run(self)
        self.qrm.run(self)
       


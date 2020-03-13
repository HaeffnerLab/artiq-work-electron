from pulse_sequence import PulseSequence
from subsequences.rabi_excitation import RabiExcitation
from subsequences.state_preparation import StatePreparation
from subsequences.setup_single_ion_vaet import SetupSingleIonVAET
from artiq.experiment import *


class SingleIonVAET(PulseSequence):
    PulseSequence.accessed_params = {
        "SingleIonVAET.line_selection",
        "SingleIonVAET.DP_amp",
        "SingleIonVAET.DP_att",
        "SingleIonVAET.J_amp",
        "SingleIonVAET.J_att",
        "SingleIonVAET.Δ_amp",
        "SingleIonVAET.Δ_att",
        "SingleIonVAET.RSB_amp",
        "SingleIonVAET.RSB_att",
        "SingleIonVAET.BSB_amp",
        "SingleIonVAET.BSB_att",
        "SingleIonVAET.ν_eff",
        "SingleIonVAET.rotate_in_y",
        "SingleIonVAET.rotate_out_y",
        "SingleIonVAET.duration",
        "SingleIonVAET.selection_sideband",
        "SingleIonVAET.line_selection",
        "Rotation729G.amplitude",
        "Rotation729G.att",
        "Rotation729G.pi_time"
    }


    PulseSequence.scan_params.update(
        SingleIonVAET=[
            ("SingleIonVAET", ("SingleIonVAET.duration", 0., 1000*ms, 20, "ms"))
        ]
    )

    def run_initially(self):
        self.stateprep = self.add_subsequence(StatePreparation)
        self.basis_rotation = self.add_subsequence(RabiExcitation)
        self.vaet = self.add_subsequence(SetupSingleIonVAET)

    @kernel
    def set_subsequence_single_ion_vaet(self):
        self.vaet.duration = self.get_variable_parameter("SingleIonVAET_duration")
        self.basis_rotation.amp_729 = self.Rotation729G_amplitude
        self.basis_rotation.att_729 = self.Rotation729G_att
        self.basis_rotation.duration = self.Rotation729G_pi_time / 2
        self.basis_rotation.freq_729 = self.calc_frequency(
            self.Rotation729G_line_selection,
            dds="729G"
        )

    @kernel
    def SingleIonVAET(self):
        pass
        # phase_ref_time = now_mu()
        # self.basis_rotation.phase_ref_time = phase_ref_time
        # self.vaet.phase_ref_time = phase_ref_time

        # self.stateprep.run(self)
        # if self.SingleIonVAET_rotate_in_y:
        #     self.basis_rotation.run(self)
        # self.vaet.run(self)
        # if self.SingleIonVAET_rotate_out_y:
        #     self.basis_rotation.phase_729 = 180.
        #     self.basis_rotation.run(self)

    
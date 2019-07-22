from artiq.experiment import *
from artiq.coredevice.ad9910 import PHASE_MODE_TRACKING
import numpy as np

class RabiExcitation:
    freq_729="Excitation_729.rabi_excitation_frequency"
    amp_729="Excitation_729.rabi_excitation_amplitude"
    att_729="Excitation_729.rabi_excitation_att"
    phase_729="Excitation_729.rabi_excitation_phase"
    channel_729="Excitation_729.channel_729"
    duration="Excitation_729.rabi_excitation_duration"
    line_selection="Excitation_729.line_selection"
    sp_amp_729="Excitation_729.single_pass_amplitude"
    sp_att_729="Excitation_729.single_pass_att"
    phase_ref_time=np.int64(0)

    def subsequence(self):
        r = RabiExcitation
        self.get_729_dds(r.channel_729)
        print("r.phase_ref_time", r.phase_ref_time)
        self.core.break_realtime()
        self.dds_729.set(r.freq_729,
                         amplitude=r.amp_729,
                         phase=r.phase_729 / 360.,
                         phase_mode=PHASE_MODE_TRACKING,
                         ref_time_mu=r.phase_ref_time)
        self.dds_729.set_att(r.att_729)
        sp_freq_729 = 80*MHz + self.get_offset_frequency(r.channel_729)
        self.dds_729_SP.set(sp_freq_729, amplitude=r.sp_amp_729,
                             phase_mode=PHASE_MODE_TRACKING, ref_time_mu=r.phase_ref_time)
        self.dds_729_SP.set_att(r.sp_att_729)
        
        with parallel:
            self.dds_729.sw.on()
            self.dds_729_SP.sw.on()
        delay(r.duration)
        with parallel:
            self.dds_729.sw.off()
            self.dds_729_SP.sw.off()
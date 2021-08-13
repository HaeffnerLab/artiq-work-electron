from artiq.experiment import *
import numpy as np
from artiq.coredevice.ad9910 import PHASE_MODE_ABSOLUTE

class RAP:
    T="RAP.duration"
    delta="RAP.detuning_max"
    omega="RAP.amp_max"
    ss="RAP.stark_shift"
    aux_strength="RAP.aux_strength"
    aux_att="RAP.aux_att"
    att="RAP.att"
    line_selection="RAP.line_selection"
    sideband_selection="RAP.sideband_selection"
    order="RAP.order"
    dp_amp="RAP.dp_amp"
    dp_att="RAP.dp_att"
    channel="RAP.channel_729"
    beta="RAP.beta"

    def subsequence(self):
        r = RAP

        dp_freq = self.calc_frequency(
                r.line_selection,
                dds=r.channel,
                sideband=r.sideband_selection,
                order=r.order,
            )
        sp_offset_freq = self.get_offset_frequency(r.channel)
        sp_freq = 80*MHz + sp_offset_freq

        # Setup DP
        self.dds_729.set(
                dp_freq,
                amplitude=r.dp_amp,
                phase_mode=PHASE_MODE_ABSOLUTE
            )
        self.dds_729.set_att(r.dp_att)

        # Setup RAP_amp
        self.dds_RAP_amp.set_frequency(400*MHz + sp_offset_freq)
        self.dds_RAP_amp.set_phase_mode(PHASE_MODE_ABSOLUTE)
        self.dds_RAP_amp.set_att(r.att)
        # self.dds_RAP_amp.set_amplitude(1.0)

        # Setup RAP_freq
        self.dds_RAP_freq.set_frequency(80*MHz)
        self.dds_RAP_freq.set_amplitude(r.omega)
        self.dds_RAP_freq.set_phase_mode(PHASE_MODE_ABSOLUTE)
        self.dds_RAP_freq.set_att(0.0)

        # Setup RAP_aux
        self.dds_RAP_aux.set(
                sp_freq,
                amplitude=r.aux_strength
            )
        self.dds_RAP_aux.set_att(r.aux_att)

        # Run it
        with parallel:
            self.trigger.on()
            self.dds_RAP_amp.cpld.io_update.pulse_mu(8)
            self.dds_RAP_freq.cpld.io_update.pulse_mu(8)
            self.dds_RAP_amp.sw.on()
            self.dds_RAP_freq.sw.on()
            self.dds_RAP_aux.sw.on()
        delay(r.T)
        with parallel:
            self.dds_RAP_amp.sw.off()
            self.dds_RAP_freq.sw.off()
            self.dds_RAP_aux.sw.off()
            self.trigger.off()

        self.dds_RAP_amp.set_cfr1()
        self.dds_RAP_freq.set_cfr1()
        


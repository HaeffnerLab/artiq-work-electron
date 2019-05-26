from artiq.experiment import *
# from pulse_sequence import get_729_dds, calc_frequency
# from subsequence import Subsequence


class SidebandCooling:
    line_selection="SidebandCooling.line_selection"
    selection_sideband="SidebandCooling.selection_sideband"
    order="SidebandCooling.order"
    stark_shift="SidebandCooling.order"
    channel_729="StatePreparation.channel_729"
    repump_additional="OpticalPumpingContinuous.optical_pumping_continuous_duration"
    amplitude_729="SidebandCooling.amplitude_729"
    att_729="SidebandCooling.att_729"
    duration="SidebandCoolingContinuous.sideband_cooling_continuous_duration"

    sequential_enable="SequentialSBCooling.enable"
    sequential_channel_729="SequentialSBCooling.channel_729"

    sequential1_enable="SequentialSBCooling1.enable"
    sequential1_channel_729="SequentialSBCooling1.channel_729"

    sequential2_enable="SequentialSBCooling2.enable"
    sequential2_channel_729="SequentialSBCooling2.channel_729"

    def subsequence(self):
        self.get_729_dds(SidebandCooling.channel_729)#

        freq_729 = self.calc_frequency( 
                    SidebandCooling.line_selection,
                    detuning=SidebandCooling.stark_shift,
                    sideband=SidebandCooling.selection_sideband,
                    order=SidebandCooling.order,
                    dds=SidebandCooling.channel_729)
        print("FREQUENCY 729: ", freq_729)
        self.dds_729.set(freq_729, amplitude=SidebandCooling.amplitude_729)
        self.dds_729.set_att(SidebandCooling.att_729)
        
        krun(self)
        
        if SidebandCooling.sequential_enable:
            self.get_729_dds(SidebandCooling.sequential_channel_729)
            krun(self)

        if SidebandCooling.sequential1_enable:
            self.get_729_dds(SidebandCooling.sequential1_channel_729)
            krun(self)

        if SidebandCooling.sequential2_enable:
            self.get_729_dds(SidebandCooling.sequential2_channel_729)
            krun(self)
        
        
        
        delay(SidebandCooling.repump_additional)
        self.dds_854.sw.off()
        delay(SidebandCooling.repump_additional)
        self.dds_866.sw.off()

@kernel
def krun(self):
    with parallel:
        self.dds_729.sw.on()
        self.dds_729_SP.sw.on()
        self.dds_854.sw.on()
        self.dds_866.sw.on()
    delay(SidebandCooling.duration)
    with parallel:
        self.dds_729.sw.off()
        self.dds_729_SP.sw.off()

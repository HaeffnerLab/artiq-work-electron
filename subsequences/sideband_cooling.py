from artiq.experiment import *
from subsequences.optical_pumping import OpticalPumping

class SidebandCooling:
    line_selection="SidebandCooling.line_selection"
    selection_sideband="SidebandCooling.selection_sideband"
    order="SidebandCooling.order"
    stark_shift="SidebandCooling.stark_shift"
    channel_729="StatePreparation.channel_729"
    repump_additional="OpticalPumpingContinuous.optical_pumping_continuous_repump_additional"
    amplitude_729="SidebandCooling.amplitude_729"
    att_729="SidebandCooling.att_729"
    duration="SidebandCooling.duration"
    sp_amp_729="Excitation_729.single_pass_amplitude"
    sp_att_729="Excitation_729.single_pass_att"
    
    freq_866="SidebandCooling.frequency_866"
    amp_866="SidebandCooling.amplitude_866"
    att_866="SidebandCooling.att_866"
    
    freq_854="SidebandCooling.frequency_854"
    amp_854="SidebandCooling.amplitude_854"
    att_854="SidebandCooling.att_854"

    sideband_cooling_cycles="SidebandCooling.sideband_cooling_cycles"

    sequential_enable="SequentialSBCooling.enable"
    sequential_channel_729="SequentialSBCooling.channel_729"
    sequential_selection_sideband="SequentialSBcooling.selection_sideband"
    sequential_order="SequentialSBCooling.order"

    sequential1_enable="SequentialSBCooling1.enable"
    sequential1_channel_729="SequentialSBCooling1.channel_729"
    sequential1_selection_sideband="SequentialSBcooling1.selection_sideband"
    sequential1_order="SequentialSBCooling1.order"

    sequential2_enable="SequentialSBCooling2.enable"
    sequential2_channel_729="SequentialSBCooling2.channel_729"
    sequential2_selection_sideband="SequentialSBcooling2.selection_sideband"
    sequential2_order="SequentialSBCooling2.order"

    def add_child_subsequences(pulse_sequence):
        s = SidebandCooling
        s.op = pulse_sequence.add_subsequence(OpticalPumping)

    def subsequence(self):
        s = SidebandCooling

        num_cycles = int(s.sideband_cooling_cycles)
        for i in range(num_cycles):
            delay(100*us)

            self.get_729_dds(s.channel_729)
            freq_729 = self.calc_frequency(
                            s.line_selection,
                            detuning=s.stark_shift,
                            sideband=s.selection_sideband,
                            order=s.order,
                            dds=s.channel_729
                        )
            self.dds_729.set(freq_729, 
                            amplitude=s.amplitude_729)
            self.dds_729.set_att(s.att_729)
            self.dds_729_SP.set_amplitude(s.sp_amp_729)
            self.dds_729_SP.set_att(s.sp_att_729)
            self.dds_854.set(s.freq_854, 
                            amplitude=s.amp_854)
            self.dds_854.set_att(s.att_854)
            self.dds_866.set(s.freq_866, 
                            amplitude=s.amp_866)
            self.dds_866.set_att(s.att_866)
            with parallel:
                self.dds_854.sw.on()
                self.dds_866.sw.on()
                self.dds_729.sw.on()
                self.dds_729_SP.sw.on()
            delay(s.duration)
            with parallel:
                self.dds_729.sw.off()
                self.dds_729_SP.sw.off()
            s.op.run(self)
            delay(100*us)
            
            if s.sequential_enable:
                self.get_729_dds(s.sequential_channel_729)
                freq_729 = self.calc_frequency( 
                        s.line_selection,
                        detuning=s.stark_shift,
                        sideband=s.sequential_selection_sideband,
                        order=s.sequential_order,
                        dds=s.sequential_channel_729)
                self.dds_729.set(freq_729, 
                                amplitude=s.amplitude_729)
                self.dds_729.set_att(s.att_729)
                self.dds_729_SP.set_amplitude(s.sp_amp_729)
                self.dds_729_SP.set_att(s.sp_att_729)
                self.dds_854.set(s.freq_854, 
                                amplitude=s.amp_854)
                self.dds_854.set_att(s.att_854)
                self.dds_866.set(s.freq_866, 
                                amplitude=s.amp_866)
                self.dds_866.set_att(s.att_866)
                with parallel:
                    self.dds_854.sw.on()
                    self.dds_866.sw.on()
                    self.dds_729.sw.on()
                    self.dds_729_SP.sw.on()
                delay(s.duration)
                with parallel:
                    self.dds_729.sw.off()
                    self.dds_729_SP.sw.off()
                s.op.run(self)
                delay(100*us)

            if s.sequential1_enable:
                self.get_729_dds(s.sequential1_channel_729)
                freq_729 = self.calc_frequency( 
                        s.line_selection,
                        detuning=s.stark_shift,
                        sideband=s.sequential1_selection_sideband,
                        order=s.sequential1_order,
                        dds=s.sequential1_channel_729)
                self.dds_729.set(freq_729, 
                                amplitude=s.amplitude_729)
                self.dds_729.set_att(s.att_729)
                self.dds_729_SP.set_amplitude(s.sp_amp_729)
                self.dds_729_SP.set_att(s.sp_att_729)
                self.dds_854.set(s.freq_854, 
                                amplitude=s.amp_854)
                self.dds_854.set_att(s.att_854)
                self.dds_866.set(s.freq_866, 
                                amplitude=s.amp_866)
                self.dds_866.set_att(s.att_866)
                with parallel:
                    self.dds_854.sw.on()
                    self.dds_866.sw.on()
                    self.dds_729.sw.on()
                    self.dds_729_SP.sw.on()
                delay(s.duration)
                with parallel:
                    self.dds_729.sw.off()
                    self.dds_729_SP.sw.off()
                s.op.run(self)
                delay(100*us)

            if s.sequential2_enable:
                self.get_729_dds(s.sequential2_channel_729)
                freq_729 = self.calc_frequency( 
                        s.line_selection,
                        detuning=s.stark_shift,
                        sideband=s.sequential2_selection_sideband,
                        order=s.sequential2_order,
                        dds=s.sequential2_channel_729)
                self.dds_729.set(freq_729, 
                                amplitude=s.amplitude_729)
                self.dds_729.set_att(s.att_729)
                self.dds_729_SP.set_amplitude(s.sp_amp_729)
                self.dds_729_SP.set_att(s.sp_att_729)
                self.dds_854.set(s.freq_854, 
                                amplitude=s.amp_854)
                self.dds_854.set_att(s.att_854)
                self.dds_866.set(s.freq_866, 
                                amplitude=s.amp_866)
                self.dds_866.set_att(s.att_866)
                with parallel:
                    self.dds_854.sw.on()
                    self.dds_866.sw.on()
                    self.dds_729.sw.on()
                    self.dds_729_SP.sw.on()
                delay(s.duration)
                with parallel:
                    self.dds_729.sw.off()
                    self.dds_729_SP.sw.off()
                s.op.run(self)
                delay(100*us)
            
        delay(3 * s.repump_additional)
        with parallel:
            self.dds_854.sw.off()
            self.dds_866.sw.off()

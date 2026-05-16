import struct

class Upsampler:
    def __init__(self):
        self.reset()
        # Default values (0-100 scale usually)
        self.strength = 50
        self.treble = 50
        self.resonance = 50
        self.filter_strength = 50
        self.saturation = 50

    def reset(self):
        self.last = 0
        self.s1z1 = 0
        self.s1z2 = 0
        self.s2z1 = 0
        self.s2z2 = 0
        self.nz1 = 0
        self.nz2 = 0
        self.nz3 = 0
        self.nz4 = 0
        # Exciter state
        self.ex_z1 = 0

    def set_param(self, name, value):
        if hasattr(self, name):
            setattr(self, name, max(0, min(100, value)))

    def process(self, in_data):
        n_samples = len(in_data) // 2
        if n_samples == 0:
            return in_data
            
        samples_in = struct.unpack(f'<{n_samples}h', in_data)
        
        # Mapping sliders to internal deltas
        d_strength = self.strength - 50
        d_treble = self.treble - 50
        d_res = self.resonance - 50
        d_filt = self.filter_strength - 50
        d_sat = self.saturation - 50
        
        # Resonance and Saturation impact A2 and g_comp
        a2_val = 12000 + (d_res * (100 if d_res < 0 else 25))
        g_comp = 1024 + (d_sat * (6 if d_sat < 0 else 1))
        
        # Recovery/Exciter strength based on resonance and strength
        # This will be used to inject high-frequency armonics
        exciter_gain = max(0, (self.resonance * self.strength) >> 7)
        
        # Filter Coefficients
        B0, B1, B2, A1 = 1974, 3948, 1974, -15871
        f_mix = 16384 + (d_filt * 128)
        
        N1_B0, N1_B1, N1_B2, N1_A1, N1_A2 = 11160, -11540, 11160, -11540, 8000
        N2_B0, N2_B1, N2_B2, N2_A1, N2_A2 = 8000, 0, 8000, -12000, 6000
        
        out_samples = []
        _append = out_samples.append
        
        for c_s in samples_in:
            # Frequency Recovery Stage: Harmonic Excitation
            # Create a non-linear version of the signal to generate high armonics
            # We use absolute value (rectification) for a rich spectrum
            rectified = abs(c_s)
            # High-pass the rectified signal to keep only the "new" high frequencies
            hp_exciter = rectified - self.ex_z1
            self.ex_z1 = rectified
            
            # Scale the recovered frequencies
            recovered_hf = (hp_exciter * exciter_gain) >> 7

            for j in range(4):
                # 4x Oversampling Linear Interpolation
                smp = self.last + ((c_s - self.last) * j >> 2)
                
                # Add the recovered high frequencies back to the interpolated signal
                # We add them only to the sub-samples to avoid DC offset issues
                if j > 0:
                    smp = max(-32768, min(32767, smp + (recovered_hf >> (j % 2))))

                # Stages 1 & 2 (Saturation & Character)
                v1 = (smp * B0 + self.s1z1) >> 14
                self.s1z1 = smp * B1 - A1 * v1 + self.s1z2
                self.s1z2 = smp * B2 - a2_val * v1
                
                v2 = (v1 * B0 + self.s2z1) >> 14
                self.s2z1 = v1 * B1 - A1 * v2 + self.s2z2
                self.s2z2 = v1 * B2 - a2_val * v2
                
                # Dual Notch Filters (Anti-Aliasing)
                vn1 = v2 - ((N1_A1 * self.nz1 + N1_A2 * self.nz2) >> 14)
                o_n1 = (N1_B0 * vn1 + N1_B1 * self.nz1 + N1_B2 * self.nz2) >> 14
                self.nz2 = self.nz1
                self.nz1 = vn1
                
                vn2 = o_n1 - ((N2_A1 * self.nz3 + N2_A2 * self.nz4) >> 14)
                o_n2 = (N2_B0 * vn2 + N2_B1 * self.nz3 + N2_B2 * self.nz4) >> 14
                self.nz4 = self.nz3
                self.nz3 = vn2
                
                # Apply filter mix
                filt_s = (o_n2 * f_mix) >> 14
                
                # Final Mix with Treble control
                b_val = 50 + (d_treble if d_treble < 0 else (d_treble >> 2) + (d_treble >> 4))
                final_s = (filt_s + (filt_s >> 2) + (filt_s * b_val >> 7))
                
                # Apply Compensation and Clamp
                final_s = (final_s * g_comp) >> 10
                final_s = max(-32768, min(32767, final_s))
                
                _append(final_s)
            
            self.last = c_s
            
        return struct.pack(f'<{len(out_samples)}h', *out_samples)

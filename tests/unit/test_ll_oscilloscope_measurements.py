from typing import List, NamedTuple, Optional
from functools import partial
import unittest
import ll_oscilloscope_measurements as llom

class WaveForm(NamedTuple):
    times: List[float] = None
    chan0: List[float] = None
    chan1: List[float] = None


class LlOscilloscopeMeasurementsTest(unittest.TestCase):

    @classmethod
    def load_waveforms(kls, filename: str):
        times = []
        chan0 = []
        chan1 = []

        with open("./tests/data/oscilloscope_measurements/" + filename + ".csv", "r") as waveform_file:
            for line in waveform_file.readlines():
                if line.startswith("sep="):
                    continue
                if line.startswith("Time"):
                    continue
                if not line.strip():
                    continue

                line_split = line.split()
                times.append(float(line_split[0]))
                chan0.append(float(line_split[1]))
                chan1.append(float(line_split[2]))
        
        return WaveForm(times, chan0, chan1)
    
    def setUp(kls):
        # sine waves
        kls.sine_0_4vpp_1khz = kls.load_waveforms("sine_0.4vpp_1khz")
        kls.sine_1vpp_1khz = kls.load_waveforms("sine_1vpp_1khz")
        kls.sine_1vpp_200hz = kls.load_waveforms("sine_1vpp_200hz")
        kls.sine_1vpp_200hz_2v_offset = kls.load_waveforms("sine_1vpp_200hz_2v_offset")
        kls.sine_1vpp_200hz_m2v_offset = kls.load_waveforms("sine_1vpp_200hz_-2v_offset")
        kls.sine_5vpp_1khz = kls.load_waveforms("sine_5vpp_1khz")
        kls.sine_1vpp_1khz_delayed_5 = kls.load_waveforms("sine_1vpp_1khz_delayed_5")
        kls.sine_1vpp_1khz_delayed_10 = kls.load_waveforms("sine_1vpp_1khz_delayed_10")
        kls.sine_1vpp_1khz_delayed_15 = kls.load_waveforms("sine_1vpp_1khz_delayed_15")
        kls.sine_1vpp_1khz_delayed_20 = kls.load_waveforms("sine_1vpp_1khz_delayed_20")

        kls.sine_1vpp_200hz_delayed_25 = kls.load_waveforms("sine_1vpp_200hz_delayed_25")
        kls.sine_1vpp_200hz_delayed_50 = kls.load_waveforms("sine_1vpp_200hz_delayed_50")
        kls.sine_1vpp_200hz_delayed_62 = kls.load_waveforms("sine_1vpp_200hz_delayed_62")
        kls.sine_1vpp_200hz_delayed_75 = kls.load_waveforms("sine_1vpp_200hz_delayed_75")
        kls.sine_1vpp_200hz_delayed_100 = kls.load_waveforms("sine_1vpp_200hz_delayed_100")
        kls.sine_1vpp_200hz_delayed_125 = kls.load_waveforms("sine_1vpp_200hz_delayed_125")

        # square waves
        kls.square_0_4vpp_1khz = kls.load_waveforms("square_0.4vpp_1khz")
        kls.square_1vpp_1khz = kls.load_waveforms("square_1vpp_1khz")
        kls.square_1vpp_200hz = kls.load_waveforms("square_1vpp_200hz")
        kls.square_1vpp_200hz_2v_offset = kls.load_waveforms("square_1vpp_200hz_2v_offset")
        kls.square_1vpp_200hz_m2v_offset = kls.load_waveforms("square_1vpp_200hz_-2v_offset")
        kls.square_5vpp_1khz = kls.load_waveforms("square_5vpp_1khz")

        kls.square_1vpp_1khz_delayed_5 = kls.load_waveforms("square_1vpp_1khz_delayed_5")
        kls.square_1vpp_1khz_delayed_10 = kls.load_waveforms("square_1vpp_1khz_delayed_10")
        kls.square_1vpp_1khz_delayed_15 = kls.load_waveforms("square_1vpp_1khz_delayed_15")
        kls.square_1vpp_1khz_delayed_20 = kls.load_waveforms("square_1vpp_1khz_delayed_20")

        kls.square_1vpp_200hz_delayed_25 = kls.load_waveforms("square_1vpp_200hz_delayed_25")
        kls.square_1vpp_200hz_delayed_50 = kls.load_waveforms("square_1vpp_200hz_delayed_50")
        kls.square_1vpp_200hz_delayed_62 = kls.load_waveforms("square_1vpp_200hz_delayed_62")
        kls.square_1vpp_200hz_delayed_75 = kls.load_waveforms("square_1vpp_200hz_delayed_75")
        kls.square_1vpp_200hz_delayed_100 = kls.load_waveforms("square_1vpp_200hz_delayed_100")
        kls.square_1vpp_200hz_delayed_125 = kls.load_waveforms("square_1vpp_200hz_delayed_125")

        # triangle waves
        kls.triangle_1vpp_1khz = kls.load_waveforms("triangle_1vpp_1khz")
        kls.triangle_1vpp_200hz = kls.load_waveforms("triangle_1vpp_200hz")
        kls.triangle_5vpp_1khz = kls.load_waveforms("triangle_5vpp_1khz")

        # rampup waves
        kls.rampup_1vpp_1khz = kls.load_waveforms("rampup_1vpp_1khz")
        kls.rampup_1vpp_200hz = kls.load_waveforms("rampup_1vpp_200hz")
        kls.rampup_5vpp_1khz = kls.load_waveforms("rampup_5vpp_1khz")

    def _calculate_and_test(self, waveform: WaveForm, expected: float, delta: float, function: str, other_channel_samples: Optional[List[float]] = None, channel: str = 'chan0'):
        # the default is minSampleRate=25_000, 2ms
        # this means: if you take the first 500 samples
        # with a sample rate of 25000, what you get is
        # 10 blocks of 2ms each (500 * (1 / 25000) = 0.02 for the whole
        # diagram of 10 blocks)
        result = llom.calculate_oscilloscope_measurement(function, getattr(waveform, channel), 25000.0, other_channel_samples)
        self.assertAlmostEqual(result, expected, delta=delta)

    def test_voltage_peak_to_peak(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_peak_to_peak')

        calculate_and_test(self.sine_1vpp_1khz, expected=1.0, delta=0.1)
        calculate_and_test(self.square_1vpp_1khz, expected=1.0, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=1.0, delta=0.1)
        calculate_and_test(self.rampup_1vpp_1khz, expected=1.0, delta=0.1)

        calculate_and_test(self.sine_5vpp_1khz, expected=5.0, delta=0.5)
        calculate_and_test(self.square_5vpp_1khz, expected=5.0, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=5.0, delta=0.5)
        calculate_and_test(self.rampup_5vpp_1khz, expected=5.0, delta=0.5)

        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.4, delta=0.04)
        calculate_and_test(self.square_0_4vpp_1khz, expected=0.4, delta=0.4)

        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=1.0, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=1.0, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=1.0, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=1.0, delta=0.1)

    def test_voltage_average(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_average')

        calculate_and_test(self.sine_1vpp_1khz, expected=0.0, delta=0.3)
        calculate_and_test(self.square_1vpp_1khz, expected=0.0, delta=0.3)
        calculate_and_test(self.triangle_1vpp_1khz, expected=0.0, delta=0.3)

        calculate_and_test(self.sine_5vpp_1khz, expected=0.0, delta=0.5)
        calculate_and_test(self.square_5vpp_1khz, expected=0.0, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=0.0, delta=0.5)

        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.0, delta=0.04)
        calculate_and_test(self.square_0_4vpp_1khz, expected=0.0, delta=0.4)

        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=2.0, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=-2.0, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=2.0, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=-2.0, delta=0.1)

    def test_voltage_rms(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_rms')

        calculate_and_test(self.sine_1vpp_1khz, expected=0.355, delta=0.1)
        calculate_and_test(self.square_1vpp_1khz, expected=0.5, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=0.2904, delta=0.1)

        calculate_and_test(self.sine_5vpp_1khz, expected=1.759, delta=0.5)
        calculate_and_test(self.square_5vpp_1khz, expected=2.5, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=1.44, delta=0.5)

        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.1174, delta=0.04)
        calculate_and_test(self.square_0_4vpp_1khz, expected=0.2, delta=0.04)

        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=2.0, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=2.0, delta=0.1)

    def test_voltage_max(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_max')

        calculate_and_test(self.sine_1vpp_1khz, expected=0.5, delta=0.1)
        calculate_and_test(self.square_1vpp_1khz, expected=0.5, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=0.5, delta=0.1)
        calculate_and_test(self.rampup_1vpp_1khz, expected=0.5, delta=0.1)

        calculate_and_test(self.sine_5vpp_1khz, expected=2.5, delta=0.5)
        calculate_and_test(self.square_5vpp_1khz, expected=2.5, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=2.5, delta=0.5)
        calculate_and_test(self.rampup_5vpp_1khz, expected=2.5, delta=0.5)

        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.2, delta=0.05)
        calculate_and_test(self.square_0_4vpp_1khz, expected=0.2, delta=0.5)

        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=2.5, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=-1.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=2.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=-1.5, delta=0.1)

    def test_voltage_min(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_min')

        calculate_and_test(self.sine_1vpp_1khz, expected=-0.5, delta=0.1)
        calculate_and_test(self.square_1vpp_1khz, expected=-0.5, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=-0.5, delta=0.1)
        calculate_and_test(self.rampup_1vpp_1khz, expected=-0.5, delta=0.1)

        calculate_and_test(self.sine_5vpp_1khz, expected=-2.5, delta=0.5)
        calculate_and_test(self.square_5vpp_1khz, expected=-2.5, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=-2.5, delta=0.5)
        calculate_and_test(self.rampup_5vpp_1khz, expected=-2.5, delta=0.5)

        calculate_and_test(self.sine_0_4vpp_1khz, expected=-0.2, delta=0.05)
        calculate_and_test(self.square_0_4vpp_1khz, expected=-0.2, delta=0.5)

        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=1.5, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=-2.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=1.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=-2.5, delta=0.1)

    def test_voltage_base(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_base')

        calculate_and_test(self.square_1vpp_1khz, expected=-0.5, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=-2.46, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=-0.1656, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=1.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=-2.5, delta=0.1)

    def test_voltage_top(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_top')

        calculate_and_test(self.square_1vpp_1khz, expected=0.5, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=2.46, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=0.1656, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=2.5, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=-1.5, delta=0.1)

    def test_voltage_amplitude(self):
        calculate_and_test = partial(self._calculate_and_test, function='voltage_amplitude')

        calculate_and_test(self.square_1vpp_1khz, expected=1.0, delta=0.1)
        calculate_and_test(self.sine_1vpp_1khz, expected=1.0, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=1.0, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=5.0, delta=0.5)
        calculate_and_test(self.sine_5vpp_1khz, expected=5.0, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=5.0, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=0.4, delta=0.5)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.4, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=1, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=1, delta=0.1)

    def test_preshoot(self):
        calculate_and_test = partial(self._calculate_and_test, function='preshoot')

        calculate_and_test(self.square_1vpp_1khz, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_1khz, expected=0.1, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=0.1, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.sine_5vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=0.1, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.1, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=0.1, delta=0.1)

    def test_overshoot(self):
        calculate_and_test = partial(self._calculate_and_test, function='overshoot')

        calculate_and_test(self.square_1vpp_1khz, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_1khz, expected=0.1, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=0.1, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.sine_5vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=0.1, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=0.1, delta=0.5)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=0.1, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=0.1, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=0.1, delta=0.1)

    def test_frequency(self):
        calculate_and_test = partial(self._calculate_and_test, function='frequency')

        calculate_and_test(self.square_1vpp_1khz, expected=1_000, delta=0.1)
        calculate_and_test(self.sine_1vpp_1khz, expected=1_000, delta=0.1)
        calculate_and_test(self.triangle_1vpp_1khz, expected=1_000, delta=0.1)

        calculate_and_test(self.square_5vpp_1khz, expected=1_000, delta=0.5)
        calculate_and_test(self.sine_5vpp_1khz, expected=1_000, delta=0.5)
        calculate_and_test(self.triangle_5vpp_1khz, expected=1_000, delta=0.5)

        calculate_and_test(self.square_0_4vpp_1khz, expected=1_000, delta=0.5)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=1_000, delta=0.5)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=200, delta=0.1)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=200, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=200, delta=0.1)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=200, delta=0.1)

    def test_period(self):
        calculate_and_test = partial(self._calculate_and_test, function='period')

        calculate_and_test(self.square_1vpp_1khz, expected=1/1_000, delta=0)
        calculate_and_test(self.sine_1vpp_1khz, expected=1/1_000, delta=0)
        calculate_and_test(self.triangle_1vpp_1khz, expected=1/1_000, delta=0)

        calculate_and_test(self.square_5vpp_1khz, expected=1/1_000, delta=0)
        calculate_and_test(self.sine_5vpp_1khz, expected=1/1_000, delta=0)
        calculate_and_test(self.triangle_5vpp_1khz, expected=1/1_000, delta=0)

        calculate_and_test(self.square_0_4vpp_1khz, expected=1/1_000, delta=0)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=1/1_000, delta=0)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=1/200, delta=0)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=1/200, delta=0)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=1/200, delta=0)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=1/200, delta=0)

    def test_rise_time(self):
        calculate_and_test = partial(self._calculate_and_test, function='rise_time')

        time_sin_1v_200hz = 0.00162
        time_sin_1v_1khz = 0.00036
        time_triang_1khz = 0.00044
        time_square_200hz = 1/25_000 # min time (1 sample)
        time_square_1khz = 1/25_000 # min time (1 sample)

        calculate_and_test(self.sine_1vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)
        calculate_and_test(self.square_1vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.triangle_1vpp_1khz, expected=time_triang_1khz, delta=0.0001)

        calculate_and_test(self.sine_1vpp_200hz, expected=time_sin_1v_200hz, delta=0.0001)
        calculate_and_test(self.square_1vpp_200hz, expected=time_square_200hz, delta=0.0001)

        calculate_and_test(self.square_5vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.sine_5vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)
        calculate_and_test(self.triangle_5vpp_1khz, expected=time_triang_1khz, delta=0.0001)

        calculate_and_test(self.square_0_4vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=time_square_200hz, delta=0.0001)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=time_square_200hz, delta=0.0001)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=time_sin_1v_200hz, delta=0.0001)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=time_sin_1v_200hz, delta=0.0001)

    def test_fall_time(self):
        calculate_and_test = partial(self._calculate_and_test, function='fall_time')

        time_sin_1v_200hz = 0.00162
        time_sin_1v_1khz = 0.00036
        time_triang_1khz = 0.00044
        time_square_200hz = 1/25_000 # min time (1 sample)
        time_square_1khz = 1/25_000 # min time (1 sample)

        calculate_and_test(self.sine_1vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)
        calculate_and_test(self.square_1vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.triangle_1vpp_1khz, expected=time_triang_1khz, delta=0.0001)

        calculate_and_test(self.sine_1vpp_200hz, expected=time_sin_1v_200hz, delta=0.0001)
        calculate_and_test(self.square_1vpp_200hz, expected=time_square_200hz, delta=0.0001)

        calculate_and_test(self.square_5vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.sine_5vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)
        calculate_and_test(self.triangle_5vpp_1khz, expected=time_triang_1khz, delta=0.0001)

        calculate_and_test(self.square_0_4vpp_1khz, expected=time_square_1khz, delta=0.0001)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=time_sin_1v_1khz, delta=0.0001)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=time_square_200hz, delta=0.0001)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=time_square_200hz, delta=0.0001)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=time_sin_1v_200hz, delta=0.0001)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=time_sin_1v_200hz, delta=0.0001)

    def test_positive_duty_cycle(self):
        calculate_and_test = partial(self._calculate_and_test, function='positive_duty_cycle')

        calculate_and_test(self.sine_1vpp_1khz, expected=50, delta=3)
        calculate_and_test(self.square_1vpp_1khz, expected=50, delta=3)
        calculate_and_test(self.triangle_1vpp_1khz, expected=50, delta=3)

        calculate_and_test(self.sine_1vpp_200hz, expected=50, delta=3)
        calculate_and_test(self.square_1vpp_200hz, expected=50, delta=3)

        calculate_and_test(self.square_5vpp_1khz, expected=50, delta=3)
        calculate_and_test(self.sine_5vpp_1khz, expected=50, delta=3)
        calculate_and_test(self.triangle_5vpp_1khz, expected=50, delta=3)

        calculate_and_test(self.square_0_4vpp_1khz, expected=50, delta=3)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=50, delta=3)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=50, delta=3)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=50, delta=3)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=50, delta=3)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=50, delta=3)

    def test_positive_width(self):
        calculate_and_test = partial(self._calculate_and_test, function='positive_width')

        positive_width_1khz = 0.0005
        positive_width_200hz = 0.0025

        calculate_and_test(self.sine_1vpp_1khz, expected=positive_width_1khz, delta=0.0001)
        calculate_and_test(self.square_1vpp_1khz, expected=positive_width_1khz, delta=0.0001)
        calculate_and_test(self.triangle_1vpp_1khz, expected=positive_width_1khz, delta=0.0001)

        calculate_and_test(self.sine_1vpp_200hz, expected=positive_width_200hz, delta=0.001)
        calculate_and_test(self.square_1vpp_200hz, expected=positive_width_200hz, delta=0.001)

        calculate_and_test(self.square_5vpp_1khz, expected=positive_width_1khz, delta=0.0001)
        calculate_and_test(self.sine_5vpp_1khz, expected=positive_width_1khz, delta=0.0001)
        calculate_and_test(self.triangle_5vpp_1khz, expected=positive_width_1khz, delta=0.0001)

        calculate_and_test(self.square_0_4vpp_1khz, expected=positive_width_1khz, delta=0.0001)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=positive_width_1khz, delta=0.0001)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=positive_width_200hz, delta=0.001)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=positive_width_200hz, delta=0.001)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=positive_width_200hz, delta=0.001)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=positive_width_200hz, delta=0.001)

    def test_negative_width(self):
        calculate_and_test = partial(self._calculate_and_test, function='negative_width')

        negative_width_1khz = 0.0005
        negative_width_200hz = 0.0025

        calculate_and_test(self.sine_1vpp_1khz, expected=negative_width_1khz, delta=0.0001)
        calculate_and_test(self.square_1vpp_1khz, expected=negative_width_1khz, delta=0.0001)
        calculate_and_test(self.triangle_1vpp_1khz, expected=negative_width_1khz, delta=0.0001)

        calculate_and_test(self.sine_1vpp_200hz, expected=negative_width_200hz, delta=0.001)
        calculate_and_test(self.square_1vpp_200hz, expected=negative_width_200hz, delta=0.001)

        calculate_and_test(self.square_5vpp_1khz, expected=negative_width_1khz, delta=0.0001)
        calculate_and_test(self.sine_5vpp_1khz, expected=negative_width_1khz, delta=0.0001)
        calculate_and_test(self.triangle_5vpp_1khz, expected=negative_width_1khz, delta=0.0001)

        calculate_and_test(self.square_0_4vpp_1khz, expected=negative_width_1khz, delta=0.0001)
        calculate_and_test(self.sine_0_4vpp_1khz, expected=negative_width_1khz, delta=0.0001)

        calculate_and_test(self.square_1vpp_200hz_2v_offset, expected=negative_width_200hz, delta=0.001)
        calculate_and_test(self.square_1vpp_200hz_m2v_offset, expected=negative_width_200hz, delta=0.001)
        calculate_and_test(self.sine_1vpp_200hz_2v_offset, expected=negative_width_200hz, delta=0.001)
        calculate_and_test(self.sine_1vpp_200hz_m2v_offset, expected=negative_width_200hz, delta=0.001)

    def test_phase_delay(self):
        calculate_and_test = partial(self._calculate_and_test, function='phase_delay')

        # TODO: not sure about these values

        calculate_and_test(self.sine_1vpp_200hz, other_channel_samples=self.sine_1vpp_200hz.chan0, expected=0, delta=7)
        calculate_and_test(self.sine_1vpp_200hz, other_channel_samples=self.sine_1vpp_200hz_delayed_125.chan0, expected=0, delta=7)
        calculate_and_test(self.sine_1vpp_200hz, other_channel_samples=self.sine_1vpp_200hz_delayed_62.chan0, expected=-180, delta=7)

        calculate_and_test(self.square_1vpp_200hz, other_channel_samples=self.square_1vpp_200hz.chan0, expected=0, delta=7)
        calculate_and_test(self.square_1vpp_200hz, other_channel_samples=self.square_1vpp_200hz_delayed_125.chan0, expected=0, delta=7)
        calculate_and_test(self.square_1vpp_200hz, other_channel_samples=self.square_1vpp_200hz_delayed_62.chan0, expected=-180, delta=7)

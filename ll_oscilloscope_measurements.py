#!/usr/bin/python
#
# Copyright (C) 2023 onwards LabsLand, Inc.
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

"""
This code calculates standard measurement values that you can find in an
oscilloscope, given a particular signal.

Some of the functions were based on page 79 at:
https://ece.engin.umich.edu/wp-content/uploads/sites/4/2019/08/D3000-97000_man.pdf

as well as other documentation.
"""

import logging

from typing import List, Optional

import numpy as np
from scipy import signal

logger = logging.getLogger(__name__)

ERROR_RESULT = -1000


class MeasurementFunctions:  # pylint: disable=too-few-public-methods
    """
    List of functions currently supported
    """
    voltage_peak_to_peak = 'voltage_peak_to_peak'
    voltage_average = 'voltage_average'
    voltage_rms = 'voltage_rms'
    voltage_max = 'voltage_max'
    voltage_min = 'voltage_min'
    voltage_base = 'voltage_base'
    voltage_top = 'voltage_top'
    voltage_amplitude = 'voltage_amplitude'
    preshoot = 'preshoot'
    overshoot = 'overshoot'
    positive_duty_cycle = 'positive_duty_cycle'
    rise_time = 'rise_time'
    fall_time = 'fall_time'
    frequency = 'frequency'
    period = 'period'
    positive_width = 'positive_width'
    negative_width = 'negative_width'
    phase_delay = 'phase_delay'


def calculate_oscilloscope_measurement(
        function: str,
        samples: List[float],
        sampling_rate: Optional[float] = None,
        other_channel_samples: Optional[List[float]] = None
) -> float:
    """
    Given the name of 'function', the samples and optionally the sampling rate
    and the samples in the other channel, provide the result of the
    measurement.

    Internally, this function calls the rest of the functions in this module.
    Data is a list of float.
    """
    if function == 'none':
        return 0.0

    if function is None:
        return -1.0

    np_samples = np.array(samples, float)

    functions_using_only_samples = {
        MeasurementFunctions.voltage_peak_to_peak:
            calculate_voltage_peak_to_peak,
        MeasurementFunctions.voltage_average:
            calculate_voltage_average,
        MeasurementFunctions.voltage_rms:
            calculate_voltage_rms,
        MeasurementFunctions.voltage_max:
            calculate_voltage_max,
        MeasurementFunctions.voltage_min:
            calculate_voltage_min,
        MeasurementFunctions.voltage_base:
            calculate_voltage_base,
        MeasurementFunctions.voltage_top:
            calculate_voltage_top,
        MeasurementFunctions.voltage_amplitude:
            calculate_voltage_amplitude,
        MeasurementFunctions.preshoot:
            calculate_preshoot,
        MeasurementFunctions.overshoot:
            calculate_overshoot,
        MeasurementFunctions.positive_duty_cycle:
            calculate_positive_duty_cycle,
    }

    if function in functions_using_only_samples:
        return functions_using_only_samples[function](np_samples)

    functions_using_samples_and_sampling_rate = {
        MeasurementFunctions.rise_time: calculate_rise_time,
        MeasurementFunctions.fall_time: calculate_fall_time,
        MeasurementFunctions.frequency: calculate_frequency,
        MeasurementFunctions.period: calculate_period,
        MeasurementFunctions.positive_width: calculate_positive_width,
        MeasurementFunctions.negative_width: calculate_negative_width,
    }

    if function in functions_using_samples_and_sampling_rate:
        function_to_call = functions_using_samples_and_sampling_rate[function]
        return function_to_call(np_samples, sampling_rate)

    if function == MeasurementFunctions.phase_delay:
        return calculate_phase_delay(
                np_samples,
                sampling_rate,
                other_channel_samples
        )

    # else... just send a clearly wrong number
    return ERROR_RESULT


def calculate_voltage_peak_to_peak(samples: np.ndarray) -> float:
    """
    Calculate the voltage peak to peak of an array.
    """
    return np.max(samples) - min(samples)


def calculate_voltage_average(samples: np.ndarray) -> float:
    """
    Calculate the voltage average of the samples
    """
    return np.mean(samples)


def calculate_voltage_rms(samples: np.ndarray) -> float:
    """
    Calculate the RMS (Root Mean Square)
    """
    samples_squared = samples ** 2
    mean_squared = np.mean(samples_squared)
    return np.sqrt(mean_squared)


def calculate_voltage_max(samples: np.ndarray) -> float:
    """
    Calculate the max voltage of the samples
    """
    return np.max(samples)


def calculate_voltage_min(samples: np.ndarray) -> float:
    """
    Calculate the min voltage of the samples
    """
    return np.min(samples)


def calculate_voltage_base(samples: np.ndarray) -> float:
    """
    Calculate the VBase (voltage base) of the samples.

    We use as definition the average of the bottom 10% of the sample values.
    """
    # VBase is the mean of the bottom 10% of the values
    sorted_samples = np.sort(samples)
    bottom_10_percent_samples = sorted_samples[:round(0.1*len(samples))]
    vbase = np.mean(bottom_10_percent_samples)
    return vbase


def calculate_voltage_top(samples: np.ndarray) -> float:
    """
    Calculate the VTop (voltage top) of the samples.

    We use as definition the average of the top 10% of the sample values.
    """
    sorted_samples = np.sort(samples)
    top_10_percent_samples = sorted_samples[-round(0.1*len(samples)):]
    vtop = np.mean(top_10_percent_samples)
    return vtop


def calculate_voltage_amplitude(samples: np.ndarray) -> float:
    """
    Calculate the voltage amplitude of the samples.

    We use as definition the difference between the VTop and VBase
    """
    # Don't call calculate_voltage_base and calculate_voltage_top to avoid
    # sorting twice
    sorted_samples = np.sort(samples)
    top_10_percent_samples = sorted_samples[-round(0.1*len(samples)):]
    vtop = np.mean(top_10_percent_samples)
    bottom_10_percent_samples = sorted_samples[:round(0.1*len(samples))]
    vbase = np.mean(bottom_10_percent_samples)
    return vtop - vbase


def calculate_preshoot(samples: np.ndarray) -> float:
    """
    Calculate the preshoot of the samples.

    We use as definition the difference between VBase and Vmin
    """
    vbase = calculate_voltage_base(samples)
    vmin = calculate_voltage_min(samples)
    return vbase - vmin


def calculate_overshoot(samples: np.ndarray) -> float:
    """
    Calculate the overshoot of the samples.

    We use as definition the difference between Vmax and VTop
    """
    vmax = calculate_voltage_max(samples)
    vtop = calculate_voltage_top(samples)
    return vmax - vtop


def calculate_rise_time(samples: np.ndarray, sampling_rate: float) -> float:
    """
    Calculate the rise time of the samples.
    """
    dc_offset = np.mean(samples)
    samples_without_offset = samples - dc_offset

    # We are using the amplitude without bases,
    # of the signal is from the maximum to the minimum
    amplitude = max(samples_without_offset) - min(samples_without_offset)

    # Identify the amplitude value corresponding to the 10% level
    # of the signal. Find 10% of the  peak amplitude.
    amplitude_10_percent = (
            dc_offset
            + 0.1 * amplitude
            + min(samples_without_offset)
    )

    # Identify the index the amplitude value corresponding to the
    # 90% level of the signal. Find 90%  of the peak amplitude.
    amplitude_90_percent = (
            dc_offset
            + 0.9 * amplitude
            + min(samples_without_offset)
    )

    # Find the index corresponding to the first occurrence of the
    # amplitude crossing the 90% level (rising edge).
    latest_under_10 = None
    next_over_90 = None
    for position, sample in enumerate(samples):
        if sample <= amplitude_10_percent:
            latest_under_10 = position
        elif latest_under_10 is not None:
            if sample >= amplitude_90_percent:
                # We were under 10% in latest_under_10
                # and now we are over 90%.
                next_over_90 = position
                break

    if next_over_90 is None or latest_under_10 is None:
        # Error: no change found
        return ERROR_RESULT

    # Calculate the rise time by subtracting the time corresponding
    # to the 10% level from the time corresponding to the 90% level.
    # This can be done by multiplying the index difference by the
    # sampling period.
    sampling_period = 1 / sampling_rate
    rise_time = (next_over_90 - latest_under_10) * sampling_period
    return rise_time


def calculate_fall_time(samples: np.ndarray, sampling_rate: float) -> float:
    """
    Calculate the fall time of the samples.
    """
    dc_offset = np.mean(samples)
    samples_without_offset = samples - dc_offset

    # We are using the amplitude without bases,
    # of the signal is from the maximum to the minimum
    amplitude = max(samples_without_offset) - min(samples_without_offset)

    # Identify the amplitude value corresponding to the 10% level
    # of the signal. Find 10% of the  peak amplitude.
    amplitude_10_percent = (
            dc_offset
            + 0.1 * amplitude
            + min(samples_without_offset)
    )

    # Identify the index the amplitude value corresponding to the
    # 90% level of the signal. Find 90%  of the peak amplitude.
    amplitude_90_percent = (
            dc_offset
            + 0.9 * amplitude
            + min(samples_without_offset)
    )

    # Find the index corresponding to the first occurrence of the
    # amplitude crossing the 90% level (rising edge).
    latest_over_90 = None
    next_under_10 = None
    for position, sample in enumerate(samples):
        if sample >= amplitude_90_percent:
            latest_over_90 = position
        elif latest_over_90 is not None:
            if sample <= amplitude_10_percent:
                # We were under 10% in latest_over_90
                # and now we are over 90%.
                next_under_10 = position
                break

    if next_under_10 is None or latest_over_90 is None:
        # Error: no change found
        return ERROR_RESULT

    sampling_period = 1 / sampling_rate
    fall_time = (next_under_10 - latest_over_90) * sampling_period
    return fall_time


def calculate_frequency(samples: np.ndarray, sampling_rate: float) -> float:
    """
    Calculate the frequency of the samples using Welch's method:

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html
    """
    frequencies, psd = signal.welch(
                            samples,
                            sampling_rate,
                            nperseg=len(samples))
    peak_index = np.argmax(psd)
    return frequencies[peak_index]


def calculate_period(samples: np.ndarray, sampling_rate: float) -> float:
    """
    Calculate the period of the samples (1/frequency).
    """
    frequency = calculate_frequency(samples, sampling_rate)
    return 1 / frequency


def calculate_positive_duty_cycle(samples: np.ndarray) -> float:
    """
    Calculate the positive duty cycle (% of samples that are "HIGH").

    This does not mean positive (as in "more than 5V"), but only that
    they are on the high side.
    """
    mean = np.mean(samples)
    positive_samples = np.sum(samples > mean)

    return (positive_samples / len(samples)) * 100


def calculate_positive_width(
        samples: np.ndarray,
        sampling_rate: float
) -> float:
    """
    Calculate the positive width, using the Welch's method as in frequency.
    """
    _, psd = signal.welch(samples, sampling_rate, nperseg=len(samples))
    peak_index = np.argmax(psd)

    # peak_index now is how many periods are there in
    # the 20ms (or whatever 10 x 1/ sampling_rate is)
    # that we have. 1 KHz will get us peak_index=20

    # time that the signal is "HIGH" in a period
    mean = np.mean(samples)
    positive_samples = np.sum(samples > mean)

    return positive_samples / peak_index / sampling_rate


def calculate_negative_width(
        samples: np.ndarray,
        sampling_rate: float
) -> float:
    """
    Calculate the negative width, using the Welch's method as in frequency.
    """
    _, psd = signal.welch(samples, sampling_rate, nperseg=len(samples))
    peak_index = np.argmax(psd)

    # peak_index now is how many periods are there in
    # the 20ms (or whatever 10 x 1/ sampling_rate is)
    # that we have. 1 KHz will get us peak_index=20

    # time that the signal is "HIGH" in a period
    mean = np.mean(samples)
    negative_samples = np.sum(samples < mean)

    return negative_samples / peak_index / sampling_rate


def calculate_phase_delay(
        samples: np.ndarray,
        sampling_rate: float,
        other_channel_samples: List[float]
) -> float:
    """
    Calculate the phase delay between two signals.
    """
    # Compute the cross-correlation between the two signals
    cross_correlation = np.correlate(
                            samples,
                            other_channel_samples,
                            mode='full')

    # Find the index of the maximum value in the cross-correlation function
    max_index = np.argmax(cross_correlation)

    # Calculate the phase delay in terms of sample shifts
    phase_delay_samples = len(samples) - max_index - 1

    # Convert the phase delay to degrees
    time_delay = phase_delay_samples / sampling_rate
    signal_frequency = calculate_frequency(samples, sampling_rate)

    phase_delay_degrees = (time_delay * signal_frequency) * 360
    return phase_delay_degrees

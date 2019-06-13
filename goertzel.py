# Originate:
# Mark (1): 1270 Hz sine wave
# Space (0): 1070 Hz sine wave
# Answer:
# Mark (1): 2225 Hz sine wave
# Space (0): 2025 Hz sine wave

# Goertzel Filter Algorithm
# Decide on the sampling rate.
# Choose the block size, N.
# Precompute one cosine and one sine term.
# Precompute one coefficient.

import numpy as np


class Goertzel:

    def __init__(self, sample_rate, block_size, target_frequency):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.target_frequency = target_frequency
        self.k = 0
        self.w = 0
        self.cosine = 0
        self.sine = 0
        self.coeff = 0
        self.q0 = 0  # Current
        self.q1 = 0  # Previous
        self.q2 = 0  # Previous Previous
        self.real = 0
        self.imag = 0
        self.magnitude = 0

        # Compute constants at instantiation
        self.compute_constants()

    # Compute constants for Goertzel Filter equation
    def compute_constants(self):
        # self.k = 0.5 + (self.block_size * self.target_frequency)/self.sample_rate
        self.k = (self.block_size * self.target_frequency)/self.sample_rate
        self.w = ((2 * np.pi) / self.block_size) * self.k
        self.cosine = np.cos(self.w)
        self.sine = np.sin(self.w)
        self.coeff = 2 * self.cosine

    # Goertzel Filter
    def filter(self, samples):
        for sample in samples:
            self.q0 = self.coeff * self.q1 - self.q2 + sample
            self.q2 = self.q1
            self.q1 = self.q0

        self.real = self.q1 - self.q2 * self.cosine
        self.imag = self.q2 * self.sine
        self.magnitude = np.sqrt(np.square(self.real) + np.square(self.imag))

        self.reset()

    # Reset Q values for next filter operation
    def reset(self):
        self.q0 = 0
        self.q1 = 0
        self.q2 = 0

    def __str__(self):
        return (f'Real: {self.real}\n'
                f'Imag: {self.imag}\n'
                f'Magnitude Squared: {np.square(self.magnitude)}\n'
                f'Magnitude: {self.magnitude}\n')

    def __gt__(self, other):
        return self.magnitude > other.magnitude

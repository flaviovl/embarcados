MAX_CONTROL_SIGNAL = 100
MIN_CONTROL_SIGNAL = -100
SAMPLE_PERIOD = 1  # Período de Amostragem (ms)
KP = 30
KI = 0.2
KD = 400


class PIDController:
    def __init__(self, kp=KP, ki=KI, kd=KD):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.ref_temp = 0  # temperatura de referencia (objetivo)
        self.last_error = 0  # erro anterior
        self.sum_error = 0  # erro total

    def update_const(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def update_reference_temperature(self, ref_temp):
        self.ref_temp = ref_temp

    def pid_control(self, current_temp):
        current_error = self.ref_temp - current_temp
        delta_error = current_error - self.last_error

        self.sum_error += current_error

        if self.sum_error > MAX_CONTROL_SIGNAL:
            self.sum_error = MAX_CONTROL_SIGNAL

        elif self.sum_error < MIN_CONTROL_SIGNAL:
            self.sum_error = MIN_CONTROL_SIGNAL

        P = self.kp * current_error
        I = self.ki * self.sum_error
        D = self.kd * delta_error

        control_signal = P + I + D

        if control_signal > MAX_CONTROL_SIGNAL:
            control_signal = MAX_CONTROL_SIGNAL

        elif control_signal < MIN_CONTROL_SIGNAL:
            control_signal = MIN_CONTROL_SIGNAL

        self.last_error = current_error

        return control_signal

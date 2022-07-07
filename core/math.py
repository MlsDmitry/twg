from math import inf


def clamp(num, a, b):
    return min(max(num, a), b)


class SmoothDamper:
    def __init__(self, max_speed=inf):
        self.velocity = 0.0
        self.max_speed = max_speed

        
    def smooth_damp(self, current, target, smooth_time, dt):
        smooth_time = max(0.0001, smooth_time)
        omega = 2 / smooth_time

        x = omega * dt
        exp = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x)
        change = current - target
        original_to = target

        maxChange = self.max_speed * smooth_time
        change = clamp(change, -maxChange, maxChange)
        target = current - change

        temp = (self.velocity + omega * change) * dt
        self.velocity = (self.velocity - omega * temp) * exp
        output = target + (change + temp) * exp

        if (original_to - current > 0.0) == (output > original_to):
            output = original_to
            self.velocity = (output - original_to) / dt
        return output

    
    def reset(self):
        self.velocity = 0.0

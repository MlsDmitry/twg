from panda3d.core import Vec3

from core import ModelManager

class Player:

    def __init__(self):
        self.model = ModelManager().get('hero')
        self.model.setPos(Vec3(0, -1, 0))
        # self.model.setScale(100)
        self.model.setP(self.model, 90)
        self.model.setH(self.model, 180)

        self.pos = self.model.getPos()
        self.direction = Vec3(0)
        self.velocity = Vec3(1.5, 0, 1.5)
        self.counter = 0

        self.speed = 2.5
        self.max_speed = 2.5
        self.min_speed = 0.15
        
    def smooth_step(self, x):
        p = (x - self.min_speed) / (self.max_speed - self.min_speed)
        if p < 0:
            p = 0
        if p > 1:
            p = 1
        
        return p * p * (3 - 2 * p)

    # def smooth_damp(self, current, target, current_velocity, smooth_time, max_speed, delta_time):
    #     output_x = 0.0
    #     output_z = 0.0

    #     smooth_time = max(0.0001, smooth_time)
    #     omega = 2.0 / smooth_time

    #     x = omega * delta_time
    #     exp = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
    #     change_x = current.x - target.x
    #     change_z = current.z - target.z

    #     original_to = target

    #     max_change = max_speed * smooth_time

    #     max_change_sq = max_change * max_change
    #     sqrmag = change_x * change_x + change_z * change_z
    #     if sqrmag > max_change_sq:
    #         mag = sqrmag ** 0.5
    #         change_x = change_x / mag * max_change
    #         change_z = change_z / mag * max_change

    #     target.x = current.x - change_x
    #     target.z = current.z - change_z

    #     temp_x = (current_velocity.x + omega * change_x) * delta_time
    #     temp_z = (current_velocity.z + omega * change_z) * delta_time

    #     current_velocity.x = (current_velocity.x - omega * temp_x) * exp
    #     current_velocity.z = (current_velocity.z - omega * temp_z) * exp

    #     output_x = target.x + (change_x + temp_x) * exp
    #     output_z = target.z + (change_z + temp_z) * exp

    #     orig_minus_current_x = original_to.x - current.x
    #     orig_minus_current_z = original_to.z - current.z
    #     out_minus_orig_x = output_x - original_to.x
    #     out_minus_orig_z = output_z - original_to.z

    #     if (orig_minus_current_x * out_minus_orig_x + orig_minus_current_z * out_minus_orig_z) > 0:
    #         output_x = original_to.x
    #         output_z = original_to.z

    #         current_velocity.x = (output_x - original_to.x) / delta_time
    #         current_velocity.z = (output_z - original_to.z) / delta_time

    #     return Vec3(output_x, 0, output_z)
        
    def smooth_damp(self, current, target, current_velocity, smooth_time, max_speed, delta_time):
        smooth_time = max(0.0001, smooth_time)
        omega = 2.0 / smooth_time

        x = omega * delta_time
        exp = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
        change = current - target
        original_to = target

        max_change = max_speed * smooth_time
        change = self.clamp(change, -max_change, max_change)
        target = current - change

        temp = (current_velocity + omega * change) * delta_time
        current_velocity = (current_velocity - omega * temp) * exp
        output = target + (change + temp) * exp

        if original_to - current > 0.0 == output > original_to:
            output = original_to
            current_velocity = (output - original_to) / delta_time

        return output
            
            

    def clamp(self, value, min_v, max_v):
        if value < min_v:
            value = min_v
        elif value > max_v:
            value = max_v 

        return value
        
                          
        



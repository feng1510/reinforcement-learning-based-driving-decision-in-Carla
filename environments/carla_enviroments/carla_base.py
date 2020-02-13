import sys
import gym
from environments.carla_enviroments.carla_config import base_config
try:
    sys.path.append(base_config.egg_file)
except IndexError:
    pass
import carla
from utilities.logging import logger

class carla_base(gym.Env):
    """connect the carla server"""
    world = None ## carla world obj

    """connect the carla server"""
    def __init__(self):
        try:
            client = carla.Client('127.0.0.1', 2000)
            logger.info('carla connecting...')
            client.set_timeout(2.0)
            self.world = client.get_world()
        except:
            raise RuntimeError('carla connection fail...')
        else:
            logger.info('carla connection success...')

    def start_synchronous_mode(self):
        """carla synchoronous mode"""
        self.world.apply_settings(carla.WorldSettings(no_rendering_mode=False,
                                                      synchronous_mode=True))

    def close_synchronous_mode(self):
        """close synchoronous mode"""
        self.world.apply_settings(carla.WorldSettings(no_rendering_mode=False,
                                                      synchronous_mode=False))

    def wait_carla_runing(self, time):
        """Wait for Carla to run for a specific time"""
        time_elapse = 0.
        while True:
            time_elapse += self.wait_for_response()
            if time_elapse > time:
                break

    def wait_for_response(self):
        """wait for carla response
        Return:
            response time consumption
        """
        self.world.tick()
        elapse_time = self.world.wait_for_tick()
        # logger.info('respond time consumption %f'%(round(ts.delta_seconds, 6)))
        return elapse_time.delta_seconds

if __name__ == '__main__':
    a = carla_base()
    pass
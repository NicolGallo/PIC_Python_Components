#####
#
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.data.SensorData import SensorData


class CoParticleSensorSimTask(BaseSensorSimTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, dataSet=None):
        super(CoParticleSensorSimTask, self).__init__(name = ConfigConst.CO_PARTICLE_SENSOR_NAME,
                                                      typeID = ConfigConst.CO_PARTICLE_SENSOR_TYPE,
                                                      dataSet = dataSet,
                                                      minVal = SensorDataGenerator.LOW_NORMAL_ENV_PARTICLE,
                                                      maxVal = SensorDataGenerator.HI_NORMAL_ENV_PARTICLE)
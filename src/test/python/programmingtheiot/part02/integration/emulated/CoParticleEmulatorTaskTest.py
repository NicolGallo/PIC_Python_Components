#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.emulated.CoParticleSensorEmulatorTask import CoParticleSensorEmulatorTask


class CoParticleSensorEmulatorTaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing CoParticleEmulatorTaskTest class [using SenseHAT emulator]...")
        self.paTask = CoParticleSensorEmulatorTask()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadEmulator(self):
        sd1 = self.paTask.generateTelemetry()

        if sd1:
            self.assertEqual(sd1.getTypeID(), ConfigConst.CO_PARTICLE_SENSOR_TYPE)
            logging.info("SensorData: %f - %s", sd1.getValue(), str(sd1))

            # wait 5 seconds
            sleep(5)
        else:
            logging.warning("FAIL: SensorData is None.")

        sd2 = self.paTask.generateTelemetry()

        if sd2:
            self.assertEqual(sd2.getTypeID(), ConfigConst.CO_PARTICLE_SENSOR_TYPE)
            logging.info("SensorData: %f - %s", sd2.getValue(), str(sd2))

            # wait 5 seconds
            sleep(5)
        else:
            logging.warning("FAIL: SensorData is None.")


if __name__ == "__main__":
    unittest.main()

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

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.emulated.CoParticleEmulatorTask import CoParticleEmulatorTask


class CoParticleActuatorEmulatorTaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing CoParticleEmulatorTask class [using SenseHAT emulator]...")
        self.paSimTask = CoParticleEmulatorTask()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateEmulator(self):
        ad = ActuatorData(typeID = ConfigConst.CO_PARTICLE_ACTUATOR_TYPE)
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setValue(18.0)

        adr = self.paSimTask.updateActuator(ad)

        if adr:
            self.assertEqual(adr.getCommand(), ConfigConst.COMMAND_ON)
            self.assertEqual(adr.getStatusCode(), 0)
            logging.info("ActuatorData: " + str(adr))

            # wait 5 seconds
            sleep(5)
        else:
            logging.warning("ActuatorData is None.")

        ad.setValue(35.0)

        adr = self.paSimTask.updateActuator(ad)

        if adr:
            self.assertEqual(adr.getCommand(), ConfigConst.COMMAND_ON)
            self.assertEqual(adr.getStatusCode(), 0)
            logging.info("ActuatorData: " + str(adr))

        # wait 5 seconds
        else:
            logging.warning("ActuatorData is None.")

        ad.setCommand(ConfigConst.COMMAND_OFF)

        adr = self.paSimTask.updateActuator(ad)

        if adr:
            self.assertEqual(adr.getCommand(), ConfigConst.COMMAND_OFF)
            self.assertEqual(adr.getStatusCode(), 0)
            logging.info("ActuatorData: " + str(adr))
        else:
            logging.warning("ActuatorData is None.")


if __name__ == "__main__":
    unittest.main()

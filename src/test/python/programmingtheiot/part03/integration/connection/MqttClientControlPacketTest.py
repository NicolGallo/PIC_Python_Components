
import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil


class MqttClientControlPacketTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Executing the MqttClientControlPacketTest class...")

        self.cfg = ConfigUtil()

        # NOTE: Be sure to use a DIFFERENT clientID than that which is used
        # for your CDA when running separately from this test
        #
        # The clientID shown below is an example only - please use your own
        # unique value for this test
        self.mcc = MqttClientConnector(clientID="ClientTestingTests")

    @unittest.skip("Ignore for now.")
    def setUp(self):
        """
        # If client is already connected, it disconnects to start each test with a clean state.
        if self.mcc.mqttClient and self.mcc.mqttClient.is_connected():
            self.mcc.disconnectClient()
        sleep(0.5)
        """
        pass

    @unittest.skip("Ignore for now.")
    def tearDown(self):
        """
        # Stop every test if connection stay active
        try:
            if self.mcc.mqttClient and self.mcc.mqttClient.is_connected():
                self.mcc.disconnectClient()
        except Exception as e:
            logging.warning("It has been the next error during tearDown: " + str(e))
        sleep(0.5)
        """
        pass

    #@unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        # Client connection
        connectResult = self.mcc.connectClient()
        self.assertTrue(connectResult, "Client must connect successfully")
        sleep(1)

        # Verifica que el cliente esté conectado
        self.assertTrue(self.mcc.mqttClient.is_connected(), "Client must be connected.")

        # Se desconecta el cliente
        disconnectResult = self.mcc.disconnectClient()
        self.assertTrue(disconnectResult, "Client must disconnect successfully")
        sleep(1)  # Espera para la desconexión

        self.assertFalse(self.mcc.mqttClient.is_connected(), "Client must be disconnected.")

    #@unittest.skip("Ignore for now.")
    def testServerPing(self):
        # Objective: Check that the broker responds to pings and maintains the connection.
        connectResult = self.mcc.connectClient()
        self.assertTrue(connectResult, "Client must connect successfully")
        sleep(1)
        self.assertTrue(self.mcc.mqttClient.is_connected(), "Client must be connected.")

        # Wait longer than keepAlive to confirm the connection remains active.
        waitTime = self.mcc.keepAlive * 2
        logging.info(f"Waiting {waitTime} seconds to check the server ping...")
        sleep(waitTime)

        self.assertTrue(self.mcc.mqttClient.is_connected(),
                        "Client must be connected after ping check.")
        self.mcc.disconnectClient()

    #@unittest.skip("Ignore for now.")
    def testPubSub(self):
        self.mcc.setDataMessageListener(DefaultDataMessageListener())
        self.mcc.connectClient()

        for qos in [1, 2]:
            # Test publishing a message
            actuatorData = ActuatorData()
            actuatorDataJson = DataUtil().actuatorDataToJson(actuatorData)

            self.mcc.publishMessage(
                resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
                msg=actuatorDataJson,
                qos=qos,
            )

            sleep(2)

            # Test subscribing to a message
            self.mcc.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, qos)

            sleep(2)

            # Now with sensor data
            sensorData = SensorData()
            sensorDataJson = DataUtil().sensorDataToJson(sensorData)

            self.mcc.publishMessage(
                resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                msg=sensorDataJson,
                qos=qos,
            )

            sleep(2)

            self.mcc.unsubscribeFromTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
            self.mcc.subscribeToTopic(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, qos)

            # Now with system performance data
            sysPerfData = SystemPerformanceData()
            sysPerfDataJson = DataUtil().systemPerformanceDataToJson(sysPerfData)

            self.mcc.publishMessage(
                resource=ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE,
                msg=sysPerfDataJson,
                qos=qos,
            )

            sleep(2)

            self.mcc.unsubscribeFromTopic(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
            self.mcc.subscribeToTopic(
                ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, qos
            )

        sleep(2)
        self.mcc.disconnectClient()


if __name__ == '__main__':
    unittest.main()

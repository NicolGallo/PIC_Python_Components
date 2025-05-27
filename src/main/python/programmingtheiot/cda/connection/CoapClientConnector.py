#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import socket
import traceback
import asyncio

from aiocoap import *   #Using aiocoap library

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

from programmingtheiot.data.DataUtil import DataUtil



class CoapClientConnector(IRequestResponseClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.config = ConfigUtil()
		self.dataMsgListener = dataMsgListener
		self.enableConfirmedMsgs = False
		self.coapClient = None

		self.observeRequests = {}

		self.host = self.config.getProperty(
			ConfigConst.COAP_GATEWAY_SERVICE,
			ConfigConst.HOST_KEY,
			ConfigConst.DEFAULT_HOST
		)
		self.port = self.config.getInteger(
			ConfigConst.COAP_GATEWAY_SERVICE,
			ConfigConst.PORT_KEY,
			ConfigConst.DEFAULT_COAP_PORT
		)
		self.uriPath = "CoAP://" + self.host + ":" + str(self.port) + "/"

		logging.info('\tHost:Port: %s:%s', self.host, str(self.port))

		self.includeDebugLogDetail = True

		try:
			tmpHost = socket.gethostbyname(self.host)

			if tmpHost:
				self.host = tmpHost
				self._initClient()
			else:
				logging.error("Can't resolve host: " + self.host)

		except socket.gaierror:
			logging.info("Failed to resolve host: " + self.host)



	
	def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method sendDiscoveryRequest has been called.")

		logging.info("Discovering remote resources...")

		return self.sendGetRequest(resource = None, name = '.well-known/core', enableCON = False, timeout = timeout)



	def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method sendDeleteRequest has been called.")
		return True




	def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method sendGetRequest has been called.")

		if resource or name:
			resourcePath = self._createResourcePath(resource, name)

			logging.info("Issuing Async GET to path: " + resourcePath)

			asyncio.get_event_loop().run_until_complete(
				self._handleGetRequest(resourcePath=resourcePath, enableCON=enableCON)
			)

			return True
		else:
			logging.warning("Can't issue Async GET - no path or path list provided.")
			return False

	async def _handleGetRequest(self, resourcePath: str = None, enableCON: bool = False):
		try:
			msgType = NON

			if enableCON:
				msgType = CON

			completed_uri = self.uriPath + resourcePath
			msg = Message(mtype=msgType, code=Code.GET, uri=completed_uri)
			req = self.coapClient.request(msg)
			responseData = await req.response

			self._onGetResponse(responseData)

		except Exception as e:
			logging.warning("Failed to process GET request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)

	def _onGetResponse(self, response):
		if not response:
			logging.warning('Async GET response invalid. Ignoring.')
			return

		logging.info('Async GET response received.')

		jsonData = response.payload.decode("utf-8")

		if len(response.requested_path) >= 3:
			dataType = response.requested_path[2]

			if dataType == ConfigConst.ACTUATOR_CMD:
				# TODO: convert payload to ActuatorData and verify!
				logging.info("ActuatorData received: %s", jsonData)

				try:
					ad = DataUtil().jsonToActuatorData(jsonData)

					if self.dataMsgListener:
						self.dataMsgListener.handleActuatorCommandMessage(ad)
				except:
					logging.warning("Failed to decode actuator data. Ignoring: %s", jsonData)
					return
			else:
				logging.info("Response data received. Payload: %s", jsonData)
		else:
			logging.info("Response data received. Payload: %s", jsonData)




	def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method sendPostRequest has been called.")

		if resource or name:
			resourcePath = self._createResourcePath(resource, name)

			logging.info("Issuing Async POST to path: " + resourcePath)

			asyncio.get_event_loop().run_until_complete(
				self._handlePostRequest(
					resourcePath=resourcePath,
					payload=payload,
					enableCON=enableCON
				)
			)

			return True

		else:
			logging.warning("Can't issue Async POST - no path or path list provided.")
			return False

	async def _handlePostRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
		try:
			msgType = NON

			if enableCON:
				msgType = CON

			payloadBytes = b''

			# Decide which encoding to use - can also load from config
			if payload:
				payloadBytes = payload.encode('utf-8')

			completed_uri = self.uriPath + resourcePath
			msg = Message(mtype=msgType, payload=payloadBytes, code=Code.POST, uri=completed_uri)
			req = self.coapClient.request(msg)
			responseData = await req.response

			self._onPostResponse(responseData)

		except Exception as e:
			logging.warning("Failed to process POST request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)

	def _onPostResponse(self, response):
		if not response:
			logging.warning('POST response invalid. Ignoring.')
			return

		logging.info('POST response received: %s', response.payload)


	def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method sendPutRequest has been called.")

		if resource or name:
			resourcePath = self._createResourcePath(resource, name)

			logging.info("Issuing Async PUT to path: " + resourcePath)

			asyncio.get_event_loop().run_until_complete(
				self._handlePutRequest(
					resourcePath=resourcePath,
					payload=payload,
					enableCON=enableCON
				)
			)

			return True

		else:
			logging.warning("Can't issue Async PUT - no path or path list provided.")
			return False

	async def _handlePutRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
		try:
			msgType = NON

			if enableCON:
				msgType = CON

			payloadBytes = b''

			# Decide which encoding to use - can also load from config
			if payload:
				payloadBytes = payload.encode('utf-8')

			completed_uri = self.uriPath + resourcePath
			msg = Message(mtype=msgType, payload=payloadBytes, code=Code.PUT, uri=completed_uri)
			req = self.coapClient.request(msg)
			responseData = await req.response

			self._onPutResponse(responseData)

		except Exception as e:
			logging.warning("Failed to process PUT request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)

	def _onPutResponse(self, response):
		if not response:
			logging.warning('PUT response invalid. Ignoring.')
			return

		logging.info('PUT response received: %s', response.payload)



	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMsgListener = listener
			logging.info("IDataMessageListener set for CoapClientConnector.")
			return True
		else:
			logging.warning("Attempted to set a null IDataMessageListener.")
			return False

	def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
		logging.info("The method startObserver has been called.")
		return True

	def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("The method stopObserver has been called.")
		return True



	#The following implementation is using aiocoap library

	def _initClient(self):
		asyncio.get_event_loop().run_until_complete(self._initClientContext())

	async def _initClientContext(self):
		try:
			logging.info("Creating CoAP client for URI path: " + self.uriPath)

			self.coapClient = await Context.create_client_context()

			logging.info('Client context created. Will invoke resources at: ' + self.uriPath)

		except Exception as e:
			# obviously, this is a critical failure - you may want to handle this differently
			logging.error("Failed to create CoAP client to URI path: " + self.uriPath)
			traceback.print_exception(type(e), e, e.__traceback__)



	def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None):
		resourcePath = ""
		hasResource = False

		if resource:
			resourcePath = resourcePath + resource.value
			hasResource = True

		if name:
			if hasResource:
				resourcePath = resourcePath + '/'

			resourcePath = resourcePath + name

		return resourcePath
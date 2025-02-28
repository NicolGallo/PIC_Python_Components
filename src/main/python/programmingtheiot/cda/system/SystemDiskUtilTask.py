#####
#
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemDiskUtilTask(BaseSystemUtilTask):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self):
        super(SystemDiskUtilTask, self).__init__(name=ConfigConst.DISK_UTIL_NAME, typeID=ConfigConst.DISK_UTIL_TYPE)

    def getTelemetryValue(self) -> float:
        pass
        #return psutil.disk_usage().percent

    #TODO: Falta poner el parametro dentro del disk_usage para dar el valor esperado

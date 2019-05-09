import logging
import time

from ..exception import VMError, ServiceError, ConnectionError
from ..data_types import AnalyticsTarget
from .commons import Tools

CKEY = AnalyticsTarget()

class Mhn(Tools):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(__name__)

    def vm_install(self, config):
        vm_conn = None
        try:
            vm_conn = self.try_connection()

            command = "mkdir mhn"
            vm_conn.runCommandOverSSH(command)
            vm_conn.copyFile("%s/mhn.tar.gz" %(self.tools_dir), "mhn.tar.gz")
            
            command = "tar -zxvf mhn.tar.gz"
            vm_conn.runCommandOverSSH(command)

            service_config = config[CKEY.SERVICE_CONFIG]
            vm_conn.writeRemoteJsonFile(service_config, "./mhn/server/mhn_spec.json")
    
            command = "export LC_ALL=C"
            vm_conn.runCommandOverSSH(command)

            command = "sudo python mhn/server/setupip.py" 
            outdata, error = vm_conn.runCommandOverSSH(command)
            
          #  vm_conn.copyFile("%s/emerging.rules.tar.gz" %(self.tools_dir), "emerging.relus.tar.gz")
            vm_conn.copyFile("%s/mhn_sensors.tar.gz" %(self.tools_dir), "mhn_sensors.tar.gz")
            
            command = "sudo tar -zxvf mhn_sensors.tar.gz -C /opt"
            vm_conn.runCommandOverSSH(command)
            
            command = "sudo cp -r /opt/mhn_sensors/. /opt"
            vm_conn.runCommandOverSSH(command)

            vm_conn.copyFile("%s/mhn_sensors_tmp.tar.gz" %(self.tools_dir), "mhn_sensors_tmp.tar.gz")

            command = "sudo tar -zxvf mhn_sensors_tmp.tar.gz -C /tmp"
            vm_conn.runCommandOverSSH(command)
            
            command = "sudo cp -r /tmp/mhn_sensors_tmp/. /tmp"     
            vm_conn.runCommandOverSSH(command)

            command = "sudo ./mhn/install_mhn.sh"
            vm_conn.runCommandOverSSH(command)
        
            command = "sudo python mhn/deploy.py"
            outdata, error = vm_conn.runCommandOverSSH(command)


        except VMError as e:
            self.log.error("%s - Unable to get ip address of the tool: %s - " %(self.__class__.__name__,str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Unable to get ip address of the tool - %s - "%(self.__class__.__name__,str(e)))


        except ConnectionError as e:
            self.log.info("%s - Error during SSH operations: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error during SSH operations - %s - "%(self.__class__.__name__,str(e)))
        finally:
            if(vm_conn is not None):
                vm_conn.closeSSHConnection()
        self.log.info("%s - installed on ip - %s " %(self.__class__.__name__,self.IP))
        

    def vm_update(self, config):
        vm_conn = None
        try:
            time.sleep(120)

            vm_conn = self.try_connection()
            
            vm_conn.copyFile("%s/mhn_sensors.tar.gz" %(self.tools_dir), "mhn_sensors.tar.gz")
           
            command = "sudo tar -zxvf mhn_sensors.tar.gz -C /opt"
            vm_conn.runCommandOverSSH(command)

            command = "sudo cp -r /opt/mhn_sensors/. /opt"
            vm_conn.runCommandOverSSH(command)
            
            
            vm_conn.copyFile("%s/mhn_sensors_tmp.tar.gz" %(self.tools_dir), "mhn_sensors_tmp.tar.gz")
            
            command = "sudo tar -zxvf mhn_sensors_tmp.tar.gz -C /tmp"
            vm_conn.runCommandOverSSH(command)
            
            command = "sudo cp -r /tmp/mhn_sensors_tmp/. /tmp"
            vm_conn.runCommandOverSSH(command)
           
            command = "sudo python mhn/deploy.py"
            outdata, error = vm_conn.runCommandOverSSH(command)

        except VMError as e:
            self.log.error("%s - Unable to get ip address of the tool: %s - " %(self.__class__.__name__,str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Unable to get ip address of the tool - %s - "%(self.__class__.__name__,str(e)))

        except ConnectionError as e:
            self.log.info("%s - Error during SSH operations: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error during SSH operations - %s - "%(self.__class__.__name__,str(e)))
        
        finally:
            if(vm_conn is not None):
                vm_conn.closeSSHConnection()
                self.log.info("%s - installed on ip - %s " %(self.__class__.__name__,self.IP))
            

    def getServiceSpec(self):
        try:     
            self.get_service_spec("./mhn/server/mhn_spec.json")
        except ServiceError:
             raise
         
    def getStatus(self, platform_type):
         try:
             return self.get_service_status(platform_type, "./mhn/server/mhn_spec.json")
         except ServiceError:
             raise

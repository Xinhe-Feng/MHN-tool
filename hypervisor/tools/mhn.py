from ..exception import VMError, ServiceError
from ..platforms.tool_connections import ManageSSH
from ..data_types import SuccessState, PlatformTypes, ContextKeys, AnalyticsTarget
import logging
from logging import getLogger
import json
import time

CKEY = AnalyticsTarget()

class Mhn:

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def docker_install(self, tool_id, tool_config, pl):
        pass

    def vm_install(self, tool_id, config, pl, platform_type):
        tools_dir = pl.conf.TOOLS_DIR
        ip = ""
        try:
            time.sleep(120)
            vm_conn = None
            ip = pl.get_tool_ip(tool_id)
            #ip = "10.100.6.13"
            if ip == "":
                raise ServiceError(self.__class__.__name__,"%s - Ip address not available to connect. Cannot proceed with install - "%self.__class__.name__)

            vm_conn = ManageSSH("recovery", "recovery", ip)

            command = "mkdir mhn"
            vm_conn.runCommandOverSSH(command)
            vm_conn.copyFile("%s/mhn.tar.gz" %(tools_dir), "mhn.tar.gz")

            command = "tar -zxvf mhn.tar.gz"
            vm_conn.runCommandOverSSH(command)

            #command = "sudo chmod a+x mhn/install_mhn.sh"
            #vm_conn.runCommandOverSSH(command)

            service_config = config[CKEY.SERVICE_CONFIG]
            vm_conn.writeRemoteJsonFile(service_config, "./mhn/server/mhn_spec.json")
    
            command = "export LANGUAGE=en_US.UTF-8"
            vm_conn.runCommandOverSSH(command)

            command = "export LANG=en_US.UTF-8"
            vm_conn.runCommandOverSSH(command)

            command = "export LC_ALL=en_US.UTF-8"
            vm_conn.runCommandOverSSH(command)

            command = "sudo locale-gen en_US.UTF-8"
            vm_conn.runCommandOverSSH(command)
            
            #command = "sudo pip install celery"
            #vm_conn.runCommandOverSSH(command)

            command = "sudo ./mhn/install_mhn.sh"
            outdata, error = vm_conn.runCommandOverSSH(command)
           
            #command = "sudo python mhn/deploy.py"
            #outdata, error = vm_conn.runCommandOverSSH(command)

        except VMError as e:
            self.log.error("%s - Unable to get ip address of the tool: %s - " %(self.__class__.__name__,str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Unable to get ip address of the tool - %s - "%(self.__class__.__name__,str(e)))

        except ConnectionError as e:
            self.log.info("%s - Error during SSH operations: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error during SSH operations - %s - "%(self.__class__.__name__,str(e)))
        finally:
            if(vm_conn is not None):
                vm_conn.closeSSHConnection()
        self.log.info("%s - installed on ip - %s - %s - %s - " %(self.__class__.__name__,ip, outdata, error))
        return ip

    def tool_update(self,tool_id,config,pl, platform_type):
        tools_dir = pl.conf.TOOLS_DIR
        ip = ""
        try:
            time.sleep(120)
            vm_conn = None
            ip = pl.get_tool_ip(tool_id)
            #ip = "10.100.6.13"
            if ip == "":
                raise ServiceError(self.__class__.__name__,"%s - Ip address not available to connect. Cannot proceed with install - "%self.__class__.name__)

            vm_conn = ManageSSH("recovery", "recovery", ip)
            
           # command = "sudo pip install celery"
           # vm_conn.runCommandOverSSH(command)
            
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
                self.log.info("%s - installed on ip - %s - %s - %s - " %(self.__class__.__name__,ip, outdata, error))
                return ip


    def update(self,tool_id, config, pl, platform_type):
        try:
            self.init_update = -1
            if(platform_type == PlatformTypes.VM):
                return self.tool_update(tool_id, config, pl, platform_type)
            elif(platform_type == PlatformTypes.DOCKER):
                return self.docker_install(tool_id, config, pl, platform_type)
        except:
            raise

    def install(self, tool_id, config, pl, platform_type):
        try:
            self.init_update = 0
            if (platform_type == PlatformTypes.VM):
                return self.vm_install(tool_id, config, pl, platform_type)
            elif (platform_type == PlatformTypes.DOCKER):
                return self.docker_install(tool_id, config, pl, platform_type)
        except:
            raise

    def getServiceSpec(self, ip, tool_id, platform_type):
        vm_conn = None
        try:
            self.log.info("%s - using ip - %s" %(self.__class__.__name__,ip))
            vm_conn = ManageSSH("recovery", "recovery", ip)
            service_spec = vm_conn.readRemoteJsonFile("spec.json")
            return service_spec
        except ConnectionError as e:
            self.log.error("%s - Error during SSH operations: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error during SSH operations: %s - "%(self.__class__.__name__,str(e)))

        except json.decoder.JSONDecodeError as e:
            self.log.error("%s - Error in reading json spec file: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error in reading json spec file: %s - "%(self.__class__.__name__,str(e)))
        finally:
            if(vm_conn is not None):
                vm_conn.closeSSHConnection()
           
    def getStatus(self, tool_id, pl, platform_type):
        vm_conn = None
        try:
            ip = pl.get_tool_ip(tool_id)
            if ip == "":
                raise ServiceError(platform_type,"%s - Ip address not available to connect. Cannot proceed with install - "%(self.__class__.__name__))
            vm_conn = ManageSSH("recovery", "recovery", ip)
            wireshark_status = vm_conn.readRemoteJsonFile("mhn_installed")
            return wireshark_status
        except VMError as e:
            self.log.error("%s - Unable to get ip address of the tool: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Unable to get ip address of the tool: %s - "%(self.__class__.__name__, str(e)))
        except ConnectionError as e:
            self.log.error("%s - Error during SSH operations: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error during SSH operations: %s - "%(self.__class__.__name__, str(e)))
        except json.decoder.JSONDecodeError as e:
            self.log.error("%s - Error in reading json status file: %s - " %(self.__class__.__name__, str(e)))
            raise ServiceError(self.__class__.__name__, "%s - Error in reading json status file: %s - "%(self.__class__.__name__, str(e)))
        finally:
            if(vm_conn is not None):
                vm_conn.closeSSHConnection()

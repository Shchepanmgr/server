from enum import Enum
import pickle
import struct


class Header(Enum):
    WAITING = 1
    COMMAND = 2
    RESPONSE = 3
    IDLE = 4
    EXIT = 5


class Command(Enum):
    LS = 'ls'
    LS_TREE = 'ls_tree'
    CREATE_FOLDER = 'create_folder'
    UPLOAD_FILE = 'download_file'
    UPLOAD_FOLDER = 'download_folder'
    DOWNLOAD_FILE = 'upload_file'
    REMOVE_FILE = 'remove_file'
    REMOVE_FOLDER = 'remove_folder'
    UPDATE_CONFIG = 'update_config'
    START_EXE = 'start_exe'
    CHECK_PROCESS_RUNNING = 'check_process'
    COMMAND_NOT_KNOWN = 'command_not_known'


class Message:
    # header: Header
    # command: Command

    # def __init__(self, header, command=None, payload=None):
    def __init__(self, payload=None):
        # self.header = header
        # self.command = command
        self.payload = payload

    def ToBytes(self):
        # return pickle.dumps(self)
        return struct.pack('>I', int(self.payload))

    @staticmethod
    def FromBytes(bytes):
        # return pickle.loads(bytes)
        return struct.unpack('>I', bytes)

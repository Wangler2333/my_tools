#!/usr/bin/env python
"""Collects logs from an attached iOS like device."""
import logging
import sys
import subprocess
import argparse
import os
import time
import shlex
import errno
import tarfile
import socket
from Functions.shell import *

try:
    import coloredlogs

    USE_COLOREDLOGS = True
except ImportError:
    USE_COLOREDLOGS = False


class FileProcess(object):
    '''
    Usage:
          for file compress and uncompress
          now only can use for tgz formt
    '''

    def __init__(self):
        self.compress = 'cd %s; tar -zcvf %s %s &>/dev/null'
        self.uncompress = 'cd %s; tar -xzf %s &>/dev/null'

    def tgz_compress(self, obj, force=False):
        '''
        :param obj:     file path for compress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        final = ".".join([name, "tgz"])
        a, b = shell(self.compress % (path, final, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)

    def tgz_uncompress(self, obj, force=False):
        '''
        :param obj:     file path for uncompress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        a, b = shell(self.uncompress % (path, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)


# Feel free to add to this list, note that it is an error to add a
# subdirectory if a parent is already listed
EOS_DIRECTORIES = [
    "/AppleInternal/Diags/Baseband/coredump.dz",
    "/AppleInternal/Diags/Earthbound/Worlds/",
    "/AppleInternal/Diags/Logs/",
    "/AppleInternal/Diags/OSD/",
    "/AppleInternal/Diags/WiFiFirmware/socram.out",
    "/System/Library/Caches/com.apple.factorydata",
    "/private/var/db/Earthbound/",
    "/private/var/logs/Earthbound/",
    "/private/var/logs/Inferno/",
    "/private/var/logs/BurnIn/",
    "/private/var/logs/AppleSupport/",
    "/private/var/logs/Baseband/",
    "/private/var/logs/CrashReporter/",
    "/private/var/logs/IQAgent/",
    "/private/var/logs/fairplayd.log",
    "/private/var/logs/lockdownd.log",
    "/private/var/logs/diagsproxyd.log",
    "/private/var/logs/SwitchLog.txt",
    "/private/var/logs/StdErrSwitchLcdUTest.txt",
    "/private/var/logs/StdErrSwitchOperator.txt",
    "/private/var/wireless/Library/Logs/CrashReporter/",
    "/private/var/mobile/Library/Logs/CrashReporter/",
    "/private/var/mobile/Media/FactoryLogs/",
    "/private/var/log/CoreCapture/"
]
"""Arr(str) The directories to rsync from the iOS-like device"""

MACOS_DIRECTORIES = [
    "/AppleInternal/Diagnostics/Logs/",
    "/Library/Logs",
]

EOS_SSH = "/usr/local/bin/eos-ssh"
"""str: The path to the eos-ssh binary"""

EOS_SCP = "/usr/local/bin/eos-scp"
"""str: The path to the eos-scp binary"""

SSH = "/usr/bin/ssh"
"""str: The path to the ssh binary"""

LOG_COLLECT_COMMAND = "log collect"
"""str: The command to collect logs"""

RSYNC = "/usr/bin/rsync"
"""str: The path to the rsync binary"""


class Command(object):
    """A class to manage processes spawned by the tool, can be used in a with statement"""

    def __init__(self, cmd, hostname):
        self.base_cmd = cmd
        self.hostname = hostname
        if hostname:
            self.cmd = " ".join([SSH, hostname, "-C", "\"", cmd, "\""])
        else:
            self.cmd = self.base_cmd
        logging.warning("Command: %s", cmd)
        logging.debug("%s: Creating object", self.cmd)
        self.proc = None

    def start(self):
        """Starts the process"""
        logging.debug("%s: starting process", self.cmd)
        self.proc = subprocess.Popen(
            shlex.split(self.cmd), stdin=subprocess.PIPE)

    def communicate(self, msg):
        """Sends a message to stdin"""
        logging.debug("%s: communicate %s", self.cmd, msg)
        self.proc.communicate(msg)

    def kill(self):
        """Stops the process if running by sending SIGKILL"""
        logging.debug("%s: killing process", self.cmd)
        while self.__is_running():
            self.proc.kill()
            time.sleep(1)

    def wait(self):
        """Waits for the process to terminate"""
        logging.debug("%s: waiting on process", self.cmd)
        if self.proc:
            self.proc.wait()

    def __is_running(self):
        """Checks if the process is running
            Returns:
                bool: True if process is running, false otherwise
        """
        if self.proc:
            self.proc.poll()
            logging.debug("%s: Return code is %s",
                          self.cmd, self.proc.returncode)
            if self.proc.returncode is None:
                return True
        return False

    def __enter__(self):
        """Entering a with clause, starts the process"""
        logging.debug("%s: __enter__", self.cmd)
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit handler for with statement"""
        logging.debug("%s: __exit__", self.cmd)
        self.kill()


class PathPair(object):
    """A struct like class that manages a remote directory and
    the expected destination directory on the host
    """

    def __init__(self, remote_dir, destination_dir, hostname):
        """Initializes the PathPair
            Args:
                remote_dir (str): The path on the iOS like device to be collected
                destination_dir(str): The path on the host to store the remote_dir contents
                hostname (str): The host where the logs live
                """
        self.remote_dir = remote_dir
        self.destination_dir = destination_dir
        self.hostname = hostname

    def __str__(self):
        """Helper method to pretty print PathPair objects
        """
        return "Remote: " + self.remote_dir + " Destination: " + self.destination_dir

    def move_logs(self):
        """Gets logs from a device
            Args:
            path_pair(PathPair): The PathPair to collect
        """
        logging.debug("Moving file: %s", str(self))
        logging.debug("Creating directory structure on Host: %s",
                      self.destination_dir)
        with Command(" ".join(["mkdir", "-p", self.destination_dir]), self.hostname) as mkdirs_cmd:
            mkdirs_cmd.wait()
        if self.remote_dir.startswith("eos:"):
            command = EOS_SCP + " " + self.remote_dir + " " + self.destination_dir
            with Command(command, self.hostname) as process:
                process.wait()
        else:
            logging.info("Copying %s to %s", self.remote_dir,
                         self.destination_dir)
            cmd = "/bin/cp -rv " + self.remote_dir + " " + self.destination_dir
            with Command(cmd, self.hostname) as cp_cmd:
                cp_cmd.wait()


def get_args():
    """Sets up argument parsing and returns an args function
        Returns:
            argparse args object
            """
    parser = argparse.ArgumentParser(
        description="""Collects the logs from an attached iOS-like device.
                        Currently this tool only supports
                        collecting from one device at a time. Will collect both macOS and bridgeOS logs.""")
    parser.add_argument('-d', '--destination',
                        help='Specifies the destination directory on the device running the script (' + socket.gethostname(
                        ) + ')',
                        default="/tmp/Logs/")
    parser.add_argument('-n', '--name',
                        help="""The name for the folder in the destination directory.
                        (Hint, use the serial number to easily track results)""",
                        default=time.strftime("Logs-%Y-%m-%d-%H-%M-%S"))
    parser.add_argument('-f', '--finder', help="Open a finder window when done",
                        default=False, action='store_true')
    parser.add_argument('-t', '--targz',
                        help="Create a tgz file at the specified location", default=None)
    parser.add_argument('--debug', help="Enables debug logging for " +
                                        os.path.basename(__file__), action='store_true', default=False)
    parser.add_argument(
        '--sshpath',
        help="Collect logs from a hostname, you probably want to send your public key or get ready to type your password forever. Example: gpburdell@apple.com")

    return parser.parse_args()


def setup_logging(debug):
    """Configures the logging systems
        Args:
            debug (bool): Enables debug logging
            """
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    if USE_COLOREDLOGS:
        # coloredlogs is a cool new tool Josh showed me.
        coloredlogs.install(level=level)
        logging.debug("Using coloredlogs")
    else:
        if sys.stdout.isatty():
            class Color(object):
                """A class to hold common shell color commands"""
                PURPLE = '\033[95m'
                CYAN = '\033[96m'
                DARKCYAN = '\033[36m'
                BLUE = '\033[94m'
                GREEN = '\033[92m'
                YELLOW = '\033[93m'
                RED = '\033[91m'
                BOLD = '\033[1m'
                UNDERLINE = '\033[4m'
                END = '\033[0m'

            logging.basicConfig(
                format=Color.BOLD +
                       '%(asctime)s<%(levelname)s> - ' + Color.END + ' %(message)s',
                level=level)
        else:
            logging.basicConfig(
                format='%(asctime)s<%(levelname)s> - %(message)s', level=level)
        logging.debug(
            "Not using coloredlogs, 'pip install coloredlogs' for cool logs!")


def configure(args):
    """Configures the system, also ensures the enviornment is sane
        Args:
            args: Argparse object for the module
            """
    setup_logging(debug=args['debug'])
    if args['targz']:
        assert args['targz'].endswith(".tgz") or args['targz'].endswith(
            ".tar.gz"), "The targz argument must end in .tgz or .tar.gz"
    assert os.path.exists(
        EOS_SSH), "The eos-ssh binary must be present at " + EOS_SSH + \
                  ", you can get eos-ssh with an AppleInternal macOS"
    assert os.path.exists(
        EOS_SCP), "The eos-scp binary must be present at " + EOS_SCP + \
                  ", you can get eos-scp with an AppleInternal macOS"


def collect_logs(destination, directories, hostname):
    """Collects the logs from the iOS like device
        Args:
            destination(str): The destination directory
            directories(Array(str)): An array of paths on the iOS-like device to collect
            hostname(str): The host where the logs live
            """

    path_pairs = []
    for remote_dir in directories:
        eos_path = False
        if remote_dir.startswith("eos:"):
            eos_path = True
        platformname = "bridgeOS" if eos_path else "macOS"
        logging.debug("Platform name: %s", platformname)
        if os.path.isabs(remote_dir) and os.path.isabs(destination):
            # Cant use os.path.join because they are both absolute paths
            dst_dir = os.path.join(destination, platformname) + remote_dir
        else:
            dst_dir = os.path.join(destination, platformname, remote_dir)
        logging.debug("dst_dir: %s", dst_dir)
        dst_dir = dst_dir.replace("eos:/", "")
        logging.debug("destination = %s, remote_dir = %s, dst_dir = %s",
                      destination, remote_dir, dst_dir)
        path_pairs.append(PathPair(remote_dir, dst_dir, hostname))

    for pair in path_pairs:
        pair.move_logs()


def open_finder(location):
    """Opens a finder window
        Args:
            location(str): Where the finder window should be pointing to
            """
    cmd = "/usr/bin/open " + location
    logging.debug("Opening finder window with '%s'", cmd)
    subprocess.check_call(shlex.split(cmd))


def compress_dir(source, destination):
    """Compresses a directory into a tar.gz archive
        Args:
            source(str): The source directory to compress
            destination(str): The destination archive
            """
    logging.debug("Will compress all files in %s into %s", source, destination)
    logging.debug("Creating directory structure for compressed file")
    try:
        os.makedirs(os.path.dirname(destination))
    except OSError as oserror:
        logging.debug(
            "Got an OSError creating paths for the compressed archive: %s", oserror)
        if oserror.errno != errno.EEXIST:
            logging.exception(
                "An unhandled exception occured while creating the compressed archive dir!")
            exit(20)
    with tarfile.open(destination, "w:gz") as tar:
        logging.debug("Adding %s to tar file", source)
        tar.add(source, arcname=os.path.basename(source))
    logging.debug("Done creating")


def main(args):
    """Collects the logs according to the args
        Args:
            args(Argparse): Argparse object with directions on how to collect the logs"""
    logging.debug("%s invoked with args %s",
                  os.path.basename(__file__), str(args))

    hostname = args['sshpath']
    dest = os.path.join(args['destination'], args['name'])
    mac_dest = os.path.join(dest, "macos")
    logging.info("Logs will be stored in: %s", dest)
    os.makedirs(mac_dest)
    logging.warning("Collecting logs on the device")
    try:
        cmd_eos = [EOS_SSH, LOG_COLLECT_COMMAND, "--output",
                   "/var/logs/Earthbound/system_logs_" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".logarchive"]
        cmd_macos = [LOG_COLLECT_COMMAND, "--output", os.path.join(
            mac_dest, "system_logs_" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".logarchive")]
        for cmd_arr in [cmd_eos, cmd_macos]:
            cmd = " ".join(cmd_arr)
            with Command(cmd, hostname) as logcollect:
                logcollect.wait()
    except subprocess.CalledProcessError as cpe:
        logging.exception("Log collecting command failed: %s", cpe)

    # try:
    #     cmd = "/usr/bin/sysdiagnose -b -f " + mac_dest
    #     with Command(cmd, hostname) as sysdiagnose:
    #         sysdiagnose.communicate("\n")
    #         sysdiagnose.wait()
    # except subprocess.CalledProcessError as cpe:
    #     logging.exception("Sysdiagnose command failed: %s", cpe)
    directories = []
    for eos_path in EOS_DIRECTORIES:
        directories.append("eos:" + eos_path)
    for macos_path in MACOS_DIRECTORIES:
        directories.append(macos_path)

    collect_logs(destination=dest, directories=directories, hostname=hostname)

    # Sync the collected logs back to the host running the script.
    if hostname:
        if not os.path.exists(dest):
            os.makedirs(dest)
        rsync_command = " ".join(
            [RSYNC, "-avzuh", hostname + ":" + dest + "/", dest])
        with Command(rsync_command, hostname=None) as rsync_proc:
            rsync_proc.wait()
    if args['targz']:
        # Compress the files we just copied, so in this case source==dest
        compress_dir(source=dest, destination=args['targz'])

    logging.info("Logs are in: %s", dest)

    if args['finder']:
        open_finder(location=dest)
    logging.info("Logs successfully collected!")


def log_running(dict_):
    ARGS = dict_
    configure(ARGS)
    main(ARGS)
    t = FileProcess()
    t.tgz_compress(os.path.join(ARGS['destination'], ARGS['name']), force=True)


if __name__ == "__main__":
    pass

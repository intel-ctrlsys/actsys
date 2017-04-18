# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Implements a provisioner for warewulf
"""
import socket
from ..plugin import DeclarePlugin
from .provisioner import Provisioner, ProvisionerException
from ..utilities import Utilities


@DeclarePlugin('warewulf', 100)
class Warewulf(Provisioner):
    """
    The class implements the Provisioner interface for WareWulf
    """
    UNSET_KEY = "UNDEF"
    DATABASE_INSERT_ERROR = "DBD::mysql::st execute failed:"
    PROVISIONER_NAME = "warewulf"

    def __init__(self):
        """
        Construct the obj, nothing more.
        """
        self.utilities = Utilities()

    def add(self, device):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y node new <device.hostname>
        Command Output:
            No output
            Return Code: 0
        Exceptional Case: No permissions
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
            DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
            DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
            ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                table 'binstore'
            WARNING:  Could not open /etc/hosts: Permission denied

            Return Code: 0
        Warewulf will let you add multiple nodes with the same name! So an additional check is needed.

        """
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)

        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            output = self.utilities.execute_subprocess(['wwsh', '-y', 'node', 'new', device_name_for_provisioner])
            self._check_for_general_errors(output)

        device[self.PROVISIONER_KEY] = self.PROVISIONER_NAME
        return device

    def delete(self, device):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y node delete <device.hostname>
        Command Output:
            About to apply 1 action(s) to 1 node(s):

                 DEL: NODE test-1

            Proceed?
            Deleted 1 nodes.
        Exceptional Case: The node doesn't exist in warewulf
            No nodes found
        Exceptional Case: No permissions
            About to apply 1 action(s) to 1 node(s):

                 DEL: NODE test-1

            Proceed?
          DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
            DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
            DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
            DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
            DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
            ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                table 'binstore'
            WARNING:  Could not open /etc/hosts: Permission denied
            Deleted 1 nodes.
        """
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is True:
            output = self.utilities.execute_subprocess(['wwsh', '-y', 'node', 'delete', device_name_for_provisioner])

            self._check_for_general_errors(output)
            if output.stdout is not None and "Deleted 1 nodes." not in output.stdout \
                    and "No Nodes Found" not in output.stdout:
                raise ProvisionerException("Some unknown error occured", output)

        device.pop(self.PROVISIONER_KEY, None)
        return device

    def set_ip_address(self, device, ip_address, interface="eth0"):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y node set --netdev=<interface> --ipaddr=<ip_address?UNDEF>
        Command Output:
            No output
            Return code: 0
        Command Output 2: When attempting to delete. This still returns success.
            stderr:
                ERROR:  Object c1 has no netdev "eth0" configured!
            Return code: 1
        Exceptional case: IP address is not valid.
            No output, but warewulf doesn't set anything.
            Return Code: 0
        Exceptional case: Permission denied
            stderr:
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner (warewulf)."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if ip_address is None:
            ip_address = self.UNSET_KEY
        # BUG: Warewulf can't unset a ip_addr: https://groups.google.com/a/lbl.gov/forum/#!topic/warewulf/IgfWiPh2y90
        # To get around this bug, we delete the whole interface, then add back the hw address if it was there.
        if ip_address == self.UNSET_KEY:
            hw_address_key = self._get_hardware_address_key(device, interface)
            hw_address_value = device.get(hw_address_key)

            output = self.utilities.execute_subprocess(['wwsh', '-y', 'node', 'set', device_name_for_provisioner,
                                                        '--netdel', interface])

            if output.return_code == 1 and output.stderr is not None \
                    and "ERROR:  Object c1 has no netdev" in output.stderr:
                # This is an ok error to have... everything was deleted as needed.
                output.return_code = 0

            if hw_address_value is not None:
                self.set_hardware_address(device, hw_address_value, interface)
        else:
            # Validate ip_address
            try:
                socket.inet_aton(ip_address)
            except socket.error:
                raise ProvisionerException(
                    "The IP address `{}` is not valid. See man inet(3) for details.".format(ip_address))

            output = self.utilities.execute_subprocess(
                ['wwsh', '-y', 'node', 'set', device_name_for_provisioner, '--netdev={}'.format(interface),
                 '--ipaddr={}'.format(ip_address)])

        # Check for other, more general, errors.
        self._check_for_general_errors(output)

        key = self._get_ip_address_key(device, interface)

        if ip_address == self.UNSET_KEY:
            device.pop(key, None)
        else:
            device[key] = ip_address

        return device

    def set_hardware_address(self, device, hardware_address, interface="eth0"):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y node set --netdev=<interface> --hwaddr=<hardware_address?UNDEF>
        Command Output:
            No output
            Return code: 0
        Exceptional case: Hardware address is not valid.
            stderr:
                ERROR:  Option 'hwaddr' has invalid characters
            Return Code: 1
        Exceptional case: Permission denied
            stderr:
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner (warewulf)."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if hardware_address is None:
            hardware_address = self.UNSET_KEY
        # BUG: Warewulf can't unset a ip_addr: https://groups.google.com/a/lbl.gov/forum/#!topic/warewulf/IgfWiPh2y90
        if hardware_address == self.UNSET_KEY:
            ip_address_value = device.get(self._get_ip_address_key(device, interface))

            output = self.utilities.execute_subprocess(['wwsh', '-y', 'node', 'set', device_name_for_provisioner,
                                                        '--netdel', interface])

            if output.return_code == 1 and output.stderr is not None \
                    and "ERROR:  Object c1 has no netdev" in output.stderr:
                # This is an ok error to have... everything was deleted as needed.
                output.return_code = 0

            if ip_address_value is not None:
                self.set_ip_address(device, ip_address_value, interface)
        else:
            output = self.utilities.execute_subprocess(
                ['wwsh', '-y', 'node', 'set', device_name_for_provisioner, '--netdev={}'.format(interface),
                 '--hwaddr={}'.format(hardware_address)])

            if output.stderr is not None and "ERROR:  Option 'hwaddr' has invalid characters" in output.stderr:
                raise ProvisionerException("The hardware address `{}` is not valid.".format(hardware_address), output)

        self._check_for_general_errors(output)

        key = self._get_hardware_address_key(device, interface)

        if hardware_address == self.UNSET_KEY:
            device.pop(key, None)
        else:
            device[key] = hardware_address

        return device

    def set_image(self, device, image):
        """
        See @Provisioner for interface details. Implementation here.

        Command: wwsh -y provision set --vnfs=<image?UNDEF>
        Command Output:
            No output
            Return code: 0
        Exceptional case: VNFS/image not found
            stderr:
                ERROR:  No VNFS named: <image>
            Return code: 1
        Exceptional case: Permission denied
            stderr:
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if image is None:
            image = self.UNSET_KEY

        output = self.utilities.execute_subprocess(
            ['wwsh', '-y', 'provision', 'set', device_name_for_provisioner, '--vnfs={}'.format(image)])
        # Check for errors becuase of No VNFS
        if output.stderr is not None and "No VNFS named:" in output.stderr:
            raise ProvisionerException("The image supplied is not known by the provisioner.", output)
        # Check for other, more general, errors.
        self._check_for_general_errors(output)

        if image == self.UNSET_KEY:
            device.pop(self.PROVISIONER_IMAGE_KEY, None)
        else:
            device[self.PROVISIONER_IMAGE_KEY] = image
        return device

    def set_bootstrap(self, device, bootstrap):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y provision set --bootstrap=<bootstrap?UNDEF>
        Command Output:
            No output
            Return code: 0
        Exceptional case: bootstrap not found
            stderr:
                ERROR:  No bootstrap named: <bootstrap>
            Return code: 1
        Exceptional case: Permission denied
            stderr:
                 DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if bootstrap is None:
            bootstrap = self.UNSET_KEY

        output = self.utilities.execute_subprocess(
            ['wwsh', '-y', 'provision', 'set', device_name_for_provisioner, '--bootstrap={}'.format(bootstrap)])
        # Check for errors because of no bootstrap with this name
        if output.stderr is not None and "No bootstrap named:" in output.stderr:
            raise ProvisionerException("The bootstrap supplied is not known by the provisioner.", output)
        # Check for other, more general, errors.
        self._check_for_general_errors(output)

        if bootstrap == self.UNSET_KEY:
            device.pop(self.PROVISIONER_BOOTSTRAP_KEY, None)
        else:
            device[self.PROVISIONER_BOOTSTRAP_KEY] = bootstrap
        return device

    def set_files(self, device, files):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y provision set --files=<files?UNDEF>
        Command Output:
            No output
            Return code: 0
        Exceptional case: File(s) not found
            stderr:
                ERROR:  No file found for name: <file>
                ... for each file not found
            Return code: 0/1
            If no file in the supplied list were applied then returns 1. If one ore more were applied,
            sets those and returns 0.
        Exceptional case: Permission denied
            stderr:
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if files is None:
            files = self.UNSET_KEY

        output = self.utilities.execute_subprocess(
            ['wwsh', '-y', 'provision', 'set', device_name_for_provisioner, '--files={}'.format(files)])
        # Check for errors because of no file(s) with this name
        # TODO: This needs to be changed because of the possibility of partial success!
        if output.stderr is not None and "No file found for name:" in output.stderr:
            raise ProvisionerException("The file(s) supplied are not known by the provisioner.", output)
        # Check for other, more general, errors.
        self._check_for_general_errors(output)

        if files == self.UNSET_KEY:
            device.pop(self.PROVISIONER_FILE_KEY, None)
        else:
            device[self.PROVISIONER_FILE_KEY] = files
        return device

    def set_kernel_args(self, device, args):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh -y provision set --kargs=<args?UNDEF>
        Command Output:
            No output
            Return code: 0
        Exceptional case: Permission denied
            stderr:
                 DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 434.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::st execute failed: UPDATE command denied to user 'user'@'localhost' for table 'datastore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 447.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 450.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'lookup' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 472.
                DBD::mysql::db do failed: DELETE command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 600.
                DBD::mysql::st execute failed: INSERT command denied to user 'user'@'localhost' for table 'binstore' /
                    at /usr/share/perl5/vendor_perl/Warewulf/DataStore/SQL/MySQL.pm line 604.
                ERROR:  put_chunk() failed with error:  INSERT command denied to user 'user'@'localhost' for /
                    table 'binstore'
                WARNING:  Could not open /etc/hosts: Permission denied
            Return Code: 0
        """
        # Check the pre-reqs: 1) Device has a hostname. 2) The device is in the provisioner
        device_name_for_provisioner = self.get_device_name_for_provisioner(device)
        if self.device_exists_in_provisioner(device_name_for_provisioner) is False:
            raise ProvisionerException("The device {} is not found in the provisioner."
                                       .format(device_name_for_provisioner))

        # Warewulf unset's fields by a special key...
        if args is None:
            args = self.UNSET_KEY

        output = self.utilities.execute_subprocess(
            ['wwsh', '-y', 'provision', 'set', device_name_for_provisioner, '--kargs={}'.format(args)])
        # Check for other, more general, errors.
        self._check_for_general_errors(output)

        if args == self.UNSET_KEY:
            device.pop(self.PROVISIONER_KARGS_KEY, None)
        else:
            device[self.PROVISIONER_KARGS_KEY] = args
        return device

    def list(self):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh node list
        Command Output:
        NAME                GROUPS              IPADDR              HWADDR
        ================================================================================
        test1               NodePool            192.168.1.11        00:1e:67:f9:ba:35
        test2               NodePool            192.168.1.50,192.168.2.50 00:1e:67:f9:ca:4d
        test3               UNDEF
        """
        output = self.utilities.execute_subprocess(['wwsh', 'node', 'list'])
        device_names = list()
        output_lines = output.stdout.splitlines()
        for device_line in output_lines:
            if device_line.startswith("NAME") or device_line.startswith("==================="):
                # Header lines
                continue
            device_names.append(device_line.split()[0])

        return device_names

    def list_images(self):
        """
        See @Provisioner for interface details. Implementation here.
        Command: wwsh vnfs list
        Command output:
        VNFS NAME            SIZE (M) CHROOT LOCATION
        custom               16.1     /root/imgs/custom
        redhat7.3            1672.2   /opt/intel/hpc-orchestrator/admin/images/redhat7.3
        centos7.3            407.1    /opt/intel/hpc-orchestrator/admin/images/centos7.3
        sles12sp1            1217.4   /opt/intel/hpc-orchestrator/admin/images/sles12sp1
        """
        output = self.utilities.execute_subprocess(['wwsh', 'vnfs', 'list'])
        image_names = list()
        output_lines = output.stdout.splitlines()
        for image_line in output_lines:
            if image_line.startswith("VNFS"):
                # Header lines
                continue
            image_names.append(image_line.split()[0])

        return image_names

    #
    # *************** Non-Interface methods *****************
    #

    @staticmethod
    def get_device_name_for_provisioner(device):
        """Get the apropriate name for this device"""
        name_for_provisioner = device.get("hostname")

        if name_for_provisioner is None:
            raise ProvisionerException("Could not get a hostname to use with this provisioner.")

        return name_for_provisioner

    def device_exists_in_provisioner(self, device_name_for_provisioner):
        """Check if this device is already in the provisioner"""
        command_output = self.utilities.execute_subprocess(['wwsh', 'node', 'print', device_name_for_provisioner])
        return command_output.return_code == 0

    @staticmethod
    def _get_hardware_address_key(device, interface):
        """Get the hardware haddress key. This is how it will appear in the configuration."""
        key = "mac_address"
        if device.get("default_network_interface", "eth0") != interface:
            key = "{}_{}".format(interface, key)
        return key

    @staticmethod
    def _get_ip_address_key(device, interface):
        """Get the IP address key. This is how it will appear in the configuration."""
        key = "ip_address"
        if device.get("default_network_interface", "eth0") != interface:
            key = "{}_{}".format(interface, key)
        return key

    @staticmethod
    def _check_for_general_errors(output, assert_is_zero=True):
        """Check for the most common errors in warewulf commands. Permission errors, and pad error codes."""
        if output.stderr is not None and Warewulf.DATABASE_INSERT_ERROR in output.stderr:
            raise ProvisionerException("Could not complete action due to insufficient"
                                       " permissions to the warewulf db.", output)
        if assert_is_zero and output.return_code != 0:
            raise ProvisionerException("Warewulf returned non-zero return code: {}".format(output.return_code), output)

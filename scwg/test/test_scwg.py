import unittest
import os
from scwg.config_parser import ConfigParser, Terminal


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config_parser = ConfigParser()
        self.test_config_file = os.path.join(os.path.dirname(__file__), 'test_config.xml')

    def tearDown(self):
        pass

    def testGetTerminalsReturnsList(self):
        self.config_parser.read_config_file(self.test_config_file)
        terminals = self.config_parser.get_terminals()
        self.assertIsInstance(terminals, list)
        self.assertEquals(3, len(terminals))

    
    def testParseSshConnection(self):
        xml_string = """
        <ssh user="root" ip="192.168.1.50" ran_tun="yes" /> 
        """
        connection = self.config_parser.parse_ssh_connection(xml_string)
        self.assertEquals('root', connection.user)
        self.assertEquals('192.168.1.50', connection.ip)
        self.assertEquals(True, connection.create_tunnel)


    def testParseTerminalNode(self):
        xml_string = """
        <term name="s_server2">
            <ssh user="root" ip="192.168.3.81" ran_tun="yes" /> 
            <ssh user="root" ip="192.168.6.84" ran_tun="yes" /> 
        </term>
        """
        terminal = self.config_parser.parse_terminal_node(xml_string)
        self.assertIsInstance(terminal, Terminal)
        self.assertIsInstance(terminal.connections, list)
        self.assertEquals('s_server2', terminal.name)
        self.assertEquals(2, len(terminal.connections))
        first_connection = terminal.connections[0]
        self.assertEquals('192.168.3.81', first_connection.ip)
        self.assertEquals(True, first_connection.create_tunnel)


        






if __name__ == '__main__':
    unittest.main()

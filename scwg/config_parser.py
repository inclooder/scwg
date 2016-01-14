
class SshConnection:

    def __init__(self, user, ip, create_tunnel, port = 22):
        self.user = user 
        self.ip = ip 
        self.create_tunnel = create_tunnel
        self.port = port
        
class Terminal:

    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)


from xml.dom import minidom

class ConfigParser:

    def __init__(self):
        self.terminals = []

    def read_config_file(self, config_file):
        dom_tree = minidom.parse(config_file)

        child_nodes = dom_tree.childNodes
        for child_node in child_nodes[0] .getElementsByTagName('term'):
            self.terminals.append(self.parse_terminal_node(child_node.toxml()))

    def parse_ssh_connection(self, xml_string):
        doc = minidom.parseString(xml_string)
        doc_element = doc.documentElement
        
        user = doc_element.getAttribute('user')
        ip = doc_element.getAttribute('ip')
        create_tunnel = doc_element.getAttribute('ran_tun')
        
        create_tunnel = (create_tunnel.lower() == 'yes')
        if(doc_element.hasAttribute('port')):
            port = doc_element.getAttribute('port')
            return SshConnection(user, ip, create_tunnel, int(port))
        else:
            return SshConnection(user, ip, create_tunnel)

    def parse_terminal_node(self, xml_string):
        doc = minidom.parseString(xml_string)
        doc_element = doc.documentElement
        terminal = Terminal(doc_element.getAttribute('name'))
        for child_node in doc_element.getElementsByTagName('ssh'):
            connection = self.parse_ssh_connection(child_node.toxml())
            terminal.add_connection(connection)


        return terminal


    def get_terminals(self):
        return self.terminals
    

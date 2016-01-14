from xml.dom import minidom
import config_parser

def appendTunnelPortGeneration(text):
    text += '\n'
    text += 'tun_port=`shuf -i 2000-65000 -n 1`\n'
    text += 'echo "Tunnel port $tun_port"\n'
    return text

def appendBashFunctionBegin(functionName, text):
    text += '{0}(){{\n'.format(functionName)
    return text


def appendBashFunctionEnd(text):
    text += '}\n'
    return text


def appendSshCall(userName = 'root', ipAddress = 'localhost', port = 22, tunnelPort = None, text = ''):
        text += 'ssh {0}@{1} '.format(userName, ipAddress)
        if port:
            text += '-p {0} '.format(port)

        if tunnelPort:
            text += '-L {1}:localhost:{0}\n'.format(port, tunnelPort)
        else:
            text += '\n'

        return text


def create_func(term):
    temp='\n'
    _name = term.name
    temp = appendBashFunctionBegin(_name, temp)

    elems=[]
    for conn in term.connections:
        elems.append(conn)


    if elems[0]:
        ran_tun = elems[0].create_tunnel
        if ran_tun:
            temp = appendTunnelPortGeneration(temp)

        _port = elems[0].port
        _last_ip = elems[0].ip
        temp = appendSshCall(text = temp, userName = elems[0].user, ipAddress = _last_ip, port = _port, tunnelPort = '$tun_port')


    for elem in elems[1:]:
      ran_tun = elem.create_tunnel

      temp+='if [ $? -eq 255 ]; then\n'
      temp+='echo "Nie mozna sie polaczyc z adresem {0}"\n'.format(_last_ip)

      _last_ip=elem.ip
      _port = elem.port
      temp = appendSshCall(text = temp, userName = elem.user, ipAddress = elem.ip, port = _port, tunnelPort = '$tun_port')

      temp+='fi\n'

    temp = appendBashFunctionEnd(temp)
    return temp


import sys

def main(argv):
    try:
        argv[1]
    except IndexError:
        print "usage {0} <configfile>"
        sys.exit(2)

    parser =  config_parser.ConfigParser()
    configfile = argv[1]
    parser.read_config_file(configfile)

    file_temp='''
#!/bin/sh
'''
    terminals = parser.get_terminals()



    for term in terminals:
        file_temp += create_func(term)

    print file_temp


if __name__ == "__main__":
    main(sys.argv)

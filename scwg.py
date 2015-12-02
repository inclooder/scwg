from xml.dom import minidom

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
    _name=term.getAttribute('name')
    temp = appendBashFunctionBegin(_name, temp)

    elems=[]
    for conn in term.childNodes:
        if isinstance(conn, minidom.Element):
            elems.append(conn)


    if elems[0]:
        if elems[0].getAttribute('ran_tun') == 'yes':
          ran_tun = True
        else:
          ran_tun = False

        if ran_tun:
            temp = appendTunnelPortGeneration(temp)

        _port = elems[0].getAttribute('port') or 22
        _last_ip = elems[0].getAttribute('ip')
        temp = appendSshCall(text = temp, userName = elems[0].getAttribute('user'), ipAddress = _last_ip, port = _port, tunnelPort = '$tun_port')


    for elem in elems[1:]:
      if elem.getAttribute('ran_tun') == 'yes':
          ran_tun = True
      else:
          ran_tun = False

      temp+='if [ $? -eq 255 ]; then\n'
      temp+='echo "Nie mozna sie polaczyc z adresem {0}"\n'.format(_last_ip)

      _last_ip=elem.getAttribute('ip')
      _port = elem.getAttribute('port') or 22
      temp = appendSshCall(text = temp, userName = elem.getAttribute('user'), ipAddress = elem.getAttribute('ip'), port = _port, tunnelPort = '$tun_port')

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

    configfile = argv[1]
    DOMTree = minidom.parse(configfile)
    #print DOMTree.toxml()

    cNodes = DOMTree.childNodes
    file_temp='''
#!/bin/sh
'''
    for term in cNodes[0].getElementsByTagName("term"):
        file_temp += create_func(term)

    print file_temp


if __name__ == "__main__":
    main(sys.argv)

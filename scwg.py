from xml.dom import minidom


def create_func(term):
    temp='\n'
    _name=term.getAttribute('name')
    temp+='{0}(){{\n'.format(_name)

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
            temp+='''
tun_port=`shuf -i 2000-65000 -n 1`
echo "Tunnel port $tun_port"
'''

        _last_ip=elems[0].getAttribute('ip')
        temp+='ssh {0}@{1} '.format(elems[0].getAttribute('user'), elems[0].getAttribute('ip'))
        _port = elems[0].getAttribute('port') or 22
        if _port:
            temp+= '-p {0} '.format(_port)

        if ran_tun:
            temp+='-L $tun_port:localhost:{0}\n'.format(_port)
        else:
            temp+='\n'


    for elem in elems[1:]:
      if elem.getAttribute('ran_tun') == 'yes':
          ran_tun = True
      else:
          ran_tun = False

      temp+='if [ $? -eq 255 ]; then\n'
      temp+='echo "Nie mozna sie polaczyc z adresem {0}"\n'.format(_last_ip)

      _last_ip=elem.getAttribute('ip')
      temp+='ssh {0}@{1} '.format(elem.getAttribute('user'), elem.getAttribute('ip'))
      _port = elem.getAttribute('port') or 22
      if _port:
          temp+= '-p {0} '.format(_port)

      if ran_tun:
          temp+='-L $tun_port:localhost:{0}\n'.format(_port)
      else:
          temp+='\n'


      temp+='fi\n'

    temp+='}\n'
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

# About

Scwg is a tiny tool that helps you connect to ssh server.
Scwg creates bash function for each server you define.
Servers can have multiple addresses.
Firstly you'll need to create xml file with server definition. 
Take a look at this example.  
```xml
<config>
  <term name="s_server1">
    <ssh user="root" ip="192.168.1.100" ran_tun="no" /> 
  </term>
  
  <term name="s_server2">
    <ssh user="root" ip="192.168.1.50" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.1.65" ran_tun="yes" /> 
  </term>
  
  <term name="s_server2">
    <ssh user="root" ip="192.168.2.80" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.3.81" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.4.82" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.5.83" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.6.84" ran_tun="yes" /> 
    <ssh user="root" ip="192.168.7.85" ran_tun="yes" /> 
  </term>
</config>
```


# Requirements
* Python 2.7
* bash

# Installation
```sh
apt-get install python
python setup.py install
```

# Usage
```sh
python scwg.py config_template.xml
```

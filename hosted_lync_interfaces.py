from http import server
import re
import sys



configuration_file = input("Enter name of the configuration file:")

def lastWord(string):
    newstring = ""     # taking empty string
    length = len(string)    # calculating length of string 
    for i in range(length-1, 0, -1):    # traversing from last   
        if (string[i] == " "):     # if space is occurred then return
            return newstring[::-1] # return reverse of newstring
        else:
            newstring = newstring + string[i]


def vdom_names(conf_file):
    vdoms = []
    conf_g_token = 0
    search_token = 0
    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                search_token = 1
                continue
            if "edit" in line and search_token == 1:
                vdom = re.search(r"(edit)\s(.+)", line).group(2)
                vdoms.append(vdom)
                search_token = 0
    interface_zones
    return(vdoms)




def interface_zones(conf_file):
    interfaces = []
    tmp_dict = {
        'vdom': '-',
        'zone': '-',
        'name': '-'
    }
    conf_g_token = 0
    search_token = 0
    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                search_token = 1
                continue
            if "edit" in line and search_token == 1:
                vdom = re.search(r"(edit)\s(.+)", line).group(2)
                tmp_dict['vdom'] = vdom
                search_token = 2
                #print(vdom)
            if "config system zone" in line and search_token == 2:
                search_token = 3
            if 'edit' in line and search_token == 3:
                zone = re.search(r"(edit)\s(.+)", line).group(2)
                tmp_dict['zone'] = zone
                #print ('\t', zone.strip('\"'))
            if 'set interface' in line and search_token == 3:
                interface = re.search('(?<=set interface).*', line).group(0)
                interface_list = interface.split()
                tmp_dict['name'] = interface_list
                #print(interface_list)
            if line.strip() == 'next' and search_token == 3:
                interfaces.append(tmp_dict)
                tmp_dict = {
                    'vdom': vdom,
                    'zone': '-',
                    'name': '-'
                }
                continue
            if line.strip() == 'end' and search_token == 3:
                tmp_dict = {
                    'vdom': '-',
                    'zone': '-',
                    'name': '-'
                }
                search_token = 0
    
    return(interfaces)

                
def interface_config(conf_file):
    search_token = 0
    tmp_lines = []
    tmp_dict = {
        'name': '-',
        'vdom': '-',
        'type': '-',
        'vlan_int': '-',
        'vlan_id': '-'
    }
    interfaces = []

    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "config system interface" in line:
                search_token = 4
            if search_token == 4:
                tmp_lines.append(line)
            if line.strip() == 'end':
                search_token = 0
        
        for line in tmp_lines:
            if "edit" in line:
                name = re.search('\".*\"', line).group(0)
                #print(name)
                tmp_dict['name'] = name
                continue
            elif 'set vdom' in line:
                vdom = re.search('\".*\"', line).group(0)
                tmp_dict['vdom'] = vdom.strip('\"')
                #print(tmp_dict['vdom'])
                continue
            elif 'set type' in line:
                type = lastWord(line.rstrip())
                #print(type)
                tmp_dict['type'] = type
                continue
            elif 'set interface' in line:
                vlan_int = re.search('\".*\"', line).group(0)
                #print(vlan_int)
                tmp_dict['vlan_int'] = vlan_int
                continue
            elif 'set vlanid' in line:
                vlan_id = re.search('[0-9]+', line).group(0)
                #print(vlan_id)
                tmp_dict['vlan_id'] = vlan_id
                continue
            elif line.strip() == 'next':
                interfaces.append(tmp_dict)
                tmp_dict = {
                    'name': '-',
                    'vdom': '-',
                    'type': '-',
                    'vlan_int': '-',
                    'vlan_id': '-'
                }
                continue

    return(interfaces)


def hlync_sources(conf_file):
    search_token = 0
    tmp_lines = []
    tmp_dict = {
        'name': '-',
        'vdom': '-',
        'ip': '-',
        'vlan_id': '-'
    }
    interfaces = []

    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "config system interface" in line:
                search_token = 4
            if search_token == 4:
                tmp_lines.append(line)
            if line.strip() == 'end':
                search_token = 0

    for line in tmp_lines:
        #if re.match(r'\s+edit \"...-internal', line) or re.match(r'\s+edit \"...-dmz-int', line):
        if re.match(r'\s+edit \"...-internal', line):
            name = re.search('\".*\"', line).group(0)
            tmp_dict['name'] = name.strip('\"')
            search_token = 5
            #print(tmp_dict['name'])
            continue
        if re.match(r'\s+edit \"...-dmz-int', line):
            name = re.search('\".*\"', line).group(0)
            tmp_dict['name'] = name.strip('\"')
            search_token = 5
            #print(tmp_dict['name'])
            continue
        if 'set vdom' in line and search_token == 5:
            vdom = re.search('\".*\"', line).group(0)
            tmp_dict['vdom'] = vdom.strip('\"')
            #print(tmp_dict['vdom'])
            continue
        if 'set ip' in line and search_token == 5:
            ip = re.search('\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+', line).group(0)
            tmp_dict['ip'] = ip
            #print(tmp_dict['ip'])
            continue
        elif 'set vlanid' in line and search_token == 5:
            vlan_id = re.search('[0-9]+', line).group(0)
            tmp_dict['vlan_id'] = vlan_id
            #print(tmp_dict['vlan_id'])
            continue
        elif line.strip() == 'next' and search_token == 5:
            interfaces.append(tmp_dict)
            tmp_dict = {
                'name': '-',
                'vdom': '-',
                'ip': '-',
                'vlan_id': '-'
            }
            search_token = 0
            continue

    return(interfaces)



def bgp(conf_file):

    vdoms = []
    conf_g_token = 0

    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                continue
            if "set as " in line and conf_g_token == 1:
                if not vdom in vdoms:
                    vdoms.append(vdom)
    
    return(vdoms)


def ipsec(conf_file):

    vdoms = []
    conf_g_token = 0

    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                continue
            if "config vpn ipsec " in line and conf_g_token == 1:
                if not vdom in vdoms:
                    vdoms.append(vdom)
    
    return(vdoms)
                

def routing (conf_file):

    tmp_dict = {
        'vdom': '',
        'dst': '0.0.0.0 0.0.0.0',
        'gateway': '',
        'device': '',
        'comment': ''
    }

    routes = []
    conf_g_token = 0
    search_token = 0

    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                tmp_dict['vdom'] = vdom.strip('\"')
                search_token = 1
                continue
            if 'config router static' in line and search_token == 1:
                search_token = 2
            if 'edit' in line and search_token == 2:
                search_token = 3
            if 'set dst' in line and search_token == 3:
                destination = re.search('\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+', line).group(0)
                tmp_dict['dst'] = destination
                #print(tmp_dict['dst'])
            if 'set gateway' in line and search_token == 3:
                gateway = re.search('\d+\.\d+\.\d+\.\d+', line).group(0)
                tmp_dict['gateway'] = gateway
                #print(tmp_dict['gateway'])
            if 'set device' in line and search_token == 3:
                device = re.search('\".*\"', line).group(0)
                tmp_dict['device'] = device
                #print(tmp_dict['device'])
            if 'set comment' in line and search_token == 3:
                comment = re.search('\".*\"', line).group(0)
                tmp_dict['comment'] = comment
                #print(tmp_dict['comment'])
            if 'next' in line and search_token == 3:
                routes.append(tmp_dict)
                search_token = 2
                tmp_dict = {
                    'vdom': vdom,
                    'dst': '0.0.0.0 0.0.0.0',
                    'gateway': '',
                    'device': '',
                    'comment': ''
                }
            if 'end' in line and search_token == 2:
                tmp_dict = {
                    'vdom': '',
                    'dst': '0.0.0.0 0.0.0.0',
                    'gateway': '',
                    'device': '',
                    'comment': ''
                }
                search_token = 0

    return(routes)



def ssl_vpn(conf_file):

    vdoms = []
    conf_g_token = 0

    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                continue
            if "set tunnel-ip" in line and conf_g_token == 1:
                if not vdom in vdoms:
                    vdoms.append(vdom)
    
    return(vdoms) 


def fw_vip(conf_file):

    vips = []
    conf_g_token = 0
    search_token = 0

    tmp_dict = {
        'vdom': '',
        'extip': '',
        'mappedip': '',
        'extport': '',
        'mappedport': ''
    }
    
    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                tmp_dict['vdom'] = vdom.strip('\"')
                search_token = 1
                #print(tmp_dict['vdom'])
                continue
            if line.strip() == 'config firewall vip' and conf_g_token == 1:
                search_token = 2
            if 'edit' in line and search_token == 2:
                search_token = 3
            if 'set extip' in line and search_token == 3:
                extip = lastWord(line.rstrip())
                tmp_dict['extip'] = extip
                #print(tmp_dict['extip'])
            if 'set mappedip' in line and search_token == 3:
                mappedip = lastWord(line.rstrip()).strip('\"')
                tmp_dict['mappedip'] = mappedip
                #print(tmp_dict['mappedip'])
            if 'set extport' in line and search_token == 3:
                extport = lastWord(line.rstrip())
                tmp_dict['extport'] = extport
                #print(tmp_dict['extport'])
            if 'set extport' in line and search_token == 3:
                mappedport = lastWord(line.rstrip())
                tmp_dict['mappedport'] = mappedport
                #print(tmp_dict['mappedport'])
            if line.strip() == 'next' and search_token == 3:
                search_token = 2
                vips.append(tmp_dict)
                tmp_dict = {
                    'vdom': vdom,
                    'extip': '',
                    'mappedip': '',
                    'extport': '',
                    'mappedport': ''
                }
            if line.strip() == 'end' and search_token == 2:
                tmp_dict = {
                    'vdom': '',
                    'extip': '',
                    'mappedip': '',
                    'extport': '',
                    'mappedport': ''
                }
                search_token = 0

    return(vips)
                


def voip_alg_mode(conf_file):

    vdoms = []
    conf_g_token = 0
    search_token = 0

    tmp_dict = {
        'vdom': '',
        'mode': 'proxy-based'
    }

    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # skipp global config
            if "config global" in line:
                conf_g_token = 1
                continue
            if "config vdom" in line and conf_g_token == 1:
                edit_vdom = lines[index + 1].rstrip()
                vdom = re.search('(?<=\s).*', edit_vdom).group(0)
                tmp_dict['vdom'] = vdom.strip('\"')
                search_token = 1
                continue
            if 'config system settings' in line and search_token == 1:
                search_token = 2
            if 'kernel-helper-based' in line and search_token == 2:
                tmp_dict['mode'] = 'kernel-helper-based'
            if 'end' in line and search_token == 2:
                vdoms.append(tmp_dict)
                search_token = 0
                tmp_dict = {
                    'vdom': '',
                    'mode': 'proxy-based'
                }
    return(vdoms)
            

def certificates(conf_file):

    certs = []
    search_token = 0

    tmp_dict = {
        'type': '',
        'cert': ''
    }

    with open(conf_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "config certificate ca" in line and search_token == 0:
                tmp_dict['type'] = 'ca_cert'
                search_token = 1
                continue
            if 'edit' in line and search_token == 1:
                crt = re.search(r"(edit)\s(.+)", line).group(2)
                tmp_dict['cert'] = crt
            if line.strip() == 'next' and search_token == 1:
                certs.append(tmp_dict)
                tmp_dict = {
                    'type': 'ca_cert',
                    'cert': ''
                }
            if line.strip() == 'end' and search_token == 1:
                tmp_dict = {
                    'type': '',
                    'cert': ''
                }
                search_token = 0
            if "config certificate local" in line and search_token == 0:
                tmp_dict['type'] = 'local_cert'
                search_token = 2
            if 'edit' in line and search_token == 2:
                crt = re.search(r"(edit)\s(.+)", line).group(2)
                tmp_dict['cert'] = crt
            if line.strip() == 'next' and search_token == 2:
                certs.append(tmp_dict)
                tmp_dict = {
                    'type': 'local_cert',
                    'cert': ''
                }
            if line.strip() == 'end' and search_token == 2:
                tmp_dict = {
                    'type': '',
                    'cert': ''
                }
                search_token = 0

    return(certs)


### Print functions


def print_vdoms():
    # Print all VDOMs
    vdoms = vdom_names(configuration_file)

    for vdom in vdoms:
        print(vdom)


def print_int_zones():
    # Loop to print all security zones and associated interfaces
    vdoms = vdom_names(configuration_file)
    int_zones = interface_zones(configuration_file)

    for vdom in vdoms:
        for interface in int_zones:
            if interface['vdom'] == vdom:
                for int_name in interface['name']:
                        print(f"{interface['vdom']},{interface['zone']},{int_name}")

                       

def print_int_types():
    # Loop to print all interfaces types
    vdoms = vdom_names(configuration_file)
    int_config = interface_config(configuration_file)

     
    for vdom in vdoms:
        for interface in int_config:
            if interface['vdom'] == vdom:
                print(f"{interface['vdom']},{interface['name']},{interface['type']},{interface['vlan_int']},{interface['vlan_id']}")



def print_hl_int():
    # Loop to print Hosted_Lync interfaces
    hlync_src = hlync_sources(configuration_file)

    sorted_hlync_src = sorted(hlync_src, key=lambda d: d['vdom'])
    for interface in sorted_hlync_src:
        print(f"{interface['vdom']},{interface['name']},{interface['ip']},{interface['vlan_id']}")


def print_bgp_vdoms():
    # Print all VDOMs with BGP configuration

    bgp_vdom = bgp(configuration_file)

    for vdom in bgp_vdom:
        print(vdom)

def print_ipsec_vdoms():
    # Print all VDOMs with IPSec configuration
    ipsec_vdom = ipsec(configuration_file)

    for vdom in ipsec_vdom:
        print(vdom)

def print_static_routes():
    # Print all static routes in all VDOMs
    routes = routing(configuration_file)

    for route in routes:
        print(f"{route['vdom']},{route['dst']},{route['gateway']},{route['device']},{route['comment']}")

def print_ssl_vpn():
    # Print all VDOMs with SSL VPN configuration
    
    ssl_vdom = ssl_vpn(configuration_file)

    for vdom in ssl_vdom:
        print(vdom)


def print_fw_vip():
    # Print all VDOMs with firewall vip configuration
    
    vips = fw_vip(configuration_file)

    for vip in vips:
        print(f"{vip['vdom']},{vip['mappedip']},{vip['mappedport']},{vip['extip']},{vip['extport']}")

def print_voip_alg():
    # Print default VoIP ALG mode for all VDOMS
    alg_mode = voip_alg_mode(configuration_file)

    for vdom in alg_mode:
        print(f"{vdom['vdom']},{vdom['mode']}")

def print_certificates():
    # Print all certificates

    certs = certificates(configuration_file)

    for cert in certs:
        print(f"{cert['type']},{cert['cert']}")



### CLI interface loop

ans=True
while ans:
    print ("""
    1. Print all VDOMs
    2. Print all security zones and associated interfaces
    3. Print all interfaces and associated configuration
    4. Print interfaces sending traffic to Hosted_Lync
    5. Print all VDOMs with BGP configuration
    6. Print all VDOMs with IPSec confguration
    7. Print all static routes
    8. Print all VDOMs with SSL VPN configuration
    9. Print all VIP (NAT) configuration
    10. Print default VoIP ALG mode for all VDOMS
    11. Print all certificates
    98. Use different configuration file
    99. Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1": 
        print_vdoms() 
    elif ans=="2":
        print_int_zones()
    elif ans=="3":
        print_int_types()
    elif ans=="4":
        print_hl_int()
    elif ans=="5":
        print_bgp_vdoms()
    elif ans=="6":
        print_ipsec_vdoms()
    elif ans=="7":
        print_static_routes()
    elif ans=="8":
        print_ssl_vpn()
    elif ans=="9":
        print_fw_vip()
    elif ans=="10":
        print_voip_alg()
    elif ans=="11":
        print_certificates()
    elif ans=="98":
        configuration_file = input("Enter name of the configuration file:")
    elif ans=="99":
        sys.exit() 
    elif ans !="":
        print("\n Not Valid Choice Try again") 


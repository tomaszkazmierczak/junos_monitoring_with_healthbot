###################################################
# Workflow: create devices, add tables and views, add notifications, create topics, create rules, create playbooks, create device-groups
###################################################

###################################################
# requirements: pip install requests
###################################################

###################################################
# usage: 
# vi variables.yml
# python ./configure_healthbot.py
###################################################

###################################################
# This block indicates the various imports
###################################################

import os
import json
import yaml
import requests
from jinja2 import Template
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint

##################################################
# This block defines the functions we will use
###################################################

def import_variables_from_file():
    my_variables_file=open('variables.yml', 'r')
    my_variables_in_string=my_variables_file.read()
    my_variables_in_yaml=yaml.load(my_variables_in_string)
    my_variables_file.close()
    return my_variables_in_yaml

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def add_device(dev):
    payload=json.dumps(dev)
    r = requests.post(url + '/device/' + dev['device-id'] + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False, data=payload)
    print 'loaded the healthbot configuration for device ' + dev['device-id']
    return r.status_code

def get_devices_name_in_running_configuration():
    r = requests.get(url + '/device/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the list of devices in the running configuration"
    pprint(r.json())
    return r.status_code

def get_devices_details_in_running_configuration():
    r = requests.get(url + '/devices/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the devices details in the running configuration "
    pprint (r.json())
    return r.status_code

def get_devices_name_in_candidate_configuration():
    r = requests.get(url + '/device/?working=true', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the list of devices in the candidate configuration"
    pprint(r.json())
    return r.status_code

def get_devices_details_in_candidate_configuration():
    r = requests.get(url + '/devices/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the devices details in the candidate configuration "
    pprint (r.json())
    return r.status_code

def commit():
    r = requests.post(url + '/configuration', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print 'healthbot configuration commited'
    return r.status_code

def get_tables_and_views(table):
    files = {'up_file': open('tables_and_views/' + table,'r')}
    r=requests.get(url + '/files/helper-files/' + table, auth=HTTPBasicAuth(authuser, authpwd), headers={ 'Accept' : 'application/json', 'Content-Type': 'multipart/form-data' }, verify=False)
    print r.content
    return r.status_code

def add_tables_and_views(table):
    files = {'up_file': open('tables_and_views/' + table,'r')}
    r=requests.post(url + '/files/helper-files/' + table, auth=HTTPBasicAuth(authuser, authpwd), headers={ 'Accept' : 'application/json' }, verify=False, files=files)
    print "added table " + table 
    return r.status_code

def add_device_group(group):
    payload=json.dumps(group)
    r = requests.post(url + '/device-group/' + group['device-group-name'] + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False, data=payload)
    print 'loaded the healthbot device group ' + group['device-group-name']
    return r.status_code

def get_device_group(group):
    r = requests.get(url + '/device-group/'+ group + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def get_device_groups():
    r = requests.get(url + '/device-group/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def add_notification(notification):
    payload=json.dumps(notification)
    r = requests.post(url + '/notification/' + notification['notification-name'] + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False, data=payload)
    print 'loaded the healthbot notification ' + notification['notification-name']
    return r.status_code

def get_notifications():
    r = requests.get(url + '/notification/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def get_playbooks():
    r = requests.get(url + '/playbook/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def get_playbook(playbook):
    r = requests.get(url + '/playbook/'+ playbook['playbook-name']  + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def add_playbook(playbook):
    payload=json.dumps(playbook)
    r = requests.post(url + '/playbook/' + playbook['playbook-name'] + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False, data=payload)
    return r.status_code

def get_topics():
    r = requests.get(url + '/topic/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def get_topic(topic):
    r = requests.get(url + '/topic/'+ topic + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def add_topic(topic):
    payload=json.dumps(topic)
    r = requests.post(url + '/topic/' + topic['topic-name'] + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False, data=payload)
    return r.status_code

def get_rules(topic):
    r = requests.get(url + '/topic/' + topic + '/rule/' , auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

def get_rule(topic, rule):
    r = requests.get(url + '/topic/' + topic + '/rule/' + rule + '/' , auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    pprint (r.json())
    return r.status_code

######################################################
# Below blocks are REST calls to configure healthbot
######################################################

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
my_variables_in_yaml=import_variables_from_file()
server = my_variables_in_yaml['server']
authuser = my_variables_in_yaml['authuser']
authpwd = my_variables_in_yaml['authpwd']
url = 'https://'+ server + ':8080/api/v1'
headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json' }



######################################################
# This block is to add devices to healthbot
######################################################

print '###########  Adding devices  ############'


get_devices_name_in_running_configuration()

print "adding devices to healthbot"

for item in my_variables_in_yaml['devices_list']:
    add_device(item)

get_devices_name_in_candidate_configuration()

commit()

get_devices_name_in_running_configuration()

# get_devices_details_in_running_configuration()


######################################################
# This block is to add tables (tables and views) to healthbot
######################################################

print '###########  Adding tables and views  ############'


for item in my_variables_in_yaml['tables_and_views']:
    add_tables_and_views(item)
    get_tables_and_views(item)


######################################################
# This block is to add notifications to healtbot
######################################################

print '###########  Adding notifications  ############'

get_notifications()

for item in my_variables_in_yaml['notifications']:
    add_notification(item)

commit()

get_notifications()

######################################################
# This block is to add topics to healtbot
######################################################

print '###########  Adding topics  ############'

for item in my_variables_in_yaml['topics']:
    add_topic(item)

commit()

get_topics()

#for item in my_variables_in_yaml['topics']:
#    get_topic(item)

######################################################
# This block is to add playbooks to healthbot
######################################################

print '###########  Adding playbooks  ############'


for item in my_variables_in_yaml['playbooks']:
    add_playbook(item)

commit()

get_playbooks()

for item in my_variables_in_yaml['playbooks']:
    get_playbook(item)




######################################################
# This block is to add device groups to healtbot
######################################################

print '###########  Adding device groups  ############'

get_device_groups()

for item in my_variables_in_yaml['device_groups']: 
    add_device_group(item)

commit()

get_device_groups()


for item in my_variables_in_yaml['device_groups']:
    get_device_group(item['device-group-name'])

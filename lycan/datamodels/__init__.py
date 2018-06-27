#
#  The MIT License (MIT)
#
# Copyright 2018 AT&T Intellectual Property. All other rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# OpenC2 CSD04 Language Spec

# actions
SCAN = "scan"
LOCATE = "locate"
QUERY = "query"
REPORT = "report"
NOTIFY = "notify"
DENY = "deny"
CONTAIN = "contain"
ALLOW = "allow"
START = "start"
STOP = "stop"
RESTART = "restart"
PAUSE = "pause"
RESUME = "resume"
CANCEL = "cancel"
SET = "set"
UPDATE = "update"
MOVE = "move"
REDIRECT = "redirect"
CREATE = "create"
DELETE = "delete"
SNAPSHOT = "snapshot"
DETONATE = "detonate"
RESTORE = "restore"
SAVE = "save"
THROTTLE = "throttle"
DELAY = "delay"
SUBSTITUTE = "substitute"
COPY = "copy"
SYNC = "sync"
INVESTIGATE = "investigate"
MITIGATE = "mitigate"
REMEDIATE = "remediate"

# targets
ARTIFACT = "artifact"
COMMAND = "command"
DEVICE = "device"
DIRECTORY = "directory"
DISK = "disk"
DISK_PARTITON = "disk_partition"
DOMAIN_NAME = "domain_name"
EMAIL_ADDR = "email_addr"
EMAIL_MESSAGE = "email_message"
FILE = "file"
IP_ADDR = "ip_addr"
MAC_ADDR = "mac_addr"
MEMORY = "memory"
IP_CONNECTION = "ip_connection"
OPENC2 = "openc2"
PROCESS = "process"
PROPERTY = "property"
SOFTWARE = "software"
URL = "url"
USER_ACCOUNT = "user_account"
USER_SESSION = "user_session"
VOLUME = "volume"
WINDOWS_REGISTRY_KEY = "windows_registry_key"
X509_CERTIFICATE = "x509_certificate"
SLPFF = "slpff"

# actuators
ENDPOINT = "endpoint"
ENDPOINT_WORKSTATION = "endpoint_workstation"
ENDPOINT_SERVER = "endpoint_server"
NETWORK = "network"
NETWORK_FIREWALL = "network_firewall"
NETWORK_ROUTER = "network_router"
NETWORK_PROXY = "network_proxy"
NETWORK_SENSOR = "network_sensor"
NETWORK_HIPS = "network_hips"
NETWORK_SENSE_MAKING = "network_sense_making"
PROCESS = "process"
PROCESS_ANTI_VIRUS_SCANNER = "process_anti_virus_scanner"
PROCESS_AAA_SERVICE = "process_aaa_service"
PROCESS_VIRTUALIZATION_SERVICE = "process_virtualization_service"
PROCESS_SANDBOX = "process_sandbox"
PROCESS_EMAIL_SERVICE = "process_email_service"
PROCESS_DIRECTORY_SERVICE = "process_directory_service"
PROCESS_REMEDIATION_SERVICE = "process_remediation_service"
PROCESS_LOCATION_SERVICE = "process_location_service"

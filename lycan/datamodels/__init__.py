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

# OpenC2 0.4 Language Spec

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
DISTILL = "distill"
AUGMENT = "augment"
INVESTIGATE = "investigate"
MITIGATE = "mitigate"
REMEDIATE = "remediate"
RESPONSE = "response"
ALERT = "alert"

# targets
ARTIFACT = "artifact"
DEVICE = "device"
DIRECTORY = "directory"
DISK = "disk"
DISK_PARTITON = "disk-partition"
DOMAIN_NAME = "domain-name"
EMAIL_ADDR = "email-addr"
EMAIL_MESSAGE = "email-message"
FILE = "file"
IP_CONNECTION = "ip-connection"
IPV4_ADDR = "ipv4-addr"
IPV6_ADDR = "ipv6-addr"
MAC_ADDR = "mac-addr"
MEMORY = "memory"
OPENC2 = "openc2"
PROCESS = "process"
SOFTWARE = "software"
URL = "url"
USER_ACCOUNT = "user-account"
USER_SESSION = "user-session"
VOLUME = "volume"
WINDOWS_REGISTRY_KEY = "windows-registry-key"
X509_CERTIFICATE = "x509-certificate"

# actuators
ENDPOINT = "endpoint"
ENDPOINT_WORKSTATION = "endpoint-workstation"
ENDPOINT_SERVER = "endpoint-server"
NETWORK = "network"
NETWORK_FIREWALL = "network-firewall"
NETWORK_ROUTER = "network-router"
NETWORK_PROXY = "network-proxy"
NETWORK_SENSOR = "network-sensor"
NETWORK_HIPS = "network-hips"
NETWORK_SENSE_MAKING = "network-sense-making"
PROCESS = "process"
PROCESS_ANIT_VIRUS_SCANNER = "process-anit-virus-scanner"
PROCESS_AAA_SERVICE = "process-aaa-service"
PROCESS_VIRTUALIZATION_SERVICE = "process-virtualization-service"
PROCESS_SANDBOX = "process-sandbox"
PROCESS_EMAIL_SERVICE = "process-email-service"
PROCESS_DIRECTORY_SERVICE = "process-directory-service"
PROCESS_REMEDIATION_SERVICE = "process-remediation-service"
PROCESS_LOCATION_SERVICE = "process-location-service"

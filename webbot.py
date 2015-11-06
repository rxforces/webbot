#!/usr/bin/python

import json
import os
import requests
import socket
import time
from dogapi import dog_http_api as api

# DataDog settings
api.api_key = '<REPLACEME>'
api.application_key = '<REPLACEME>'

def try_action(ssh_key):
    # access an API
    # code snipped

def cleanup_action():
    # access an API
    # code snipped

def send_to_datadog(host, success):
    ts = int(time.time())
    if success:
        result = "success"
    else:
        result = "failure"
    metric_name = "example.integration.{}".format(result)
    api.metric(metric_name, (ts, 1), tags=["host:{}".format(host)])
    print ("POSTED to DataDog")

def trigger_pagerduty(host, message):
    trigger = {"service_key" :  "<REPLACEME>",
               "event_type" : "trigger",
               "description" : "Integration test failure",
               "client" : "Example Integration Test",
               "client_url" : socket.gethostname(),
               "details" : { "failed_host": host,
                             "provider" : provider,
                             "message" : message }
                           }
    requests.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json', json = trigger)
    print ("TRIGGERED PagerDuty")

host = os.environ['HOST']
ssh_key = os.environ['SSH_KEY']
oauth_token = os.environ.get('OAUTH_TOKEN')

overall_success = False
message = ''

for i in range(2):
    (success, message) = try_action(ssh_key)
    overall_success = (success or overall_success)
    send_to_datadog(host, success)
    (success, message) = cleanup_action()

if not overall_success:
        trigger_pagerduty(host, message)

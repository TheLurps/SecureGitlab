#!/usr/bin/env python3

import argparse
import sys
import requests
import json

def disable_public_signup(url, token):
    endpoint = '/api/v4/application/settings'
    r = requests.get(url + endpoint, headers={'PRIVATE-TOKEN': token})
    id = r.json()['id']
    r = requests.put(url + endpoint, headers={'PRIVATE-TOKEN': token}, data={'id': id, 'signup_enabled': False})
    new_state = r.json()['signup_enabled']

    if new_state == False:
        print('Disabling public user signup')
    else:
        print('Disabling public user signup failed')

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('--url', help='URL of GitLab instance', type=str)
    parser.add_argument('--private-token', dest='token', help='Private token of admin user', type=str)

    parser.add_argument('--disable-public-signup', dest='disable_public_signup', action='store_true', help='Disable public user signup')

    args=parser.parse_args()

    if (args.url == None or args.token == None):
        parser.print_help()
        exit()

    if args.disable_public_signup:
        disable_public_signup(args.url, args.token)


if __name__ == '__main__':
    main()
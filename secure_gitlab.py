#!/usr/bin/env python3

import argparse
import requests

def disable_public_signup(url, token):
    endpoint = '/api/v4/application/settings'
    r = requests.get(url + endpoint, headers={'PRIVATE-TOKEN': token})
    id = r.json()['id']
    r = requests.put(url + endpoint, headers={'PRIVATE-TOKEN': token}, data={'id': id, 'signup_enabled': False})
    print('{0}: Disabling public sign up'.format('SUCCESS' if not r.json()['signup_enabled'] else 'FAILURE'))

def fetch_users(url, token):
    endpoint = '/api/v4/users'
    r = requests.get(url + endpoint, headers={'PRIVATE-TOKEN': token})
    return r.json()

def depromote_user(url, token, userid):
    endpoint = '/api/v4/users/' + str(userid)
    r = requests.put(url + endpoint, headers={'PRIVATE-TOKEN': token}, data={'id': userid, 'admin': False})
    print('{0}: Depromoting user {1}'.format('SUCCESS' if not r.json()['is_admin'] else 'FAILURE', r.json()['username']))

def block_user(url, token, userid):
    endpoint = '/api/v4/users/' + str(userid) + '/block'
    r = requests.post(url + endpoint, headers={'PRIVATE-TOKEN': token}, data={'id': userid})
    r = requests.get(url + '/api/v4/users/' + str(userid), headers={'PRIVATE-TOKEN': token})
    print('{0}: Blocking user {1}'.format('SUCCESS' if r.json()['state'] == 'blocked' else 'FAILURE', r.json()['username']))

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('--url', help='URL of GitLab instance', type=str)
    parser.add_argument('--private-token', dest='token', help='Private token of admin user', type=str)

    parser.add_argument('--disable-public-signup', dest='disable_public_signup', action='store_true', help='Disable public user signup')
    parser.add_argument('--except-user', dest='except_users', help='List of users that should should be excepted (comma-separated)')
    parser.add_argument('--depromote-users', dest='depromote_users', action='store_true', help='Depromote all users from admin role except specified ones')
    parser.add_argument('--block-users', dest='block_users', action='store_true', help='Block all users except specified ones')

    args=parser.parse_args()

    if (args.url == None or args.token == None):
        parser.print_help()
        exit()

    if args.disable_public_signup:
        disable_public_signup(args.url, args.token)

    except_users = []
    if args.except_users != None:
        except_users = args.except_users.split(',')

    if args.depromote_users or args.block_users:
        users = fetch_users(args.url, args.token)
        for user in users:
            if user['username'] not in except_users:
                if args.depromote_users:
                    depromote_user(args.url, args.token, user['id'])
                if args.block_users:
                    block_user(args.url, args.token, user['id'])

if __name__ == '__main__':
    main()
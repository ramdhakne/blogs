#!/usr/bin/env python3
import argparse
import requests
import json
 
#Common args
parser = argparse.ArgumentParser(description='To backup and Restore Couchbase RBAC Users')
parser.add_argument('--username', metavar='<username>', dest='username', default='Administrator',
                    help='The username for the Couchbase cluster')
parser.add_argument('--password', metavar='<password>', dest='password', default='password',
                    help='The password for the Couchbase cluster')
parser.add_argument('--cluster', metavar='<hostname:port>', dest='host', default='localhost:8091',
                    help='The hostname of the Couchbase cluster')
parser.add_argument('--file', metavar='<file>', dest='rbacFile', default='rbac.json',
                    help='The file to read and write the RBAC data to')
 
#Action backup or restore
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('--backup', action='store_true', default=False)
action.add_argument('--restore', action='store_true', default=False)
 
args = parser.parse_args()
 
#Backing up
print "my host : " + str(args.host)
if args.backup:
    url = 'http://' + args.host + '/settings/rbac/users'
    print "my url : " + str(url)
    response = requests.get(url, auth=(args.username, args.password))
    if response.status_code == 200:
        try:
            with open(args.rbacFile, 'wt') as f:
                f.write(response.text)
                print('Successfully backed up RBAC data to: [%s]' % args.rbacFile)
        except Exception as e:
            print('Error')
    else:
        print('Http requests {url} failed: {response.status_code}')
 
#Restoring
if args.restore:
    try:
        with open(args.rbacFile, 'r') as f:
            rbacData = json.loads(f.read())
            for user in rbacData:
                url = 'http://{args.host}/settings/rbac/users/{user["domain"]}/{user["id"]}'
                params = {}
                if 'name' in user:
                    params['name'] = user['name']
                roles = list()
                for role in user['roles']:
                    if 'bucket_name' in  role:
                        roles.append('{role["role"]}[{role["bucket_name"]}]')
                    else:
                        roles.append(role['role'])
                params['roles'] = ','.join(roles)
 
                output = 'Successfully restored user {user["id"]}'
                if user['domain'] == 'local':
                    params["password"] = 'password'
                    output = output + ' and have reset the password to "password"'
                response = requests.put(url, params, auth=(args.username, args.password))
                if response.status_code == 200:
                    print(output)
                else:
                    print(params)
                    print('Http requests {url} failed: {response.status_code} {response.text}')
 
    except Exception as e:
                print('Error: {e}')

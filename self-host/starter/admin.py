"""Interactive local-only account deactivation. Run inside the Synapse container."""
import getpass, json, urllib.request, urllib.parse
base = 'http://127.0.0.1:8008'
def call(path, body, token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(req,timeout=30) as response: return json.load(response)
username=input('Admin Matrix ID: ').strip()
password=getpass.getpass('Admin password (not echoed): ')
session=call('/_matrix/client/v3/login',{'type':'m.login.password','identifier':{'type':'m.id.user','user':username},'password':password,'initial_device_display_name':'Local account administration'})
del password
token=session['access_token']
try:
    target=input('Full Matrix ID to deactivate: ').strip()
    if not target.startswith('@') or ':' not in target: raise SystemExit('A full Matrix ID is required.')
    if target == session['user_id']: raise SystemExit('Refusing to deactivate this administrative session account.')
    if input('Type the full target Matrix ID again to confirm: ').strip()!=target: raise SystemExit('Cancelled.')
    result=call('/_synapse/admin/v1/deactivate/'+urllib.parse.quote(target,safe=''),{'erase':True},token)
    print('Account deactivation response:',json.dumps(result))
    print('Federated copies are not guaranteed to disappear. Deactivation is not ordinary room removal.')
finally:
    call('/_matrix/client/v3/logout',{},token)

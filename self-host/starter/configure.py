"""Run inside official Synapse image after its generate step. Fresh servers only."""
import os, secrets
from pathlib import Path
import yaml
p = Path('/data/homeserver.yaml')
s = yaml.safe_load(p.read_text())
if s.get('server_name') != os.environ['SERVER_NAME']:
    raise SystemExit('Permanent server name differs; refusing to change identity.')
if Path('/data/homeserver.db').exists():
    raise SystemExit('Existing SQLite database found. Follow the official migration guide; do not replace it.')
s['public_baseurl'] = 'https://' + os.environ['SERVER_NAME'] + '/'
s['database'] = {'name':'psycopg2','args':{'user':'synapse','password':os.environ['POSTGRES_PASSWORD'],'database':'synapse','host':'postgres','port':5432,'cp_min':5,'cp_max':10}}
s['listeners'] = [{'port':8008,'tls':False,'type':'http','x_forwarded':True,'bind_addresses':['0.0.0.0'],'resources':[{'names':['client','federation'],'compress':False}]}]
s['enable_registration'] = False
s['report_stats'] = False
s['registration_shared_secret'] = s.get('registration_shared_secret') or secrets.token_hex(32)
p.write_text(yaml.safe_dump(s, sort_keys=False))
p.chmod(0o600)
os.chown(p, 991, 991)
print('Fresh server configured. Closed registration; PostgreSQL; proxy-aware HTTP. Secrets not printed.')

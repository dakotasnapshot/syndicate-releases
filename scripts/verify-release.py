#!/usr/bin/env python3
"""Read-only verification of immutable public release assets."""
import hashlib
import json
import os
import sys
import urllib.request

REPO = 'dakotasnapshot/syndicate-releases'
tag = sys.argv[1]
headers = {'User-Agent': 'Syndicate-release-verifier', 'Accept': 'application/vnd.github+json'}
if os.environ.get('GH_TOKEN'):
    headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
request = urllib.request.Request(f'https://api.github.com/repos/{REPO}/releases/tags/{tag}', headers=headers)
with urllib.request.urlopen(request, timeout=60) as response:
    release = json.load(response)
assets = {a['name']: a for a in release['assets']}
with urllib.request.urlopen(assets['release-manifest.json']['browser_download_url'], timeout=60) as response:
    manifest = json.load(response)
assert manifest['tag'] == tag and manifest['repository'] == REPO
for entry in manifest['files']:
    asset = assets[entry['name']]
    assert asset['size'] == entry['size']
    expected_digest = 'sha256:' + entry['sha256']
    if asset.get('digest'):
        assert asset['digest'] == expected_digest
    digest = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(asset['browser_download_url'], timeout=120) as response:
        while block := response.read(1024 * 1024):
            size += len(block)
            digest.update(block)
    assert size == entry['size'] and digest.hexdigest() == entry['sha256'], entry['name']
    print('Verified', entry['name'], size, flush=True)
print('PASS', tag, len(manifest['files']), 'public whole-file hashes')

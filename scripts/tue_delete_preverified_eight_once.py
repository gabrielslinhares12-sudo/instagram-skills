#!/usr/bin/env python3
"""One-time cleanup of exactly 8 ZIP artifacts previously checked against Drive.

Evidence: same-size GitHub ZIP and Drive ZIP were both downloaded and their
SHA-256 was identical in the 2026-11-11 owner-authorized audit. Only artifacts
in storage/artifact-drive-verified.json are eligible. This script independently
re-downloads GitHub originals before deletion and checks their exact SHA256.
No new artifacts are eligible through this temporary mechanism.
"""
import json
import os
from pathlib import Path
import tempfile
from urllib import error
from tue_verified_drive_artifact_cleanup import api, choose, stream_hash, API

EXPECTED_IDS={13766758374,13762140586,13761625774,13760476858,
              13767511517,13766234421,13767361897,13767297700}


def main():
    repo=os.environ.get('GITHUB_REPOSITORY')
    if repo!='gabrielslinhares12-sudo/instagram-skills':
        raise RuntimeError('WRONG_REPOSITORY')
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('GITHUB_TOKEN_MISSING')
    data=json.loads(Path('storage/artifact-drive-verified.json').read_text())
    entries=data.get('artifacts',[])
    if {int(x['artifact_id']) for x in entries}!=EXPECTED_IDS or len(entries)!=8:
        raise RuntimeError('HARD_CODED_VERIFIED_ALLOWLIST_MISMATCH')
    deleted=[];absent=[];blocked=[]
    for item in entries:
        aid=int(item['artifact_id'])
        url=API+'/repos/'+repo+'/actions/artifacts/'+str(aid)
        try:
            try:
                _,meta=api(url,token)
            except error.HTTPError as exc:
                if exc.code==404:
                    absent.append(aid)
                    continue
                raise
            choose(item,meta,24)
            if int(meta['size_in_bytes']) != int(item['size_bytes']):
                raise RuntimeError('SIZE_MISMATCH')
            with tempfile.TemporaryDirectory() as tmp:
                bytes_,sha=stream_hash(url+'/zip',{'Accept':'application/vnd.github+json',
                    'Authorization':'Bearer '+token,'X-GitHub-Api-Version':'2022-11-28'},
                    Path(tmp)/'candidate.zip',redirect_without_auth=True)
            if bytes_ != int(item['size_bytes']) or sha != item['sha256']:
                raise RuntimeError('SHA256_NOT_IDENTICAL_TO_PREVIOUSLY_VERIFIED_DRIVE_COPY')
            status,_=api(url,token,method='DELETE')
            if status!=204:
                raise RuntimeError('DELETE_NOT_CONFIRMED')
            print('SAFE_DELETED_ARTIFACT',aid,'SHA256',sha)
            deleted.append(aid)
        except Exception as exc:
            print('PRESERVED_ARTIFACT',aid,str(exc))
            blocked.append((aid,str(exc)))
    summary=os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary,'a') as f:
            f.write('### Exceção única: 8 backups Faker confirmados em 2026-11-11\n')
            f.write('Excluídos: '+str(deleted)+'\nJá ausentes: '+str(absent)+'\n')
            f.write('Bloqueados: '+str(blocked)+'\n')
            f.write('Nenhum outro artefato ou arquivo do Drive é afetado.\n')
    print('SAFE_CLEANUP_COUNT',len(deleted),'BLOCKED_COUNT',len(blocked))
    if blocked:
        raise SystemExit(1)

if __name__=='__main__':
    main()
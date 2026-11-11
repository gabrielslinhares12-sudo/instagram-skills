#!/usr/bin/env python3
"""Fail-closed GitHub Actions artifact cleanup after an identical Drive ZIP is verified.

The OAuth token is never logged. Only exact-name ZIP backups are eligible.
Legacy IDs are explicitly allowlisted in a JSON manifest; future uploads can opt
in with the artifact-name prefix tue-drive-backed- and same-name ZIP on Drive.
Publication ledgers, workflow run histories, and source code are untouched.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib import error, parse, request
import zipfile

PREFIX = 'tue-drive-backed-'
BLOCKED = ('ledger', 'publication-state', 'receipt', 'audit', 'logs', 'report')
API = 'https://api.github.com'
MAX_BYTES = 500_000_000


def api(url: str, token: str, method: str = 'GET', data: bytes | None = None):
    headers = {'Accept': 'application/vnd.github+json',
               'Authorization': 'Bearer ' + token,
               'X-GitHub-Api-Version': '2022-11-28'}
    req = request.Request(url, method=method, data=data, headers=headers)
    with request.urlopen(req, timeout=50) as response:
        return response.status, (json.load(response) if method != 'DELETE' else None)


def drive_token() -> str:
    keys = ('GDRIVE_OAUTH_CLIENT_ID', 'GDRIVE_OAUTH_CLIENT_SECRET', 'GDRIVE_OAUTH_REFRESH_TOKEN')
    values = [os.environ.get(k, '') for k in keys]
    if not all(values):
        raise RuntimeError('DRIVE_OAUTH_MISSING: no deletion permitted')
    data = parse.urlencode(dict(client_id=values[0], client_secret=values[1],
                                refresh_token=values[2], grant_type='refresh_token')).encode()
    req = request.Request('https://oauth2.googleapis.com/token', data=data,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with request.urlopen(req, timeout=40) as response:
        token = json.load(response).get('access_token')
    if not token:
        raise RuntimeError('DRIVE_OAUTH_REFRESH_FAILED: no deletion permitted')
    return token


def drive_find_exact(filename: str, token: str):
    safe = filename.replace('\\', '\\\\').replace("'", "\\'")
    q = "name = '" + safe + "' and trashed = false"
    params = parse.urlencode({'q': q, 'fields': 'nextPageToken,files(id,name,size,mimeType,trashed,capabilities(canDownload))',
                              'pageSize': 100})
    req = request.Request('https://www.googleapis.com/drive/v3/files?' + params,
                          headers={'Authorization': 'Bearer ' + token})
    with request.urlopen(req, timeout=40) as response:
        body = json.load(response)
    files = body.get('files', [])
    if body.get('nextPageToken') or len(files) != 1:
        raise RuntimeError('DRIVE_EXACT_NAME_NOT_UNIQUE_OR_MISSING: ' + filename)
    file = files[0]
    if file.get('trashed') or file.get('capabilities', {}).get('canDownload') is False:
        raise RuntimeError('DRIVE_COPY_NOT_DOWNLOADABLE: ' + filename)
    return file


def stream_hash(url: str, headers: dict, output: Path, *, redirect_without_auth=False):
    """Download with bounded size; never forward GitHub credentials to storage redirects."""
    class BlockRedirect(request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, hdrs, newurl):
            return None
    opener = request.build_opener(BlockRedirect()) if redirect_without_auth else request.build_opener()
    req = request.Request(url, headers=headers)
    try:
        response = opener.open(req, timeout=120)
    except error.HTTPError as e:
        if not redirect_without_auth or e.code not in (301, 302, 303, 307, 308):
            raise
        location = e.headers.get('Location', '')
        parsed = parse.urlsplit(location)
        if parsed.scheme != 'https' or not parsed.hostname:
            raise RuntimeError('UNSAFE_ARTIFACT_REDIRECT')
        # No Authorization header on the redirected storage request.
        response = request.urlopen(request.Request(location), timeout=120)
    digest = hashlib.sha256()
    count = 0
    with response, output.open('wb') as f:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            count += len(block)
            if count > MAX_BYTES:
                raise RuntimeError('COPY_TOO_LARGE')
            digest.update(block)
            f.write(block)
    if not count:
        raise RuntimeError('EMPTY_DOWNLOAD')
    return count, digest.hexdigest()


def choose(entries: list, artifact: dict, min_age_hours: int):
    if artifact.get('expired') or not artifact.get('id'):
        raise RuntimeError('EXPIRED_OR_INVALID_ARTIFACT')
    if artifact.get('name') != entries['artifact_name']:
        raise RuntimeError('ARTIFACT_NAME_MISMATCH')
    created = datetime.fromisoformat(artifact['created_at'].replace('Z', '+00:00'))
    age = (datetime.now(timezone.utc) - created).total_seconds()
    if age < min_age_hours * 3600:
        raise RuntimeError('ARTIFACT_STILL_TOO_RECENT')
    if any(word in artifact['name'].lower() for word in BLOCKED):
        raise RuntimeError('PROTECTED_ARTIFACT_TYPE')


def verified_one(entry, github, drive, repo, execute, min_age_hours):
    artifact_id = int(entry['artifact_id'])
    path = API + '/repos/' + repo + '/actions/artifacts/' + str(artifact_id)
    try:
        _, meta = api(path, github)
    except error.HTTPError as e:
        if e.code == 404:
            return ('ABSENT', artifact_id, '')
        raise
    choose(entry, meta, min_age_hours)
    remote = drive_find_exact(entry['drive_name'], drive)
    if remote.get('mimeType') not in ('application/zip', 'application/x-zip-compressed', 'application/octet-stream'):
        raise RuntimeError('DRIVE_NOT_ZIP')
    expected_size = int(entry.get('size_bytes', 0))
    if int(remote['size']) != int(meta['size_in_bytes']) or (expected_size and expected_size != int(remote['size'])):
        raise RuntimeError('SIZE_MISMATCH')
    with tempfile.TemporaryDirectory(prefix='tue-artifact-check-') as folder:
        original = Path(folder) / 'github.zip'
        backup = Path(folder) / 'drive.zip'
        size_a, sha_a = stream_hash(path + '/zip',
                                    {'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer ' + github,
                                     'X-GitHub-Api-Version': '2022-11-28'},
                                    original, redirect_without_auth=True)
        size_b, sha_b = stream_hash('https://www.googleapis.com/drive/v3/files/' + parse.quote(remote['id']) + '?alt=media',
                                    {'Authorization': 'Bearer ' + drive}, backup, redirect_without_auth=True)
        if size_a != size_b or size_a != int(remote['size']) or sha_a != sha_b:
            raise RuntimeError('DRIVE_GITHUB_SHA256_MISMATCH')
        known = entry.get('sha256')
        if known and sha_a != known:
            raise RuntimeError('EXPECTED_SHA256_MISMATCH')
        if not zipfile.is_zipfile(backup):
            raise RuntimeError('DRIVE_FILE_NOT_VALID_ZIP')
        with zipfile.ZipFile(backup) as z:
            if z.testzip() is not None:
                raise RuntimeError('DRIVE_ZIP_CORRUPT')
    if execute:
        status, _ = api(path, github, method='DELETE')
        if status != 204:
            raise RuntimeError('GITHUB_DELETE_NOT_CONFIRMED')
        return ('DELETED', artifact_id, sha_a)
    return ('VERIFIED_DRY_RUN', artifact_id, sha_a)


def discover_opt_in(github, repo, known_ids, pages=5):
    found = []
    for page in range(1, pages + 1):
        _, payload = api(API + '/repos/' + repo + '/actions/artifacts?' + parse.urlencode({'per_page': 100, 'page': page}), github)
        artifacts = payload.get('artifacts', [])
        for artifact in artifacts:
            name = artifact.get('name', '')
            if artifact.get('id') not in known_ids and name.startswith(PREFIX) and not any(x in name.lower() for x in BLOCKED):
                found.append({'artifact_id': artifact['id'], 'artifact_name': name,
                              'drive_name': name + '.zip', 'size_bytes': artifact['size_in_bytes']})
        if len(artifacts) < 100:
            break
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', default='storage/artifact-drive-verified.json')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--min-age-hours', type=int, default=1)
    args = parser.parse_args()
    repo = os.environ.get('GITHUB_REPOSITORY', '')
    gh = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not repo or not gh:
        raise RuntimeError('GITHUB_CONTEXT_MISSING')
    doc = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    if doc['repository'] != repo:
        raise RuntimeError('MANIFEST_REPO_MISMATCH')
    entries = list(doc['artifacts'])
    entries += discover_opt_in(gh, repo, {int(x['artifact_id']) for x in entries})
    if not entries:
        print('NO_OPTED_IN_ARTIFACTS; nothing deleted')
        return
    drive = drive_token()
    stats = {'DELETED': 0, 'VERIFIED_DRY_RUN': 0, 'ABSENT': 0, 'BLOCKED': 0}
    summary = ['### TUE — limpeza de artefatos com backup no Drive', '',
               'Modo: ' + ('EXECUTE' if args.execute else 'DRY RUN'), '']
    for entry in entries[:100]:
        try:
            outcome, aid, sha = verified_one(entry, gh, drive, repo, args.execute, args.min_age_hours)
            stats[outcome] += 1
            summary.append('- ' + str(aid) + ' — ' + outcome + (' — SHA256 ' + sha if sha else ''))
            print('ARTIFACT', aid, outcome, sha)
        except Exception as exc:
            stats['BLOCKED'] += 1
            print('ARTIFACT', entry['artifact_id'], 'BLOCKED', type(exc).__name__, str(exc))
            summary.append('- ' + str(entry['artifact_id']) + ' — BLOCKED: ' + str(exc))
    summary.append('')
    summary.append('Resumo: ' + json.dumps(stats, ensure_ascii=False))
    print('CLEANUP_STATS=' + json.dumps(stats))
    step = os.environ.get('GITHUB_STEP_SUMMARY')
    if step:
        with open(step, 'a', encoding='utf-8') as f:
            f.write('\n'.join(summary) + '\n')
    if stats['BLOCKED']:
        raise SystemExit('Some artifacts not deleted: checks failed; see summary')


if __name__ == '__main__':
    main()
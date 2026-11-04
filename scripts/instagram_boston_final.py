"""Single reconciled Boston carousel attempt; never publish a child container."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from facebook_poster import FacebookPoster, FacebookConfig
from instagram_queue import GitLedger, QueueError
from meta_poster import MetaError

SLUG = 'tue-2026-11-04-boston-1919-carrossel-imediato'
OLD_CHILD = '18102820949100158'
OLD_MEDIA = '17997771024013719'


def no_duplicate(client, user_id):
    feed = client._request('GET', user_id + '/media', params={
        'fields': 'id,caption,media_type,permalink', 'limit': 100})
    records = feed.get('data')
    if not isinstance(records, list) or feed.get('paging', {}).get('next'):
        raise QueueError('Cannot establish complete account feed; stop.')
    for record in records:
        caption = str(record.get('caption') or '').lower()
        if str(record.get('id')) == OLD_MEDIA or 'boston' in caption or 'melaço' in caption:
            raise QueueError('Existing Boston media detected; stop without writing.')
    return len(records)


def verified_album(item, children, caption):
    return (item.get('media_type') == 'CAROUSEL_ALBUM'
            and item.get('username') == 'temumaexplicacao'
            and item.get('caption') == caption
            and isinstance(item.get('permalink'), str)
            and item['permalink'].startswith('https://www.instagram.com/')
            and len(children.get('data', [])) == 5
            and len({x.get('id') for x in children['data']}) == 5
            and all(x.get('media_type') == 'IMAGE' for x in children['data']))


def run():
    approval = json.loads(Path(f'content/approved/{SLUG}/approval.json').read_text(encoding="utf-8"))
    path = Path('content/publication-state.json')
    state = json.loads(path.read_text(encoding="utf-8"))
    item = state['items'][SLUG]
    assert item['status'] == 'needs_review' and item['creation_id'] == OLD_CHILD
    assert not item.get('final_album_claimed_at'), 'One attempt already consumed'
    assert approval['approved'] and approval['owner_authorized']
    assert approval['kind'] == 'carousel' and approval['page_count'] == 5
    assert approval['owner_authorized_without_music']
    assert len(approval['media_urls']) == len(approval['media_sha256']) == 5
    urls = []
    for url, digest in zip(approval['media_urls'], approval['media_sha256']):
        prefix = 'https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/'
        assert url.startswith(prefix)
        commit, relative = url[len(prefix):].split('/', 1)
        assert commit == approval['release_commit']
        cdn = f'https://cdn.jsdelivr.net/gh/gabrielslinhares12-sudo/instagram-skills@{commit}/{relative}'
        with urlopen(cdn, timeout=45) as response:
            data = response.read(15 * 1024 * 1024)
        assert hashlib.sha256(data).hexdigest() == digest, 'CDN bytes differ from approved image'
        urls.append(cdn)
    client = FacebookPoster(FacebookConfig.from_env())
    identity = client.check_identity()
    user_id = identity['instagram_user_id']
    assert user_id == '17841433004716815' and identity['username'] == 'temumaexplicacao'
    count = no_duplicate(client, user_id)
    persist = GitLedger(path)
    item['final_album_claimed_at'] = datetime.now(timezone.utc).isoformat()
    item['final_album_preflight_count'] = count
    item['final_album_children'] = []
    persist(state, 'claim(instagram): one reconciled Boston five-image album attempt')
    parent = None
    try:
        for url in urls:
            child = client._create_container({'image_url': url, 'is_carousel_item': 'true'})
            item['final_album_children'].append(child)
        assert len(set(item['final_album_children'])) == 5
        parent = client._create_container({'media_type': 'CAROUSEL',
            'children': ','.join(item['final_album_children']), 'caption': approval['caption']})
        assert parent not in item['final_album_children'] and parent != OLD_CHILD
        item['final_album_parent'] = parent
        persist(state, 'record(instagram): exact Boston parent album before publication')
        no_duplicate(client, user_id)
        result = client._request('POST', user_id + '/media_publish', data={'creation_id': parent})
        media_id = result['id']
        item['final_album_media_id'] = media_id
        persist(state, 'receipt(instagram): Boston album media ID pending verification')
        published = client._request('GET', media_id, params={
            'fields': 'id,caption,media_type,permalink,username,timestamp'})
        children = client._request('GET', media_id + '/children', params={'fields': 'id,media_type'})
        assert published['id'] == media_id and verified_album(published, children, approval['caption'])
        item['previous_partial_attempt'] = {k: item.get(k) for k in
            ('creation_id', 'media_id', 'published_at', 'actual_media_type', 'technical_note')}
        item.update(status='published', creation_id=parent, media_id=media_id,
            permalink=published['permalink'], published_at=published['timestamp'],
            actual_media_type='CAROUSEL_ALBUM', carousel_published=True,
            partial_image_published=False, manual_cleanup_required=False,
            verified_child_count=5, recovery_same_creation_id=False)
        item['technical_note'] = 'Five-image parent album verified by official Meta GET; old child was absent from feed.'
        persist(state, 'receipt(instagram): verify Boston carousel with five photos and permalink')
        print(json.dumps({'ok': True, 'media_id': media_id, 'permalink': published['permalink'], 'photos': 5}))
    except Exception as error:
        item['status'] = 'needs_review'
        item['final_album_parent'] = parent
        item['final_album_error_type'] = type(error).__name__
        if isinstance(error, MetaError):
            item['final_album_error'] = {k: getattr(error, k, None) for k in ('code', 'subcode', 'http_status')}
        persist(state, 'quarantine(instagram): retain Boston attempt without automatic retry')
        raise QueueError('Boston album not verified; no automatic retry.') from None


if __name__ == '__main__':
    run()

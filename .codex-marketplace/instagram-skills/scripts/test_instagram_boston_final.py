import unittest
from unittest.mock import Mock
from instagram_boston_final import no_duplicate, verified_album
from instagram_queue import QueueError


class BostonRecoveryTests(unittest.TestCase):
    def test_child_is_never_accepted_as_album(self):
        item = dict(media_type='IMAGE', username='temumaexplicacao', caption='approved',
                    permalink='https://www.instagram.com/p/example/')
        children = {'data': [{'id': str(i), 'media_type': 'IMAGE'} for i in range(5)]}
        self.assertFalse(verified_album(item, children, 'approved'))
        item['media_type'] = 'CAROUSEL_ALBUM'
        self.assertTrue(verified_album(item, children, 'approved'))
        children['data'].pop()
        self.assertFalse(verified_album(item, children, 'approved'))

    def test_duplicate_without_caption_is_blocked(self):
        client = Mock()
        client._request.return_value = {'data': [{'id': '17997771024013719'}]}
        with self.assertRaises(QueueError):
            no_duplicate(client, 'user')

    def test_incomplete_feed_is_blocked(self):
        client = Mock()
        client._request.return_value = {'data': [], 'paging': {'next': 'more'}}
        with self.assertRaises(QueueError):
            no_duplicate(client, 'user')


if __name__ == '__main__':
    unittest.main()

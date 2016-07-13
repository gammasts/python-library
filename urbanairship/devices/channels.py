import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class Channel(object):
    """Perform various operations on a channel object"""

    def __init__(self, airship, channel_id=None, device_type=None):

        self._airship = airship
        self.channel_id = channel_id
        self.device_type = device_type

    def tags(self, group, add=None, remove=None, set=None):
        """Add, remove, or set tags on a channel
        :param add: A list of tags to add
        :param remove: A list of tags to remove
        :param set: A list of tags to set
        :param group: The Tag group for the add, remove, and set operations
        """
        payload = {}
        if self.channel_id is not None:
            audience = {"%s_channel" % self.device_type: self.channel_id}
        else:
            raise ValueError('A channel ID is required for modifying tags')

        if (add, remove, set) == (None, None, None):
            raise ValueError('An add, remove, or set field was not set')

        payload['audience'] = audience

        if add is not None:
            if set is not None:
                raise ValueError('A tag request can only contain an add or '
                                 'remove field, both, or a single set field')
            payload['add'] = {group: add}

        if remove is not None:
            if set is not None:
                raise ValueError('A tag request can only contain an add or '
                                 'remove field, both, or a single set field')
            payload['remove'] = {group: remove}

        if set is not None:
            payload['set'] = {group: set}

        body = json.dumps(payload).encode('utf-8')
        print body
        response = self._airship._request(
            'POST', body, common.CHANNEL_TAGS_URL, 'application/json', version=3
        )

        return response.json()
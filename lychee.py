import json
import os
import re
import time

import feedparser

RC_FILE = os.path.expanduser("~/.torrentrc")
DEFAULT_RC = {
    "poll_interval": 60 * 10,
    "active_dirpath": os.path.expanduser("~/torrents/incomplete"),
    "complete_dirpath": os.path.expanduser("~/torrents/complete")
}
STATE_FILE = os.path.expanduser("~/._torrentleech_state")
DEFAULT_STATE = {
    'active_torrents': [],
}


def init_state_file():
    """Load the state file that tracks current torrents.

    """
    try:
        with open(STATE_FILE, 'r') as sf:
            state = json.loads(sf)
    except IOError:
        return DEFAULT_STATE.copy()

    return state


def write_state_file(state):
    """Write the current state to disk.

    """
    with open(STATE_FILE, 'w') as sf:
        sf.write(json.dumps(state))


def init_rc_file():
    """Load the rc file that tells us what torrents to match.

    """
    new_rc = DEFAULT_RC.copy()
    try:
        with open(RC_FILE, 'r') as sf:
            rc = json.loads(sf.read())
    except IOError:
        return new_rc

    new_rc.update(rc)
    return new_rc


def load_xml_feed(feed_url):
    """Load a given xml url, returns the raw xml as a string.

    """
    with open(os.path.expanduser('~/Desktop/feed.txt'), 'r') as ff:
        return feedparser.parse(ff.read())
    #return feedparser.parse(feed_url)


def attempt_re_match(entry, field, match):
    """Attempt to match an entry against a matcher.

    """
    entry_field = entry[field]
    match_re = re.compile(match, re.IGNORECASE)

    if match_re.match(entry_field):
        print entry_field
        print match
        print bool(match_re.match(entry_field))
        print


def main():
    # Load the state file first
    state = init_state_file()
    rc = init_rc_file()
    #while True:
    feed = load_xml_feed(rc['feed_url'])

    for key, match in rc['matchers'].items():
        if key.endswith('_re'):
            for entry in feed['entries']:
                attempt_re_match(
                    entry = entry,
                    field = key.split('_re')[0],
                    match = match)

        elif key.endswith('_glob'):
            # Glob style matcher
            pass

    # And now we wait
    # time.sleep(rc['poll_interval'])


if __name__ == '__main__':
    main()

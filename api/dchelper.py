from api import *
from api.plugins.log import *
from api.plugins.client import *

class discordhelper:
    def __init__(self):
        pass

    def extract_invite(self, invite):
        match = re.search(r'(?:(?:http:\/\/|https:\/\/)?discord\.gg\/|discordapp\.com\/invite\/|discord\.com\/invite\/)?([a-zA-Z0-9-]+)', invite)
        if match: invite =  match.group(1)
        log.dbg('Extract invite', invite)
        return invite
    
    def delay(self, delay):
        if delay == 0:
            return
        time.sleep(float(delay))

    def get_invite_info(self, invite):
        cl = client()

        r = cl.sess.get(
            f'https://discord.com/api/v9/invites/{invite}?inputValue={invite}',
            headers=cl.headers,
            cookies=cl.cookies
        )

        log.dbg('Get invite info', r.text, r.status_code)

        if r.status_code == 200: 
            return r.json()
        
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            time.sleep(float(limit))
            self.get_invite_info(invite)

        else:
            return {}

    def get_messages(self, channelid, tokens):
        random.shuffle(tokens)
        for token in tokens:
            cl = client(token)
            cl.headers['Authorization'] = token

            r = cl.sess.get(
                f'https://discord.com/api/v9/channels/{channelid}/messages?limit=50',
                headers=cl.headers,
                cookies=cl.cookies
            )

            log.dbg('Get messages', r.text, r.status_code)

            if r.status_code == 200:
                return r.json()

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                time.sleep(float(limit))
                self.get_messages(channelid, tokens)

            else:
                continue

        return {}

    def getsnowflake(self):
        return ((int(time.time() * 1000) - 1420070400000) << 22)
    
    def getemojis(self, length):
        emoji_ranges = [
            (0x1F600, 0x1F64F),
            (0x1F300, 0x1F5FF),
            (0x1F680, 0x1F6FF),
            (0x1F700, 0x1F77F),
            (0x1F900, 0x1F9FF),
        ]

        emojis = [chr(code) for start, end in emoji_ranges for code in range(start, end + 1)]
        return ''.join(random.choices(emojis, k=length))
    
    def getstr(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=length))

    def getlist(self, length, lst):
        random.shuffle(lst)
        length = min(length, len(lst))
        return lst[:length]
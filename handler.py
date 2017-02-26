# -*- coding: utf-8 -*-
import re
import httplib
import json
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def format_fix(text):
    # text = re.sub(r"(@[\w^\.]*)", r"<\1>", text)
    return text


def lambda_handler(event, context):
    logger.info(str(event))
    if 'message' not in event:
        return
    if 'text' not in event['message']:
        return

    try:
        username = event['message']['from']['username']
    except KeyError:
        username = '인라유저'

    text_raw = event['message']['text']
    text = format_fix(text_raw)

    conn = httplib.HTTPSConnection('hooks.slack.com')
    webhook_url = '/services/xxx/xxx/xxx',  # 여기에 Incoming WebHook URL을 넣으세요
    channel_name = '#채널명'  # 여기에 Slack 채널 이름을 넣으세요
    try:
        conn.request(
            'POST',
            webhook_url,
            urllib.urlencode({
                'payload': json.dumps({
                    'channel': channel_name,
                    'text': "`[텔레]` *{}*: {}".format(username, text),
                    'mrkdwn': 'true'
                })
            }),
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        conn.getresponse()
    except:
        conn.request(
            'POST',
            webhook_url,
            urllib.urlencode({
                'payload': json.dumps({
                    'channel': channel_name,
                    'text': "[에러] {}: {}\n----------\n메시지를 전달하는 도중 문제가 발생하였습니다. 메시지가 정상적으로 보이지 않을 수 있습니다.\n\"블블, 여기 에러났어. @blizzardblue\"".format(username, text)
                })
            }),
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        conn.getresponse()
    conn.close()

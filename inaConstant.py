import os.path
import requests
import yaml
import time

WATCHER_CONFIG_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'configs',
    'biliWatcher.yaml')
DLWATCHER_CONFIG_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'configs',
    'biliDLWatcher.yaml')
WRAPPER_CONFIG_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'configs',
    'biliWrapper.json')
TIMESTAMP_ASSIST_DIR = r"D:\tmp\ytd\timstamp.ini"


def initialize_config(
        config_dir: str,
        default: dict = {},
        reset: bool = False) -> dict:
    if not os.path.isfile(config_dir) or reset:
        save_config(config_dir, default)
        return default


def load_config(config_dir: str, default: dict={}, encoding: str='utf-8') -> dict:
    try:
        return yaml.safe_load(open(config_dir, 'r', encoding=encoding))
    except:
        return initialize_config(config_dir, default, reset=True)


def save_config(config_dir: str, default: dict={}) -> None:
    yaml.dump(default, open(config_dir, 'w'),)


class InfoExtractor():
    '''
    copied from ytdlp 
    '''
    def extract_API(
            self,
            *args,
            stop_after: str=None,
            time_wait=0.5) -> list:
        r = []
        for i in range(999):
            k = requests.get(self._API.format(*args, page=str(i + 1)))
            parsed, return_signal = self.parse_json(
                json_obj=k, stop_after=stop_after)
            r += parsed
            if return_signal:
                return r
            time.sleep(time_wait)
        return r

    def parse_json(self, json_obj, **kwargs):
        raise Exception()


class BilibiliChannelSeriesIE(InfoExtractor):
    # https://space.bilibili.com/592726738/channel/seriesdetail?sid=2357741&ctype=0
    _VALID_URL = r'https?://space.bilibili\.com/(?P<userid>\d+)/channel/seriesdetail.+sid=(?P<listid>\d+)'
    _GROUPED_BY = ['userid', 'listid']
    _API = r'https://api.bilibili.com/x/series/archives?mid={}&series_id={}&only_normal=true&sort=desc&pn={page}&ps=30'

    def parse_json(self, json_obj: dict, stop_after: bool = None) -> tuple:
        r = []
        if len(json_obj.json()['data']['archives']) == 0:
            return [], True
        for i in json_obj.json()['data']['archives']:
            if r'https://www.bilibili.com/video/{}'.format(
                    i['bvid']) == stop_after:
                return r, True
            r.append(
                [i['title'], r'https://www.bilibili.com/video/{}'.format(i['bvid'])])
            if stop_after is True:
                return r, True
        return r, False


class BilibiliChannelCollectionsIE(InfoExtractor):
    _VALID_URL = r'https?://space.bilibili\.com/(?P<userid>\d+)/channel/collectiondetail.+sid=(?P<listid>\d+)'
    _GROUPED_BY = ['userid', 'listid']
    _API = r'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={}&season_id={}&sort_reverse=false&page_num={page}&page_size=30'


def url_filter(r: list, or_keywords:list=[]) -> list:
    '''
    keep item in r if item has one of the or keywords
    '''
    r2 = []
    for i in r:
        if not (True in [x in i[0] for x in or_keywords]):
            continue
        r2.append(i[1])
    return r2

def my_url_filter(r: list) -> list:
    return url_filter(r, or_keywords=['歌','唱'])

def moonlight_filter(r: list) -> list:
    return url_filter(r, or_keywords=['猫猫头播放器'])
    
EXTRACTORS = {
    'biliseries': BilibiliChannelSeriesIE,
    'bilicolle': BilibiliChannelCollectionsIE,
}

FILTERS = {
    None: lambda r: [x[1] for x in r],
    'karaoke': my_url_filter,
    'moonlight': moonlight_filter
}

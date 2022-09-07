
import re
import logging
import glob, json, os
from inaseg import ytbdl, strip_medianame_out, shazaming, put_medianame_backin
import subprocess

from inaConstant import WRAPPER_CONFIG_DIR as CONFIG_DIREC

def cell_stdout(cmd: list):
    print('calling', cmd, 'in terminal:')
    with subprocess.Popen(cmd) as p:
        p.wait()
    return p.returncode

def bilibili_upload(
    globbed: list,
    media_basename: str,
    source: str = None,
    description: str = None,
    episode_limit: int = 10,
    line: str = 'kodo'):
    ripped_from = re.findall('\[.+\]', media_basename)[0][1:-1]
    if source is None:
        try:
            source = keystamps[ripped_from][0]
        except KeyError:
            raise KeyError('cant determine source url for this repost')
            source = ' '
    if description is None:
        try:
            description = keystamps[ripped_from][1]
        except:
            description = '关注{}：{}'.format(
                                           ripped_from,
                                           source,)
    try:
        tags = keystamps[ripped_from][2]
    except:
        tags = [ripped_from]
    title = media_basename[:media_basename.rfind('.')][:60]
    # title rework: [歌切][海德薇Hedvika] 20220608
    title = tags[0] + ' ' + os.path.splitext(media_basename)[0][-8:]
    globbed = sorted(globbed)
    globbed_episode_limit = []
    for i in range(len(globbed) // episode_limit + 1):
        globbed_episode_limit.append(globbed[i * episode_limit : (i + 1) * episode_limit])
    
    for i in range(len(globbed_episode_limit)):
        if i > 0: episode_limit_prefix = '_' + chr(97 + i)
        else: episode_limit_prefix = ''
        retry = 0
        cmd = [
                './biliup',
                'upload',
            ]
        for x in globbed_episode_limit[i]: cmd.append(x)
        cmd.append('--copyright=2')
        cmd.append('--desc={}'.format(description))
        cmd.append('--tid=31')
        cmd.append('--tag={}'.format(','.join(tags)))
        cmd.append('--title=[歌切]{}'.format(media_basename[:media_basename.rfind('.')][:60] + episode_limit_prefix))
        cmd.append('--source={}'.format(source))
        cmd.append('-l=' + line)
        logging.info(cmd)
        while cell_stdout(cmd) != 0:
            retry += 1
            if retry > 3: raise Exception('biliup failed for a total of {} times'.format(str(retry)))
#=================================================================================================================    
#AIO 一键url to b站上传
#=================================================================================================================

keystamps = json.load(open(CONFIG_DIREC, encoding='utf-8'))

class Biliup():

    def __init__(
        self,
        media: str,
        outdir: str = '/tf/out',
        episode_limit: int = 180,
        shazam_thread: int = 4,
        ignore_errors: bool = True,
        sound_only: bool = False,
        route: str = 'kodo',
        cleanup: bool = True,
        no_biliup: bool = False,
        ):
        self.cleanup = True #False
        self.outdir = outdir
        self.media = media
        self.episode_limit = episode_limit
        self.shazam_thread = shazam_thread
        self.ignore_errors = ignore_errors
        self.sound_only = sound_only
        self.route = route
        self.cleanup = cleanup
        self.no_biliup = no_biliup

    def run(self):
        try:
            media = self.media
            outdir = self.outdir
            if media == '': return
            os.chdir(outdir)
            if 'https:' in media: media = ytbdl(media, soundonly='', aria=16)#, outdir = outdir
            if not cell_stdout([
                'python',
                'inaseg.py',
                '--media={}'.format(media),
                '--outdir={}'.format(outdir),
                '--soundonly',
                '']) == 0:
                raise BaseException()
            # inaseg failed?
            print('inaseg completed on', media)
            # shazam 4 thread seems to be fine not triggering a ban
            shazaming(outdir, media, threads = self.shazam_thread)
            stripped_media_names = strip_medianame_out(outdir, media)
            print('preparing to upload', stripped_media_names)
            bilibili_upload(stripped_media_names, os.path.basename(media), source=None, episode_limit=self.episode_limit)
            print('finished stripping and uploading', media)
            if self.cleanup:
                os.remove(media)
                for i in stripped_media_names: os.remove(i)
            else: put_medianame_backin(stripped_media_names, media, shazamed=r'D:\tmp\ytd\convert2music', nonshazamed=r'D:\tmp\ytd\extract')
        except KeyboardInterrupt:
            raise
        except BaseException:
            if self.ignore_errors:
                for i in glob.glob('*.mp4') + glob.glob('*.aria2') + glob.glob('*.part'): os.remove(i)
            else:
                raise

outdir = '/tf/out' #os.getcwd()#r'D:\tmp\ytd\hedvika'
import os
import argparse
from datetime import datetime
parser = argparse.ArgumentParser(description='ina music segment')
parser.add_argument('--media', type=str, nargs='+', help='file path or weblink')
if __name__ == '__main__':
    logging.basicConfig(filename='inaseg.log', level=logging.DEBUG)
    args = parser.parse_args()
    for media in args.media:
        logging.info(f'inaseging {media} at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        Biliup(media=media).run()


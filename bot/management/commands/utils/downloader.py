# install

# pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
# pip install wget
# pip install requests

import re
from pprint import pprint
from time import time

import requests
import wget
import youtube_dl
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from bot.management.commands.loader import lang
from bot.models import Videos


class Downloader:

    @staticmethod
    def is_url(url):
        if Downloader.is_valid_youtube_url(url) or Downloader.is_valid_tiktok_url(
                url) or Downloader.is_valid_instagram_url(url) or Downloader.is_valid_facebook_url(url):
            return True
        else:
            return False

    @staticmethod
    def exists_video(url):
        check = Videos.objects.filter(url=url)
        if check.exists():
            return {
                "status": True,
                "file_id": check.first().file_id
            }
        return {
            "status": False
        }

    @staticmethod
    def check_url(url):
        if Downloader.is_valid_youtube_url(url):
            return "youtube"
        elif Downloader.is_valid_tiktok_url(url):
            return "tiktok"
        elif Downloader.is_valid_facebook_url(url):
            return "facebook"
        elif Downloader.is_valid_instagram_url(url):
            return "instagram"
        else:
            return None

    @staticmethod
    def is_valid_tiktok_url(url):
        tiktok_regex = r'^https?://(?:www\.)?tiktok\.com/.*'
        video_regex = r'^https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_-]+/video/\d+.*'

        if re.match(tiktok_regex, url) or re.match(video_regex, url):
            return True
        return False

    @staticmethod
    def is_valid_instagram_url(url):
        instagram_regex = r'^https?://(?:www\.)?instagram\.com/.*'
        video_regex = r'^https?://(?:www\.)?instagram\.com/p/[\w-]+/.*'

        if re.match(instagram_regex, url) or re.match(video_regex, url):
            return True
        return False

    @staticmethod
    def is_valid_youtube_url(url):
        youtube_regex = r'^https?://(?:www\.)?youtube\.com/.*'
        short_link_regex = r'^https?://(?:www\.)?youtu\.be/[\w-]+.*'

        if re.match(youtube_regex, url) or re.match(short_link_regex, url):
            return True
        return False

    @staticmethod
    def is_valid_facebook_url(url):
        youtube_regex = r'^https?://(?:www\.)?fb\.watch/.*'
        short_link_regex = r'^https?://(?:www\.)?facebook\.com/[\w-]+.*'

        if re.match(youtube_regex, url) or re.match(short_link_regex, url):
            return True
        return False

    @staticmethod
    def instagram(url):
        try:

            if not Downloader.is_valid_instagram_url(url):
                return {
                    "success": False,
                    "error": "invalid.url"
                }

            reel_id = url.split("/reel/")[1].split("/")[0].split("?")[0]
            res = requests.get(f"https://www.instagram.com/p/{reel_id}/embed/captioned/")
            content = res.content.decode("utf-8")
            soup = BeautifulSoup(content, features="html.parser")
            script = soup.find_all("script")[8].string
            url = str(script).split(",\\\"video_url\\\":\\\"")[1].split("\\\",\\\"video_view_count\\\":")[
                0].replace("\\", "")

            try:
                validate = URLValidator()
                validate(url)
            except ValidationError as e:
                return {
                    "success": False,
                    "error": "server.error"
                }

            return {
                "success": True,
                "url": url
            }
        except Exception as e:
            return {
                "error": e,
                "success": False,
            }

    @staticmethod
    def test():
        for i in range(200):
            res = Downloader.instagram("https://www.instagram.com/reel/Cur7ZXYrdKb/?igshid=MzRlODBiNWFlZA==")
            if res['success'] != True:
                print(res)
                print("tugadi")
                break
            else:
                print(i)

    @staticmethod
    def tiktok(url):
        try:

            if not Downloader.is_valid_tiktok_url(url):
                return {
                    "success": False,
                    "error": "invalid.url"
                }

            api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

            querystring = {"url": url,
                           "sender_device": "pc", "web_id": "7256363178882762282", "hd": "1"}

            payload = ""
            headers = {"x-rapidapi-key": "0b8388b775msh40849861308be70p17c033jsn3e085adc8ef1"}

            response = requests.request("GET", api_url, data=payload, headers=headers, params=querystring).json()

            if "msg" in response and response['msg'] == "Url parsing is failed! Please check url.":
                return {
                    "success": False,
                    "error": "video.not.found"
                }

            data = response['data']

            return {
                "title": data['title'],
                "size": data['size'],
                "play_count": data['play_count'],
                "url": data['play'],
                "share_count": data['share_count'],
                "success": True
            }

        except Exception as e:
            return {
                "error": e,
                "success": False
            }

    @staticmethod
    def youtube(url):
        try:
            return {'success': True, 'filepath': 'media/temp/1691518394.7586439.mp4'}
            if not Downloader.is_valid_youtube_url(url):
                return {
                    "success": False,
                    "error": "invalid.url"
                }

            filepath = "media/temp/{}.mp4".format(time())

            with youtube_dl.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info['formats']

            current_format = {"filesize": 0}
            for video_format in formats:
                try:
                    if video_format['format_note'] != "tiny" and int(video_format['filesize']) > int(
                            current_format['filesize']) and int(video_format[
                                                                    'filesize']) < (
                            1024 * 1024) * 40:
                        current_format = video_format
                except Exception as e:
                    pass
            if current_format['filesize'] == 0:
                return {
                    "success": False,
                    "message": lang.get("big.file")
                }

            wget.download(url=current_format['url'], out=filepath)

            return {
                "success": True,
                "filepath": filepath
            }
        except Exception as e:
            print(e)
            return {
                "error": e,
                "message": lang.get("download.error"),
                "success": False
            }

    @staticmethod
    def youtube_info(url):
        try:

            if not Downloader.is_valid_youtube_url(url):
                return {
                    "success": False,
                    "error": "invalid.url"
                }

            with youtube_dl.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "success": True,
                    "data": info
                }
        except Exception as e:
            return {
                "error": e,
                "success": False
            }

    @staticmethod
    def facebook(url):
        try:

            if not Downloader.is_valid_facebook_url(url):
                return {
                    "success": False,
                    "error": "invalid.url"
                }

            filepath = "media/temp/{}.mp4".format(time())

            options = dict(outtmpl=filepath)

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
            return {
                "success": True,
                "filepath": filepath
            }
        except Exception as e:
            return {
                "error": e,
                "success": False
            }

# print(Downloader.facebook(input("url: ")))
# print(Downloader.instagram(input("url: ")))
# print(Downloader.tiktok(input("url: ")))
# print(Downloader.youtube(input("url: ")))

from datetime import datetime
from enum import Enum
import json
from typing import *
import csv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .playlist import Playlist, Playlists

from common.api import YoutubeApi
from common.config import (
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION, 
    YOUTUBE_DEVELOPER_KEY
)
from common.types import (
    ParserConfig, 
    VideoItem
)
from common.utils import parse_isoduration


class YoutubeDetailsParser:
    youtube_api= YoutubeApi()
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_DEVELOPER_KEY)
    playlists: Dict[str, Playlist] = dict()
    config: dict[str, Any] = {
		'renew_days': 10,
		'json_path': "./datas/playlists.json",
		'result_path': "./results/result-#.csv",
        'max_results' : 5,
		'time_format': "%m/%d/%Y, %H:%M:%S"
	}
    
    
    def __init__(self):
        self.__get_prev_result()
        
        
    def __get_prev_result(self):
        with open(self.config[ParserConfig.json_path.value]) as f:
            obj = json.load(f)
            for p in obj['playlists']:
                self.playlists[p['id']] = p['playlist']


    def get_config(self):
        return self.config


    def set_config(self, key:str, value: Any):
        def is_config() -> bool:
            try:
                return isinstance(ParserConfig(key), ParserConfig)
            except:
                return False

        if is_config():
            self.config[key] = value
                
                
    def parse(self, pid: str):
        pl = self.playlists[pid] if self.__no_need_to_request(pid) else self.__get_playlist_by_pid(pid)
        self.out(pl)
        
        
    def __no_need_to_request(self, pid:str) -> bool:
        if pid in self.playlists:
            last_updated = self.playlists[pid]["last_updated"]
            delta = datetime.now() - datetime.strptime(last_updated, self.config[ParserConfig.time_format.value])
            if delta.days < self.config[ParserConfig.renew_days.value]:
                return True
        return False


    def out(self, playlist:Playlist):
        # header도 밖이나 위로 빼기
        header = ["idx", "title", "url", "duration"]
        data = [header]
        for vid in playlist.video_dict:
            video = playlist.video_dict[vid]
            temp = [getattr(video, key) for key in header]
            data.append(temp)
        result_path = self.config[ParserConfig.result_path.value].replace("#", playlist.playlist_id)
        with open(result_path, 'w', newline='') as cf:
            writer = csv.writer(cf)
            writer.writerows(data)
            pass

    def __get_playlist_by_pid(self, pid:str) -> Playlist:
        videos = self.youtube_api.get_playlist_items(pid=pid)
        pl = Playlist(pid,
                    last_updated=datetime.now().strftime(self.config[ParserConfig.time_format.value]),
                    videos=videos)
        videos_info = self.youtube_api.get_videos_items(pl.get_video_ids())
        videoId_duration_dict = self.__build_videoId_duration_dict(videos_info)
        pl.set_videos_duration(videoId_duration_dict)
        
        self.__append_playlists(pl)
        return pl
    
    def __build_videoId_duration_dict(self, infos: List[VideoItem]) -> Dict[str, int]:
        res = {}
        for info in infos:
            res[info.id] = parse_isoduration(info.contentDetail.duration)
        return res
    
    
    def __append_playlists(self, pl:Playlist):
        self.playlists[pl.playlist_id] = pl
        self.__update_playlist_json()
    
        
    def __update_playlist_json(self):
        pl_list = list(self.playlists.values())
        pls = Playlists(playlists=pl_list)
        json_result = json.dumps(pls, default=lambda o:o.__dict__, indent=4)
        with open(self.config[ParserConfig.json_path.value], "w") as f:
            f.write(json_result)    
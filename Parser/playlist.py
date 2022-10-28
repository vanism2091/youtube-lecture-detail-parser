from __future__ import annotations
from typing import *
from .video import Video
from common.types import (
    PlaylistItem, 
    VideoItem, 
    ReprToDict
)

class Playlists(ReprToDict):
    def __init__(self, playlists: List[Playlist]):
        self.count = len(playlists)
        self.playlists = playlists


class Playlist:
    playlist_id: str
    channel_id: str
    channel_title: str
    video_ids: List[str] = list()
    video_dict: Dict[str, Video] = dict()
    last_updated: str
    
    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


    def __init__(self, pid: str, last_updated:str, videos:List[PlaylistItem]):
        self.playlist_id = pid
        self.last_updated = last_updated
        first_snippet = videos[0].snippet
        self.channel_id = first_snippet.channelId
        self.channel_title = first_snippet.videoOwnerChannelTitle
        for video in videos:
            curVideo = Video(
                v_id=video.snippet.resourceId.videoId, 
                p_id=pid, 
                idx=video.snippet.position, 
                title=video.snippet.title, 
                description=video.snippet.description, 
                thumb_url=video.snippet.thumbnails.standard.url, 
                privacy_status=video.status.privacyStatus
            )
            self.video_ids.append(curVideo.video_id)
            self.video_dict[curVideo.video_id] = curVideo

    def get_video_ids(self) -> list[str]:
        return self.video_ids

    def set_videos_duration(self, videoId_duration_dict: Dict[str, int]):
        for v_id in videoId_duration_dict:
            if v_id in self.video_dict:
                self.video_dict[v_id].set_duration(videoId_duration_dict[v_id])
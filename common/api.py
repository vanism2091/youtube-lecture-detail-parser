from __future__ import annotations
from typing import *
from common.types import (
    PlaylistItemsListRequestParams, 
    PlaylistRequestPart, 
    PlaylistItemsListResponse, 
    VideosRequestPart, 
    VideosListResponse
)
from common.config import (
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION, 
    YOUTUBE_DEVELOPER_KEY
)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# TODO: api Error 처리 여기에서..

class YoutubeApi:
    last_playlist_response:PlaylistItemsListResponse
    
    def __init__(self):
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_DEVELOPER_KEY)

    def get_playlist_items(self, pid: str, max_results: int=5) -> PlaylistResponse:
        params = self.__get_playlistItems_params(pid, max_results)
        return self.__get_playlistItemsList_response(params).items
    
    def __get_playlistItems_params(self, pid: str, max_results: int) -> PlaylistItemsListRequestParams:
    # def __get_playlistItems_params( pid: str, max_results: int) -> PlaylistItemsListRequestParams:
        return PlaylistItemsListRequestParams(**{
            'part': [PlaylistRequestPart.snippet.value, PlaylistRequestPart.status.value],
            'playlistId': pid,
            'maxResults':max_results
        })

    def __get_playlistItemsList_response(self, params: PlaylistItemsListRequestParams) -> PlaylistItemsListResponse:
        res = self.youtube.playlistItems().list(
            part=",".join(params.part),
            playlistId=params.playlistId,
            maxResults=params.maxResults 
        ).execute()
        self.last_playlist_response = PlaylistItemsListResponse(**res)
        return self.last_playlist_response
    
    def get_videos_items(self, video_ids:List[str]):
        res = self.__get_videosList_response(video_ids)
        return res.items
    
    def __get_videosList_response(self, video_ids:List[str]):
        res = self.youtube.videos().list(
            part=VideosRequestPart.contentDetails.value,
            id=','.join(video_ids)
        ).execute()
        # self.last_video_response
        return VideosListResponse(**res)
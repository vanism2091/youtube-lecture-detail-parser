from __future__ import annotations
import string
from typing import *
from enum import Enum
import json


class ReprToDict:
    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)


## YOUTUBE DETAIL PARSER

class ParserConfig(Enum):
	renew_days = 'renew_days'
	json_path = 'json_path'
	result_path = 'result_path'
	max_results = 'max_results'
	time_format = 'time_format'



######### Request / Response

class PlaylistRequestPart(Enum):
    id = "id"
    snippet = "snippet"
    contentDetails = "contentDetails"
    status = "status"

class VideosRequestPart(Enum):
    id = "id"
    snippet =  "snippet"
    contentDetails =  "contentDetails"
    liveStreamingDetails =  "liveStreamingDetails"
    player =  "player"
    recordingDetails =  "recordingDetails"
    statistics =  "statistics"
    status =  "status"
    topicDetails =  "topicDetails"

## ---------- PlaylistItems

class PlaylistItemsListRequestParams(ReprToDict):
    part: List[str]
    # pageToken: str
    maxResults: str
    playlistId: str
    
    def __init__(self, part: List[str], playlistId:str, maxResults: int, **kwargs):
        self.part = part
        self.playlistId = playlistId
        self.maxResults = maxResults
        # self.pageToken = kwargs["pageToken"]

        
class PlaylistItemsListResponse(ReprToDict):
    def __init__(self, items:List[dict], **kwargs):
        self.items = [PlaylistItem(**item) for item in items]
        
class PlaylistItem(ReprToDict):
    def __init__(self, snippet: dict, status:dict, **kwargs):
        self.snippet = PlaylistItemsSnippetInfo(**snippet)
        self.status = PlaylistItemsStatusInfo(**status)

class PlaylistItemsSnippetInfo(ReprToDict):
    def __init__(self, channelId:str, description:str, videoOwnerChannelTitle:str, title:str, resourceId:dict, thumbnails:dict, position: int, **kwargs):
        self.channelId = channelId
        self.videoOwnerChannelTitle = videoOwnerChannelTitle
        self.title = title
        self.resourceId = PlaylistItemsResourcesIdInfo(**resourceId)
        self.position = position
        self.description = description
        self.thumbnails = PlaylistItemsThumbnailInfo(**thumbnails)

class PlaylistItemsResourcesIdInfo(ReprToDict):
    def __init__(self, videoId:str, **kwargs):
        self.videoId = videoId
        
class PlaylistItemsThumbnailInfo(ReprToDict):
    def __init__(self, standard, **kwargs):
        self.standard = ThumbnailDetail(**standard)
        
class ThumbnailDetail(ReprToDict):
    def __init__(self, url, **kwargs):
        self.url = url 
    
class PlaylistItemsStatusInfo(ReprToDict):
    def __init__(self, privacyStatus):
        self.privacyStatus = privacyStatus 

        
#### VideosList

class VideosListResponse(ReprToDict):
    def __init__(self, items:List[dict], **kwargs):
        self.items = [VideoItem(**item) for item in items]
    
class VideoItem(ReprToDict):
    def __init__(self, id:str, contentDetails:dict, **kwargs):
        self.id = id
        self.contentDetail = VideoItemContentDetailsInfo(**contentDetails)

class VideoItemContentDetailsInfo(ReprToDict):
    def __init__(self, duration:str, **kwargs):
        self.duration = duration
        pass

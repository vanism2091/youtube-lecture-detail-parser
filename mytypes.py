import string
from typing import TypedDict
from enum import Enum

## YOUTUBE

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

class PlaylistRequest(TypedDict):
    part: list[str]
    onBehalfOfContentOwner: str
    pageToken: str
    playlistId: str
    videoId: str
    maxResults: str
    id: str

class PlaylistItemThumbnail(TypedDict):
    url: str

class PlaylistItemResourceId(TypedDict):
    videoId: str
#     pass

class PlaylistItemSnippet(TypedDict):
    channelId: str
    title: str
    description: str
    thumbnails: dict[str, PlaylistItemThumbnail] # standard
    position: int
    resourceId: PlaylistItemResourceId
    videoOwnerChannelTitle: str

    pass

class PlaylistItemStatus(TypedDict):
    privacyStatus: str
    pass
class PlaylistItemResponse(TypedDict):
    snippet: dict

class PlaylistResponse(TypedDict):
    items: list[PlaylistItemResponse]
    status: PlaylistItemStatus


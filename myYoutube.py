from array import array
from datetime import datetime
from enum import Enum
import json
from typing import Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, YOUTUBE_DEVELOPER_KEY
from mytypes import PlaylistRequest, PlaylistResponse, PlaylistRequestPart, PlaylistItemResponse, VideosRequestPart
from myutils import parse_isoduration
import csv

class Video():
	video_id: str
	duration: int
	playlist_id: str
	idx: str
	title: str
	description: str
	thumb_url: str
	privacy_status: str
	url: str

	def __init__(self, v_id, p_id, idx, title, description, thumb_url, privacy_status):
		self.video_id = v_id
		self.playlist_id = p_id
		self.idx = idx
		self.title = title
		self.description = description
		self.thumb_url = thumb_url
		self.privacy_status = privacy_status
		self.url = f'https://www.youtube.com/watch?v={v_id}&list={p_id}'
		pass

	def set_duration(self, duration: int):
		self.duration = duration

class Playlist():
	playlist_id: str
	channel_id: str
	channel_title: str
	video_ids: list[str] = list()
	video_dict: dict[str, Video] = dict()
	last_updated: str

	def __init__(self, id: str,  time_format:str):
		self.playlist_id = id
		self.last_updated = datetime.now().strftime(time_format)

	def get_video_ids(self) -> list[str]:
		return self.video_ids
		
class ParserConfig(Enum):
	renew_days = 'renew_days'
	json_path = 'json_path'
	result_path = 'result_path'
	time_format = 'time_format'

class YoutubeDetailsParser:
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_DEVELOPER_KEY)
	playlists: dict[str, Playlist] = dict()
	config: dict[str, Any] = {
		'renew_days': 10,
		'json_path': "playlists.json",
		'result_path': "result.csv",
		'time_format': "%m/%d/%Y, %H:%M:%S"
	}

	def __init__(self):
		self.get_prev_result()

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
		
	def get_prev_result(self):
		with open(self.config[ParserConfig.json_path.value]) as f:
			obj = json.load(f)
			for p in obj['playlists']:
				self.playlists[p['id']] = p['playlist']
	
	def parse(self, pid: str):
		# pid가 이미 있는지 확인한다
		def needToRequest(pid:str) -> bool:
			if pid in self.playlists:
				last_updated = self.playlists[pid].last_updated
				delta = datetime.now() - datetime.strptime(last_updated, self.config[ParserConfig.time_format.value])
				if delta.days > self.config[ParserConfig.renew_days.value]:
					return True
			return False

		pl = self.playlists[pid] if needToRequest(pid) else self.get_playlist_by_pid(pid)
		self.out(pl)

		

	def out(self, playlist:Playlist):
		header = ["idx", "title", "description", "url", "duration"]
		data = [header]
		for vid in playlist.video_dict:
			video = playlist.video_dict[vid]
			temp = [getattr(video, key) for key in header]
			data.append(temp)
		with open(self.config[ParserConfig.result_path.value], 'w', newline='') as cf:
			writer = csv.writer(cf)
			writer.writerows(data)
			pass

	def get_playlist_by_pid(self, pid:str) -> Playlist:
		def get_playlistItems_params(pid: str) -> PlaylistRequest:
			return PlaylistRequest({
				'part': [PlaylistRequestPart.snippet.value, PlaylistRequestPart.status.value],
				'playlistId': pid,
				'maxResults':50
			})
		
		def get_playlistItems_response(params: PlaylistRequest) -> PlaylistResponse:
			return self.youtube.playlistItems().list(
				part=",".join(params['part']),
				playlistId=params['playlistId'],
				maxResults=params['maxResults'] 
			).execute()

		def make_playlists(pid:str, res:PlaylistResponse) -> Playlist:
			pl = Playlist(pid, time_format=self.config[ParserConfig.time_format.value])
			videos = res['items']
			first_video = PlaylistItemResponse(videos[0])
			pl.channel_id = first_video['snippet']['channelId']
			pl.channel_title = first_video['snippet']['videoOwnerChannelTitle']
			for video in videos:
				v_id = video['snippet']['resourceId']['videoId']
				currVideo = Video(
					v_id=v_id,
					p_id=pid,
					idx=video['snippet']['position'],
					title = video['snippet']['title'],
					description = video['snippet']['description'],
					thumb_url = video['snippet']['thumbnails']['standard']['url'],
					privacy_status = video['status']['privacyStatus']
				)
				pl.video_ids.append(v_id)
				pl.video_dict[v_id] = currVideo
			return pl

		def set_video_durations(playlist:Playlist):
			res = self.youtube.videos().list(
				# part=",".join([VideosRequestPart.contentDetails.value]),
				part=VideosRequestPart.contentDetails.value,
				id=','.join(playlist.video_ids)
			).execute()
			videos = res['items']
			for video in videos:
				v_id = video['id']
				v_duration = parse_isoduration(video['contentDetails']['duration'])
				if v_id in playlist.video_dict:
					playlist.video_dict[v_id].set_duration(v_duration)	
		
		def save_json():
			def make_pl_list() -> list[dict[str, Any]]:
				res = []
				for pid in self.playlists:
					temp = {}
					temp['id'] = pid
					temp['playlist'] = self.playlists[pid]
					res.append(temp)
				return res

			pls = make_pl_list()
			obj= {
				'count': len(self.playlists),
				'playlists': pls 
			}

			json_result = json.dumps(obj, default=vars)
			with open(self.config[ParserConfig.json_path.value], "w") as f:
				f.write(json_result)

		params = get_playlistItems_params(pid)
		response = get_playlistItems_response(params=params)
		pl = make_playlists(pid=pid, res=response)
		set_video_durations(pl)
		self.playlists[pid] = pl
		save_json()

		return pl
					


			
			
		

	
    
	

	


      
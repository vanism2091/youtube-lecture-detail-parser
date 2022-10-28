from typing import *
from common.types import ReprToDict

class Video(ReprToDict):
	def __init__(self, v_id:str, p_id:str, idx:str, title:str, description:str, thumb_url:str, privacy_status:str):
		self.video_id = v_id
		self.playlist_id = p_id
		self.idx = idx
		self.title = title
		self.description = description
		self.thumb_url = thumb_url
		self.privacy_status = privacy_status
		self.url = f'https://www.youtube.com/watch?v={v_id}&list={p_id}'

	def set_duration(self, duration: int):
		self.duration = duration
from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id):
        try:
            video_response = super().get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video_id
                                                                 ).execute()

            self.id = video_id
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f"https://youtu.be/{video_response['items'][0]['id']}"
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        if video_id in video_ids:
            super().__init__(video_id)
            self.playlist_id = playlist_id
        else:
            raise ValueError(f"Видео {video_id} нету в плейлисте {playlist_id}")

    def __str__(self):
        return self.title

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RhythmDataSerializer
from django.views.decorators.csrf import csrf_exempt

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def find_home(request):
    return render(request, '../templates/find/find_home.html')


DEVELOPER_KEY = 'AIzaSyBNfNwPVBhWZL9a6Yc27uw9LZRCQUVzPuM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_songs_with_rhythm(rhythm):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    try:
        search_response = youtube.search().list(
            q=rhythm,
            part='id',
            maxResults=10,
            type='video'
        ).execute()

        video_ids = []
        for search_result in search_response.get('items', []):
            video_ids.append(search_result['id']['videoId'])

        if video_ids:
            video_links = [f'https://www.youtube.com/watch?v={video_id}' for video_id in video_ids]
            return video_links
        else:
            return "По вашему запросу не найдено ни одной песни на YouTube."

    except HttpError as e:
        return f"An HTTP error {e.resp.status} occurred: {e.content}"


def detect_beat(rhythm_data):
    # Преобразует временные отметки ударов в BMP (удары в минуту)
    if len(rhythm_data) < 2:
        return []

    # Преобразовать временные отметки в интервалы между ударами
    intervals = []
    for i in range(1, len(rhythm_data)):
        intervals.append(rhythm_data[i] - rhythm_data[i - 1])

    # Преобразовать интервалы в BMP
    bmp_values = [60000 / interval for interval in intervals]

    return bmp_values


@csrf_exempt
@api_view(['POST'])
def rhythm_view(request):
    serializer = RhythmDataSerializer(data=request.data)
    if serializer.is_valid():
        rhythm_data = serializer.validated_data['rhythm_data']
        rhythm = detect_beat(rhythm_data)
        rhythm_string = ' '.join(map(str, rhythm))  # convert the rhythm to a string
        results = search_songs_with_rhythm(rhythm_string)
        return Response(results, status=200)
    else:
        return Response(serializer.errors, status=400)

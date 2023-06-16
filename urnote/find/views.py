from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RhythmDataSerializer
from django.views.decorators.csrf import csrf_exempt

from . import models


def find_home(request):
    return render(request, 'find/find_home.html')


def search_songs_with_rhythm(bpm):
    song_list = models.Song.objects.all()
    similarities_list = []
    result = []

    for song in song_list:
        if song.bpm-5 <= bpm <= song.bpm+5:
            similarities_list.append(song)

    for res in similarities_list:
        result.append({
            'title': res.title,
            'artist': res.artist,
            'youtube_link': res.youtube_link,
            'bpm': res.bpm,
        })

    if len(result)==0:
        return -1
    return result


def detect_beat(rhythm_data):
    # Преобразует временные отметки ударов в BPM
    amount_beats = len(rhythm_data)

    if amount_beats < 2:
        return []

    # Преобразовать временные отметки в интервалы между ударами
    intervals = []
    for i in range(1, amount_beats):
        intervals.append(rhythm_data[i] - rhythm_data[i - 1])

    # Преобразовать интервалы в BPM
    bpm_values = [60000 / interval for interval in intervals]

    average_bpm = sum(bpm_values) // (amount_beats - 1)

    print('amount_beats: ', amount_beats)
    print('BPM Values: ', bpm_values)
    print('BPM: ', average_bpm)

    return average_bpm


@csrf_exempt
@api_view(['POST'])
def rhythm_view(request):
    serializer = RhythmDataSerializer(data=request.data)
    if serializer.is_valid():
        rhythm_data = serializer.validated_data['rhythm_data']
        rhythm = detect_beat(rhythm_data)
        # rhythm_string = ' '.join(map(str, rhythm))  # convert the rhythm to a string
        results = search_songs_with_rhythm(rhythm)
        return Response(results, status=200)
    else:
        return Response(serializer.errors, status=400)

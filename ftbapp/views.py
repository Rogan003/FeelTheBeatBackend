from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework import status

from ftbapp.bars import bar_analyzer
from ftbapp.colors.generatecolors import get_colors
from ftbapp.shared import utils
from ftbapp.vibrations import vibration_analyzer

class UploadSongView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = default_storage.save(f'audio/{audio_file.name}', audio_file)

        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path.replace('audio/', 'audio/'))

        return Response({
            "file_path": file_path,
            "file_url": file_url
            }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def bars(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    # Open the file
    with default_storage.open(file_path, 'rb') as f:
        y, sr = utils.audio_file_to_y_sr(f)

    # Example logic
    result = bar_analyzer.convert_song_to_bars(y, sr)
    return Response({"result": result})

@api_view(['GET'])
def vibrations(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    with default_storage.open(file_path, 'rb') as f:
        y, sr = utils.audio_file_to_y_sr(f)

    result = vibration_analyzer.sound_to_vibration(y, sr)

    return Response({"result": result})

@api_view(['GET'])
def colors(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    result = get_colors(file_path)
    return Response({"result": result})
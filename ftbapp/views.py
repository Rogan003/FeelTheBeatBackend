from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework import status

class UploadSongView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = default_storage.save(f'audio/{audio_file.name}', audio_file)
        return Response({"file_path": file_path}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def bars(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    # Open the file
    with default_storage.open(file_path, 'rb') as f:
        audio_data = f.read()
        # process audio_data here...

    # Example logic
    result = ["sound1", "sound2", "sound3"]
    return Response({"result": result})

@api_view(['GET'])
def vibrations(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    # Open the file
    with default_storage.open(file_path, 'rb') as f:
        audio_data = f.read()
        # process audio_data here...

    # Example logic
    result = [1, 2, 3]
    return Response({"result": result})

@api_view(['GET'])
def colors(request, file_path):
    if not file_path or not default_storage.exists(file_path):
        return Response({"error": "Invalid or missing file path"}, status=400)

    # Open the file
    with default_storage.open(file_path, 'rb') as f:
        audio_data = f.read()
        # process audio_data here...

    # Example logic
    result = ["A", "B", "C"]
    return Response({"result": result})
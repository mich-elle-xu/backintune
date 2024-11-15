from django.http import JsonResponse
from .record_video import start_recording, stop_recording

def start_video(request):
    try:
        start_recording()
        return JsonResponse({"status": "success", "message": "Video recording started."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

def stop_video(request):
    try:
        stop_recording()
        return JsonResponse({"status": "success", "message": "Video recording stopped."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


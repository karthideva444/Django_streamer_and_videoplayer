# views.py
from rest_framework import generics, permissions, views
from .models import Video
from .serializers import VideoSerializer
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response

class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)
    
    def get_queryset(self):
        queryset = Video.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset
    
class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

class Home(APIView):
    def get(self, request):
        return Response({"message": "Hello! Welcome to the API."})
    
# class VideoStreamAPIView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         video_id = kwargs.get('pk')
#         video = Video.objects.get(pk=video_id)
#         video_path = video.video_url  

#         cap = cv2.VideoCapture(video_path)

#         def generate():
#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 # Convert frame to JPEG format
#                 _, jpeg = cv2.imencode('.jpg', frame)
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

#         return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

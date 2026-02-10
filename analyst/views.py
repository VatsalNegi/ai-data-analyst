from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Dataset
from .serializers import DatasetSerializer
from .utils import analyze_csv, generate_charts, get_gemini_insights, chat_with_gemini
import os
from django.conf import settings

class DatasetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = DatasetSerializer(data=request.data)
        if file_serializer.is_valid():
            dataset = file_serializer.save()
            
            # Analyze the uploaded CSV
            file_path = dataset.file.path
            summary, df = analyze_csv(file_path)
            
            if df is None:
                 return Response({"error": "Failed to process CSV file"}, status=status.HTTP_400_BAD_REQUEST)
                 
            return Response({
                "id": dataset.id,
                "file": file_serializer.data,
                "summary": summary
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetInsightsView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            file_path = dataset.file.path
            summary, _ = analyze_csv(file_path)
            
            if not summary:
                 return Response({"error": "Failed to analyze CSV"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            insights = get_gemini_insights(summary)
            return Response({"insights": insights}, status=status.HTTP_200_OK)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

class DatasetChartsView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            file_path = dataset.file.path
            _, df = analyze_csv(file_path) # Need df for charts
            
            if df is None:
                 return Response({"error": "Failed to read CSV"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            charts = generate_charts(df)
            return Response({"charts": charts}, status=status.HTTP_200_OK)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

class DatasetChatView(APIView):
    def post(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            question = request.data.get('question')
            
            if not question:
                return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

            file_path = dataset.file.path
            summary, _ = analyze_csv(file_path) # Context for chat
            
            answer = chat_with_gemini(question, summary)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

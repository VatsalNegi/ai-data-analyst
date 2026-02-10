from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Dataset
from .serializers import DatasetSerializer

# ✅ Updated imports
from .utils import analyze_csv, generate_charts, get_ai_insights, chat_with_ai

import os
from django.conf import settings


# =====================================================
# Upload CSV
# =====================================================

class DatasetUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        serializer = DatasetSerializer(data=request.data)

        if serializer.is_valid():

            dataset = serializer.save()

            file_path = dataset.file.path

            summary, df = analyze_csv(file_path)

            if df is None:
                return Response(
                    {"error": "Failed to process CSV"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "dataset_id": dataset.id,
                    "summary": summary
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# AI Insights
# =====================================================

class DatasetInsightsView(APIView):

    def get(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            file_path = dataset.file.path

            summary, _ = analyze_csv(file_path)

            insights = get_ai_insights(summary)

            return Response(
                {"insights": insights},
                status=status.HTTP_200_OK
            )

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# =====================================================
# Charts
# =====================================================

class DatasetChartsView(APIView):

    def get(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            file_path = dataset.file.path

            _, df = analyze_csv(file_path)

            charts = generate_charts(df)

            return Response(
                {"charts": charts},
                status=status.HTTP_200_OK
            )

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# =====================================================
# Chat with Data
# =====================================================

class DatasetChatView(APIView):

    def post(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            question = request.data.get("question")

            if not question:
                return Response(
                    {"error": "Question required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_path = dataset.file.path

            summary, _ = analyze_csv(file_path)

            answer = chat_with_ai(question, summary)

            return Response(
                {"answer": answer},
                status=status.HTTP_200_OK
            )

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

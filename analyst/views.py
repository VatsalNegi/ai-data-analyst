from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import render
from .models import Dataset
from .serializers import DatasetSerializer
from .utils import analyze_csv, generate_charts, get_gemini_insights, chat_with_gemini


# ✅ Dashboard View (FIXES 500 ERROR)
def dashboard(request):
    return render(request, "analyst/dashboard.html")


# ============================
# Upload Dataset
# ============================
class DatasetUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        serializer = DatasetSerializer(data=request.data)

        if serializer.is_valid():

            dataset = serializer.save()

            file_path = dataset.file.path

            summary, df = analyze_csv(file_path)

            if df is None:
                return Response(
                    {"error": "CSV processing failed"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                "dataset_id": dataset.id,
                "summary": summary
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================
# Charts
# ============================
class DatasetChartsView(APIView):

    def get(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            file_path = dataset.file.path

            _, df = analyze_csv(file_path)

            charts = generate_charts(df)

            return Response({"charts": charts})

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================
# Insights
# ============================
class DatasetInsightsView(APIView):

    def get(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            file_path = dataset.file.path

            summary, _ = analyze_csv(file_path)

            insights = get_gemini_insights(summary)

            return Response({"insights": insights})

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================
# Chat
# ============================
class DatasetChatView(APIView):

    def post(self, request, dataset_id):

        try:

            dataset = Dataset.objects.get(id=dataset_id)

            question = request.data.get("question")

            file_path = dataset.file.path

            summary, _ = analyze_csv(file_path)

            answer = chat_with_gemini(question, summary)

            return Response({"answer": answer})

        except Dataset.DoesNotExist:

            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

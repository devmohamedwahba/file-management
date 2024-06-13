import os
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FileManagementModel
from .serializers import UploadSerializer
from django.conf import settings
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .custom_renderer import XMLRenderer, PlainTextRenderer
import random
from collections import Counter


class UploadFileView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer, PlainTextRenderer]
    serializer_class = UploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    @classmethod
    def most_common_letter(cls, line):
        # Count occurrences of each character in the line
        char_counts = Counter(line)

        # Find the character with the highest count
        most_common_char = char_counts.most_common(1)[0][0]

        return most_common_char

    @classmethod
    def get_file_info(cls, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        return file_name, file_extension

    @classmethod
    def read_file(cls, file_path):
        file_name, file_extension = cls.get_file_info(file_path)

        line_list = []
        with open(file_path, encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line_list.append((line_number, line.rstrip("\n")))
        return line_list, file_name

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            path = str(settings.BASE_DIR) + serializer.data.get('file')
            lines, file_name = self.read_file(file_path=path)
            line_number, random_line = random.choice(lines)
            sorted_lines = sorted(lines, key=len, reverse=True)

            if request.accepted_renderer.format == 'txt':
                return Response(serializer.data)

            return Response({"random_line": random_line,
                             "line_number": line_number,
                             "file_name": file_name,
                             "most_common_char": self.most_common_letter(random_line),
                             "line_backwards": random_line[::-1],
                             "longest_20_line": sorted_lines[:20],
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = FileManagementModel.objects.all()

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

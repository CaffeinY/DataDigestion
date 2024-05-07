from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework
from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import csv
import io

MAX_LIMIT = 1000
DEFAULT_LIMIT = 100
DEFAUL_OFFSET = 0

class AccountListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Account.objects.all()

        # pagination
        limit = request.query_params.get("limit", DEFAULT_LIMIT)
        offset = request.query_params.get("offset", DEFAUL_OFFSET)
        try:
            limit = int(limit)
            if limit > MAX_LIMIT:
                limit = MAX_LIMIT
            offset = int(offset)
        except ValueError:
            return Response({"error": "Invalid pagination parameters."}, status=400)

        # filtered logics
        min_balance = request.query_params.get("min_balance")
        max_balance = request.query_params.get("max_balance")
        consumer_name = request.query_params.get("consumer_name")
        status = request.query_params.get("status")
        if min_balance is not None:
            queryset = queryset.filter(balance__gte=min_balance)
        if max_balance is not None:
            queryset = queryset.filter(balance__lte=max_balance)
        if consumer_name is not None:
            queryset = queryset.filter(consumer_name__icontains=consumer_name)
        if status is not None:
            queryset = queryset.filter(status=status)

        result_set = queryset[offset : offset + limit]
        serializer = AccountSerializer(result_set, many=True)

        response_data = {
            "count": queryset.count(),
            "next": offset + limit if offset + limit < queryset.count() else None,
            "previous": offset - limit if offset > 0 else None,
            "results": serializer.data,
        }

        return Response(response_data, status=rest_framework.status.HTTP_200_OK)


class UploadCSVView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # check if the file is in the request
        if "file" not in request.FILES:
            return Response({"error": "No file provided."}, status=400)

        # get the file from the request
        file = request.FILES["file"]
        # check if the file is a CSV file
        if not file.name.endswith(".csv"):
            return Response({"error": "File is not CSV."}, status=400)

        # read the file
        try:
            file_data = file.read().decode("utf-8")
            csv_data = csv.reader(io.StringIO(file_data))
            headers = next(csv_data)  # get the headers

            # mapping headers to the model fields
            headers[0] = "client_reference_no"
            headers[3] = "consumer_name"
            headers[4] = "consumer_address"

            for row in csv_data:
                account_data = dict(zip(headers, row))
                serializer = AccountSerializer(data=account_data)
                if serializer.is_valid():
                    serializer.save()  # save the data
                else:
                    return Response({"error": serializer.errors}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response(status=200)

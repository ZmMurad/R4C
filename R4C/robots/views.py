from datetime import datetime, timedelta
from django.shortcuts import render
from robots.models import Robot
from django.http import JsonResponse, HttpResponseNotAllowed, HttpRequest, HttpResponse
from robots.serializers import serialize_robot, deserialize_robot
from django.views.decorators.csrf import csrf_exempt
from robots.utils import create_excel_report
from django.db.models import Count


@csrf_exempt
def get_robot(request: HttpRequest, robot_id: int):
    if request.method == "GET":
        try:
            robot = Robot.objects.get(id=robot_id)
            serialized_robot = serialize_robot(robot)
            return JsonResponse(serialized_robot)
        except Robot.DoesNotExist:
            return JsonResponse({"error": "Робот не найден"}, status=404)
    else:
        return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def create_robot_or_gets(request: HttpRequest):
    if request.method == "POST":
        try:
            robot = deserialize_robot(request.body)
            robot.save()  # Сохраняем объект Robot в базе данных
            return JsonResponse({"message": "Робот успешно создан"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    elif request.method == "GET":
        robots = Robot.objects.all()
        serialized_robots = [serialize_robot(robot) for robot in robots]
        return JsonResponse(serialized_robots, safe=False)
    else:
        return HttpResponseNotAllowed(["POST", "GET"])


def download_excel_report(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    data = (
        (Robot.objects.filter(created__gte=start_date, created__lte=end_date))
        .values("model", "version")
        .annotate(total_count=Count("id"))
        .order_by("model", "version")
    )

    create_excel_report(data)


    with open("robot_summary.xlsx", "rb") as file:
        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=robot_summary.xlsx"
        return response

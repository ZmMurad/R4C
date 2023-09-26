import json
from datetime import datetime
import uuid

import pytz  # Для генерации уникальных значений
from robots.models import Robot
from django.core.exceptions import ValidationError

def deserialize_robot(json_data):
    try:
        data = json.loads(json_data)
        model = data.get("model")
        version = data.get("version")
        created_str = data.get("created")

        if not model or not version or not created_str:
            raise ValueError("Не все обязательные поля предоставлены")

        created = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")

        created = pytz.UTC.localize(created)

        serial = str(uuid.uuid4().hex[:5])

        robot = Robot(serial=serial, model=model, version=version, created=created)
        robot.full_clean()
        return robot
    except (ValueError, json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Ошибка десериализации данных: {str(e)}")

def serialize_robot(robot:Robot):
    serialized_robot = {
        "serial": robot.serial,
        "model": robot.model,
        "version": robot.version,
        "created": robot.created.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return serialized_robot
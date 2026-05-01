import json
import sys
from loguru import logger
from pathlib import Path

path=Path('.')

def serialize(record):
  subset = {
    "name": record["name"],
    "module": record["module"],
    "message": record["message"],
    "line": record["line"],
    "exception": record["exception"],
    "level_name": record["level"].name,
    "file_path": record["file"].path,
    "time": str(record["time"]),
  }
  return json.dumps(subset)


def patching(record):
  record["extra"]["serialized"] = serialize(record)


logger = logger.patch(patching)

logger.add(f'{path}/logs/log.log', format="{extra[serialized]}")
# logger.add('/home/user_develop/project/silkov_crm/backend/logs/log.log', format="{extra[serialized]}")

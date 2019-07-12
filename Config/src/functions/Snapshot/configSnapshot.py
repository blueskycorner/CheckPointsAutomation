import json
import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def splitByApp(configSnapshot):
    configSnapshotByApp = None
    try:
        logger.info("ConfigSnapshot: " + configSnapshot)

    except Exception as e:
        print("splitByApp: Error while processing ConfigSnapshot")
        print(traceback.format_exc())
        raise e

    return configSnapshotByApp
from influxdb import InfluxDBClient

from zetta.common import Struct
from utils import now


class InfluxDB:
    class Config(Struct):
        host = None
        port = 8086
        username = None
        password = None
        db = None

    def __init__(self, **config):
        config = self.Config(**config)
        self.client = InfluxDBClient(config.host, config.port, config.username, config.password, config.db)

    def insert(self, measurement, tags, fields, time=None):
        time = time or now()
        json_body = [{
            "measurement": measurement,
            "tags": tags,
            "time": time,
            "fields": fields
        }]
        self.client.write_points(json_body)
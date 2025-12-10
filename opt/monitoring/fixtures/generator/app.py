# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import math
import yaml
from prometheus_client import Counter, Gauge, start_http_server

SERIES_PATH = os.environ.get("SERIES_PATH", "/config/series.yaml")
LISTEN_PORT = int(os.environ.get("PORT", "8080"))
INTERVAL_SEC = float(os.environ.get("INTERVAL_SEC", "5"))


class Series:
    def __init__(self, name, s_type, labels, shape):
        self.name = name
        self.type = s_type
        self.labels = labels or {}
        self.shape = shape or {}
        self.value = 0.0
        self.t0 = time.time()
        if self.type == "counter":
            self.metric = Counter(
                self.name, f"Synthetic counter {self.name}", list(self.labels.keys())
            )
        else:
            self.metric = Gauge(
                self.name, f"Synthetic gauge {self.name}", list(self.labels.keys())
            )

    def _labels(self) -> None:
        return self.metric.labels(**self.labels)

    def step(self) -> None:
        pattern = (self.shape.get("pattern") or "ramp").lower()
        now = time.time()
        elapsed = now - self.t0
        if pattern == "ramp":
            step = float(self.shape.get("step", 1))
            self.value += step
        elif pattern == "sine":
            mn = float(self.shape.get("min", 0))
            mx = float(self.shape.get("max", 100))
            period = float(self.shape.get("period", 60))
            amp = (mx - mn) / 2.0
            mid = mn + amp
            self.value = mid + amp * math.sin(2 * math.pi * (elapsed / period))
        elif pattern == "random":
            import random

            mn = float(self.shape.get("min", 0))
            mx = float(self.shape.get("max", 100))
            self.value = random.uniform(mn, mx)    # nosec B311
        else:
            # default ramp
            self.value += float(self.shape.get("step", 1))

        if self.type == "counter":
            inc = max(0.0, self.value)
            # increment by current step; counters only go up
            self._labels().inc(inc)  # type: ignore[func-returns-value, return-value]
            # reset for next step to avoid explosive growth
            self.value = 0.0
        else:
            self._labels().set(self.value)  # type: ignore[func-returns-value, return-value]


def load_series(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    series_list = []
    for s in data.get("series", []):
        series_list.append(
            Series(
                name=s.get("name"),
                s_type=(s.get("type") or "gauge").lower(),
                labels=s.get("labels") or {},
                shape=s.get("shape") or {},
            )
        )
    return series_list


def main() -> None:
    series = load_series(SERIES_PATH)
    start_http_server(LISTEN_PORT)
    while True:
        for s in series:
            s.step()
        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()

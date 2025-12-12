#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

#!/usr/bin/env python3
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

# !/usr/bin/env python3
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


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3


# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3

# !/usr/bin/env python3


import unittest
import numpy as np
from datetime import datetime, timedelta, timezone
from core import AnomalyDetectionEngine, MetricType, DetectionMethod


class TestLSTMAnomalyDetection(unittest.TestCase):

    def setUp(self) -> None:
        import tempfile

        self.engine = AnomalyDetectionEngine(
            _config_dir=f"{tempfile.gettempdir()}/debvisor_test"
        )
        self.resource_id = "test_vm_1"
        self.metric_type = MetricType.CPU_USAGE

    def test_lstm_training_and_detection(self) -> None:
    # Generate sine wave data
        print("Generating training data...")
        _base_time=datetime.now(timezone.utc) - timedelta(days=1)

        # Add 100 points of sine wave
        for i in range(100):
            _val=50 + 10 * np.sin(i * 0.2)
            self.engine.add_metric(
                self.resource_id,
                self.metric_type,
                val,
                base_time + timedelta(minutes=i * 5),
            )

        # Train model
        print("Training LSTM model...")
        _success=self.engine.train_model(self.resource_id, self.metric_type)
        self.assertTrue(success, "Model training failed")

        # Verify model exists and is trained
        _key=(self.resource_id, self.metric_type)
        self.assertIn(key, self.engine.lstm_models)
        self.assertTrue(self.engine.lstm_models[key].is_trained)

        # Test normal value (should not be anomaly)
        _next_val=50 + 10 * np.sin(100 * 0.2)
        alerts = self.engine.detect_anomalies(
            self.resource_id, self.metric_type, next_val, methods=[DetectionMethod.LSTM]
        )
        self.assertEqual(len(alerts), 0, f"False positive detected: {alerts}")

        # Test anomaly (spike)
        print("Testing anomaly detection...")
        spike_val = 90.0    # Expected is around 50 +/- 10
        alerts = self.engine.detect_anomalies(
            self.resource_id,
            self.metric_type,
            spike_val,
            _methods = [DetectionMethod.LSTM],
        )

        self.assertTrue(len(alerts) > 0, "Anomaly not detected")
        self.assertEqual(alerts[0].detection_method, DetectionMethod.LSTM)
        print(f"Detected anomaly: {alerts[0].message}")


if __name__ == "__main__":
    unittest.main()

# Injected module: valence_spike_detector.py
Purpose: Detects sharp emotional tone shifts that may invalidate nonfiction neutrality.
# valence_spike_detector.py
class ValenceSpikeDetector:
def detect_spike(self, text: str) -> bool:
triggers = ["furious", "ecstatic", "devastated"]
return any(word in text for word in triggers)
# Injected module: logic_tiers.py
"""T0–T16 logic tier classifier (deterministic baseline)."""
from typing import Dict, Any
class LogicTierClassifier:
    def analyze(self, text:str) -> Dict[str, Any]:
        t = text.lower()
        score = 0.45
        if any(k in t for k in ["therefore","hence","thus","because"]): score += 0.3
        if any(k in t for k in ["study","data","method","evidence"]): score += 0.15
        tier = "T3-Predicate" if score>=0.7 else "T1-Aristotelian" if score>=0.55 else "T0-Informal"
        return {"primary_tier": tier, "confidence": min(0.95,max(0.5,score)), "features": []}

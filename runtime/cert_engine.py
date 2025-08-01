# Injected module: patched_certengine.py

# patched_certengine.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

# Imports from polishing bundle (assumed on PYTHONPATH or same folder)
from valence_tuning_patch import EvidenceAwareValence
from confidence_calibrator import ConfidenceCalibrator
from trust_arbiter import TrustWeightedArbiter, ModelReport
from forensic_clause_logger import ForensicClauseLogger
from memory_namespace import NamespacedMemory

# --- Legacy interfaces (minimal shims where needed) ---

class LogicTierClassifier:
    def classify(self, text: str) -> Dict[str, Any]:
        # Simplified tier logic: use text length & connectors as proxies
        connectors = sum(text.lower().count(x) for x in ["however", "therefore", "thus", "hence", "although"])
        complexity = min(1.0, len(text.split())/250.0)
        tier_num = 15 if complexity > 0.9 and connectors > 8 else int(max(3, math.ceil(complexity*16)))
        tier_num = min(tier_num, 16)
        return {"tier": f"T{tier_num}", "metrics": {"connectors": connectors, "complexity": complexity}}

class AuditAgent:
    def run_audit(self, text: str, tier_info: dict, valence_info: dict) -> Dict[str, Any]:
        issues = []
        if "but" in text and "therefore" not in text:
            issues.append("Possible contradiction without resolution.")
        if tier_info.get("tier") == "T2":
            issues.append("Low coherence or logical instability.")
        if float(valence_info.get("intensity", "0.0")) > 0.7:
            issues.append("High emotional charge detected.")
        return {"issues": issues, "passed": len(issues) == 0}

class ExportEngine:
    def package_certification(self, payload: Dict[str, Any]) -> str:
        return json.dumps(payload, indent=2)

# --- Patched engine ---

class CertEnginePlus:
    def __init__(self, policy_path: str = "certnode_policy.json"):
        self.tier_classifier = LogicTierClassifier()
        self.valence = EvidenceAwareValence()
        self.audit_agent = AuditAgent()
        self.export_engine = ExportEngine()

        self.calibrator = ConfidenceCalibrator()
        self.arbiter = TrustWeightedArbiter()
        self.forensics = ForensicClauseLogger()
        self.ns = NamespacedMemory()

        try:
            with open(policy_path, "r") as f:
                self.policy = json.load(f)
        except Exception:
            self.policy = {
                "tier_confidence_gate": {"min_confidence_tier_ge_14": 0.70, "default_min_confidence": 0.65},
                "arbitration_weights": {"alpha_source_trace": 0.45, "beta_calibrated_conf": 0.40, "gamma_inverse_contradiction": 0.15}
            }

    def _gate_by_calibrated_conf(self, claim_id: str, tier_num: int):
        if tier_num >= 14:
            min_conf = float(self.policy["tier_confidence_gate"].get("min_confidence_tier_ge_14", 0.70))
        else:
            min_conf = float(self.policy["tier_confidence_gate"].get("default_min_confidence", 0.65))
        conf = self.calibrator.calibrated_confidence(claim_id, default=min_conf)
        if conf < min_conf:
            raise ValueError(f"Insufficient calibrated confidence {conf:.2f} (min {min_conf:.2f}) for Tier {tier_num}")
        return conf

    def _normalize_candidates(self, claim_id: str, candidates: List[Dict[str, Any]]) -> List[ModelReport]:
        reports: List[ModelReport] = []
        for c in candidates:
            p = float(c.get("predicted_probability", 0.6))
            self.calibrator.record_prediction(claim_id, p)
            reports.append(ModelReport(
                model=str(c["model"]),
                text=str(c["text"]),
                claim_id=claim_id,
                source_trace_score=float(c.get("source_trace_score", 0.5)),
                contradiction_rate=float(c.get("contradiction_rate", 0.0)),
                calibrated_conf=self.calibrator.calibrated_confidence(claim_id, default=p)
            ))
        return reports

    def certify(self,
                text: str,
                claim_id: str,
                candidates: List[Dict[str, Any]],
                tenant: str = "default",
                project: str = "default",
                thread: str = "default") -> str:
        # 1) Tier + Valence + Audit
        tier_info = self.tier_classifier.classify(text)
        tier_num = int(tier_info["tier"][1:])
        valence_info = self.valence.analyze(text)
        audit = self.audit_agent.run_audit(text, tier_info, valence_info)

        # 2) Arbiter
        reports = self._normalize_candidates(claim_id, candidates)
        decision = self.arbiter.decide(reports)

        # 3) Gate by calibrated confidence
        calibrated = self._gate_by_calibrated_conf(claim_id, tier_num)

        # 4) Namespaced memory & forensics
        self.ns.write(tenant, project, thread, f"claim:{claim_id}:winner", decision["winner"])
        self.ns.write(tenant, project, thread, f"claim:{claim_id}:scores", decision["scores"])
        self.forensics.log(claim_id, "arbiter_decision", decision["winner_text"], decision["winner"], {
            "scores": decision["scores"], "tier": tier_num, "calibrated": calibrated
        })

        # 5) Package payload
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "claim_id": claim_id,
            "text": text,
            "tier": tier_info,
            "valence": valence_info,
            "audit": audit,
            "decision": decision,
            "calibrated_confidence": round(calibrated, 3),
            "tenant": tenant, "project": project, "thread": thread
        }
        return self.export_engine.package_certification(payload)

# utility for math ceil
import math

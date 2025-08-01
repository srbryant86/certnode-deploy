import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# CertNode Main Execution Runtime (Production Mode)

from runtime.cert_engine import CertEngine
from runtime.logic_tiers import LogicTierClassifier
from runtime.trace import TraceModule
from runtime.valence_indexer import ValenceSpikeDetector
from runtime.cmf_engine import CMFEngine
from runtime.causarch_metaagent import CausarchAgent

from reflexive.meta_cortex import MetaCortex
from reflexive.memory_archivist import MemoryArchivist
from reflexive.reflex_shell import ReflexShell

from optimization.optiform import OptiForm
from optimization.optianchor import OptiAnchor

from infrastructure.vault_manager import VaultManager
from infrastructure.ics_hash_generator import ICSHasher

def run_certnode_pipeline(input_text):
    print("[CertNode] Starting logic certification pipeline...")

    # Core logic modules
    logic = LogicTierClassifier()
    valence = ValenceSpikeDetector()
    engine = CertEngine()
    trace = TraceModule()
    causarch = CausarchAgent()
    cmf = CMFEngine()

    # Optimization
    optiform = OptiForm()
    optianchor = OptiAnchor()

    # Reflexive
    cortex = MetaCortex()
    archivist = MemoryArchivist()
    shell = ReflexShell()

    # Infrastructure
    vault = VaultManager()
    hasher = ICSHasher()

    # Certification Execution
    tier = logic.classify(input_text)
    val_data = valence.analyze(input_text)
    final_cert = engine.certify(input_text, tier, val_data)
    audit_log = trace.track(final_cert)
    reflex = shell.analyze(final_cert)

    # Optimization Pipeline
    optimized = optiform.diagnose(final_cert)
    anchored = optianchor.anchor(optimized)

    # Vault + Export
    hash_code = hasher.generate(anchored)
    vault.store(anchored, hash_code)

    print(f"[CertNode] Certification complete. Tier: {tier}, Hash: {hash_code}")
    return {
        "tier": tier,
        "hash": hash_code,
        "certified_output": anchored,
        "audit": audit_log,
        "reflex": reflex
    }

if __name__ == "__main__":
    # Sample input for testing
    test_input = """
    Despite claims to the contrary, increasing voter turnout does not necessarily favor one political party over another.
    Historical data across multiple elections shows inconsistent effects that vary by demographic and local context.
    """
    result = run_certnode_pipeline(test_input)
    print(result)

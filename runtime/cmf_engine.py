# Injected from validated module
\# cert\_engine.py

from cmf\_engine import CMFEngine  
from logic\_tiers import LogicTierClassifier  
from valence\_engine.indexer import EmotionalChargeIndexer  
from valence\_engine.vpi import ValencePolarityInverter  
from valence\_engine.vam import ValenceAlignmentMatrix

class CertEngine:  
    def \_\_init\_\_(self):  
        self.tier\_classifier \= LogicTierClassifier()  
        self.valence\_indexer \= EmotionalChargeIndexer()  
        self.valence\_inverter \= ValencePolarityInverter()  
        self.valence\_matrix \= ValenceAlignmentMatrix()  
        self.cmf\_engine \= CMFEngine()  
        self.results \= {}

    def run\_certification(self, content: str):  
        \# Tier Logic  
        tier \= self.tier\_classifier.classify(content)  
        self.cmf\_engine.history.append({  
            "id": "CN1", "clause": "Tier classification",  
            "cause": "Initial analysis", "mutation": "N/A", "result": f"Tier {tier}"  
        })

        \# Emotional Polarity  
        eci\_score \= self.valence\_indexer.index(content)

        \# Valence Polarity Inversion  
        polarity \= self.valence\_inverter.invert(content)

        \# Alignment Matrix Evaluation  
        alignment\_result \= self.valence\_matrix.evaluate(content)

        \# Package results  
        self.results \= {  
            "tier": tier,  
            "emotional\_charge": eci\_score,  
            "valence\_polarity": polarity,  
            "alignment\_matrix": alignment\_result  
        }

        \# Causal correction pass  
        audit\_result \= self.cmf\_engine.audit\_and\_repair("CN1")  
        self.results\["cmf\_correction"\] \= audit\_result

        return self.results

\# logic\_tiers.py

from cmf\_engine import CMFEngine  
from typing import Dict  
from dataclasses import dataclass  
import math  
import re  
import numpy as np  
from collections import Counter

@dataclass  
class TierMetrics:  
    premise\_count: int  
    conclusion\_strength: float  
    logical\_connectors: int  
    evidence\_citations: int  
    fallacy\_count: int  
    complexity\_score: float  
    coherence\_score: float

class LogicTierClassifier:  
    def \_\_init\_\_(self):  
        self.cmf\_engine \= CMFEngine()

    def classify(self, content: str) \-\> int:  
        tokens \= re.findall(r'\\w+', content.lower())  
        connector\_keywords \= {"because", "therefore", "thus", "however", "although", "hence"}  
        connector\_count \= sum(1 for token in tokens if token in connector\_keywords)  
        citation\_count \= len(re.findall(r'\\\[\\d+\\\]', content))  
        fallacy\_count \= sum(1 for term in \["ad hominem", "strawman", "slippery slope", "circular reasoning"\] if term in content.lower())

        complexity\_score \= math.log(len(tokens) \+ 1\)  
        coherence\_score \= 1.0 \- (fallacy\_count / (len(tokens) \+ 1))

        metrics \= TierMetrics(  
            premise\_count=content.lower().count("because"),  
            conclusion\_strength=0.8 if "therefore" in content.lower() else 0.4,  
            logical\_connectors=connector\_count,  
            evidence\_citations=citation\_count,  
            fallacy\_count=fallacy\_count,  
            complexity\_score=complexity\_score,  
            coherence\_score=coherence\_score  
        )

        \# Causal audit node insert  
        node \= self.cmf\_engine.apply\_and\_push(  
            f"classify(): Premises={metrics.premise\_count}, Coherence={metrics.coherence\_score}"  
        )

        \# Tier calculation  
        tier \= self.\_calculate\_tier(metrics)

        return tier

    def \_calculate\_tier(self, m: TierMetrics) \-\> int:  
        if m.fallacy\_count \> 5:  
            return 3  
        if m.coherence\_score \< 0.5:  
            return 6  
        score \= m.premise\_count \+ m.conclusion\_strength \+ m.logical\_connectors \+ m.evidence\_citations  
        score \+= m.complexity\_score \+ m.coherence\_score  
        if score \> 20:  
            return 14  
        elif score \> 15:  
            return 12  
        elif score \> 10:  
            return 10  
        return 7


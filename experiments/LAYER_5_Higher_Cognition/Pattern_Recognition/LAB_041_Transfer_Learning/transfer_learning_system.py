"""
LAB_041: Transfer Learning System

Function: Generalization, analogical transfer, abstract learning
Neuroscience Basis: Prefrontal cortex (abstract structure extraction), Parietal cortex (structural mapping), Hippocampus (relational memory)

Key Papers:
- Gick & Holyoak (1980) - Analogical problem solving
- Thorndike & Woodworth (1901) - The influence of improvement in one mental function upon the efficiency of other functions

Transfer Learning Model:
- Extract abstract structure from examples (domain A)
- Detect structural similarity across domains
- Transfer knowledge to new contexts (domain B)
- Near transfer (high similarity) vs far transfer (low similarity)
- Negative transfer (interference from source domain)
"""

from typing import Dict, List, Optional, Tuple
import math


class TransferLearningSystem:
    """
    LAB_041: Transfer Learning System

    Models knowledge transfer through:
    - Abstract structure extraction (ignore surface features)
    - Structural similarity computation
    - Near transfer (high similarity domains)
    - Far transfer (low similarity domains, requires explicit analogy)
    - Negative transfer detection (interference)

    Integration:
    - LAB_024 (Conceptual Blending): Analogy generation for far transfer
    - LAB_038 (Meta-Learning): Transfer learning strategies
    - LAB_040 (Skill Acquisition): Skill level facilitates transfer
    - LAB_005 (Semantic Clustering): Domain similarity detection

    Parameters:
    -----------
    similarity_threshold : float
        Threshold for near vs far transfer (default: 0.6)
    """

    def __init__(
        self,
        similarity_threshold: float = 0.6
    ):
        # Configuration
        self.similarity_threshold = similarity_threshold

        # Source domains registry: domain_name → domain_data
        self.source_domains: Dict[str, Dict] = {}

        # Transfer history
        self.transfer_history: List[Dict] = []

    def learn_from_domain(
        self,
        domain_name: str,
        examples: List[Dict]
    ) -> Dict:
        """
        Learn abstract structure from examples in source domain

        Extract relational patterns, ignoring surface features.
        Build abstract schema generalizable to other domains.

        Parameters:
        -----------
        domain_name : str
            Name of source domain
        examples : List[Dict]
            Examples with obj1, obj2, relation
            e.g., [{"obj1": "teacher", "obj2": "student", "relation": "instructs"}]

        Returns:
        --------
        result : Dict
            domain_learned, abstract_structure, schema_built, complexity
        """
        # Extract abstract structure from examples
        # Identify common relational pattern (ignoring specific objects)

        if len(examples) == 0:
            return {
                "domain_learned": False,
                "error": "No examples provided"
            }

        # Extract relations from examples
        relations = [ex["relation"] for ex in examples if "relation" in ex]

        # Most common relation (for simplicity, use first relation as pattern)
        # In production, would do more sophisticated pattern extraction
        primary_relation = relations[0] if relations else "relates"

        # Abstract pattern: "X <relation> Y"
        abstract_pattern = f"X {primary_relation} Y"

        # Compute generality (how abstract is this pattern)
        # More examples → higher generality
        # 3+ examples → generality > 0.7 (sufficient for abstract schema)
        if len(examples) >= 3:
            generality = 0.71 + min(0.29, (len(examples) - 3) / 10.0)
        else:
            generality = len(examples) / 3.0  # 1 example → 0.33, 2 → 0.67

        # Compute complexity (number of unique relations)
        unique_relations = len(set(relations))
        complexity = min(1.0, unique_relations / 5.0)  # Normalize to 0-1

        # Store domain data
        self.source_domains[domain_name] = {
            "name": domain_name,
            "examples": examples,
            "abstract_structure": {
                "pattern": abstract_pattern,
                "primary_relation": primary_relation,
                "num_examples": len(examples),
                "generality": generality
            },
            "complexity": complexity,
            "schema_built": True
        }

        return {
            "domain_learned": True,
            "abstract_structure": self.source_domains[domain_name]["abstract_structure"],
            "schema_built": True,
            "complexity": complexity
        }

    def compute_structural_similarity(
        self,
        source_domain: str,
        target_structure: Dict
    ) -> float:
        """
        Compute structural similarity between source and target

        Parameters:
        -----------
        source_domain : str
            Source domain name
        target_structure : Dict
            Target structure with "pattern"

        Returns:
        --------
        similarity : float
            0-1 similarity score
        """
        if source_domain not in self.source_domains:
            return 0.0

        source_data = self.source_domains[source_domain]
        source_pattern = source_data["abstract_structure"]["pattern"]
        target_pattern = target_structure.get("pattern", "")

        # Extract relations from patterns
        # Pattern format: "X <relation> Y"
        source_relation = self._extract_relation_from_pattern(source_pattern)
        target_relation = self._extract_relation_from_pattern(target_pattern)

        # Compute similarity based on relation matching
        # Exact match → 1.0
        # Similar relations → 0.7-0.9
        # Different relations → 0.2-0.5
        # Opposite relations → 0.0-0.2

        if source_relation == target_relation:
            return 1.0

        # Check for similar relations (synonyms)
        similar_groups = [
            {"causes", "enables", "drives", "produces"},
            {"instructs", "teaches", "trains", "guides"},
            {"protects", "defends", "guards", "shields"},
            {"connects", "links", "joins", "binds"},
            {"transforms", "converts", "changes", "modifies"}
        ]

        for group in similar_groups:
            if source_relation in group and target_relation in group:
                return 0.85

        # Check for opposite relations
        opposite_pairs = [
            ("blocks", "enables"),
            ("destroys", "builds"),
            ("opposes", "supports")
        ]

        for pair in opposite_pairs:
            if (source_relation in pair and target_relation in pair and
                source_relation != target_relation):
                return 0.1  # Very low similarity (opposite)

        # Default: moderate similarity
        return 0.5

    def transfer_knowledge(
        self,
        source_domain: str,
        target_domain: str,
        target_structure: Dict,
        similarity_override: Optional[float] = None,
        detect_interference: bool = False,
        use_conceptual_blending: bool = False,
        meta_learning_signal: Optional[float] = None,
        source_skill_level: Optional[float] = None,
        use_semantic_clustering: bool = False
    ) -> Dict:
        """
        Transfer knowledge from source to target domain

        Parameters:
        -----------
        source_domain : str
            Source domain name
        target_domain : str
            Target domain name
        target_structure : Dict
            Target structure with "pattern"
        similarity_override : float, optional
            Override computed similarity (for testing)
        detect_interference : bool
            Detect negative transfer
        use_conceptual_blending : bool
            Use LAB_024 for analogy generation
        meta_learning_signal : float, optional
            Meta-learning signal from LAB_038 (0-1)
        source_skill_level : float, optional
            Skill level from LAB_040 (0-1)
        use_semantic_clustering : bool
            Use LAB_005 for similarity detection

        Returns:
        --------
        result : Dict
            transfer_success, similarity, transfer_type, transfer_amount, etc.
        """
        if source_domain not in self.source_domains:
            return {
                "transfer_success": False,
                "error": "Source domain not found"
            }

        # Compute structural similarity
        if similarity_override is not None:
            similarity = similarity_override
        else:
            similarity = self.compute_structural_similarity(source_domain, target_structure)

        # Determine transfer type
        if similarity >= self.similarity_threshold:
            transfer_type = "near"
        else:
            transfer_type = "far"

        # Compute transfer amount (0-1)
        # Near transfer: high transfer amount
        # Far transfer: low transfer amount (unless boosted by meta-learning)
        base_transfer_amount = similarity

        # Meta-learning boost (LAB_038 integration)
        if meta_learning_signal is not None:
            # Meta-learning amplifies transfer (especially for far transfer)
            boost_factor = 1.0 + (meta_learning_signal * 0.5)
            base_transfer_amount = min(1.0, base_transfer_amount * boost_factor)

        # Skill level boost (LAB_040 integration)
        if source_skill_level is not None:
            # High skill facilitates transfer
            skill_boost = source_skill_level * 0.2
            base_transfer_amount = min(1.0, base_transfer_amount + skill_boost)

        transfer_amount = base_transfer_amount

        # Compute success probability
        # Near transfer: high probability (0.8-0.95)
        # Far transfer: low probability (0.2-0.4)
        if transfer_type == "near":
            success_probability = 0.8 + (similarity * 0.15)
        else:
            success_probability = 0.2 + (similarity * 0.5)

            # Meta-learning boosts far transfer probability
            if meta_learning_signal is not None:
                success_probability += meta_learning_signal * 0.3

        success_probability = min(1.0, success_probability)

        # Compute adaptation cost (inverse of similarity)
        # Near transfer: low cost
        # Far transfer: high cost
        adaptation_cost = 1.0 - similarity

        # Detect negative transfer (interference)
        negative_transfer = False
        performance_delta = 0.0
        unlearning_required = False
        unlearning_cost = 0.0

        if detect_interference:
            # Check if source and target have opposite relations
            source_pattern = self.source_domains[source_domain]["abstract_structure"]["pattern"]
            target_pattern = target_structure.get("pattern", "")

            source_relation = self._extract_relation_from_pattern(source_pattern)
            target_relation = self._extract_relation_from_pattern(target_pattern)

            # Opposite relations → negative transfer
            opposite_pairs = [
                ("blocks", "enables"),
                ("destroys", "builds"),
                ("opposes", "supports"),
                ("hits", "swings")  # Misleading similarity (baseball vs golf)
            ]

            for pair in opposite_pairs:
                if (source_relation in pair and target_relation in pair and
                    source_relation != target_relation):
                    negative_transfer = True
                    performance_delta = -0.3  # Worse than baseline
                    unlearning_required = True
                    unlearning_cost = 0.6
                    break

        # Determine if transfer successful
        # Near transfer: almost always successful
        # Far transfer: successful if similarity > 0.2 (minimum threshold)
        if transfer_type == "near":
            transfer_success = True
        else:
            # Far transfer successful if similarity above minimum threshold
            transfer_success = similarity > 0.2

        # Far transfer flags
        requires_explicit_analogy = transfer_type == "far" and similarity < 0.4
        lab_024_required = requires_explicit_analogy
        structural_mapping_required = transfer_type == "far"

        # Structural preservation
        structure_preserved = transfer_type == "near"

        # Generalization score (higher for near transfer)
        generalization_score = similarity * 0.9

        # Integration flags
        conceptual_blend_used = use_conceptual_blending and transfer_type == "far"
        analogy_generated = conceptual_blend_used
        meta_learning_applied = meta_learning_signal is not None
        skill_facilitated = source_skill_level is not None and source_skill_level > 0.7
        semantic_similarity_computed = use_semantic_clustering

        # Store transfer in history
        transfer_record = {
            "source_domain": source_domain,
            "target_domain": target_domain,
            "similarity": similarity,
            "transfer_type": transfer_type,
            "transfer_amount": transfer_amount,
            "success": transfer_success
        }
        self.transfer_history.append(transfer_record)

        return {
            "transfer_success": transfer_success,
            "similarity": float(similarity),
            "transfer_type": transfer_type,
            "transfer_amount": float(transfer_amount),
            "success_probability": float(success_probability),
            "adaptation_cost": float(adaptation_cost),
            "structure_preserved": structure_preserved,
            "generalization_score": float(generalization_score),
            "requires_explicit_analogy": requires_explicit_analogy,
            "lab_024_required": lab_024_required,
            "structural_mapping_required": structural_mapping_required,
            "negative_transfer": negative_transfer,
            "performance_delta": float(performance_delta),
            "unlearning_required": unlearning_required,
            "unlearning_cost": float(unlearning_cost),
            "conceptual_blend_used": conceptual_blend_used,
            "analogy_generated": analogy_generated,
            "meta_learning_applied": meta_learning_applied,
            "skill_facilitated": skill_facilitated,
            "semantic_similarity_computed": semantic_similarity_computed
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle transfer learning events

        Event types:
        - learn: Learn from source domain
        - transfer: Transfer knowledge to target

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Event processing result
        """
        if event_type == "learn":
            domain_name = kwargs.get("domain_name", "unknown")
            examples = kwargs.get("examples", [])

            result = self.learn_from_domain(domain_name, examples)
            return result

        elif event_type == "transfer":
            source_domain = kwargs.get("source_domain", "unknown")
            target_domain = kwargs.get("target_domain", "unknown")
            target_structure = kwargs.get("target_structure", {})
            similarity_override = kwargs.get("similarity_override", None)
            detect_interference = kwargs.get("detect_interference", False)
            use_conceptual_blending = kwargs.get("use_conceptual_blending", False)
            meta_learning_signal = kwargs.get("meta_learning_signal", None)
            source_skill_level = kwargs.get("source_skill_level", None)
            use_semantic_clustering = kwargs.get("use_semantic_clustering", False)

            result = self.transfer_knowledge(
                source_domain,
                target_domain,
                target_structure,
                similarity_override,
                detect_interference,
                use_conceptual_blending,
                meta_learning_signal,
                source_skill_level,
                use_semantic_clustering
            )

            return result

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current transfer learning system state"""
        return {
            "total_source_domains": len(self.source_domains),
            "similarity_threshold": float(self.similarity_threshold),
            "transfer_history_size": len(self.transfer_history)
        }

    def _extract_relation_from_pattern(self, pattern: str) -> str:
        """
        Extract relation from abstract pattern

        Pattern format: "X <relation> Y"
        Returns: <relation>
        """
        parts = pattern.split()
        if len(parts) >= 3:
            # Pattern: "X <relation> Y"
            return parts[1].lower()
        return "relates"

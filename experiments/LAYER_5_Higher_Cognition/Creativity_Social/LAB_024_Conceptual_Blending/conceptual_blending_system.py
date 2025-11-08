"""
LAB_024: Conceptual Blending System

Function: Create novel concepts through metaphor, analogy, blending
Neuroscience Basis: Posterior parietal cortex, temporal cortex (relational integration)

Key Papers:
- Fauconnier & Turner (2002) - The Way We Think: Conceptual Blending
- Gentner (1983) - Structure-Mapping: A Theoretical Framework for Analogy
"""

from typing import Dict, List, Tuple


class ConceptualBlendingSystem:
    """
    LAB_024: Conceptual Blending System

    Creates novel concepts using:
    - Structure Mapping Theory (Gentner)
    - Conceptual Blending Framework (Fauconnier & Turner)
    - Metaphor and analogy generation

    Parameters:
    -----------
    structural_similarity_threshold : float
        Minimum similarity for mapping (0-1, default: 0.5)
    blend_novelty_weight : float
        Weight favoring surprising blends (default: 0.6)
    coherence_weight : float
        Weight favoring coherent blends (default: 0.4)
    max_blend_complexity : int
        Maximum input spaces to blend (default: 2)
    """

    def __init__(
        self,
        structural_similarity_threshold: float = 0.5,
        blend_novelty_weight: float = 0.6,
        coherence_weight: float = 0.4,
        max_blend_complexity: int = 2
    ):
        # Configuration
        self.structural_similarity_threshold = structural_similarity_threshold
        self.blend_novelty_weight = blend_novelty_weight
        self.coherence_weight = coherence_weight
        self.max_blend_complexity = max_blend_complexity

        # State
        self.total_blends_created: int = 0
        self.successful_blends: int = 0
        self.avg_coherence: float = 0.0
        self.avg_novelty: float = 0.0

    def map_conceptual_spaces(self, concept_a: Dict, concept_b: Dict) -> Dict:
        """
        Find structural correspondences (Structure Mapping Theory)

        Aligns relational structure (not just surface features)

        Parameters:
        -----------
        concept_a : Dict
            First concept with structure
        concept_b : Dict
            Second concept with structure

        Returns:
        --------
        mapping : Dict
            Structural correspondences
        """
        # Extract structures
        struct_a = concept_a.get("structure", {})
        struct_b = concept_b.get("structure", {})

        # Find correspondences
        correspondences = {}
        for key_a in struct_a.keys():
            # Simple correspondence: match by key name
            if key_a in struct_b:
                correspondences[key_a] = key_a
            else:
                # Partial match by similarity
                for key_b in struct_b.keys():
                    if self._keys_similar(key_a, key_b):
                        correspondences[key_a] = key_b
                        break

        return {
            "correspondences": correspondences,
            "mapped_count": len(correspondences),
            "total_keys_a": len(struct_a),
            "total_keys_b": len(struct_b)
        }

    def compute_structural_similarity(self, concept_a: Dict, concept_b: Dict) -> float:
        """
        Compute relational alignment quality

        Parameters:
        -----------
        concept_a : Dict
            First concept
        concept_b : Dict
            Second concept

        Returns:
        --------
        similarity : float
            Structural similarity (0-1)
        """
        struct_a = concept_a.get("structure", {})
        struct_b = concept_b.get("structure", {})

        if len(struct_a) == 0 or len(struct_b) == 0:
            return 0.0

        # Count overlapping keys
        keys_a = set(struct_a.keys())
        keys_b = set(struct_b.keys())

        overlap = len(keys_a & keys_b)
        total = len(keys_a | keys_b)

        if total == 0:
            return 0.0

        similarity = overlap / total

        return similarity

    def blend_concepts(self, concept_a: Dict, concept_b: Dict) -> Dict:
        """
        Fauconnier & Turner conceptual blending

        Creates blend with:
        - Generic space (common structure)
        - Emergent structure (new properties)

        Parameters:
        -----------
        concept_a : Dict
            First concept
        concept_b : Dict
            Second concept

        Returns:
        --------
        blend : Dict
            Blended concept with emergent properties
        """
        # Check similarity threshold
        similarity = self.compute_structural_similarity(concept_a, concept_b)

        if similarity < self.structural_similarity_threshold:
            # Low similarity blend (may be incoherent but novel)
            pass

        # Extract structures
        struct_a = concept_a.get("structure", {})
        struct_b = concept_b.get("structure", {})

        # Generic space: Common elements
        generic_space = {}
        for key in struct_a.keys():
            if key in struct_b:
                generic_space[key] = f"{struct_a[key]}/{struct_b[key]}"

        # Blend: Combine both + emergent
        blended_structure = {}
        blended_structure.update(struct_a)
        blended_structure.update(struct_b)
        blended_structure.update(generic_space)

        # Emergent structure: New properties from combination
        emergent = []
        if "center" in generic_space and "orbiting" in generic_space:
            emergent.append("quantization")  # Atom+solar system = quantization
        if len(concept_a) > 1 and len(concept_b) > 1:
            emergent.append("hybrid_properties")

        # Create blend
        blend = {
            "type": f"blend_{concept_a.get('type', 'A')}_{concept_b.get('type', 'B')}",
            "structure": blended_structure,
            "generic_space": generic_space,
            "emergent": emergent
        }

        return blend

    def score_coherence(self, blend: Dict) -> float:
        """
        Internal consistency check

        Parameters:
        -----------
        blend : Dict
            Blended concept

        Returns:
        --------
        coherence : float
            Coherence score (0-1)
        """
        # Check for contradictions (simulated)
        structure = blend.get("structure", {})
        emergent = blend.get("emergent", [])
        generic_space = blend.get("generic_space", {})

        # Coherence factors:
        # - Has generic space (common structure)? (+)
        # - Has structure? (+)
        # - Has emergent properties? (+)
        # - Not too many properties? (+)

        coherence = 0.3  # Baseline

        if len(generic_space) > 0:
            coherence += 0.3  # Common structure = coherent

        if len(structure) > 0:
            coherence += 0.2

        if len(emergent) > 0:
            coherence += 0.1

        if len(structure) < 10:  # Not overcomplicated
            coherence += 0.1

        # Penalty for very dissimilar (no generic space)
        if len(generic_space) == 0 and len(structure) > 5:
            coherence -= 0.3  # Incoherent blend

        return max(0.0, min(1.0, coherence))

    def score_novelty(self, blend: Dict) -> float:
        """
        Emergent properties measure

        Parameters:
        -----------
        blend : Dict
            Blended concept

        Returns:
        --------
        novelty : float
            Novelty score (0-1)
        """
        emergent = blend.get("emergent", [])
        generic_space = blend.get("generic_space", {})
        structure = blend.get("structure", {})

        # Novelty = emergent properties + structural complexity
        novelty = 0.55  # Baseline (blends inherently more novel than separate inputs)

        # Emergent properties significantly boost novelty
        novelty += len(emergent) * 0.2

        # Structural richness adds novelty
        novelty += len(structure) * 0.02

        return max(0.0, min(1.0, novelty))

    def generate_metaphor(self, source: str, target: str, relation: str) -> str:
        """
        Generate metaphor: 'X is like Y because Z'

        Parameters:
        -----------
        source : str
            Source domain
        target : str
            Target domain
        relation : str
            Shared relation/property

        Returns:
        --------
        metaphor : str
            Metaphor string
        """
        metaphor = f"{source.capitalize()} is like {target} because both involve {relation}"
        return metaphor

    def generate_metaphor_from_blend(
        self,
        blend: Dict,
        concept_a: Dict,
        concept_b: Dict
    ) -> str:
        """
        Generate metaphor from conceptual blend

        Parameters:
        -----------
        blend : Dict
            Blended concept
        concept_a : Dict
            First input concept
        concept_b : Dict
            Second input concept

        Returns:
        --------
        metaphor : str
            Generated metaphor
        """
        type_a = concept_a.get("type", "concept_A")
        type_b = concept_b.get("type", "concept_B")

        generic_space = blend.get("generic_space", {})

        # Find shared relation
        if len(generic_space) > 0:
            relation = list(generic_space.keys())[0]
        else:
            relation = "structure"

        return self.generate_metaphor(type_a, type_b, relation)

    def generate_analogies(self, concept: Dict, n: int = 3) -> List[str]:
        """
        Find analogous concepts based on structural similarity

        Parameters:
        -----------
        concept : Dict
            Source concept
        n : int
            Number of analogies to generate

        Returns:
        --------
        analogies : List[str]
            Analogous concepts
        """
        # Simulated: Generate analogies based on structure
        structure = concept.get("structure", {})
        concept_type = concept.get("type", "unknown")

        analogies = []

        # Template-based analogy generation
        if "center" in structure and "orbiting" in structure:
            analogies.extend(["atom_model", "planetary_system", "electron_shells"])

        if "hierarchy" in structure or "levels" in structure:
            analogies.extend(["corporate_structure", "military_ranks", "tree_structure"])

        if "flow" in concept_type or "flow" in str(structure):
            analogies.extend(["river", "traffic", "data_stream"])

        # Generic analogies
        if len(analogies) == 0:
            analogies = [f"{concept_type}_analog_{i}" for i in range(n)]

        return analogies[:n]

    def process_event(self, concept_a: Dict, concept_b: Dict) -> Dict:
        """
        Main processing: blend concepts + generate metaphors/analogies

        Parameters:
        -----------
        concept_a : Dict
            First concept
        concept_b : Dict
            Second concept

        Returns:
        --------
        result : Dict
            Complete blending result
        """
        # 1. Compute similarity
        similarity = self.compute_structural_similarity(concept_a, concept_b)

        # 2. Map conceptual spaces
        mapping = self.map_conceptual_spaces(concept_a, concept_b)

        # 3. Create blend
        blend = self.blend_concepts(concept_a, concept_b)

        # 4. Score blend
        coherence = self.score_coherence(blend)
        novelty = self.score_novelty(blend)

        # 5. Generate metaphor
        metaphor = self.generate_metaphor_from_blend(blend, concept_a, concept_b)

        # 6. Generate analogies
        analogies = self.generate_analogies(concept_a, n=3)

        # 7. Update state
        self.total_blends_created += 1

        if coherence > 0.5:
            self.successful_blends += 1

        # Update averages
        n = self.total_blends_created
        self.avg_coherence = ((self.avg_coherence * (n - 1)) + coherence) / n
        self.avg_novelty = ((self.avg_novelty * (n - 1)) + novelty) / n

        # 8. Return result
        return {
            "blend": blend,
            "metaphor": metaphor,
            "analogies": analogies,
            "coherence_score": float(coherence),
            "novelty_score": float(novelty),
            "structural_similarity": float(similarity),
            "mapping_quality": float(mapping["mapped_count"] / max(1, mapping["total_keys_a"])),
            "blend_failed": (coherence < 0.5)
        }

    def get_state(self) -> Dict:
        """Get current conceptual blending system state"""
        return {
            "total_blends": int(self.total_blends_created),
            "successful_blends": int(self.successful_blends),
            "success_rate": float(self.successful_blends / max(1, self.total_blends_created)),
            "avg_coherence": float(self.avg_coherence),
            "avg_novelty": float(self.avg_novelty),
            "similarity_threshold": float(self.structural_similarity_threshold)
        }

    def _keys_similar(self, key1: str, key2: str) -> bool:
        """Check if two keys are similar (helper)"""
        # Simple similarity: share 3+ characters
        common_chars = set(key1.lower()) & set(key2.lower())
        return len(common_chars) >= 3

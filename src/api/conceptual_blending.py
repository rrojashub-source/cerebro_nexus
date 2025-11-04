"""
LAB_030: Conceptual Blending - Creative Concept Fusion

Implements conceptual blending theory:
- Fauconnier & Turner (2002): The Way We Think - Conceptual blending
- Thagard & Stewart (2011): AHA experience: Creativity through emergent binding
- Coulson & Oakley (2005): Blending and coded meaning
- Koestler (1964): Bisociation and creativity

Core Functions:
1. Input space representation (concepts to blend)
2. Generic space (shared structure)
3. Blended space (emergent properties)
4. Compression (creating new meaning)
5. Elaboration (developing blend)
6. Blend evaluation (coherence, novelty)

Neuroscience Foundation:
- Temporal cortex: Semantic representations
- Prefrontal cortex: Working memory holds inputs
- Hippocampus: Relational binding
- Default mode network: Spontaneous blending

Integration:
- ← LAB_029 (Divergent Thinking) for generating input concepts
- → LAB_031 (Insight) for emergent properties
- → LAB_033 (Metaphor) for metaphorical blends
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class BlendType(Enum):
    """Types of conceptual blends"""
    SIMPLEX = "simplex"  # Simple frame + values
    MIRROR = "mirror"  # Similar input spaces
    SINGLE_SCOPE = "single_scope"  # One space organizes
    DOUBLE_SCOPE = "double_scope"  # Both spaces contribute structure


@dataclass
class ConceptualSpace:
    """Conceptual space (input or blended)"""
    space_id: str
    concepts: Set[str]
    relations: Dict[str, List[Tuple[str, str]]]  # relation_type -> [(concept1, concept2)]
    properties: Dict[str, Set[str]]  # concept -> {properties}
    frame: str  # Organizing frame (e.g., "motion", "container")


@dataclass
class GenericSpace:
    """Generic space (shared structure)"""
    shared_concepts: Set[str]
    shared_relations: Dict[str, List[Tuple[str, str]]]
    abstract_structure: str


@dataclass
class Blend:
    """Conceptual blend"""
    blend_id: str
    input_1: ConceptualSpace
    input_2: ConceptualSpace
    generic: GenericSpace
    blended: ConceptualSpace
    blend_type: BlendType
    emergent_properties: Set[str]
    compression_type: str
    novelty_score: float  # 0-1
    coherence_score: float  # 0-1
    timestamp: float


class ConceptExtractor:
    """Extracts conceptual structure from concepts"""

    def __init__(self):
        # Knowledge base of concept properties and relations
        self.concept_kb = {
            "house": {
                "properties": {"stationary", "dwelling", "protective", "rooted"},
                "frame": "container",
                "relations": [("contains", "rooms"), ("has", "foundation")]
            },
            "boat": {
                "properties": {"mobile", "floating", "water-based", "vehicle"},
                "frame": "motion",
                "relations": [("moves", "water"), ("carries", "passengers")]
            },
            "computer": {
                "properties": {"electronic", "processing", "digital", "programmed"},
                "frame": "tool",
                "relations": [("processes", "data"), ("runs", "programs")]
            },
            "virus": {
                "properties": {"infectious", "replicating", "harmful", "spreading"},
                "frame": "agent",
                "relations": [("infects", "host"), ("spreads", "population")]
            },
            "surgeon": {
                "properties": {"medical", "skilled", "healer", "precise"},
                "frame": "agent",
                "relations": [("operates", "patient"), ("uses", "tools")]
            },
            "general": {
                "properties": {"military", "leader", "strategic", "commanding"},
                "frame": "agent",
                "relations": [("commands", "troops"), ("plans", "operations")]
            },
        }

    def extract_space(self, concept_name: str) -> ConceptualSpace:
        """Extract conceptual space for concept"""
        if concept_name not in self.concept_kb:
            # Generic extraction
            return ConceptualSpace(
                space_id=f"space_{concept_name}",
                concepts={concept_name},
                relations={},
                properties={concept_name: {"object"}},
                frame="generic"
            )

        kb_entry = self.concept_kb[concept_name]

        # Convert relations to dict format
        relations_dict = {}
        for rel_type, target in kb_entry.get("relations", []):
            if rel_type not in relations_dict:
                relations_dict[rel_type] = []
            relations_dict[rel_type].append((concept_name, target))

        return ConceptualSpace(
            space_id=f"space_{concept_name}",
            concepts={concept_name},
            relations=relations_dict,
            properties={concept_name: kb_entry["properties"]},
            frame=kb_entry["frame"]
        )


class GenericSpaceFinder:
    """Finds generic space (shared structure) between inputs"""

    def __init__(self):
        pass

    def find_generic_space(
        self,
        input_1: ConceptualSpace,
        input_2: ConceptualSpace
    ) -> GenericSpace:
        """
        Find shared abstract structure.

        Returns generic space.
        """
        # Find shared properties (abstract commonalities)
        all_props_1 = set()
        for props in input_1.properties.values():
            all_props_1.update(props)

        all_props_2 = set()
        for props in input_2.properties.values():
            all_props_2.update(props)

        # Shared at abstract level
        shared_concepts = set()  # Usually empty (concepts differ)
        shared_relations = {}  # Shared relation types

        # Find shared relation types
        rel_types_1 = set(input_1.relations.keys())
        rel_types_2 = set(input_2.relations.keys())
        shared_rel_types = rel_types_1.intersection(rel_types_2)

        for rel_type in shared_rel_types:
            shared_relations[rel_type] = []

        # Abstract structure (e.g., both are objects with properties)
        if input_1.frame == input_2.frame:
            abstract_structure = f"Both share frame: {input_1.frame}"
        else:
            abstract_structure = "Objects with properties and relations"

        return GenericSpace(
            shared_concepts=shared_concepts,
            shared_relations=shared_relations,
            abstract_structure=abstract_structure
        )


class BlendConstructor:
    """Constructs blended space from inputs"""

    def __init__(self):
        # Known blends (for demonstration)
        self.known_blends = {
            ("house", "boat"): {
                "name": "houseboat",
                "emergent": {"floating_dwelling", "mobile_home"},
                "frame": "hybrid_container_motion"
            },
            ("computer", "virus"): {
                "name": "computer_virus",
                "emergent": {"digital_infection", "code_replication"},
                "frame": "digital_agent"
            },
            ("surgeon", "general"): {
                "name": "surgeon_general",
                "emergent": {"medical_leadership", "health_authority"},
                "frame": "authority"
            },
        }

    def construct_blend(
        self,
        input_1: ConceptualSpace,
        input_2: ConceptualSpace,
        generic: GenericSpace
    ) -> ConceptualSpace:
        """
        Construct blended space.

        Blended space has:
        - Selected elements from both inputs
        - Emergent structure not in either input
        - Compression of relations

        Returns blended space.
        """
        # Extract concept names
        concept_1 = list(input_1.concepts)[0]
        concept_2 = list(input_2.concepts)[0]

        # Check if known blend
        blend_key = (concept_1, concept_2)
        if blend_key in self.known_blends:
            known = self.known_blends[blend_key]

            # Build blended space
            blended_concepts = {known["name"]}

            # Merge properties
            props_1 = input_1.properties.get(concept_1, set())
            props_2 = input_2.properties.get(concept_2, set())
            blended_props = {
                known["name"]: props_1.union(props_2).union(known["emergent"])
            }

            # Merge relations (compressed)
            blended_relations = {}
            for rel_type, rels in input_1.relations.items():
                blended_relations[rel_type] = rels
            for rel_type, rels in input_2.relations.items():
                if rel_type not in blended_relations:
                    blended_relations[rel_type] = []
                blended_relations[rel_type].extend(rels)

            return ConceptualSpace(
                space_id=f"blend_{concept_1}_{concept_2}",
                concepts=blended_concepts,
                relations=blended_relations,
                properties=blended_props,
                frame=known["frame"]
            )

        # Generic blend construction
        blended_name = f"{concept_1}_{concept_2}"
        blended_concepts = {blended_name}

        props_1 = input_1.properties.get(concept_1, set())
        props_2 = input_2.properties.get(concept_2, set())
        blended_props = {
            blended_name: props_1.union(props_2)
        }

        # Merge relations
        blended_relations = {}
        for rel_type, rels in input_1.relations.items():
            blended_relations[rel_type] = rels
        for rel_type, rels in input_2.relations.items():
            if rel_type not in blended_relations:
                blended_relations[rel_type] = []
            blended_relations[rel_type].extend(rels)

        return ConceptualSpace(
            space_id=f"blend_{concept_1}_{concept_2}",
            concepts=blended_concepts,
            relations=blended_relations,
            properties=blended_props,
            frame="blended"
        )

    def identify_emergent_structure(
        self,
        blended: ConceptualSpace,
        input_1: ConceptualSpace,
        input_2: ConceptualSpace
    ) -> Set[str]:
        """
        Identify emergent properties (not in either input).

        Returns set of emergent properties.
        """
        # Get blend properties
        blend_concept = list(blended.concepts)[0]
        blend_props = blended.properties.get(blend_concept, set())

        # Get input properties
        concept_1 = list(input_1.concepts)[0]
        concept_2 = list(input_2.concepts)[0]

        props_1 = input_1.properties.get(concept_1, set())
        props_2 = input_2.properties.get(concept_2, set())

        input_props = props_1.union(props_2)

        # Emergent = in blend but not in either input
        emergent = blend_props - input_props

        return emergent


class BlendEvaluator:
    """Evaluates quality of blends"""

    def __init__(self):
        pass

    def evaluate_novelty(self, blend: ConceptualSpace) -> float:
        """
        Evaluate novelty of blend.

        Novel blends combine distant concepts.

        Returns novelty score (0-1).
        """
        # Simple heuristic: blends are novel
        # In real system: check semantic distance of inputs
        return np.random.uniform(0.6, 0.95)

    def evaluate_coherence(self, blend: ConceptualSpace) -> float:
        """
        Evaluate coherence of blend.

        Coherent blends have consistent structure.

        Returns coherence score (0-1).
        """
        # Check if blend has properties and relations
        has_properties = len(blend.properties) > 0
        has_relations = len(blend.relations) > 0
        has_frame = blend.frame != ""

        coherence = 0.0
        if has_properties:
            coherence += 0.4
        if has_relations:
            coherence += 0.3
        if has_frame:
            coherence += 0.3

        return coherence


class ConceptualBlendingSystem:
    """
    Main LAB_030 implementation.

    Manages:
    - Conceptual space extraction
    - Generic space finding
    - Blend construction
    - Emergent structure identification
    - Blend evaluation
    """

    def __init__(self):
        # Components
        self.concept_extractor = ConceptExtractor()
        self.generic_finder = GenericSpaceFinder()
        self.blend_constructor = BlendConstructor()
        self.blend_evaluator = BlendEvaluator()

        # History
        self.blends: List[Blend] = []
        self.blend_counter = 0

    def create_blend(
        self,
        concept_1: str,
        concept_2: str
    ) -> Blend:
        """
        Create conceptual blend from two concepts.

        Returns blend.
        """
        # Extract input spaces
        input_1 = self.concept_extractor.extract_space(concept_1)
        input_2 = self.concept_extractor.extract_space(concept_2)

        # Find generic space
        generic = self.generic_finder.find_generic_space(input_1, input_2)

        # Construct blend
        blended = self.blend_constructor.construct_blend(input_1, input_2, generic)

        # Identify emergent structure
        emergent = self.blend_constructor.identify_emergent_structure(
            blended, input_1, input_2
        )

        # Evaluate blend
        novelty = self.blend_evaluator.evaluate_novelty(blended)
        coherence = self.blend_evaluator.evaluate_coherence(blended)

        # Determine blend type
        if input_1.frame == input_2.frame:
            blend_type = BlendType.MIRROR
        elif blended.frame == input_1.frame or blended.frame == input_2.frame:
            blend_type = BlendType.SINGLE_SCOPE
        else:
            blend_type = BlendType.DOUBLE_SCOPE

        # Create blend record
        blend = Blend(
            blend_id=f"blend_{self.blend_counter:03d}",
            input_1=input_1,
            input_2=input_2,
            generic=generic,
            blended=blended,
            blend_type=blend_type,
            emergent_properties=emergent,
            compression_type="relation",
            novelty_score=novelty,
            coherence_score=coherence,
            timestamp=time.time()
        )

        self.blends.append(blend)
        self.blend_counter += 1

        return blend

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        if not self.blends:
            return {
                "total_blends": 0,
                "avg_novelty": 0.0,
                "avg_coherence": 0.0,
            }

        return {
            "total_blends": len(self.blends),
            "avg_novelty": np.mean([b.novelty_score for b in self.blends]),
            "avg_coherence": np.mean([b.coherence_score for b in self.blends]),
            "blend_types": {bt.value: sum(1 for b in self.blends if b.blend_type == bt)
                           for bt in BlendType},
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_030: Conceptual Blending - Test")
    print("=" * 60)

    system = ConceptualBlendingSystem()

    # Scenario 1: Classic houseboat blend
    print("\n🏠⛵ Scenario 1: House + Boat = Houseboat...")
    blend = system.create_blend("house", "boat")

    print(f"  Blend ID: {blend.blend_id}")
    print(f"  Blend type: {blend.blend_type.value}")
    print(f"  Blended concept: {list(blend.blended.concepts)[0]}")
    print(f"  Novelty: {blend.novelty_score:.3f}")
    print(f"  Coherence: {blend.coherence_score:.3f}")

    print(f"\n  Input 1 (house) properties:")
    for concept, props in blend.input_1.properties.items():
        print(f"    {concept}: {', '.join(sorted(props))}")

    print(f"\n  Input 2 (boat) properties:")
    for concept, props in blend.input_2.properties.items():
        print(f"    {concept}: {', '.join(sorted(props))}")

    print(f"\n  Blended properties:")
    for concept, props in blend.blended.properties.items():
        print(f"    {concept}: {', '.join(sorted(props))}")

    print(f"\n  Emergent structure: {', '.join(sorted(blend.emergent_properties))}")

    # Scenario 2: Computer virus blend
    print("\n💻🦠 Scenario 2: Computer + Virus = Computer Virus...")
    blend2 = system.create_blend("computer", "virus")

    print(f"  Blended concept: {list(blend2.blended.concepts)[0]}")
    print(f"  Blend type: {blend2.blend_type.value}")
    print(f"  Emergent properties: {', '.join(sorted(blend2.emergent_properties))}")
    print(f"  Novelty: {blend2.novelty_score:.3f}")
    print(f"  Coherence: {blend2.coherence_score:.3f}")

    # Scenario 3: Surgeon general blend
    print("\n⚕️⭐ Scenario 3: Surgeon + General = Surgeon General...")
    blend3 = system.create_blend("surgeon", "general")

    print(f"  Blended concept: {list(blend3.blended.concepts)[0]}")
    print(f"  Generic space structure: {blend3.generic.abstract_structure}")
    print(f"  Emergent properties: {', '.join(sorted(blend3.emergent_properties))}")

    # Show combined properties
    surgeon_props = blend3.input_1.properties.get("surgeon", set())
    general_props = blend3.input_2.properties.get("general", set())
    print(f"\n  Surgeon properties: {', '.join(sorted(surgeon_props))}")
    print(f"  General properties: {', '.join(sorted(general_props))}")
    print(f"  Result: Authority combining {', '.join(sorted(blend3.emergent_properties))}")

    # Final statistics
    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    print(f"  Total blends: {stats['total_blends']}")
    print(f"  Average novelty: {stats['avg_novelty']:.3f}")
    print(f"  Average coherence: {stats['avg_coherence']:.3f}")
    print(f"  Blend types: {stats['blend_types']}")

    print("\n✅ LAB_030 Test Complete!")

"""
LAB_032: Analogical Reasoning - Structural Mapping and Transfer

Implements analogical reasoning and transfer:
- Gentner (1983): Structure-mapping theory
- Holyoak & Thagard (1989): Analogical mapping by constraint satisfaction
- Gick & Holyoak (1980): Analogical problem solving
- Forbus et al. (2017): Extending SME to handle large-scale analogies

Core Functions:
1. Structural representation of source and target
2. Similarity computation (surface vs structural)
3. Mapping construction (align relations)
4. Inference projection (transfer knowledge)
5. Evaluation of mapping quality
6. Analogical retrieval from memory

Neuroscience Foundation:
- Prefrontal cortex: Relational reasoning
- Posterior parietal: Spatial analogies
- Hippocampus: Relational memory
- Rostrolateral PFC: Integration of relations

Integration:
- ← LAB_011 (Working Memory) for holding mappings
- ← LAB_031 (Insight) for analogical insight
- → LAB_033 (Metaphor) for metaphorical mapping
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class RelationType(Enum):
    """Types of relations"""
    CAUSE = "cause"
    PART_OF = "part_of"
    ABOVE = "above"
    LARGER_THAN = "larger_than"
    SIMILAR_TO = "similar_to"
    ENABLE = "enable"
    PREVENT = "prevent"


@dataclass
class Entity:
    """Entity in analogy"""
    entity_id: str
    attributes: Set[str]
    entity_type: str  # "object", "agent", "concept"


@dataclass
class Relation:
    """Relation between entities"""
    relation_type: RelationType
    args: Tuple[str, ...]  # Entity IDs


@dataclass
class Structure:
    """Structured representation (source or target)"""
    structure_id: str
    entities: Dict[str, Entity]
    relations: List[Relation]
    higher_order: List[Relation]  # Relations between relations


@dataclass
class Mapping:
    """Mapping from source to target"""
    mapping_id: str
    source: Structure
    target: Structure
    entity_mappings: Dict[str, str]  # source_id -> target_id
    relation_mappings: List[Tuple[Relation, Relation]]  # (source_rel, target_rel)
    structural_similarity: float  # 0-1
    surface_similarity: float  # 0-1
    systematicity: float  # 0-1 (depth of relational structure)
    inferences: List[Relation]  # Projected to target


class StructureExtractor:
    """Extracts structured representations"""

    def __init__(self):
        # Example structures (knowledge base)
        self.structures_kb = {
            "solar_system": {
                "entities": {
                    "sun": {"type": "object", "attrs": {"massive", "hot", "central"}},
                    "earth": {"type": "object", "attrs": {"small", "orbiting"}},
                    "mars": {"type": "object", "attrs": {"small", "orbiting"}},
                },
                "relations": [
                    (RelationType.CAUSE, ("sun", "earth")),  # sun attracts earth
                    (RelationType.CAUSE, ("sun", "mars")),
                    (RelationType.LARGER_THAN, ("sun", "earth")),
                ],
            },
            "atom": {
                "entities": {
                    "nucleus": {"type": "object", "attrs": {"massive", "charged", "central"}},
                    "electron1": {"type": "object", "attrs": {"small", "orbiting"}},
                    "electron2": {"type": "object", "attrs": {"small", "orbiting"}},
                },
                "relations": [
                    (RelationType.CAUSE, ("nucleus", "electron1")),
                    (RelationType.CAUSE, ("nucleus", "electron2")),
                    (RelationType.LARGER_THAN, ("nucleus", "electron1")),
                ],
            },
        }

    def extract_structure(self, structure_name: str) -> Structure:
        """Extract structure from knowledge base"""
        if structure_name not in self.structures_kb:
            return Structure(
                structure_id=structure_name,
                entities={},
                relations=[],
                higher_order=[]
            )

        kb = self.structures_kb[structure_name]

        # Create entities
        entities = {}
        for ent_id, ent_data in kb["entities"].items():
            entities[ent_id] = Entity(
                entity_id=ent_id,
                attributes=ent_data["attrs"],
                entity_type=ent_data["type"]
            )

        # Create relations
        relations = []
        for rel_type, args in kb["relations"]:
            relations.append(Relation(
                relation_type=rel_type,
                args=args
            ))

        return Structure(
            structure_id=structure_name,
            entities=entities,
            relations=relations,
            higher_order=[]
        )


class SimilarityComputer:
    """Computes similarity between structures"""

    def __init__(self):
        pass

    def compute_surface_similarity(
        self,
        source: Structure,
        target: Structure
    ) -> float:
        """
        Compute surface (attribute) similarity.

        Returns similarity score (0-1).
        """
        # Count matching attributes
        source_attrs = set()
        for entity in source.entities.values():
            source_attrs.update(entity.attributes)

        target_attrs = set()
        for entity in target.entities.values():
            target_attrs.update(entity.attributes)

        if not source_attrs or not target_attrs:
            return 0.0

        # Jaccard similarity
        intersection = len(source_attrs.intersection(target_attrs))
        union = len(source_attrs.union(target_attrs))

        return intersection / union if union > 0 else 0.0

    def compute_structural_similarity(
        self,
        source: Structure,
        target: Structure,
        mapping: Dict[str, str]
    ) -> float:
        """
        Compute structural (relational) similarity.

        Higher score for matching relations.

        Returns similarity score (0-1).
        """
        # Count aligned relations
        aligned = 0
        total = max(len(source.relations), len(target.relations))

        if total == 0:
            return 0.0

        for source_rel in source.relations:
            # Check if this relation maps to target
            for target_rel in target.relations:
                if source_rel.relation_type == target_rel.relation_type:
                    # Check if arguments map
                    source_args = source_rel.args
                    target_args = target_rel.args

                    if len(source_args) == len(target_args):
                        args_match = all(
                            mapping.get(source_args[i]) == target_args[i]
                            for i in range(len(source_args))
                            if source_args[i] in mapping
                        )

                        if args_match:
                            aligned += 1
                            break

        return aligned / total if total > 0 else 0.0


class MappingConstructor:
    """Constructs mappings using structure-mapping"""

    def __init__(self):
        self.similarity_computer = SimilarityComputer()

    def construct_mapping(
        self,
        source: Structure,
        target: Structure
    ) -> Mapping:
        """
        Construct mapping from source to target.

        Uses greedy structure-mapping algorithm.

        Returns mapping.
        """
        # Initialize entity mappings (greedy)
        entity_mappings = {}

        source_ents = list(source.entities.values())
        target_ents = list(target.entities.values())

        # Match entities by type and attributes
        for s_ent in source_ents:
            best_match = None
            best_score = 0.0

            for t_ent in target_ents:
                if t_ent.entity_id in entity_mappings.values():
                    continue  # Already mapped

                # Score match
                score = 0.0

                # Type match
                if s_ent.entity_type == t_ent.entity_type:
                    score += 0.5

                # Attribute overlap
                attr_overlap = len(s_ent.attributes.intersection(t_ent.attributes))
                attr_total = len(s_ent.attributes.union(t_ent.attributes))
                if attr_total > 0:
                    score += 0.5 * (attr_overlap / attr_total)

                if score > best_score:
                    best_score = score
                    best_match = t_ent

            if best_match:
                entity_mappings[s_ent.entity_id] = best_match.entity_id

        # Map relations
        relation_mappings = []

        for s_rel in source.relations:
            for t_rel in target.relations:
                if s_rel.relation_type == t_rel.relation_type:
                    # Check if args map
                    if len(s_rel.args) == len(t_rel.args):
                        args_map = all(
                            entity_mappings.get(s_rel.args[i]) == t_rel.args[i]
                            for i in range(len(s_rel.args))
                            if s_rel.args[i] in entity_mappings
                        )

                        if args_map:
                            relation_mappings.append((s_rel, t_rel))
                            break

        # Compute similarities
        surface_sim = self.similarity_computer.compute_surface_similarity(source, target)
        structural_sim = self.similarity_computer.compute_structural_similarity(
            source, target, entity_mappings
        )

        # Systematicity (depth of relational structure)
        systematicity = len(relation_mappings) / max(len(source.relations), 1)

        # Generate inferences (project unmapped source relations)
        inferences = []
        for s_rel in source.relations:
            # Check if mapped
            mapped = any(s_rel == s for s, t in relation_mappings)

            if not mapped:
                # Project to target
                if all(arg in entity_mappings for arg in s_rel.args):
                    target_args = tuple(entity_mappings[arg] for arg in s_rel.args)
                    inferred_rel = Relation(
                        relation_type=s_rel.relation_type,
                        args=target_args
                    )
                    inferences.append(inferred_rel)

        mapping = Mapping(
            mapping_id=f"map_{source.structure_id}_to_{target.structure_id}",
            source=source,
            target=target,
            entity_mappings=entity_mappings,
            relation_mappings=relation_mappings,
            structural_similarity=structural_sim,
            surface_similarity=surface_sim,
            systematicity=systematicity,
            inferences=inferences
        )

        return mapping


class AnalogicalReasoningSystem:
    """
    Main LAB_032 implementation.

    Manages:
    - Structure extraction
    - Similarity computation
    - Mapping construction
    - Inference projection
    """

    def __init__(self):
        # Components
        self.structure_extractor = StructureExtractor()
        self.mapping_constructor = MappingConstructor()

        # History
        self.mappings: List[Mapping] = []

    def create_analogy(
        self,
        source_name: str,
        target_name: str
    ) -> Mapping:
        """
        Create analogy from source to target.

        Returns mapping.
        """
        # Extract structures
        source = self.structure_extractor.extract_structure(source_name)
        target = self.structure_extractor.extract_structure(target_name)

        # Construct mapping
        mapping = self.mapping_constructor.construct_mapping(source, target)

        self.mappings.append(mapping)

        return mapping

    def evaluate_mapping_quality(self, mapping: Mapping) -> float:
        """
        Evaluate overall mapping quality.

        Good mappings: high structural similarity, high systematicity

        Returns quality score (0-1).
        """
        # Weight structural over surface
        quality = 0.6 * mapping.structural_similarity + \
                 0.3 * mapping.systematicity + \
                 0.1 * mapping.surface_similarity

        return quality

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        if not self.mappings:
            return {
                "total_mappings": 0,
                "avg_structural_sim": 0.0,
                "avg_surface_sim": 0.0,
                "avg_systematicity": 0.0,
            }

        return {
            "total_mappings": len(self.mappings),
            "avg_structural_sim": np.mean([m.structural_similarity for m in self.mappings]),
            "avg_surface_sim": np.mean([m.surface_similarity for m in self.mappings]),
            "avg_systematicity": np.mean([m.systematicity for m in self.mappings]),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_032: Analogical Reasoning - Test")
    print("=" * 60)

    system = AnalogicalReasoningSystem()

    # Scenario 1: Classic solar system / atom analogy
    print("\n☀️⚛️ Scenario 1: Solar System → Atom Analogy...")
    mapping = system.create_analogy("solar_system", "atom")

    print(f"  Mapping: {mapping.source.structure_id} → {mapping.target.structure_id}")
    print(f"\n  Entity Mappings:")
    for source_id, target_id in mapping.entity_mappings.items():
        print(f"    {source_id} → {target_id}")

    print(f"\n  Relation Mappings ({len(mapping.relation_mappings)}):")
    for s_rel, t_rel in mapping.relation_mappings:
        print(f"    {s_rel.relation_type.value}({', '.join(s_rel.args)}) → "
              f"{t_rel.relation_type.value}({', '.join(t_rel.args)})")

    print(f"\n  Similarities:")
    print(f"    Surface similarity: {mapping.surface_similarity:.3f}")
    print(f"    Structural similarity: {mapping.structural_similarity:.3f}")
    print(f"    Systematicity: {mapping.systematicity:.3f}")

    # Evaluate quality
    quality = system.evaluate_mapping_quality(mapping)
    print(f"    Overall quality: {quality:.3f}")

    # Show inferences
    print(f"\n  Inferences (projected to target): {len(mapping.inferences)}")
    for inference in mapping.inferences:
        print(f"    {inference.relation_type.value}({', '.join(inference.args)})")

    # Scenario 2: Examining source structure
    print(f"\n🔍 Scenario 2: Examining source structure (solar_system)...")
    source_structure = mapping.source
    print(f"  Entities ({len(source_structure.entities)}):")
    for ent_id, entity in source_structure.entities.items():
        print(f"    {ent_id}: type={entity.entity_type}, attrs={entity.attributes}")

    print(f"\n  Relations ({len(source_structure.relations)}):")
    for rel in source_structure.relations:
        print(f"    {rel.relation_type.value}({', '.join(rel.args)})")

    # Scenario 3: Examining target structure
    print(f"\n🔍 Scenario 3: Examining target structure (atom)...")
    target_structure = mapping.target
    print(f"  Entities ({len(target_structure.entities)}):")
    for ent_id, entity in target_structure.entities.items():
        print(f"    {ent_id}: type={entity.entity_type}, attrs={entity.attributes}")

    print(f"\n  Relations ({len(target_structure.relations)}):")
    for rel in target_structure.relations:
        print(f"    {rel.relation_type.value}({', '.join(rel.args)})")

    # Final statistics
    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_032 Test Complete!")

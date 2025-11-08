"""
LAB_026: Dream Logic

Function: Unconstrained association, surreal combinations (REM-like)
Neuroscience Basis: REM sleep, reduced dorsolateral prefrontal cortex activity

Key Papers:
- Hobson & McCarley (1977) - Activation-synthesis hypothesis
- Stickgold et al. (2000) - Sleep, learning, and dreams: offline memory reprocessing
"""

from typing import Dict, List, Tuple
import random


class DreamLogicSystem:
    """
    LAB_026: Dream Logic

    Models dream-like cognition through:
    - Suspended logical constraints
    - Emotion-driven associations (LAB_001)
    - Bizarre/surreal combinations
    - Offline memory consolidation (LAB_003)
    - Novel connection extraction

    Parameters:
    -----------
    logical_constraint_strength : float
        0 = pure dream logic, 1 = awake logic (default: 0.1)
    emotional_connection_weight : float
        Weight for emotion-driven associations (default: 0.8)
    bizarreness_tolerance : float
        Tolerance for contradictions/impossibilities (default: 0.9)
    consolidation_rate : float
        Memory strengthening rate during consolidation (default: 0.05)
    """

    def __init__(
        self,
        logical_constraint_strength: float = 0.1,
        emotional_connection_weight: float = 0.8,
        bizarreness_tolerance: float = 0.9,
        consolidation_rate: float = 0.05
    ):
        # Configuration
        self.logical_constraint_strength = logical_constraint_strength
        self.emotional_connection_weight = emotional_connection_weight
        self.bizarreness_tolerance = bizarreness_tolerance
        self.consolidation_rate = consolidation_rate

        # State
        self.total_dream_sessions: int = 0
        self.novel_connections_found: int = 0
        self.avg_bizarreness: float = 0.0

    def suspend_logical_constraints(self) -> float:
        """
        Reduce logical consistency checking

        Dream state = low prefrontal control
        Returns current constraint strength (low = dream-like)

        Returns:
        --------
        constraint_level : float
            Current logical constraint strength (0-1)
        """
        return self.logical_constraint_strength

    def associate_by_emotion(self, memories: List[Dict]) -> List[Tuple]:
        """
        Connect memories by emotional similarity (not semantic)

        Integration with LAB_001 (Emotional Salience)
        REM sleep: emotion > logic

        Parameters:
        -----------
        memories : List[Dict]
            Memories with emotion tags

        Returns:
        --------
        associations : List[Tuple]
            Pairs: (mem_a, mem_b, similarity)
        """
        if len(memories) < 2:
            return []

        associations = []

        # Find pairs with similar emotions
        for i in range(len(memories)):
            for j in range(i + 1, len(memories)):
                mem_a = memories[i]
                mem_b = memories[j]

                emotion_a = mem_a.get("emotion", "neutral")
                emotion_b = mem_b.get("emotion", "neutral")

                # Compute emotional similarity
                if emotion_a == emotion_b:
                    # Same emotion = high similarity
                    similarity = 0.9 + random.random() * 0.1
                elif self._emotions_compatible(emotion_a, emotion_b):
                    # Compatible emotions = medium similarity
                    similarity = 0.5 + random.random() * 0.3
                else:
                    # Opposite emotions = low/no similarity
                    similarity = 0.0 + random.random() * 0.2

                # Apply emotional connection weight
                similarity *= self.emotional_connection_weight

                # Only keep strong emotional connections
                if similarity > 0.5:
                    associations.append((mem_a, mem_b, similarity))

        return associations

    def generate_bizarre_combination(self, fragments: List[Dict]) -> Dict:
        """
        Mix unrelated elements, allow contradictions

        Low logical constraints = high bizarreness

        Parameters:
        -----------
        fragments : List[Dict]
            Memory fragments to combine

        Returns:
        --------
        narrative : Dict
            Bizarre/surreal combination
        """
        if len(fragments) == 0:
            return {"elements": [], "narrative": "empty", "contradiction_count": 0}

        # Combine all fragments
        narrative = {
            "elements": fragments.copy(),
            "narrative": " + ".join([f.get("content", "unknown") for f in fragments]),
            "contradiction_count": 0
        }

        # Count contradictions (simulated)
        # Look for contradictory pairs
        contradictory_keywords = [
            ("underwater", "fire"),
            ("square", "circle"),
            ("dry", "water"),
            ("hot", "cold"),
            ("up", "down")
        ]

        content_combined = " ".join([f.get("content", "") for f in fragments]).lower()

        for (keyword_a, keyword_b) in contradictory_keywords:
            if keyword_a in content_combined and keyword_b in content_combined:
                narrative["contradiction_count"] += 1

        # Allow contradictions based on constraint strength
        # Low constraint = keep contradictions
        # High constraint = filter out contradictions
        if self.logical_constraint_strength > 0.5:
            # Wake logic: reduce contradictions
            narrative["contradiction_count"] = int(
                narrative["contradiction_count"] * (1.0 - self.logical_constraint_strength)
            )

        return narrative

    def offline_consolidation(self, memories: List[Dict]) -> List[Dict]:
        """
        Offline memory consolidation during sleep

        Integration with LAB_003 (Sleep Consolidation)
        Reactivate, recombine, strengthen connections

        Parameters:
        -----------
        memories : List[Dict]
            Memories to consolidate

        Returns:
        --------
        consolidated : List[Dict]
            Strengthened/reorganized memories
        """
        consolidated = []

        for mem in memories:
            # Copy memory
            consolidated_mem = mem.copy()

            # Strengthen based on consolidation rate
            if "strength" in consolidated_mem:
                consolidated_mem["strength"] += self.consolidation_rate
                # Cap at 1.0
                consolidated_mem["strength"] = min(1.0, consolidated_mem["strength"])

            # Extract patterns (simulated)
            if "pattern" in mem:
                # Pattern recognition during consolidation
                consolidated_mem["pattern_recognized"] = True

            consolidated.append(consolidated_mem)

        return consolidated

    def score_bizarreness(self, narrative: Dict) -> float:
        """
        Measure surrealism/bizarreness of narrative

        Factors:
        - Contradiction count
        - Unusual combinations
        - Impossibility detection

        Parameters:
        -----------
        narrative : Dict
            Dream narrative

        Returns:
        --------
        bizarreness : float
            Bizarreness score (0-1)
        """
        # Base bizarreness
        bizarreness = 0.3

        # Add bizarreness from contradictions
        contradiction_count = narrative.get("contradiction_count", 0)
        bizarreness += contradiction_count * 0.2

        # Add bizarreness from element count (more elements = more bizarre)
        element_count = len(narrative.get("elements", []))
        bizarreness += min(0.3, element_count * 0.05)

        # Modulate by constraint strength
        # Low constraint = allow high bizarreness
        # High constraint = suppress bizarreness
        bizarreness *= (1.0 - self.logical_constraint_strength * 0.5)

        # Modulate by tolerance
        bizarreness *= self.bizarreness_tolerance

        return max(0.0, min(1.0, bizarreness))

    def extract_novel_connections(self, narrative: Dict) -> List[Tuple]:
        """
        Find new associations created by dream

        Novel connections = creative insights for waking use

        Parameters:
        -----------
        narrative : Dict
            Dream narrative

        Returns:
        --------
        connections : List[Tuple]
            Novel connections: (concept_A, concept_B, strength)
        """
        elements = narrative.get("elements", [])
        associations = narrative.get("associations", [])

        novel_connections = []

        # Extract from explicit associations
        if len(associations) > 0:
            novel_connections.extend(associations)

        # Generate from elements
        if len(elements) >= 2:
            for i in range(len(elements)):
                for j in range(i + 1, len(elements)):
                    concept_a = elements[i].get("content", f"concept_{i}")
                    concept_b = elements[j].get("content", f"concept_{j}")

                    # Compute connection strength (simulated)
                    strength = random.random() * 0.5 + 0.3  # 0.3-0.8

                    novel_connections.append((concept_a, concept_b, strength))

        # Update state
        self.novel_connections_found += len(novel_connections)

        return novel_connections

    def process_event(self, memory_fragments: List[Dict], mode: str = "dream") -> Dict:
        """
        Main processing: generate dream narrative

        Mode:
        - "dream": Low constraints, high bizarreness
        - "wake": Normal logic, low bizarreness

        Parameters:
        -----------
        memory_fragments : List[Dict]
            Memory fragments to process
        mode : str
            "dream" or "wake"

        Returns:
        --------
        result : Dict
            Complete dream logic result
        """
        # 1. Set constraint level based on mode
        if mode == "wake":
            # Temporarily increase constraints
            original_constraint = self.logical_constraint_strength
            self.logical_constraint_strength = 0.8
        else:
            original_constraint = self.logical_constraint_strength

        # 2. Associate by emotion
        associations = self.associate_by_emotion(memory_fragments)

        # 3. Generate bizarre combination
        narrative = self.generate_bizarre_combination(memory_fragments)

        # Add associations to narrative
        narrative["associations"] = associations

        # 4. Score bizarreness
        bizarreness_score = self.score_bizarreness(narrative)

        # 5. Extract novel connections
        novel_connections = self.extract_novel_connections(narrative)

        # 6. Offline consolidation (if dream mode)
        if mode == "dream":
            consolidated_memories = self.offline_consolidation(memory_fragments)
        else:
            consolidated_memories = memory_fragments

        # 7. Update state
        self.total_dream_sessions += 1

        # Update average bizarreness
        n = self.total_dream_sessions
        self.avg_bizarreness = ((self.avg_bizarreness * (n - 1)) + bizarreness_score) / n

        # 8. Restore constraint level
        if mode == "wake":
            self.logical_constraint_strength = original_constraint

        # 9. Extract emotional themes
        emotions = [f.get("emotion", "neutral") for f in memory_fragments]
        emotional_themes = list(set(emotions))

        # 10. Return result
        result = {
            "dream_narrative": narrative.get("narrative", ""),
            "narrative": narrative,
            "memory_fragments_used": len(memory_fragments),
            "emotional_themes": emotional_themes,
            "novel_connections": novel_connections,
            "bizarreness_score": float(bizarreness_score),
            "consolidated_memories": consolidated_memories
        }

        return result

    def get_state(self) -> Dict:
        """Get current dream logic system state"""
        return {
            "total_dream_sessions": int(self.total_dream_sessions),
            "novel_connections_found": int(self.novel_connections_found),
            "avg_bizarreness": float(self.avg_bizarreness),
            "logical_constraint_strength": float(self.logical_constraint_strength),
            "bizarreness_tolerance": float(self.bizarreness_tolerance)
        }

    def _emotions_compatible(self, emotion_a: str, emotion_b: str) -> bool:
        """
        Check if two emotions are compatible (helper)

        Compatible = can coexist in same narrative
        """
        # Compatible pairs
        compatible = [
            ("joy", "love"),
            ("joy", "excitement"),
            ("fear", "anxiety"),
            ("sadness", "nostalgia"),
            ("surprise", "curiosity")
        ]

        # Check both orderings
        for (e1, e2) in compatible:
            if (emotion_a == e1 and emotion_b == e2) or (emotion_a == e2 and emotion_b == e1):
                return True

        return False

"""
LAB_023: Divergent Thinking Engine

Function: Generate multiple creative solutions through remote associations
Neuroscience Basis: Default Mode Network, right hemisphere semantic networks

Key Papers:
- Guilford (1967) - The Nature of Human Intelligence (divergent thinking framework)
- Beaty et al. (2016) - DMN & creativity
"""

from typing import List, Dict
import random
import hashlib


class DivergentThinkingSystem:
    """
    LAB_023: Divergent Thinking Engine

    Generates multiple creative solutions using:
    - Remote semantic associations
    - Inhibition of conventional responses
    - Guilford's metrics (fluency, flexibility, originality)

    Parameters:
    -----------
    semantic_distance_threshold : float
        Minimum distance for "creative" idea (0-1, default: 0.6)
    inhibition_strength : float
        How much to suppress conventional responses (0-1, default: 0.7)
    generation_time : float
        Duration for idea generation in seconds (default: 60.0)
    fluency_weight : float
        Weight for number of ideas in creativity score (default: 0.3)
    flexibility_weight : float
        Weight for category diversity in creativity score (default: 0.4)
    originality_weight : float
        Weight for novelty in creativity score (default: 0.3)
    """

    def __init__(
        self,
        semantic_distance_threshold: float = 0.6,
        inhibition_strength: float = 0.7,
        generation_time: float = 60.0,
        fluency_weight: float = 0.3,
        flexibility_weight: float = 0.4,
        originality_weight: float = 0.3
    ):
        # Configuration
        self.semantic_distance_threshold = semantic_distance_threshold
        self.inhibition_strength = inhibition_strength
        self.generation_time = generation_time
        self.fluency_weight = fluency_weight
        self.flexibility_weight = flexibility_weight
        self.originality_weight = originality_weight

        # State
        self.total_prompts_processed: int = 0
        self.total_ideas_generated: int = 0
        self.avg_fluency: float = 0.0
        self.avg_flexibility: float = 0.0
        self.avg_originality: float = 0.0

    def generate_ideas(self, prompt: str, n_ideas: int = 10) -> List[str]:
        """
        Generate multiple ideas for prompt

        Uses simulated semantic distance (hash-based).
        Production: Use embeddings (Word2Vec, BERT, etc.)

        Parameters:
        -----------
        prompt : str
            Problem/prompt to generate ideas for
        n_ideas : int
            Requested number of ideas (actual may vary)

        Returns:
        --------
        ideas : List[str]
            Generated ideas (filtered by semantic distance)
        """
        if not prompt or len(prompt.strip()) == 0:
            return []

        # Generate candidate ideas (simulated)
        candidates = []
        prompt_words = prompt.lower().split()

        # Strategy 1: Word combinations
        idea_prefixes = [
            "use_as", "combine_with", "repurpose_for", "apply_to",
            "transform_into", "integrate_with", "adapt_for", "reimagine_as"
        ]

        idea_contexts = [
            "tool", "decoration", "game", "art", "science", "education",
            "transportation", "communication", "entertainment", "safety"
        ]

        for prefix in idea_prefixes:
            for context in idea_contexts:
                # Create candidate idea
                candidate = f"{prefix}_{context}"

                # Compute semantic distance (simulated)
                distance = self.compute_semantic_distance(candidate, prompt)

                # Filter by threshold
                if distance >= self.semantic_distance_threshold:
                    candidates.append(candidate)

        # Shuffle and limit
        random.shuffle(candidates)
        ideas = candidates[:n_ideas + random.randint(-3, 3)]  # Variance

        # Ensure no duplicates
        ideas = list(dict.fromkeys(ideas))

        # Apply inhibition to filter conventional responses
        # Low inhibition = keep more ideas (including conventional)
        # High inhibition = filter more aggressively
        if self.inhibition_strength > 0.0:
            filtered_ideas = []
            for idea in ideas:
                # Unconventionality: longer = more unconventional
                # Shorter ideas = conventional (high conventionality score)
                unconventionality = len(idea) / 40.0  # Normalize to 0-1
                unconventionality = min(1.0, unconventionality)

                # Apply inhibition threshold
                # Low inhibition (0.2) → keep if unconventionality > 0.2 (most ideas)
                # High inhibition (0.9) → keep if unconventionality > 0.9 (only very unconventional)
                # Inverted: Keep if (1.0 - unconventionality) < (1.0 - inhibition_strength)
                # Simplifies to: Keep if unconventionality > inhibition_strength
                # But that filters too much. Let's use: keep if passes randomized threshold
                # Actually simpler: inhibition acts as minimum unconventionality required
                threshold = self.inhibition_strength * 0.5  # Scale down for practical filtering
                if unconventionality >= threshold:
                    filtered_ideas.append(idea)
            return filtered_ideas
        else:
            return ideas

    def compute_semantic_distance(self, idea: str, context: str) -> float:
        """
        Compute semantic distance between idea and context

        Simulated: Hash-based distance
        Production: Cosine distance of embeddings

        Parameters:
        -----------
        idea : str
            Candidate idea
        context : str
            Original prompt

        Returns:
        --------
        distance : float
            Semantic distance (0.0 = identical, 1.0 = completely unrelated)
        """
        # Hash both strings
        idea_hash = int(hashlib.md5(idea.encode()).hexdigest(), 16)
        context_hash = int(hashlib.md5(context.encode()).hexdigest(), 16)

        # XOR and normalize
        xor_val = idea_hash ^ context_hash
        distance = (xor_val % 1000) / 1000.0

        return distance

    def inhibit_conventional(self, ideas: List[str], threshold: float) -> List[str]:
        """
        Filter out conventional/obvious responses

        Integration with LAB_019 (Inhibitory Control)

        Parameters:
        -----------
        ideas : List[str]
            All candidate ideas
        threshold : float
            Semantic distance threshold for filtering

        Returns:
        --------
        filtered : List[str]
            Only remote/creative ideas
        """
        # Simulate conventionality score (shorter = more conventional)
        filtered = []
        for idea in ideas:
            conventionality = 1.0 - (len(idea) / 100.0)  # Shorter = conventional
            conventionality = max(0.0, min(1.0, conventionality))

            # Apply inhibition
            if conventionality < (1.0 - self.inhibition_strength):
                filtered.append(idea)

        return filtered

    def score_fluency(self, ideas: List[str]) -> float:
        """
        Guilford's fluency metric: Total number of ideas

        Parameters:
        -----------
        ideas : List[str]
            Generated ideas

        Returns:
        --------
        fluency : float
            Fluency score (number of valid ideas)
        """
        return float(len(ideas))

    def score_flexibility(self, ideas: List[str]) -> float:
        """
        Guilford's flexibility metric: Number of distinct categories

        Simulated: Use word clustering (first 2-3 words or prefix as category)
        Production: Use semantic clustering

        Parameters:
        -----------
        ideas : List[str]
            Generated ideas

        Returns:
        --------
        flexibility : float
            Number of distinct conceptual categories
        """
        if len(ideas) == 0:
            return 0.0

        # Extract categories
        # Strategy: Use LAST word (object/context) as category
        # This captures semantic diversity better than first word (verb)
        categories = set()
        for idea in ideas:
            parts = idea.split("_")
            if len(parts) >= 2:
                # Use last word as category (e.g. "tool", "decoration", "game")
                category = parts[-1]
            elif len(parts) == 1:
                # No underscores: use first 4 chars as category prefix
                category = idea[:4]
            else:
                category = parts[0]

            categories.add(category)

        return float(len(categories))

    def score_originality(self, ideas: List[str]) -> float:
        """
        Guilford's originality metric: Statistical rarity of responses

        Simulated: Longer/more specific = rarer
        Production: Inverse frequency in corpus

        Parameters:
        -----------
        ideas : List[str]
            Generated ideas

        Returns:
        --------
        originality : float
            Average originality (0-1, higher = more novel)
        """
        if len(ideas) == 0:
            return 0.0

        # Simulate rarity: longer/more complex = rarer
        originalities = []
        for idea in ideas:
            # Length-based rarity
            length_score = min(1.0, len(idea) / 50.0)

            # Complexity-based rarity (number of underscores = structure)
            complexity_score = min(1.0, idea.count("_") / 5.0)

            # Combined
            rarity = (length_score * 0.6) + (complexity_score * 0.4)
            originalities.append(rarity)

        return sum(originalities) / len(originalities)

    def compute_creativity_score(
        self,
        fluency: float,
        flexibility: float,
        originality: float
    ) -> float:
        """
        Weighted combination of Guilford's metrics

        Parameters:
        -----------
        fluency : float
            Fluency score
        flexibility : float
            Flexibility score
        originality : float
            Originality score

        Returns:
        --------
        creativity : float
            Combined creativity score (0-1)
        """
        # Normalize fluency and flexibility (typically 0-10+ range)
        fluency_norm = min(1.0, fluency / 10.0)
        flexibility_norm = min(1.0, flexibility / 5.0)

        # Originality already 0-1

        creativity = (
            self.fluency_weight * fluency_norm +
            self.flexibility_weight * flexibility_norm +
            self.originality_weight * originality
        )

        return max(0.0, min(1.0, creativity))

    def modulate_inhibition_by_gaba(self, gaba_level: float) -> float:
        """
        Integration with LAB_017 (GABA/Glutamate)

        Low GABA (high E/I) → reduced inhibition → more ideas

        Parameters:
        -----------
        gaba_level : float
            GABA level from LAB_017 (0-1)

        Returns:
        --------
        modulated_inhibition : float
            Adjusted inhibition strength
        """
        # Inverse relationship: low GABA = low inhibition
        modulated = self.inhibition_strength * gaba_level

        return max(0.0, min(1.0, modulated))

    def apply_inhibitory_control(
        self,
        ideas: List[str],
        control_strength: float
    ) -> List[str]:
        """
        Integration with LAB_019 (Inhibitory Control)

        Suppress conventional responses based on control strength

        Parameters:
        -----------
        ideas : List[str]
            All candidate ideas
        control_strength : float
            Inhibitory control strength from LAB_019 (0-1)

        Returns:
        --------
        filtered : List[str]
            Ideas after inhibitory filtering
        """
        # Higher control = more filtering
        threshold = control_strength * 0.8

        filtered = []
        for idea in ideas:
            # Conventionality score (simulated)
            conventionality = 1.0 - (len(idea) / 80.0)
            conventionality = max(0.0, min(1.0, conventionality))

            # Keep only if passes threshold
            if conventionality < threshold:
                filtered.append(idea)

        return filtered

    def process_event(self, prompt: str) -> Dict:
        """
        Main processing: generate ideas + compute creativity metrics

        Parameters:
        -----------
        prompt : str
            Problem/prompt for idea generation

        Returns:
        --------
        result : Dict
            Complete creativity analysis
        """
        # 1. Generate ideas
        ideas = self.generate_ideas(prompt, n_ideas=10)

        # 2. Score creativity
        fluency = self.score_fluency(ideas)
        flexibility = self.score_flexibility(ideas)
        originality = self.score_originality(ideas)
        creativity = self.compute_creativity_score(fluency, flexibility, originality)

        # 3. Find most novel idea
        most_novel = None
        max_novelty = 0.0

        for idea in ideas:
            # Novelty = length + complexity (simulated)
            novelty = len(idea) / 50.0 + idea.count("_") / 5.0
            if novelty > max_novelty:
                max_novelty = novelty
                most_novel = idea

        # 4. Update state
        self.total_prompts_processed += 1
        self.total_ideas_generated += len(ideas)

        # Update averages
        n = self.total_prompts_processed
        self.avg_fluency = ((self.avg_fluency * (n - 1)) + fluency) / n
        self.avg_flexibility = ((self.avg_flexibility * (n - 1)) + flexibility) / n
        self.avg_originality = ((self.avg_originality * (n - 1)) + originality) / n

        # 5. Return complete result
        return {
            "ideas": ideas,
            "fluency_score": float(fluency),
            "flexibility_score": float(flexibility),
            "originality_score": float(originality),
            "creativity_score": float(creativity),
            "most_novel_idea": most_novel if most_novel else (ideas[0] if ideas else None)
        }

    def get_state(self) -> Dict:
        """Get current divergent thinking system state"""
        return {
            "total_prompts": int(self.total_prompts_processed),
            "total_ideas": int(self.total_ideas_generated),
            "avg_fluency": float(self.avg_fluency),
            "avg_flexibility": float(self.avg_flexibility),
            "avg_originality": float(self.avg_originality),
            "semantic_distance_threshold": float(self.semantic_distance_threshold),
            "inhibition_strength": float(self.inhibition_strength)
        }

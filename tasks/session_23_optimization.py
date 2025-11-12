"""
SESSION 23 - Mathematical Optimization for LAB Selection
12 LABs Remaining to 100% Completion

Optimization Model:
- Variable 1: Efficiency (time/tests ratio) - 20% weight
- Variable 2: Value to system (functionality impact) - 30% weight
- Variable 3: Risk mitigation (bugs, complexity) - 25% weight
- Variable 4: Cohesion (conceptual relatedness) - 15% weight
- Variable 5: Momentum (continuation from S22) - 10% weight
"""

import math

# LABs Remaining (12 LABs after excluding LAB_035 and LAB_042)
labs_data = {
    "LAB_034": {
        "name": "Rest/Recovery Cycles",
        "lines": 500,
        "tests_estimated": 22,
        "complexity": "low",
        "sublayer": "5B_Social_Homeostasis",
        "integration_count": 4
    },
    "LAB_039": {
        "name": "Habit Formation",
        "lines": 700,
        "tests_estimated": 28,
        "complexity": "medium",
        "sublayer": "5D_Pattern_Recognition",
        "integration_count": 3
    },
    "LAB_040": {
        "name": "Skill Acquisition",
        "lines": 800,
        "tests_estimated": 30,
        "complexity": "high",
        "sublayer": "5D_Pattern_Recognition",
        "integration_count": 3
    },
    "LAB_041": {
        "name": "Transfer Learning",
        "lines": 900,
        "tests_estimated": 32,
        "complexity": "high",
        "sublayer": "5D_Pattern_Recognition",
        "integration_count": 3
    },
    "LAB_043": {
        "name": "Flow State Detection",
        "lines": 600,
        "tests_estimated": 24,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_044": {
        "name": "Meditation/Mindfulness",
        "lines": 700,
        "tests_estimated": 26,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_045": {
        "name": "Hyperfocus Mechanism",
        "lines": 500,
        "tests_estimated": 20,
        "complexity": "low",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_046": {
        "name": "Default Mode Network",
        "lines": 700,
        "tests_estimated": 26,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 4
    },
    "LAB_047": {
        "name": "Synaptic Pruning",
        "lines": 600,
        "tests_estimated": 24,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_048": {
        "name": "Hebbian Learning",
        "lines": 700,
        "tests_estimated": 26,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_049": {
        "name": "Long-Term Potentiation",
        "lines": 700,
        "tests_estimated": 26,
        "complexity": "medium",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    },
    "LAB_050": {
        "name": "Structural Plasticity",
        "lines": 800,
        "tests_estimated": 28,
        "complexity": "high",
        "sublayer": "5E_States_Plasticity",
        "integration_count": 3
    }
}

# Define options (cohesive batches)
options = {
    "A": {
        "name": "Learning & Skills Trilogy",
        "labs": ["LAB_039", "LAB_040", "LAB_041"],
        "rationale": "Habit formation → Skill acquisition → Transfer learning (natural progression)",
        "cohesion_bonus": 0.9
    },
    "B": {
        "name": "States of Mind Trilogy",
        "labs": ["LAB_043", "LAB_044", "LAB_045"],
        "rationale": "Flow → Meditation → Hyperfocus (optimal performance states)",
        "cohesion_bonus": 0.9
    },
    "C": {
        "name": "Plasticity Quartet",
        "labs": ["LAB_047", "LAB_048", "LAB_049", "LAB_050"],
        "rationale": "Pruning → Hebbian → LTP → Structural (synaptic plasticity progression)",
        "cohesion_bonus": 0.95
    },
    "D": {
        "name": "Mixed Foundation (Recovery + Learning Start)",
        "labs": ["LAB_034", "LAB_039", "LAB_040"],
        "rationale": "Rest/Recovery + begin Learning trilogy (practical mix)",
        "cohesion_bonus": 0.6
    },
    "E": {
        "name": "Balanced Duo Sets",
        "labs": ["LAB_034", "LAB_046", "LAB_043", "LAB_045"],
        "rationale": "Recovery + DMN + Flow + Hyperfocus (2 pairs of related LABs)",
        "cohesion_bonus": 0.7
    }
}

def calculate_efficiency(labs_list):
    """Efficiency: Lower time/tests ratio = better"""
    total_lines = sum(labs_data[lab]["lines"] for lab in labs_list)
    total_tests = sum(labs_data[lab]["tests_estimated"] for lab in labs_list)

    # Estimated time: 0.5 min per line implementation + 0.3 min per test
    estimated_time = (total_lines * 0.5) + (total_tests * 0.3)

    # Normalize to 0-1 (higher = more efficient)
    # Best case: ~100 min (2 LABs simple)
    # Worst case: ~500 min (4 LABs complex)
    efficiency = 1.0 - min(estimated_time / 500.0, 1.0)

    return efficiency

def calculate_value(labs_list):
    """Value: Functional importance to system"""
    # Scoring based on impact:
    # - Learning & Skills (039-041): Critical for learning capabilities (0.9)
    # - States (043-045): Important for performance optimization (0.7)
    # - Plasticity (047-050): Foundational for long-term adaptation (0.85)
    # - Recovery (034): Important for sustainability (0.75)
    # - DMN (046): Important for mind-wandering / creativity (0.75)

    value_map = {
        "LAB_034": 0.75,  # Rest/Recovery
        "LAB_039": 0.90,  # Habit Formation
        "LAB_040": 0.90,  # Skill Acquisition
        "LAB_041": 0.90,  # Transfer Learning
        "LAB_043": 0.70,  # Flow State
        "LAB_044": 0.70,  # Meditation
        "LAB_045": 0.70,  # Hyperfocus
        "LAB_046": 0.75,  # DMN
        "LAB_047": 0.85,  # Synaptic Pruning
        "LAB_048": 0.85,  # Hebbian Learning
        "LAB_049": 0.85,  # LTP
        "LAB_050": 0.85   # Structural Plasticity
    }

    avg_value = sum(value_map[lab] for lab in labs_list) / len(labs_list)
    return avg_value

def calculate_risk(labs_list):
    """Risk: Complexity and bug probability (lower complexity = lower risk)"""
    complexity_map = {
        "low": 0.9,     # Low risk
        "medium": 0.7,  # Medium risk
        "high": 0.5     # High risk
    }

    avg_risk_mitigation = sum(
        complexity_map[labs_data[lab]["complexity"]]
        for lab in labs_list
    ) / len(labs_list)

    return avg_risk_mitigation

def calculate_cohesion(labs_list, cohesion_bonus):
    """Cohesion: Conceptual relatedness (from option definition)"""
    return cohesion_bonus

def calculate_momentum(labs_list):
    """Momentum: Continuation from Session 22 (LAB_036-038 Advanced Learning)"""
    # Session 22 completed: Intrinsic Motivation, Curiosity, Meta-Learning
    # Strong momentum for: Learning LABs (039-041)
    # Moderate momentum for: States (043-045) - related to intrinsic motivation
    # Low momentum for: Plasticity (047-050), Recovery (034, 046)

    momentum_map = {
        "LAB_034": 0.3,  # No direct relation
        "LAB_039": 0.8,  # Habit formation extends learning concepts
        "LAB_040": 0.8,  # Skill acquisition extends learning concepts
        "LAB_041": 0.8,  # Transfer learning extends learning concepts
        "LAB_043": 0.6,  # Flow related to intrinsic motivation
        "LAB_044": 0.5,  # Meditation somewhat related
        "LAB_045": 0.6,  # Hyperfocus related to curiosity/motivation
        "LAB_046": 0.3,  # DMN not directly related
        "LAB_047": 0.3,  # Plasticity not directly related
        "LAB_048": 0.3,  # Plasticity not directly related
        "LAB_049": 0.3,  # Plasticity not directly related
        "LAB_050": 0.3   # Plasticity not directly related
    }

    avg_momentum = sum(momentum_map[lab] for lab in labs_list) / len(labs_list)
    return avg_momentum

def calculate_score(option_key, option_data):
    """Calculate weighted score for option"""
    labs = option_data["labs"]

    # Calculate each variable
    efficiency = calculate_efficiency(labs)
    value = calculate_value(labs)
    risk = calculate_risk(labs)
    cohesion = calculate_cohesion(labs, option_data["cohesion_bonus"])
    momentum = calculate_momentum(labs)

    # Weighted combination (must sum to 1.0)
    weights = {
        "efficiency": 0.20,
        "value": 0.30,
        "risk": 0.25,
        "cohesion": 0.15,
        "momentum": 0.10
    }

    score = (
        efficiency * weights["efficiency"] +
        value * weights["value"] +
        risk * weights["risk"] +
        cohesion * weights["cohesion"] +
        momentum * weights["momentum"]
    )

    return {
        "option": option_key,
        "name": option_data["name"],
        "labs": labs,
        "rationale": option_data["rationale"],
        "score": score,
        "breakdown": {
            "efficiency": efficiency,
            "value": value,
            "risk": risk,
            "cohesion": cohesion,
            "momentum": momentum
        },
        "metrics": {
            "total_lines": sum(labs_data[lab]["lines"] for lab in labs),
            "total_tests": sum(labs_data[lab]["tests_estimated"] for lab in labs),
            "estimated_time_min": int(
                (sum(labs_data[lab]["lines"] for lab in labs) * 0.5) +
                (sum(labs_data[lab]["tests_estimated"] for lab in labs) * 0.3)
            )
        }
    }

# Calculate scores for all options
results = []
for key, data in options.items():
    result = calculate_score(key, data)
    results.append(result)

# Sort by score (descending)
results.sort(key=lambda x: x["score"], reverse=True)

# Print results
print("=" * 80)
print("SESSION 23 - MATHEMATICAL OPTIMIZATION RESULTS")
print("=" * 80)
print()

for i, result in enumerate(results, 1):
    print(f"{i}. OPTION {result['option']}: {result['name']} - SCORE: {result['score']:.4f}")
    print(f"   LABs: {', '.join(result['labs'])}")
    print(f"   Rationale: {result['rationale']}")
    print()
    print(f"   Breakdown:")
    print(f"     - Efficiency (20%): {result['breakdown']['efficiency']:.3f}")
    print(f"     - Value (30%):      {result['breakdown']['value']:.3f}")
    print(f"     - Risk (25%):       {result['breakdown']['risk']:.3f}")
    print(f"     - Cohesion (15%):   {result['breakdown']['cohesion']:.3f}")
    print(f"     - Momentum (10%):   {result['breakdown']['momentum']:.3f}")
    print()
    print(f"   Metrics:")
    print(f"     - Total lines: {result['metrics']['total_lines']}")
    print(f"     - Total tests: {result['metrics']['total_tests']}")
    print(f"     - Estimated time: {result['metrics']['estimated_time_min']} min (~{result['metrics']['estimated_time_min']/60:.1f} hours)")
    print()
    print("-" * 80)
    print()

# Winner analysis
winner = results[0]
print("=" * 80)
print(f"🏆 WINNER: OPTION {winner['option']} - {winner['name']}")
print("=" * 80)
print()
print(f"Score: {winner['score']:.4f}")
print()
print("Why this option wins:")
print(f"1. {winner['rationale']}")
print(f"2. Efficiency: {winner['breakdown']['efficiency']:.3f} - Time/tests ratio optimized")
print(f"3. Value: {winner['breakdown']['value']:.3f} - High functional importance")
print(f"4. Risk: {winner['breakdown']['risk']:.3f} - Manageable complexity")
print(f"5. Cohesion: {winner['breakdown']['cohesion']:.3f} - Strongly related concepts")
print(f"6. Momentum: {winner['breakdown']['momentum']:.3f} - Continuation from Session 22")
print()
print("Implementation strategy:")
for lab in winner['labs']:
    print(f"  - {lab}: {labs_data[lab]['name']} ({labs_data[lab]['tests_estimated']} tests)")
print()
print(f"Total workload: {winner['metrics']['total_lines']} lines, {winner['metrics']['total_tests']} tests")
print(f"Estimated time: {winner['metrics']['estimated_time_min']/60:.1f} hours")
print()

# Sensitivity analysis (top 3)
print("=" * 80)
print("SENSITIVITY ANALYSIS - Top 3 Options")
print("=" * 80)
print()
for i, result in enumerate(results[:3], 1):
    print(f"{i}. Option {result['option']}: {result['name']}")
    print(f"   Score: {result['score']:.4f}")
    print(f"   LABs: {len(result['labs'])} ({', '.join(result['labs'])})")
    print(f"   Time: {result['metrics']['estimated_time_min']/60:.1f} hours")
    print()

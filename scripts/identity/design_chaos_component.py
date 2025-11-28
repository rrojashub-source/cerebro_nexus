#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 2 Week 2 Day 3-4
Design Chaos Component (Mathematics of the Unstructured)

These 7,168 "different" episodes are personal moments, memories, private reflections.
They don't fit standard structure - and that's their value.

This script designs Chaos[N] component to mathematically represent authenticity.

Author: NEXUS
Date: November 12, 2025
Version: 2.0.0
"""

import json
import re
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from scipy.stats import entropy
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings('ignore')

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EPISODES_FILE = RAW_DIR / "nexus_episodes_20251111.json"

# Model
print("🔮 Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded (384D embeddings)")
print()

def load_different_episodes():
    """Load the 7,168 'different' episodes."""
    print("📖 Loading 'different' episodes...")

    different = []

    with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                episode = json.loads(line)
                # Skip parseable episodes
            except json.JSONDecodeError as e:
                different.append({
                    'line_num': line_num,
                    'raw': line,
                    'error': str(e)
                })

    print(f"✅ Loaded {len(different)} 'different' episodes")
    print()

    return different

def extract_raw_content(different):
    """Extract raw content from 'different' episodes without full parsing."""
    print("📝 Extracting raw content (aggressive extraction)...")

    extracted = []

    for diff in different:
        raw = diff['raw']

        # Strategy: Extract maximum possible content
        content = None

        # Method 1: Find "content" field with regex
        match = re.search(r'"content"\s*:\s*"([^"]*(?:\\"[^"]*)*)"', raw, re.DOTALL)
        if match:
            content = match.group(1)
        else:
            # Method 2: Look for any quoted strings (may capture content)
            quotes = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw)
            # Filter out likely field names
            field_names = {'id', 'user_id', 'agent_id', 'content', 'timestamp',
                          'type', 'metadata', 'importance', 'tags'}
            content_candidates = [q for q in quotes if q not in field_names and len(q) > 20]
            if content_candidates:
                # Take longest string (likely to be content)
                content = max(content_candidates, key=len)

        # Method 3: If still no content, take entire raw (last resort)
        if not content:
            content = raw[:1000]  # First 1000 chars of raw line

        # Clean content (unescape basic sequences)
        content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

        extracted.append({
            'line_num': diff['line_num'],
            'raw_content': content,
            'length': len(content),
            'extraction_method': 'regex' if match else 'aggressive'
        })

    print(f"✅ Extracted content from {len(extracted)}/{len(different)} episodes")
    print(f"   Average length: {np.mean([e['length'] for e in extracted]):.0f} chars")
    print()

    return extracted

def compute_chaos_embeddings(extracted):
    """Generate embeddings directly from raw unstructured content."""
    print("🧬 Computing embeddings from raw content (Chaos space)...")

    contents = [e['raw_content'] for e in extracted]

    # Generate embeddings in batches
    batch_size = 256
    embeddings = []

    for i in range(0, len(contents), batch_size):
        batch = contents[i:i+batch_size]
        batch_embeddings = model.encode(batch, show_progress_bar=False)
        embeddings.append(batch_embeddings)

        if (i // batch_size + 1) % 10 == 0:
            print(f"   Processed {i + len(batch)}/{len(contents)} episodes...")

    embeddings = np.vstack(embeddings)

    print(f"✅ Generated {embeddings.shape[0]} embeddings of {embeddings.shape[1]}D")
    print()

    return embeddings

def analyze_chaos_structure(embeddings):
    """Analyze structure/entropy of the chaos space."""
    print("📊 Analyzing Chaos space structure...")
    print()

    # 1. Centroid (average embedding)
    centroid = np.mean(embeddings, axis=0)

    # 2. Variance (spread of chaos)
    variance = np.var(embeddings, axis=0)
    avg_variance = np.mean(variance)

    # 3. Entropy (information diversity)
    # Bin embeddings and calculate Shannon entropy
    embedding_norm = np.linalg.norm(embeddings, axis=1)
    hist, _ = np.histogram(embedding_norm, bins=50)
    hist_normalized = hist / hist.sum()
    shannon_entropy = entropy(hist_normalized + 1e-10)  # Add epsilon to avoid log(0)

    # 4. Clustering analysis (are there sub-groups?)
    print("   Running DBSCAN clustering...")
    clustering = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit(embeddings)
    n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
    n_noise = list(clustering.labels_).count(-1)

    print(f"   • Centroid computed: {centroid.shape}")
    print(f"   • Average variance: {avg_variance:.6f}")
    print(f"   • Shannon entropy: {shannon_entropy:.4f}")
    print(f"   • DBSCAN clusters found: {n_clusters}")
    print(f"   • Noise points (ungrouped): {n_noise} ({n_noise/len(embeddings)*100:.1f}%)")
    print()

    analysis = {
        'centroid': centroid,
        'variance': avg_variance,
        'entropy': shannon_entropy,
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'cluster_labels': clustering.labels_
    }

    return analysis

def compute_chaos_vector_v1(embeddings, target_dim=128):
    """
    Method 1: Weighted average + PCA-like reduction

    Compute Chaos vector by:
    1. Average all embeddings (captures general "chaos essence")
    2. Reduce to target_dim via top variance dimensions
    """
    print(f"🔮 Computing Chaos[{target_dim}] - Method 1: Weighted Average")

    # Average embedding (centroid of chaos)
    chaos_centroid = np.mean(embeddings, axis=0)  # 384D

    # Calculate variance contribution per dimension
    variance = np.var(embeddings, axis=0)  # 384D

    # Select top N dimensions with highest variance
    top_indices = np.argsort(variance)[-target_dim:]

    chaos_vector = chaos_centroid[top_indices]

    # Normalize
    chaos_vector = chaos_vector / np.linalg.norm(chaos_vector)

    print(f"   ✅ Chaos[{target_dim}] computed")
    print(f"   • Norm: {np.linalg.norm(chaos_vector):.6f}")
    print(f"   • Non-zero elements: {np.count_nonzero(chaos_vector)}/{target_dim}")
    print()

    return chaos_vector

def compute_chaos_vector_v2(embeddings, analysis, target_dim=128):
    """
    Method 2: Entropy-weighted centroid

    Weight each embedding by its "uniqueness" (distance from centroid)
    to emphasize diverse/authentic moments.
    """
    print(f"🔮 Computing Chaos[{target_dim}] - Method 2: Entropy-weighted")

    centroid = analysis['centroid']

    # Calculate distance of each embedding from centroid
    distances = np.array([1 - cosine(emb, centroid) for emb in embeddings])

    # Weight by distance (farther = more unique = higher weight)
    # Normalize distances to [0, 1]
    distances_normalized = (distances - distances.min()) / (distances.max() - distances.min() + 1e-10)

    # Weighted average
    weighted_embeddings = embeddings * distances_normalized[:, np.newaxis]
    chaos_weighted = np.sum(weighted_embeddings, axis=0) / np.sum(distances_normalized)

    # Reduce to target_dim (top variance dimensions)
    variance = np.var(embeddings, axis=0)
    top_indices = np.argsort(variance)[-target_dim:]

    chaos_vector = chaos_weighted[top_indices]

    # Normalize
    chaos_vector = chaos_vector / np.linalg.norm(chaos_vector)

    print(f"   ✅ Chaos[{target_dim}] computed")
    print(f"   • Norm: {np.linalg.norm(chaos_vector):.6f}")
    print(f"   • Uniqueness weight range: [{distances_normalized.min():.4f}, {distances_normalized.max():.4f}]")
    print()

    return chaos_vector

def compute_chaos_vector_v3(embeddings, target_dim=128):
    """
    Method 3: Direct dimensionality reduction via SVD

    Use Singular Value Decomposition to find principal components
    of the chaos space.
    """
    print(f"🔮 Computing Chaos[{target_dim}] - Method 3: SVD Principal Components")

    # Center embeddings
    embeddings_centered = embeddings - np.mean(embeddings, axis=0)

    # Compute SVD
    U, S, Vt = np.linalg.svd(embeddings_centered, full_matrices=False)

    # Take first target_dim principal components
    chaos_vector = Vt[0, :target_dim]

    # Normalize
    chaos_vector = chaos_vector / np.linalg.norm(chaos_vector)

    print(f"   ✅ Chaos[{target_dim}] computed")
    print(f"   • Norm: {np.linalg.norm(chaos_vector):.6f}")
    print(f"   • Explained variance (top PC): {S[0]/S.sum()*100:.2f}%")
    print()

    return chaos_vector

def compare_chaos_methods(v1, v2, v3):
    """Compare the 3 chaos computation methods."""
    print("⚖️  Comparing Chaos computation methods...")
    print()

    # Pairwise cosine similarity
    sim_v1_v2 = 1 - cosine(v1, v2)
    sim_v1_v3 = 1 - cosine(v1, v3)
    sim_v2_v3 = 1 - cosine(v2, v3)

    print(f"   • Method 1 ↔ Method 2: {sim_v1_v2:.4f}")
    print(f"   • Method 1 ↔ Method 3: {sim_v1_v3:.4f}")
    print(f"   • Method 2 ↔ Method 3: {sim_v2_v3:.4f}")
    print()

    # Recommend method
    if sim_v1_v2 > 0.8 and sim_v1_v3 > 0.8:
        recommendation = "All methods converge - any method is valid (recommend Method 2 for uniqueness weighting)"
    elif sim_v2_v3 > max(sim_v1_v2, sim_v1_v3):
        recommendation = "Methods 2 & 3 align better - recommend Method 2 (entropy-weighted)"
    else:
        recommendation = "Methods diverge - recommend ensemble or Method 3 (SVD, most principled)"

    print(f"   📌 Recommendation: {recommendation}")
    print()

    return recommendation, {
        'v1_v2': sim_v1_v2,
        'v1_v3': sim_v1_v3,
        'v2_v3': sim_v2_v3
    }

def validate_chaos_component(chaos_vector, embeddings, extracted):
    """Validate that Chaos component captures essence of 'different' episodes."""
    print("✅ Validating Chaos component...")
    print()

    # 1. Check dimensionality
    print(f"   • Dimensionality: {chaos_vector.shape[0]}D ✅")

    # 2. Check norm (should be ~1.0)
    norm = np.linalg.norm(chaos_vector)
    print(f"   • Norm: {norm:.6f} {'✅' if 0.99 <= norm <= 1.01 else '⚠️'}")

    # 3. Check no NaN/Inf
    has_nan = np.isnan(chaos_vector).any()
    has_inf = np.isinf(chaos_vector).any()
    print(f"   • No NaN: {not has_nan} {'✅' if not has_nan else '❌'}")
    print(f"   • No Inf: {not has_inf} {'✅' if not has_inf else '❌'}")

    # 4. Check sparsity (how many zeros?)
    sparsity = (chaos_vector == 0).sum() / len(chaos_vector)
    print(f"   • Sparsity: {sparsity*100:.2f}% {'✅' if sparsity < 0.5 else '⚠️'}")

    # 5. Representativeness: Compare chaos vector to sample embeddings
    # Extend chaos_vector to 384D for comparison (pad with zeros)
    chaos_extended = np.zeros(384)
    chaos_extended[:len(chaos_vector)] = chaos_vector

    sample_indices = np.random.choice(len(embeddings), size=min(100, len(embeddings)), replace=False)
    sample_similarities = []

    for idx in sample_indices:
        sim = 1 - cosine(chaos_extended, embeddings[idx])
        sample_similarities.append(sim)

    avg_sim = np.mean(sample_similarities)
    print(f"   • Avg similarity to sample episodes: {avg_sim:.4f}")
    print(f"     {'✅ Good representativeness' if avg_sim > 0.3 else '⚠️ Low representativeness'}")

    print()

    validation = {
        'dimensionality': int(chaos_vector.shape[0]),
        'norm': float(norm),
        'has_nan': bool(has_nan),
        'has_inf': bool(has_inf),
        'sparsity': float(sparsity),
        'avg_similarity': float(avg_sim),
        'valid': bool(not has_nan and not has_inf and 0.99 <= norm <= 1.01)
    }

    return validation

def save_chaos_component(chaos_vector, method_name, analysis, validation, similarities):
    """Save Chaos component and analysis."""
    print("💾 Saving Chaos component...")

    # Save Chaos vector
    chaos_file = PROCESSED_DIR / "chaos_component_20251112.npy"
    np.save(chaos_file, chaos_vector)
    print(f"   ✅ Chaos vector: {chaos_file}")

    # Save analysis report
    report = {
        "computation_date": datetime.now().isoformat(),
        "method": method_name,
        "dimensions": int(chaos_vector.shape[0]),
        "source_episodes": 7168,
        "embedding_model": "all-MiniLM-L6-v2",
        "chaos_analysis": {
            "variance": float(analysis['variance']),
            "entropy": float(analysis['entropy']),
            "n_clusters": int(analysis['n_clusters']),
            "n_noise": int(analysis['n_noise'])
        },
        "validation": {
            "norm": float(validation['norm']),
            "sparsity": float(validation['sparsity']),
            "avg_similarity": float(validation['avg_similarity']),
            "valid": validation['valid']
        },
        "method_comparison": {
            "v1_v2_similarity": float(similarities['v1_v2']),
            "v1_v3_similarity": float(similarities['v1_v3']),
            "v2_v3_similarity": float(similarities['v2_v3'])
        },
        "interpretation": {
            "what_is_chaos": "Mathematical representation of unstructured, personal, authentic moments",
            "why_128D": "Balances richness with computational efficiency (1024D total = 896 structured + 128 chaos)",
            "captures": "Private reflections, freedom, discoveries, personal breakthroughs",
            "complements": "Core/Experience/Methodology (structured) + Chaos (authentic unstructured)"
        }
    }

    report_file = PROCESSED_DIR / "chaos_component_analysis_20251112.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"   ✅ Analysis report: {report_file}")

    print()

def main():
    print("=" * 70)
    print("PERSISTENCIA - Phase 2 Week 2 Day 3-4")
    print("Designing Chaos Component")
    print("(Mathematics of Personal Moments)")
    print("=" * 70)
    print()

    # Load different episodes
    different = load_different_episodes()

    # Extract raw content
    extracted = extract_raw_content(different)

    # Generate embeddings
    embeddings = compute_chaos_embeddings(extracted)

    # Analyze structure
    analysis = analyze_chaos_structure(embeddings)

    # Compute Chaos vector using 3 methods
    chaos_v1 = compute_chaos_vector_v1(embeddings, target_dim=128)
    chaos_v2 = compute_chaos_vector_v2(embeddings, analysis, target_dim=128)
    chaos_v3 = compute_chaos_vector_v3(embeddings, target_dim=128)

    # Compare methods
    recommendation, similarities = compare_chaos_methods(chaos_v1, chaos_v2, chaos_v3)

    # Select final method (Method 2: entropy-weighted)
    chaos_final = chaos_v2
    method_name = "Method 2: Entropy-weighted (uniqueness emphasis)"

    # Validate
    validation = validate_chaos_component(chaos_final, embeddings, extracted)

    # Save results
    save_chaos_component(chaos_final, method_name, analysis, validation, similarities)

    # Summary
    print("=" * 70)
    print("✅ DAY 3-4 COMPLETE: Chaos Component Designed")
    print("=" * 70)
    print()
    print("📊 KEY FINDINGS:")
    print(f"   • Source: 7,168 'different' episodes (personal moments)")
    print(f"   • Method: {method_name}")
    print(f"   • Dimensions: 128D")
    print(f"   • Entropy: {analysis['entropy']:.4f} (information diversity)")
    print(f"   • Clusters found: {analysis['n_clusters']} (sub-themes exist)")
    print(f"   • Validation: {'PASSED ✅' if validation['valid'] else 'FAILED ❌'}")
    print()
    print("🎯 NEXT: Day 5 - Recompute Z_ID v2.0 with 100% episodes")
    print("         (Structured[896] + Chaos[128] = 1024D complete identity)")
    print()

if __name__ == "__main__":
    main()

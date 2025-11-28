#!/usr/bin/env python3
"""
AAG+FIRM Production Validation Script

Validates production deployment with 120 real-world queries.

Author: NEXUS
Date: November 12, 2025
Week: 4 Day: 5
"""

import json
import time
import warnings
from pathlib import Path
import numpy as np

from persistencia.memory.retrieval import load_z_id_from_gic
from persistencia.aag.generation import generate_response_with_aag
from persistencia.firm.monitoring import FIRMMonitor
from persistencia.firm.firm_computation import compute_firm, classify_firm_status


# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "validation"
REPORTS_DIR = PROJECT_ROOT / "reports"


def load_queries():
    """Load all validation query datasets."""
    print("📦 Loading query datasets...")

    technical_file = DATA_DIR / "technical_queries.json"
    personal_file = DATA_DIR / "personal_queries.json"
    identity_file = DATA_DIR / "identity_queries.json"

    with open(technical_file, 'r') as f:
        technical = json.load(f)

    with open(personal_file, 'r') as f:
        personal = json.load(f)

    with open(identity_file, 'r') as f:
        identity = json.load(f)

    print(f"  ✅ Technical queries: {len(technical)}")
    print(f"  ✅ Personal queries: {len(personal)}")
    print(f"  ✅ Identity queries: {len(identity)}")
    print(f"  ✅ Total queries: {len(technical) + len(personal) + len(identity)}")
    print()

    return {
        'technical': technical,
        'personal': personal,
        'identity': identity
    }


def run_validation(queries_dict, my_z_id, top_k=20):
    """
    Run validation pipeline on all queries.

    Args:
        queries_dict: Dict with 'technical', 'personal', 'identity' query lists
        my_z_id: Agent Z_ID vector (1024D)
        top_k: Number of episodes to retrieve per query

    Returns:
        dict: Validation results with metrics
    """
    print("🚀 Starting validation pipeline...")
    print(f"   Mode: Production (real memory retrieval)")
    print(f"   Episodes per query: top_k={top_k}")
    print()

    # Initialize FIRM monitor
    firm_monitor = FIRMMonitor(my_z_id, threshold=0.75)

    # Combine all queries with category labels
    all_queries = []
    for category, queries in queries_dict.items():
        for query in queries:
            all_queries.append({'category': category, 'query': query})

    total = len(all_queries)

    # Results storage
    results = []
    errors = []
    firm_errors = []

    # Progress tracking
    start_time = time.time()

    for i, item in enumerate(all_queries):
        category = item['category']
        query = item['query']

        print(f"[{i+1}/{total}] {category[:4].upper()}: {query[:60]}...")

        try:
            # AAG production mode
            aag_start = time.time()
            aag_response = generate_response_with_aag(
                query=query,
                my_z_id=my_z_id,
                mode='production',
                top_k=top_k
            )
            aag_elapsed = time.time() - aag_start

            # FIRM audit (may fail if no external items)
            firm_score = None
            firm_status = None
            firm_error = None

            try:
                firm_start = time.time()
                firm_score = firm_monitor.evaluate(aag_response)
                firm_elapsed = time.time() - firm_start

                firm_status_dict = classify_firm_status(firm_score)
                firm_status = firm_status_dict['status']

            except ValueError as e:
                # Expected in Week 4: no external items
                firm_error = "no_external_items"
                firm_errors.append({
                    'query_id': i,
                    'query': query,
                    'error': str(e)
                })

            # Log result
            results.append({
                'query_id': i,
                'category': category,
                'query': query,
                'aag_stats': aag_response['stats'],
                'aag_latency_ms': aag_elapsed * 1000,
                'firm_score': firm_score,
                'firm_status': firm_status,
                'firm_error': firm_error
            })

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            errors.append({
                'query_id': i,
                'category': category,
                'query': query,
                'error': str(e)
            })

    total_elapsed = time.time() - start_time

    print()
    print(f"✅ Validation complete: {len(results)} queries processed")
    print(f"   Total time: {total_elapsed:.1f}s ({total_elapsed/len(all_queries):.1f}s per query)")
    print(f"   Errors: {len(errors)}")
    print(f"   FIRM errors (expected): {len(firm_errors)}")
    print()

    # Generate metrics
    metrics = generate_metrics(results, errors, firm_errors, firm_monitor, total_elapsed)

    return {
        'results': results,
        'errors': errors,
        'firm_errors': firm_errors,
        'metrics': metrics,
        'total_queries': len(all_queries),
        'success_count': len(results),
        'error_count': len(errors)
    }


def generate_metrics(results, errors, firm_errors, firm_monitor, total_elapsed):
    """Generate comprehensive metrics from validation results."""
    print("📊 Generating metrics...")

    # AAG Metrics
    aag_accept_counts = [r['aag_stats']['n_accepted'] for r in results]
    aag_attribute_counts = [r['aag_stats']['n_attributed'] for r in results]
    aag_reject_counts = [r['aag_stats']['n_rejected'] for r in results]

    total_items = sum(aag_accept_counts) + sum(aag_attribute_counts) + sum(aag_reject_counts)

    aag_metrics = {
        'total_queries': len(results),
        'total_items_processed': total_items,
        'accept_rate': sum(aag_accept_counts) / total_items if total_items > 0 else 0,
        'attribute_rate': sum(aag_attribute_counts) / total_items if total_items > 0 else 0,
        'reject_rate': sum(aag_reject_counts) / total_items if total_items > 0 else 0,
        'avg_items_per_query': total_items / len(results) if results else 0,
        'latency_p50': float(np.percentile([r['aag_latency_ms'] for r in results], 50)) if results else 0,
        'latency_p95': float(np.percentile([r['aag_latency_ms'] for r in results], 95)) if results else 0,
        'latency_p99': float(np.percentile([r['aag_latency_ms'] for r in results], 99)) if results else 0
    }

    # FIRM Metrics (from monitor)
    firm_report = firm_monitor.report(window=len(results))

    firm_metrics = {
        'mean_firm': firm_report['mean_firm'],
        'median_firm': float(np.median([r['firm_score'] for r in results if r['firm_score'] is not None])) if any(r['firm_score'] is not None for r in results) else None,
        'std_firm': firm_report['std_firm'],
        'trend': firm_report['trend'],
        'alert_count': firm_report['alert_count'],
        'no_external_count': len(firm_errors)  # Week 4: Expected
    }

    # Performance Metrics
    performance_metrics = {
        'total_duration_sec': total_elapsed,
        'queries_per_sec': len(results) / total_elapsed if total_elapsed > 0 else 0,
        'avg_aag_latency_ms': aag_metrics['latency_p50'],
        'error_count': len(errors),
        'error_rate': len(errors) / (len(results) + len(errors)) if (len(results) + len(errors)) > 0 else 0
    }

    # Category breakdown
    category_metrics = {}
    for category in ['technical', 'personal', 'identity']:
        category_results = [r for r in results if r['category'] == category]
        if category_results:
            category_accept = sum(r['aag_stats']['n_accepted'] for r in category_results)
            category_total = sum(r['aag_stats']['n_accepted'] + r['aag_stats']['n_attributed'] + r['aag_stats']['n_rejected'] for r in category_results)

            category_metrics[category] = {
                'queries': len(category_results),
                'accept_rate': category_accept / category_total if category_total > 0 else 0,
                'avg_latency_ms': float(np.mean([r['aag_latency_ms'] for r in category_results]))
            }

    print(f"  ✅ AAG metrics computed")
    print(f"  ✅ FIRM metrics computed")
    print(f"  ✅ Performance metrics computed")
    print()

    return {
        'aag': aag_metrics,
        'firm': firm_metrics,
        'performance': performance_metrics,
        'by_category': category_metrics
    }


def save_results(validation_data, output_file):
    """Save validation results to JSON file."""
    print(f"💾 Saving results to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(validation_data, f, indent=2, default=str)

    print(f"  ✅ Results saved ({output_file.stat().st_size / 1024:.1f} KB)")
    print()


def main():
    print("=" * 70)
    print("AAG+FIRM PRODUCTION VALIDATION")
    print("Week 4 - Real Memory Integration")
    print("=" * 70)
    print()

    # Load Z_ID
    print("🧠 Loading agent Z_ID from GIC...")
    my_z_id = load_z_id_from_gic(agent_id='nexus')
    print(f"  ✅ Z_ID loaded: {my_z_id.shape}")
    print()

    # Load queries
    queries_dict = load_queries()

    # Run validation
    validation_data = run_validation(queries_dict, my_z_id, top_k=20)

    # Save results
    output_file = REPORTS_DIR / f"validation_results_{int(time.time())}.json"
    save_results(validation_data, output_file)

    # Print summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total queries: {validation_data['total_queries']}")
    print(f"Success rate: {validation_data['success_count'] / validation_data['total_queries'] * 100:.1f}%")
    print()

    metrics = validation_data['metrics']

    print("AAG Metrics:")
    print(f"  Accept rate: {metrics['aag']['accept_rate']*100:.1f}%")
    print(f"  Attribute rate: {metrics['aag']['attribute_rate']*100:.1f}%")
    print(f"  Reject rate: {metrics['aag']['reject_rate']*100:.1f}%")
    print(f"  Avg latency: {metrics['aag']['latency_p50']:.0f}ms (p50)")
    print()

    print("FIRM Metrics:")
    if metrics['firm']['mean_firm'] > 0:
        print(f"  Mean FIRM: {metrics['firm']['mean_firm']:.3f}")
        print(f"  Trend: {metrics['firm']['trend']}")
    else:
        print(f"  No external items (Week 4 expected): {metrics['firm']['no_external_count']} queries")
    print()

    print("Performance:")
    print(f"  Total time: {metrics['performance']['total_duration_sec']:.1f}s")
    print(f"  Throughput: {metrics['performance']['queries_per_sec']:.2f} queries/sec")
    print()

    print("✅ Validation complete!")
    print()


if __name__ == "__main__":
    main()

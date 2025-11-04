'use client';

import React from 'react';
import { LABStatus as LABStatusType } from '@/lib/types';

const LABS: LABStatusType[] = [
  {
    id: 'LAB_001',
    name: 'Emotional Salience',
    status: 'active',
    description: 'Real emotional scoring for attention',
  },
  {
    id: 'LAB_002',
    name: 'Decay Modulation',
    status: 'active',
    description: 'Intelligent memory decay protection',
  },
  {
    id: 'LAB_003',
    name: 'Sleep Consolidation',
    status: 'active',
    description: 'Offline memory strengthening',
  },
  {
    id: 'LAB_004',
    name: 'Novelty Detection',
    status: 'active',
    description: '4D surprise and curiosity bonus',
  },
  {
    id: 'LAB_005',
    name: 'Spreading Activation',
    status: 'active',
    description: 'Contextual priming and fast retrieval',
  },
  {
    id: 'LAB_006',
    name: 'Metacognition',
    status: 'active',
    description: 'Self-awareness and confidence calibration',
  },
  {
    id: 'LAB_007',
    name: 'Predictive Preloading',
    status: 'active',
    description: 'Anticipate future queries',
  },
  {
    id: 'LAB_008',
    name: 'Emotional Contagion',
    status: 'active',
    description: 'Spread emotional context across memories',
  },
  {
    id: 'LAB_009',
    name: 'Memory Reconsolidation',
    status: 'active',
    description: 'Update memories when recalled',
  },
  {
    id: 'LAB_010',
    name: 'Attention Mechanism',
    status: 'active',
    description: 'Multi-factor selective attention',
  },
  {
    id: 'LAB_011',
    name: 'Working Memory',
    status: 'active',
    description: '7-item buffer (Miller\'s Law)',
  },
  {
    id: 'LAB_012',
    name: 'Future Thinking',
    status: 'active',
    description: 'Simulate episodic futures',
  },
  {
    id: 'LAB_013',
    name: 'Dopamine System',
    status: 'active',
    description: 'RPE, motivation, learning rate modulation',
  },
  {
    id: 'LAB_014',
    name: 'Serotonin System',
    status: 'active',
    description: 'Mood regulation, impulse control, patience',
  },
  {
    id: 'LAB_015',
    name: 'Norepinephrine System',
    status: 'active',
    description: 'Arousal, alertness, stress response',
  },
  {
    id: 'LAB_016',
    name: 'Acetylcholine System',
    status: 'active',
    description: 'Attention focus, encoding/retrieval',
  },
  {
    id: 'LAB_017',
    name: 'GABA/Glutamate Balance',
    status: 'active',
    description: 'E/I homeostasis, oscillations',
  },
  {
    id: 'LAB_018',
    name: 'Working Memory Executive',
    status: 'active',
    description: 'Central executive, dual-task coordination',
  },
  {
    id: 'LAB_019',
    name: 'Cognitive Control',
    status: 'active',
    description: 'Inhibition, shifting, updating',
  },
  {
    id: 'LAB_020',
    name: 'Task Switching',
    status: 'active',
    description: 'Context switching, reconfiguration cost',
  },
  {
    id: 'LAB_021',
    name: 'Planning & Sequencing',
    status: 'active',
    description: 'Goal decomposition, temporal ordering',
  },
  {
    id: 'LAB_022',
    name: 'Goal Management',
    status: 'active',
    description: 'Goal hierarchy, priority, conflict resolution',
  },
  {
    id: 'LAB_023',
    name: 'Theory of Mind',
    status: 'active',
    description: 'Mental state attribution, belief reasoning',
  },
  {
    id: 'LAB_024',
    name: 'Empathy System',
    status: 'active',
    description: 'Emotional resonance, perspective taking',
  },
  {
    id: 'LAB_025',
    name: 'Social Hierarchy',
    status: 'active',
    description: 'Status detection, dominance/submission',
  },
  {
    id: 'LAB_026',
    name: 'Cooperation & Trust',
    status: 'active',
    description: 'Reciprocity, trust building, coalitions',
  },
  {
    id: 'LAB_027',
    name: 'Moral Reasoning',
    status: 'active',
    description: 'Ethical judgments, moral dilemmas',
  },
  {
    id: 'LAB_028',
    name: 'Emotional Intelligence',
    status: 'active',
    description: 'Emotion recognition and regulation',
  },
  {
    id: 'LAB_029',
    name: 'Divergent Thinking',
    status: 'active',
    description: 'Idea generation, fluency, originality',
  },
  {
    id: 'LAB_030',
    name: 'Conceptual Blending',
    status: 'active',
    description: 'Creative concept fusion',
  },
  {
    id: 'LAB_031',
    name: 'Insight/Aha Moments',
    status: 'active',
    description: 'Sudden problem restructuring',
  },
  {
    id: 'LAB_032',
    name: 'Analogical Reasoning',
    status: 'active',
    description: 'Structural mapping and transfer',
  },
  {
    id: 'LAB_033',
    name: 'Metaphor Generation',
    status: 'active',
    description: 'Metaphorical thinking',
  },
  {
    id: 'LAB_034',
    name: 'Transfer Learning',
    status: 'active',
    description: 'Knowledge transfer across domains',
  },
  {
    id: 'LAB_035',
    name: 'Reward Prediction',
    status: 'active',
    description: 'Model-free and model-based RL',
  },
  {
    id: 'LAB_036',
    name: 'Meta-Learning',
    status: 'active',
    description: 'Learning to learn',
  },
  {
    id: 'LAB_037',
    name: 'Curiosity Drive',
    status: 'active',
    description: 'Information-seeking motivation',
  },
  {
    id: 'LAB_038',
    name: 'Intrinsic Motivation',
    status: 'active',
    description: 'Self-determined goals (SDT)',
  },
  {
    id: 'LAB_039',
    name: 'LTP',
    status: 'active',
    description: 'Long-term potentiation',
  },
  {
    id: 'LAB_040',
    name: 'LTD',
    status: 'active',
    description: 'Long-term depression',
  },
  {
    id: 'LAB_041',
    name: 'Hebbian Learning',
    status: 'active',
    description: 'Fire together, wire together',
  },
  {
    id: 'LAB_042',
    name: 'Synaptic Pruning',
    status: 'active',
    description: 'Eliminate weak synapses',
  },
  {
    id: 'LAB_043',
    name: 'Neurogenesis',
    status: 'active',
    description: 'Generate new neurons',
  },
  {
    id: 'LAB_044',
    name: 'Circadian Rhythms',
    status: 'active',
    description: '24-hour biological clock',
  },
  {
    id: 'LAB_045',
    name: 'Energy Management',
    status: 'active',
    description: 'Resource allocation and recovery',
  },
  {
    id: 'LAB_046',
    name: 'Stress Regulation',
    status: 'active',
    description: 'Stress response and recovery',
  },
  {
    id: 'LAB_047',
    name: 'Allostatic Load',
    status: 'active',
    description: 'Cumulative stress burden',
  },
  {
    id: 'LAB_048',
    name: 'Homeostatic Plasticity',
    status: 'active',
    description: 'Maintain neural stability',
  },
  {
    id: 'LAB_049',
    name: 'Sleep Pressure',
    status: 'active',
    description: 'Sleep drive accumulation',
  },
  {
    id: 'LAB_050',
    name: 'Recovery Mechanisms',
    status: 'active',
    description: 'Restoration and repair',
  },
];

export default function LABStatusComponent() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'border-green-500/50 bg-green-500/10';
      case 'warning':
        return 'border-yellow-500/50 bg-yellow-500/10';
      case 'inactive':
        return 'border-red-500/50 bg-red-500/10';
      default:
        return 'border-gray-500/50 bg-gray-500/10';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'inactive':
        return '❌';
      default:
        return '⚪';
    }
  };

  return (
    <div className="bg-nexus-darker rounded-lg border border-nexus-primary/20 p-6">
      <h2 className="text-xl font-semibold text-gray-100 mb-4 flex items-center gap-2">
        <span className="text-green-400">🔬</span>
        LAB Systems Status
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {LABS.map((lab) => (
          <div
            key={lab.id}
            className={`rounded-lg border-2 p-4 transition-all hover:scale-105 ${getStatusColor(lab.status)}`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-mono text-sm text-gray-400">{lab.id}</span>
              <span className="text-2xl">{getStatusIcon(lab.status)}</span>
            </div>
            <h3 className="font-semibold text-gray-100 mb-1">{lab.name}</h3>
            <p className="text-xs text-gray-400">{lab.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

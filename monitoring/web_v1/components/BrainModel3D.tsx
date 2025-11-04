'use client';

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { NexusData } from '@/lib/types';

interface BrainModel3DProps {
  nexusData: NexusData;
}

export default function BrainModel3D({ nexusData }: BrainModel3DProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const labMeshesRef = useRef<{ [key: string]: THREE.Mesh }>({});
  const animationIdRef = useRef<number | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0f);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / 800,
      0.1,
      1000
    );
    camera.position.z = 12;
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(containerRef.current.clientWidth, 800);
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0xffffff, 1);
    pointLight1.position.set(10, 10, 10);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x00d4ff, 0.5);
    pointLight2.position.set(-10, -10, -10);
    scene.add(pointLight2);

    // Central brain structure (wireframe sphere)
    const brainGeometry = new THREE.SphereGeometry(2, 64, 64);
    const brainMaterial = new THREE.MeshBasicMaterial({
      color: 0x1e293b,
      wireframe: true,
      transparent: true,
      opacity: 0.1,
    });
    const brainMesh = new THREE.Mesh(brainGeometry, brainMaterial);
    scene.add(brainMesh);

    // LAB regions configuration - Cognitive Loop Circle (12 LABS)
    const radius = 5;
    const labsConfig = [
      // Main Cognition Loop (outer circle)
      { id: 'LAB_001', position: [radius * Math.cos(0 * Math.PI / 4), radius * Math.sin(0 * Math.PI / 4), 0], color: 0xfbbf24, name: 'Emotional Salience' },
      { id: 'LAB_010', position: [radius * Math.cos(1 * Math.PI / 4), radius * Math.sin(1 * Math.PI / 4), 0], color: 0x3b82f6, name: 'Attention' },
      { id: 'LAB_011', position: [radius * Math.cos(2 * Math.PI / 4), radius * Math.sin(2 * Math.PI / 4), 0], color: 0x8b5cf6, name: 'Working Memory' },
      { id: 'LAB_006', position: [radius * Math.cos(3 * Math.PI / 4), radius * Math.sin(3 * Math.PI / 4), 0], color: 0x06b6d4, name: 'Metacognition' },
      { id: 'LAB_009', position: [radius * Math.cos(4 * Math.PI / 4), radius * Math.sin(4 * Math.PI / 4), 0], color: 0x10b981, name: 'Reconsolidation' },
      { id: 'LAB_007', position: [radius * Math.cos(5 * Math.PI / 4), radius * Math.sin(5 * Math.PI / 4), 0], color: 0xf59e0b, name: 'Preloading' },
      { id: 'LAB_012', position: [radius * Math.cos(6 * Math.PI / 4), radius * Math.sin(6 * Math.PI / 4), 0], color: 0xa78bfa, name: 'Future Think' },
      { id: 'LAB_008', position: [radius * Math.cos(7 * Math.PI / 4), radius * Math.sin(7 * Math.PI / 4), 0], color: 0xec4899, name: 'Contagion' },

      // Support Systems (inner circle)
      { id: 'LAB_002', position: [2.5 * Math.cos(0.5 * Math.PI / 2), 2.5 * Math.sin(0.5 * Math.PI / 2), 1], color: 0x34d399, name: 'Decay Mod' },
      { id: 'LAB_003', position: [2.5 * Math.cos(2.5 * Math.PI / 2), 2.5 * Math.sin(2.5 * Math.PI / 2), 1], color: 0x60a5fa, name: 'Sleep Consol' },
      { id: 'LAB_004', position: [2.5 * Math.cos(4.5 * Math.PI / 2), 2.5 * Math.sin(4.5 * Math.PI / 2), 1], color: 0xf97316, name: 'Novelty' },
      { id: 'LAB_005', position: [2.5 * Math.cos(6.5 * Math.PI / 2), 2.5 * Math.sin(6.5 * Math.PI / 2), 1], color: 0xfbbf24, name: 'Spreading' },
    ];

    // Create LAB spheres
    labsConfig.forEach((lab) => {
      const geometry = new THREE.SphereGeometry(0.8, 32, 32);
      const material = new THREE.MeshStandardMaterial({
        color: lab.color,
        emissive: lab.color,
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.7,
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.set(lab.position[0], lab.position[1], lab.position[2]);
      scene.add(mesh);
      labMeshesRef.current[lab.id] = mesh;

      // Outer glow
      const glowGeometry = new THREE.SphereGeometry(1.0, 32, 32);
      const glowMaterial = new THREE.MeshBasicMaterial({
        color: lab.color,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide,
      });
      const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
      glowMesh.position.set(lab.position[0], lab.position[1], lab.position[2]);
      scene.add(glowMesh);

      // Label (using sprite instead of text for simplicity)
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.width = 256;
      canvas.height = 64;
      if (context) {
        context.fillStyle = '#ffffff';
        context.font = 'Bold 32px Arial';
        context.textAlign = 'center';
        context.fillText(lab.id, 128, 40);
      }
      const texture = new THREE.CanvasTexture(canvas);
      const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
      const sprite = new THREE.Sprite(spriteMaterial);
      sprite.position.set(lab.position[0], lab.position[1] + 1.2, lab.position[2]);
      sprite.scale.set(2, 0.5, 1);
      scene.add(sprite);
    });

    // Neural connections - Cognitive Loop Flow
    const getPosition = (labId: string) => {
      const lab = labsConfig.find(l => l.id === labId);
      return lab ? lab.position : [0, 0, 0];
    };

    const connections = [
      // Main cognition loop (outer circle clockwise)
      { from: getPosition('LAB_001'), to: getPosition('LAB_010'), color: 0x00d4ff, opacity: 0.6 },  // Salience → Attention
      { from: getPosition('LAB_010'), to: getPosition('LAB_011'), color: 0x00d4ff, opacity: 0.6 },  // Attention → Working Memory
      { from: getPosition('LAB_011'), to: getPosition('LAB_006'), color: 0x00d4ff, opacity: 0.6 },  // Working Memory → Metacognition
      { from: getPosition('LAB_006'), to: getPosition('LAB_009'), color: 0x00d4ff, opacity: 0.6 },  // Metacognition → Reconsolidation
      { from: getPosition('LAB_009'), to: getPosition('LAB_007'), color: 0x00d4ff, opacity: 0.6 },  // Reconsolidation → Preloading
      { from: getPosition('LAB_007'), to: getPosition('LAB_012'), color: 0x00d4ff, opacity: 0.6 },  // Preloading → Future Thinking
      { from: getPosition('LAB_012'), to: getPosition('LAB_008'), color: 0x00d4ff, opacity: 0.6 },  // Future Thinking → Contagion
      { from: getPosition('LAB_008'), to: getPosition('LAB_001'), color: 0x00d4ff, opacity: 0.6 },  // Contagion → Salience (closes loop)

      // Support systems connections (inner to outer)
      { from: getPosition('LAB_002'), to: getPosition('LAB_009'), color: 0x34d399, opacity: 0.3 },  // Decay → Reconsolidation
      { from: getPosition('LAB_003'), to: getPosition('LAB_009'), color: 0x60a5fa, opacity: 0.3 },  // Sleep → Reconsolidation
      { from: getPosition('LAB_004'), to: getPosition('LAB_010'), color: 0xf97316, opacity: 0.3 },  // Novelty → Attention
      { from: getPosition('LAB_005'), to: getPosition('LAB_010'), color: 0xfbbf24, opacity: 0.3 },  // Spreading → Attention
    ];

    connections.forEach((conn) => {
      const points = [
        new THREE.Vector3(conn.from[0], conn.from[1], conn.from[2]),
        new THREE.Vector3(conn.to[0], conn.to[1], conn.to[2]),
      ];
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial({
        color: conn.color,
        transparent: true,
        opacity: conn.opacity,
        linewidth: 2,
      });
      const line = new THREE.Line(geometry, material);
      scene.add(line);
    });

    // Background stars
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1 });
    const starsVertices = [];
    for (let i = 0; i < 200; i++) {
      const x = (Math.random() - 0.5) * 50;
      const y = (Math.random() - 0.5) * 50;
      const z = (Math.random() - 0.5) * 50;
      starsVertices.push(x, y, z);
    }
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);

    // Mouse controls
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let rotation = { x: 0, y: 0 };

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;
      rotation.y += deltaX * 0.005;
      rotation.x += deltaY * 0.005;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      camera.position.z += e.deltaY * 0.01;
      camera.position.z = Math.max(5, Math.min(20, camera.position.z));
    };

    renderer.domElement.addEventListener('mousedown', onMouseDown);
    renderer.domElement.addEventListener('mousemove', onMouseMove);
    renderer.domElement.addEventListener('mouseup', onMouseUp);
    renderer.domElement.addEventListener('wheel', onWheel);

    // Animation loop
    let time = 0;
    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);
      time += 0.01;

      // Rotate brain group
      brainMesh.rotation.y = rotation.y + time * 0.1;
      brainMesh.rotation.x = rotation.x;

      // Animate LABs
      Object.values(labMeshesRef.current).forEach((mesh) => {
        const pulse = Math.sin(time * 2) * 0.1;
        mesh.scale.setScalar(1 + pulse * 0.3);
        mesh.rotation.y += 0.002;
      });

      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    return () => {
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      renderer.domElement.removeEventListener('mousedown', onMouseDown);
      renderer.domElement.removeEventListener('mousemove', onMouseMove);
      renderer.domElement.removeEventListener('mouseup', onMouseUp);
      renderer.domElement.removeEventListener('wheel', onWheel);
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Update LAB activities based on nexusData
  useEffect(() => {
    if (!nexusData.consciousness) return;

    const emotional = nexusData.consciousness.emotional;
    const somatic = nexusData.consciousness.somatic;

    // Map consciousness states to LAB activities
    const activities = {
      LAB_001: emotional ? (emotional.joy + emotional.trust + emotional.anticipation) / 3 : 0.5,
      LAB_002: somatic ? somatic.emotional_regulation : 0.5,
      LAB_003: somatic ? (somatic.body_state + somatic.temporal_awareness) / 2 : 0.5,
      LAB_004: emotional ? (emotional.surprise + emotional.anticipation) / 2 : 0.5,
      LAB_005: somatic ? somatic.social_engagement : 0.5,
      LAB_006: somatic ? somatic.cognitive_load : 0.5,
      LAB_007: somatic ? somatic.temporal_awareness : 0.5,
      LAB_008: emotional ? (emotional.joy + emotional.trust) / 2 : 0.5,
      LAB_009: somatic ? somatic.body_state : 0.5,
      LAB_010: somatic ? (somatic.arousal + somatic.cognitive_load) / 2 : 0.5,
      LAB_011: somatic ? somatic.cognitive_load : 0.5,
      LAB_012: emotional ? emotional.anticipation : 0.5,
    };

    Object.entries(activities).forEach(([labId, activity]) => {
      const mesh = labMeshesRef.current[labId];
      if (mesh && mesh.material instanceof THREE.MeshStandardMaterial) {
        mesh.material.emissiveIntensity = activity * 0.5;
      }
    });
  }, [nexusData.consciousness]);

  return (
    <div className="w-full h-[800px] bg-nexus-darker rounded-lg border border-nexus-primary/20 overflow-hidden">
      <div ref={containerRef} className="w-full h-full" />
    </div>
  );
}

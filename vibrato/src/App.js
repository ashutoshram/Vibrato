import logo from './logo.svg';
import './App.css';
import React, {useEffect, useRef} from 'react';
import * as THREE from 'three';
import * as Tone from 'tone';
import {Hands} from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils';

function App() {
  const videoRef = useRef(null);
  
  useEffect(() => {
    // Initialize Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    camera.position.z = 5;

    // Create hand joint spheres
    const geometry = new THREE.SphereGeometry(0.1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const handJoints = [];
    for (let i = 0; i < 21; i++) {
      const sphere = new THREE.Mesh(geometry, material);
      handJoints.push(sphere);
      scene.add(sphere);
    }

    // Initialize Tone.js synth
    const synth = new Tone.Synth().toDestination();

    function playSound() {
      synth.triggerAttackRelease("C4", "8n");
    }

    // Set up MediaPipe Hands
    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });
    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    hands.onResults((results) => {
      if (results.multiHandLandmarks) {
        results.multiHandLandmarks.forEach((landmarks) => {
          for (let i = 0; i < landmarks.length; i++) {
            const { x, y, z } = landmarks[i];
            handJoints[i].position.set(x * 5, -y * 5, -z * 5); // Adjust scaling
          }
        });
        renderer.render(scene, camera);

        // Play sound based on hand position (e.g., index finger tip)
        if (results.multiHandLandmarks && results.multiHandLandmarks[0] && results.multiHandLandmarks[0].length >= 9) {
          const handPos = results.multiHandLandmarks[0][8]; // Index finger tip
          if (handPos.y < 0.5) {
            playSound();
          }
        }
      }
    });

    // Initialize webcam and handle the "play()" and "load()" issue
    const videoElement = videoRef.current;
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        videoElement.srcObject = stream;
        
        // Wait for the video to be loaded and ready before playing it
        videoElement.addEventListener('loadeddata', () => {
          videoElement.play();
        });

        // Start the MediaPipe camera after video is ready
        const camera = new Camera(videoElement, {
          onFrame: async () => {
            await hands.send({ image: videoElement });
          },
          width: 640,
          height: 480,
        });
        camera.start();
      }).catch((err) => {
        console.error('Camera not accessible:', err);
      });
    }
  }, []);

  return (
    <div className="App">
      <video ref={videoRef} style={{ display: 'none' }} />
    </div>
  );
}

export default App;
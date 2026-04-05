# BMS Thermal Tactician v1
**A High-Fidelity Digital Twin Environment for EV Battery Thermal Management**

[![OpenEnv Compliant](https://img.shields.io/badge/OpenEnv-v4--Compliant-green)](https://github.com/openenv/spec)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/Aryan0192/Bms-Thermal-Tactician-V1)

## Overview
BMS Thermal Tactician is a high-fidelity simulation environment designed to train and evaluate AI agents in **Safety-Critical Battery Management Systems (BMS)**. The environment models the thermal dynamics of a Lithium-ion battery pack under variable discharge loads, requiring the agent to maintain optimal temperatures (20°C - 25°C) using active cooling.

This project bridges the gap between Reinforcement Learning and Industrial IoT, focusing on **Thermal Runaway Prevention**—a trillion-dollar challenge in the Electric Vehicle (EV) industry.

---

## Environment Architecture

### 1. Observation Space (`TypedDict`)
The agent receives a real-time telemetry stream:
* `battery_temp` (float): Current core temperature in Celsius.
* `step_count` (int): The current progress in the mission profile.

### 2. Action Space (`Enum`)
The agent must choose between two discrete thermal management states:
* `FAN_OFF`: Passive dissipation mode (Conserves power).
* `FAN_ON`: Active convection cooling (High power draw, rapid cooling).

### 3. Reward Function (Safety-First)
* **Progressive Reward (+1.0):** Awarded for every step maintained within the safe operating window (20.0°C - 29.9°C).
* **Critical Failure (-50.0):** Immediate episode termination if temperature exceeds **30.0°C**, simulating a potential Thermal Runaway event.

---

## Hybrid XAI Baseline
The included `inference.py` demonstrates a **SRE-Compliant Hybrid Architecture**:
1. **Deterministic Guardrails:** Hard-coded safety logic to ensure 0% failure rates.
2. **eXplainable AI (XAI):** Real-time LLM diagnostics that provide a 10-word technical justification for every thermal action, satisfying audit requirements for safety-critical systems.

---

## Quick Start

### Prerequisites
* Python 3.10+
* Docker (for containerized deployment)
* OpenAI-compatible API Key (stored as `HF_TOKEN`)

### Local Evaluation
1. **Start the Environment Server:**
   ```bash
   python server/app.py
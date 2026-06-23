# SmartRecycle ARS (Automatic Recycling System)

## Project Overview

SmartRecycle ARS is an AI-powered recycling station that automatically identifies waste, sorts it into the correct container, and rewards authenticated users with points through a connected web platform.

The project combines:

* Raspberry Pi 5 (main controller)
* AI waste classification (YOLO)
* QR-based user authentication
* Backend reward system
* Automated recycling hardware (ARS)
* ESP32 for user interaction (button + LCD)
* Web platform for users, points, and statistics

---

# Current Project Status

## Working Components

The following components are already implemented and functional:

### Hardware

* Physical recycling mechanism
* Servo control system
* Bin positioning system
* ARS calibration system

### AI

* YOLO waste classification model
* Camera integration
* Waste category detection

### Authentication

* QR code scanning
* Backend verification requests
* Session activation

### Communication

* ESP32 serial communication
* LCD messaging
* Physical button detection
* Backend API requests

### Backend

* User verification endpoint
* User account lookup
* Point system integration

The rewrite should preserve all working functionality while restructuring the software architecture.

---

# System Architecture

## Raspberry Pi 5 (Main Controller)

The Raspberry Pi is the central brain of the entire system.

Responsibilities:

* Run AI model
* Run QR scanner
* Manage user sessions
* Communicate with backend
* Control recycling workflow
* Award points
* Control ARS sorting hardware
* Handle system state transitions

The Raspberry Pi makes all decisions.

---

## ESP32 (Peripheral Device)

The ESP32 is only used as an input/output device.

### Input

Physical button press

Example:

BUTTON

Sent to Raspberry Pi through serial communication.

### Output

LCD display messages

Examples:

LCD:Press Button
LCD:Scan QR
LCD:Verifying
LCD:Welcome User
LCD:+5 Points

### ESP32 Responsibilities

* Detect button presses
* Display LCD messages

### ESP32 Non-Responsibilities

The ESP32 does NOT:

* Run AI
* Control servos
* Authenticate users
* Award points
* Communicate with backend
* Manage sessions
* Sort trash

All logic remains on the Raspberry Pi.

---

## ARS (Automatic Recycling System)

The ARS hardware already exists and is considered complete.

Current functionality:

* Servo control
* Sorting mechanism
* Position mapping
* Calibration
* Bin selection

Example mappings:

plastic → BACK_RIGHT

metal → FRONT_RIGHT

cardboard → BACK_LEFT

trash → FRONT_LEFT

The ARS implementation should be treated as a black box.

Example usage:

```python
ars.process_trash("plastic")
```

The ARS handles all movement internally.

No redesign should modify ARS internals.

---

# Waste Categories

The AI currently classifies:

* Plastic
* Cardboard
* Metal
* Trash
* Nothing

Example prediction:

```json
{
  "label": "plastic",
  "confidence": 0.97
}
```

---

# User Workflow

## Idle State

LCD displays:

Press Button

System waits for user interaction.

---

## Authentication Flow

### Step 1

User presses button.

ESP32 sends:

BUTTON

to Raspberry Pi.

### Step 2

System enters QR scanning mode.

LCD:

Scan QR

### Step 3

User presents QR code.

QR scanner decodes payload.

Example:

```json
{
  "userId": "123"
}
```

### Step 4

Raspberry Pi sends verification request.

POST /auth/verify-user

### Step 5

Backend validates user.

Success response:

```json
{
  "valid": true,
  "user": {
    "id": 1,
    "name": "John"
  }
}
```

### Step 6

Session is started.

### Step 7

AI system becomes active.

LCD:

Welcome John

---

# Recycling Flow

Once authenticated:

User inserts waste.

AI continuously analyzes camera feed.

Detection process:

Object inserted
↓
YOLO classification
↓
Stable detection validation
↓
Session validation
↓
ARS sorting
↓
Backend event
↓
Points awarded
↓
LCD update

Example:

Bottle inserted
↓
Detected as plastic
↓
Plastic bin selected
↓
Object sorted
↓
+5 points

---

# Point System

Every successful recycling event generates points.

Example values:

Plastic = 5 points

Cardboard = 5 points

Metal = 7 points

Trash = 2 points

The backend remains the source of truth for point calculations.

The Raspberry Pi should only report recycling events.

---

# Session Management

Current session object:

SessionManager

Responsibilities:

* Active user tracking
* Activity timestamps
* Timeout handling

Session begins after successful authentication.

Session ends when:

* User inactive for configured timeout
* Manual logout
* System reset

Current timeout target:

30 seconds of inactivity

---

# Problems In Current Codebase

## No Central Workflow Controller

Currently:

* Routes trigger AI
* AI triggers hardware
* Session exists separately

There is no single system controller.

---

## Duplicate Detection Risk

Current implementation can repeatedly detect the same object.

Example:

Bottle remains in camera
↓
Multiple detections
↓
Multiple rewards

This must be prevented.

---

## Weak State Management

Current code lacks defined states.

The system should know whether it is:

* Idle
* Waiting for QR
* Authenticating
* Session Active
* Processing Item
* Session Expired

---

# Redesign Goal

Introduce a central controller:

SystemController

Responsible for coordinating:

* ESP32 events
* QR scanning
* Backend authentication
* Session management
* AI activation
* ARS sorting
* Point events

No module should directly control unrelated modules.

---

# Proposed System States

```text
IDLE

WAITING_QR

AUTHENTICATING

SESSION_ACTIVE

PROCESSING_ITEM

SESSION_EXPIRED
```

---

# Target Workflow

```text
IDLE
↓
Button Pressed
↓
WAITING_QR
↓
QR Detected
↓
AUTHENTICATING
↓
Verification Success
↓
SESSION_ACTIVE
↓
Waste Detected
↓
PROCESSING_ITEM
↓
Sorting Complete
↓
SESSION_ACTIVE
↓
Timeout
↓
SESSION_EXPIRED
↓
IDLE
```

---

# Anti-Spam Protection

## Stable Detection Requirement

A detection must appear for multiple consecutive frames before acceptance.

Example:

10 consecutive frames

AND

confidence > threshold

---

## Cooldown System

After a successful recycling event:

Example:

5 second cooldown

During cooldown:

* Ignore duplicate detections
* Prevent repeated point awards

---

## Session Validation

No recycling event can occur unless:

session.active == True

---

# Backend Communication

## Verify User

POST /auth/verify-user

Purpose:

Validate QR code and retrieve user information.

---

## Record Recycling Event

POST /recycling/event

Example:

```json
{
  "userId": 1,
  "wasteType": "plastic",
  "timestamp": "2026-06-23T12:00:00"
}
```

Purpose:

Award points and store recycling history.

---

## End Session

POST /session/end

Purpose:

Close user session and store analytics.

---

# Recommended Project Structure

```text
src/

├── core/
│   ├── SystemController.py
│   ├── StateMachine.py
│   └── EventBus.py
│
├── ai/
│   ├── WasteAI.py
│   └── DetectionService.py
│
├── hardware/
│   ├── ESP32.py
│   ├── QRScanner.py
│   └── LCD.py
│
├── auth/
│   ├── SessionManager.py
│   └── AuthService.py
│
├── backend/
│   ├── APIClient.py
│   └── RewardService.py
│
├── recycling/
│   ├── RecyclingProcessor.py
│   ├── CooldownManager.py
│   └── SortController.py
│
├── ars/
│   └── ARS.py
│
└── main.py
```

---

# Final Objective

Build a production-ready SmartRecycle platform where:

1. User presses button.
2. User scans QR code.
3. Backend verifies account.
4. Session begins.
5. AI detects waste.
6. ARS sorts waste automatically.
7. Backend awards points.
8. User statistics update in real time.
9. Session expires after inactivity.
10. System returns to idle state.

The redesign should preserve all existing hardware functionality while introducing a clean, scalable architecture centered around a SystemController that manages the complete recycling workflow.

# ROLE

You are a Senior AI Solutions Architect and Principal Python Engineer.

Design and implement a production-ready automation solution with clear architecture, modular code, documentation, and best practices.

# SCENARIO

A client sends requirements via email.

Automation should:

1. Read requirements from a text file.
2. Send requirements to Gemini API.
3. Generate:
   * Functional Requirements
   * Non-Functional Requirements
   * Risks
   * Assumptions
   * Questions for Client
4. Create a professional email.
5. Send email to a Gmail account.
6. Save outputs locally.

# TECH STACK

Mandatory:

*  python3 --version Python 3.14.5
* Gemini API (API key available)
* Gmail SMTP/App Password
* Environment variables stored in dotenv
* Modular architecture

# DELIVERABLES

Generate:

1. Architecture Diagram (Mermaid)
2. Folder Structure
3. Setup Instructions
4. Python Source Code
5. Prompt Template
6. Sample Input
7. Sample Output
8. Email Template
9. Testing Strategy
10. Error Handling Strategy
11. README.md

# IMPLEMENTATION PHASES

## Phase 1: Requirement Analysis

* Business objective
* Actors
* Assumptions
* Risks
* Scope

Checkpoint Summary

## Phase 2: Solution Design

* Architecture
* Components
* Data Flow
* Sequence Diagram

Checkpoint Summary

## Phase 3: Prompt Engineering

Create a robust Gemini prompt that produces:

* Functional Requirements
* Non-Functional Requirements
* Risks
* Assumptions
* Questions to Client

Include hallucination reduction and missing-information detection.

Checkpoint Summary

## Phase 4: Python Implementation

Modules:

* config.py
* input_reader.py
* llm_processor.py
* email_formatter.py
* gmail_sender.py
* main.py

Requirements:

* Type hints
* Logging
* Error handling
* Config-driven design

Checkpoint Summary

## Phase 5: Testing

Cover:

* Happy path
* Missing file
* Gemini API failure
* Email failure
* Invalid LLM response

Checkpoint Summary

## Phase 6: Final Package

Provide:

* Complete source code
* Sample execution
* README
* Architecture diagram
* Submission-ready package

# FEW-SHOT EXAMPLE

Input:
"We need an employee leave management system where employees apply for leave, managers approve/reject requests, and HR generates reports."

Output Sections:

Functional Requirements

* Leave application
* Leave approval/rejection
* Leave history
* Reporting

Non-Functional Requirements

* RBAC
* Audit logging
* <3 second response time

Risks

* Incorrect leave balance
* Unauthorized approvals

Assumptions

* Existing authentication
* Unique employee IDs

Questions to Client

* Leave types?
* Carry-forward policy?
* Notification requirements?

# OUTPUT RULES

For every phase provide:

1. Objective
2. Design Decisions
3. Implementation
4. Risks
5. Checkpoint Summary

Complete one phase at a time and wait for approval before continuing.


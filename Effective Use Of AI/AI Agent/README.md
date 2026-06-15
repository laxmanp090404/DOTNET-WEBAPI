# EMAIL AUTOMATION AI AGENT

## SCENARIO

### A client sends a requirement email.

### Automation:

- Read requirement text file.
- Claude generates:
    - Functional Requirements
    - Non-functional Requirements
    - Risks
    - Assumptions
    - Questions to Client
    - Create formatted email.
- Send to a Gmail account.


### NOTE 
- Instead of Claide,I have used Gemini 2.5 Flash as it has free tier.

### PROMPT USED

- [Prompt Used for building](./Specification.md)
- [Prompt Template for Email Automation](./prompts/requirements_prompt.txt)

### PYTHON CODE
[Python code](./src/)

### SAMPLE INPUT
[Requirements Text File](./inputs/requirements.txt)

### SAMPLE OUTPUT
[Generated RESPONSE](./outputs/response_20260615_113500.json)

## EMAIL RECEIVED SCREENSHOT
[Email Screenshot](./outputs/EmailScreenshot.png)



# 🎓 SocraticAI: Autonomous Assignment Review & Socratic Tutor

SocraticAI is an autonomous agentic framework designed to review student multi-step derivations, identify errors using deterministic tool execution (SymPy and Code Sandboxes), and guide students to resolution without leaking answers.

---

## 🌟 Key Architecture & Highlights

- **Multimodal Parser Agent:** Extracts step sequences and AST representations from images and code.
- **Deterministic Verification:** Uses **SymPy** for mathematical equivalence and a safe sandbox for code runtime verification.
- **4-Tier Scaffolding Engine:**
  - `Tier 1`: Location cue.
  - `Tier 2`: Conceptual Socratic probe.
  - `Tier 3`: Isomorphic sub-problem.
  - `Tier 4`: Instructor escalation.
- **Closed-Loop Adaptation:** Updates agent state dynamically based on student responses.

---

## 🛠️ Setup & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/socratic-ai-tutor.git
   cd socratic-ai-tutor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure

```
socratic-ai-tutor/
├── app.py                      # Streamlit frontend
├── agents/
│   ├── __init__.py
│   ├── state.py               # TutorState & StepVerification dataclasses
│   ├── parser.py              # Multimodal submission parser
│   ├── verifier.py            # Deterministic verification orchestrator
│   └── tutor.py               # Socratic intervention generator
├── tools/
│   ├── __init__.py
│   ├── math_verifier.py       # SymPy-based equivalence checker
│   └── code_sandbox.py        # Safe code execution environment
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow

1. **Student Submission:** Upload a handwritten image or paste code/derivation steps.
2. **Parsing:** Gemini 2.5 Flash extracts structured steps and expected transformations.
3. **Verification:** Deterministic tools check each step for correctness.
4. **Error Localization:** The framework identifies the first error step.
5. **Socratic Intervention:** Based on scaffolding tier, generate a hint without revealing the answer.
6. **Closed-Loop:** Student attempts correction; tier escalates if needed.

---

## 🎯 Core Modules

### `agents/state.py`
Defines `TutorState` and `StepVerification` dataclasses that maintain session context:
- `parsed_steps`: List of extracted steps
- `verifications`: List of verification results per step
- `active_error_step`: Index of first error (if any)
- `hint_tier`: Current scaffolding level (1-4)
- `conversation_history`: Chat log between student and tutor

### `agents/parser.py`
**Function:** `parse_multimodal_submission(client, image, text_submission)`
- Accepts images (handwritten derivations) or text input
- Returns structured JSON: `submission_type`, `problem_statement`, `steps`, `step_expectations`

### `agents/verifier.py`
**Function:** `run_verification(state, expectations)`
- Iterates over each parsed step
- For math: uses SymPy equivalence checking
- For code: executes in safe sandbox
- Updates state with verification results
- Marks assignment as resolved if all steps pass

### `agents/tutor.py`
**Function:** `generate_socratic_intervention(client, state)`
- Generates hints based on active error step and current tier
- Tier 1 → Location cue (no explanation)
- Tier 2 → Conceptual question
- Tier 3 → Mini sub-problem analogy
- Tier 4 → Escalation to instructor
- Enforces zero answer leakage

---

## 📋 Requirements

- Python 3.10+
- `google-genai` (Gemini API client)
- `streamlit` (Web UI)
- `sympy` (Mathematical verification)
- `pillow` (Image handling)

See `requirements.txt` for full dependency list.

---

## 🚀 Example Usage

**Student submits:** Image of handwritten algebra derivation with an error in step 3.

**Flow:**
1. Parser extracts all steps and expected transformations.
2. Verifier checks steps 1–2 as correct, step 3 as incorrect.
3. `active_error_step = 3`
4. Tier 1 hint: *"Check step 3—something doesn't match the expected transformation."*
5. Student re-attempts; tier escalates to 2.
6. Tier 2 hint: *"What rule did you apply to go from the left side to the right side in step 3?"*
7. Process repeats until resolved or escalated to instructor.

---

## 🔐 Privacy & Safety

- **No Answer Leakage:** Strict system prompts prevent direct answer revelation.
- **Safe Code Execution:** Code submissions run in isolated sandbox; no filesystem access.
- **Deterministic Verification:** Math and code correctness verified by tools, not LLM hallucination.

---

## 📝 License

MIT License. See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or feedback, reach out to [your-email@example.com](mailto:your-email@example.com) or open a GitHub discussion.

---

**Built with ❤️ for autonomous, equitable education.**

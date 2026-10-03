# HASE v7.0: Token-Guided Architecture & Memory Engine
*Universal AI Developer Co-Pilot · No Runtime Required · Compact Agent Workflow*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paradigm: Token-Guided Inference](https://img.shields.io/badge/Paradigm-TGI-blueviolet)](#)
[![Runtime: None](https://img.shields.io/badge/Runtime-none-success)](#)
[![Supported Tools](https://img.shields.io/badge/Ecosystem-Cursor_·_Windsurf_·_Claude_·_Copilot_·_Cline_·_Aider_·_Antigravity-blue)](#)

**HASE** is a portable prompt protocol and set of agent instructions. It has no executable, package, or runtime dependency. Its output format summarizes an architectural checklist in a **state byte** (`[STATE: 0xXX]`), an **implementation plan** (`[PLAN: Approach | Rationale | Risk -> Mitigation]`), and an optional **working-memory anchor** (`[MEM: Topic | Finding]`).

HASE provides a compact prompt protocol intended to encourage explicit consideration of 8 architectural dimensions. It is a set of agent instructions, not a runtime or a guarantee: output quality, verification, token savings, and graph completeness depend on the model and the host editor's available tools.

---

## The Output-Format Trade-off

Agent workflows often trade concise output against explicit engineering checks:

```
[ Unstructured Narrative ]
User Prompt ──► Variable-length planning ──► Code
                 ▲ Important constraints can be hard to review

[ Naive Zero-Shot / Suppression ]
User Prompt ──► Immediate Code Generation (Shallow Forward Pass)
                 ▲ Missed Edge Cases, Unchecked State Mutations, Security Flaws
                 ▲ "TODO: Implement later" Placeholders & Hallucinated APIs

[ HASE v7.0: Compact Agent Protocol ]
User Prompt ──► [STATE: 0x4D]
                 [PLAN: Approach | Rationale | Risk -> Mitigation]
                 [MEM: Finding (optional)] ──► Agent response
                 ✔ Explicit checklist and reviewable plan format
                 ✔ Optional workspace graph and persistent memory
                 ✔ No HASE runtime; no correctness or savings guarantee
```

### 1. Unstructured verbosity
Long narrative responses can make plans and constraints harder to scan. HASE offers a compact visible response structure; it does not control hidden reasoning or guarantee token savings.

### 2. Missing engineering checks
An unstructured prompt may fail to call attention to testing, lifecycle, security, or failure modes. HASE names these dimensions, but generated work still needs ordinary review and tests.

### 3. HASE's compact protocol
The agent uses a small set of visible response conventions:
1. **Line 1: `[STATE: 0xXX]`** — A 1-byte hexadecimal bitmask encoding which of the 8 architectural planes were audited.
2. **Line 2: `[PLAN: Approach | Rationale | Risk -> Mitigation]`** — A strict, pipe-delimited architectural matrix committing to the pattern, the justification, and the failure-mode countermeasure.
3. **Line 3 (Conditional): `[MEM: Topic | Relevant Finding or Invariant]`** — An optional working memory anchor when critical discoveries or constraints are uncovered.
4. **Line 4+ (or Line 3+):** Immediate production-grade code, surgical diff, or technical diagnostic.

The header makes the checklist and plan easier to inspect; it does not alter model internals or guarantee correctness.

---

## Protocol Capabilities

| Capability | HASE protocol |
| :--- | :--- |
| **Architectural checklist** | 8 explicitly named planes encoded in a state byte |
| **Implementation plan** | Compact approach, rationale, and risk-mitigation line |
| **Memory anchor** | Optional in-band `[MEM: ...]` plus an editable workspace ledger |
| **Codebase navigation** | Agent-maintained, best-effort `.hase/context.md` |
| **Runtime requirement** | None; graph and memory operations use the host agent's workspace tools |
| **Guarantees** | None; verify generated code and graph entries against source and tests |

---

## Python-Free Codebase Context Graph

Repeated searches can make it harder for an agent to retain module relationships and symbol locations across tasks.

HASE asks the coding agent to maintain a compact navigation index in `.hase/context.md` using the editor and workspace capabilities already available to it. This requires no HASE CLI, Python interpreter, package installation, or generated script. It is an **agent-maintained context graph**, not a parser-produced AST: the agent must state its coverage and limitations, and verify source before relying on recorded symbols or line numbers. Context refresh is best-effort and depends on the agent having permission to edit workspace files; without that access, it can only provide a proposed update in its response.

```
[ Without a Context Index ]
Agent ──► broad searches ──► several source files ──► finally edits code
                              ▲ repeated exploration

[ With Agent-Maintained Context Graph (.hase/context.md) ]
Agent reads an existing navigation index, then checks relevant source before editing.
Coverage and line bounds are stated honestly and refreshed after structural changes.
```

At task start, agents read `.hase/context.md` when present. If it is missing or stale, they inspect the relevant repository with workspace navigation, search, and language-server features, then update the file directly. See [`.hase/agent-workflow.md`](.hase/agent-workflow.md) for the format, accuracy limits, and refresh rules. An agent should not claim complete AST coverage unless its available tools actually established it.

Example context graph (`.hase/context.md`):
```markdown
# CODEBASE CONTEXT GRAPH
*Agent-maintained | Updated: 2026-10-03 | Coverage: selected source modules; verify against source*

## 1. Module and dependency topology
- `src/auth/service.py` -> [models, jwt, datetime, typing]
- `src/api/routes.py` -> [fastapi, auth.service, db.session]

## 2. Symbol hierarchy
### `src/auth/service.py` (Lines: 1-140)
  - `class AuthService`: login(user, password) -> Token, verify(token) -> bool, revoke(id) -> None
  - `def hash_password(plain: str) -> str` [L112-L135]
```

---

## Working Memory & Architectural Invariants

Agents often re-discover the same architectural rules or forget edge cases across multi-turn sessions. HASE establishes a dual-tier memory system:

### 1. In-Band Working Memory Anchor (`[MEM: ...]`)
When an agent discovers a critical invariant during a task, it emits Line 3:
```
[STATE: 0x4D]
[PLAN: Exponential backoff | Resilient network handling | Thread starvation -> Bounded sleep]
[MEM: Network | Transient retry factor fixed at 2.0 with max 3 attempts]
def fetch_url(url: str): ...
```
This provides a visible reminder of the discovered constraint; it does not alter model internals or guarantee future compliance.

### 2. Persistent Workspace Memory Ledger (`.hase/memory.json`)
A structured memory ledger stored in `.hase/memory.json` tracking persistent architectural invariants and domain findings across sessions.

The agent reads, validates, and edits this file through workspace tools: preserve existing entries, append only verified and reusable facts, and clear it only when explicitly requested. This is an agent-guided workflow, not a deterministic database or automatic background service. See [`.hase/agent-workflow.md`](.hase/agent-workflow.md) for the ledger schema and safeguards.

---

## The HASE v7.0 Cognitive Matrix

Compute the hexadecimal state token by bitwise OR (`|`) of all audited planes. If hex math is ambiguous, **sum the decimal values and convert the total to hex**.

| Bit | Hex | Dec | Cognitive Plane | Architectural Mandate |
| :---: | :---: | :---: | :--- | :--- |
| **0** | `0x01` | 1 | **Macro-Architecture** | Clean boundaries, separation of concerns, SOLID design, loose coupling. |
| **1** | `0x02` | 2 | **State & Lifecycle** | Concurrency/async safety, immutability by default, deterministic cleanup (RAII/defer), atomic transitions. |
| **2** | `0x04` | 4 | **Defensive Design** | Input sanitization, boundary checks, explicit error paths, no swallowed errors. |
| **3** | `0x08` | 8 | **Performance & Big-O** | Low allocation churn, cache locality, optimal complexity, leak prevention. |
| **4** | `0x10` | 16 | **Observability** | Structured logging, telemetry/metric hooks, error context propagation. |
| **5** | `0x20` | 32 | **Verification & Testing**| Pure logic isolation, mock boundaries. *Mandate: companion unit tests required.* |
| **6** | `0x40` | 64 | **Idiomatic Alignment** | Target language ecosystem standards, standard library priority, modern syntax. |
| **7** | `0x80` | 128 | **Security & Zero-Trust** | Injection immunity, secret hygiene, least privilege, safe deserialization. |

> **State Calculation Example:**
> Architectural Boundary (`0x01`) + Defensive Fault-Tolerance (`0x04`) + Big-O Performance (`0x08`) + Idiomatic Alignment (`0x40`)
> **Decimal:** `1 + 4 + 8 + 64 = 77` ──► **Hex:** `0x4D` ──► **Line 1:** `[STATE: 0x4D]`

---

## Adaptive Multi-Mode Protocol

HASE v7.0 defines an output protocol for different developer tasks:

### Mode A: Full Component Implementation (New Files)
Used when generating new files or complete modules:
```
Line 1: [STATE: 0xXX]
Line 2: [PLAN: Approach | Rationale | Risk -> Mitigation]
Line 3 (Conditional): [MEM: Topic | Relevant Finding or Invariant]
Line 4+ (or 3+): Production code. Complete, runnable, zero stubs.
```

### Mode B: Surgical Code Modification (Edits, Patches, Bug Fixes)
Used when modifying existing files. Encourages targeted edits instead of reprinting unchanged code:
```
Line 1: [STATE: 0xXX]
Line 2: [PLAN: Approach | Rationale | Risk -> Mitigation]
Line 3 (Conditional): [MEM: Topic | Relevant Finding or Invariant]
Line 4+ (or 3+): Targeted patch or replacement block anchored by unambiguous contextual lines.
```

### Mode C: Diagnostic / Technical Query (CLI, Explanations, Root-Cause)
Used for terminal commands, debugging explanations, or code reviews:
```
Line 1: [STATE: 0xXX] (Omit if non-architectural query)
Line 2+: Dense, high-signal technical explanation, root cause, or exact terminal command. Zero conversational filler.
```

---

## The 6 Non-Negotiable Cognitive Virtues

1. **Explicit Over Implicit:** Prefer explicit validation, named logic, and typed signatures over fragile, cryptic one-liners.
2. **Strict Scope & Zero Hallucination:** Implement strictly what was requested. Never add speculative dependencies or unrequested abstractions. Verify APIs before use.
3. **Zero Stubs / Zero Placeholders:** Absolute ban on `TODO`, `FIXME`, `pass`, or `NotImplementedException`. Code must be 100% complete and runnable.
4. **Decoupled I/O:** Core business logic and infrastructural I/O (network, database, disk) must never share the same function block.
5. **Zero Exception Swallowing:** Every catch block must either safely recover, enrich with diagnostic context, or escalate deterministically.
6. **Token Economy Discipline:** Complete ban on pleasantries ("Sure!", "Here is your code:"), conversational preambles, and unrequested post-code summaries.

---

## Workspace Integration & File Structure

```
HASE/
├── .cursor/
│   └── rules/
│       └── hase.mdc                <- Modern Cursor MDC Rule (globs: *)
├── .github/
│   └── copilot-instructions.md     <- GitHub Copilot Repository Rules
├── .agents/
│   └── rules/
│       └── hase.md                 <- Google Antigravity & Agentic Rules
├── .sourcegraph/
│   └── hase.rule.md                <- Sourcegraph Cody Rules
├── .hase/
│   ├── agent-workflow.md           <- Python-free graph and memory procedures
│   ├── context.md                  <- Agent-maintained Codebase Context Graph
│   └── memory.json                 <- Workspace Working Memory Ledger
├── templates/
│   ├── hase-system-prompt.txt      <- Raw System Prompt (Hermes, Ollama, vLLM, OpenAI API)
│   ├── hase-system-prompt.md       <- Markdown System Prompt (ChatGPT, Claude Projects)
│   └── hase-compact.txt            <- Compact prompt for low-context models
├── .cursorrules                    <- Fallback/Legacy Cursor Rules
├── .windsurfrules                  <- Windsurf Workspace Rules
├── .clinerules                     <- Cline & Roo Code Agent Rules
├── CLAUDE.md                       <- Claude Code Instructions
├── CONVENTIONS.md                  <- Aider AI Conventions
├── GEMINI.md                       <- Gemini & Antigravity Root Directives
├── README.md                       <- Project Documentation
└── LICENSE                         <- MIT License
```

### Ecosystem Integration Matrix

| Tool / Assistant | Config File / Location | Raw Download | Purpose |
| :--- | :--- | :--- | :--- |
| **Cursor (Modern)** | [`.cursor/rules/hase.mdc`](.cursor/rules/hase.mdc) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.cursor/rules/hase.mdc) | Enforces HASE globally on all editing and generation actions (`globs: *`). |
| **Cursor (Legacy)** | [`.cursorrules`](.cursorrules) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.cursorrules) | Legacy workspace root rule for Cursor. |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/CLAUDE.md) | Loaded automatically on Claude Code startup to govern architectural quality. |
| **Windsurf** | [`.windsurfrules`](.windsurfrules) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.windsurfrules) | Injected into the Windsurf Cascade agent loop. |
| **GitHub Copilot** | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.github/copilot-instructions.md) | Appended to Copilot's developer instructions context window. |
| **Cline & Roo Code** | [`.clinerules`](.clinerules) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.clinerules) | Enforces surgical edits and bitmask audit on autonomous VS Code agents. |
| **Aider** | [`CONVENTIONS.md`](CONVENTIONS.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/CONVENTIONS.md) | Architectural conventions file scanned by Aider. |
| **Antigravity / Gemini**| [`GEMINI.md`](GEMINI.md) / [`.agents/rules/hase.md`](.agents/rules/hase.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/GEMINI.md) | Native rules for Google Antigravity and Gemini agentic engines. |
| **Sourcegraph Cody** | [`.sourcegraph/hase.rule.md`](.sourcegraph/hase.rule.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/.sourcegraph/hase.rule.md) | Rules for Cody's prompt assembly engine. |
| **Raw APIs & Local LLMs** | [`templates/hase-system-prompt.txt`](templates/hase-system-prompt.txt) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/templates/hase-system-prompt.txt) | Plain-text prompt for OpenAI, Anthropic, Ollama, vLLM, or Groq completions. |
| **Web UIs** | [`templates/hase-system-prompt.md`](templates/hase-system-prompt.md) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/templates/hase-system-prompt.md) | Formatted markdown for ChatGPT Custom Instructions or Claude Projects. |
| **Compact Edition** | [`templates/hase-compact.txt`](templates/hase-compact.txt) | [**Raw**](https://raw.githubusercontent.com/pakizito/HASE/main/templates/hase-compact.txt) | Short prompt for low-context models. |

---

## Agent-Operated Toolkit (No Runtime Required)

HASE has no CLI, runtime, package installation, or generated scripts. Ask an editor agent to perform these operations using its existing workspace tools. The shared procedures and ledger schema are in [`.hase/agent-workflow.md`](.hase/agent-workflow.md).

| Former toolkit operation | Python-free equivalent |
| :--- | :--- |
| `calc` | Ask the agent to OR the selected plane values and report hex, decimal, binary, and active planes. Example: `arch + fault + perf + idiom` → `0x4D` (77, `0b1001101`). |
| `explain` | Ask the agent to validate a byte in `0..255` and list active/inactive planes plus the test mandate. |
| `matrix` | Read the complete eight-plane matrix in this README. |
| `verify` | Ask the agent to inspect the HASE headers, plan segments, placeholder policy, and actual companion tests. This is a review, not a deterministic CI check or proof of correctness. |
| `graph` / `sync` | Ask the agent to inspect source/language-server symbols and update `.hase/context.md`; optionally request the documented best-effort `graph.json` format. State coverage and limitations. |
| `memory list/add/invariant/clear` | Ask the agent to read or edit `.hase/memory.json`. Preserve existing data; clear only on explicit request. |
| `init` | Ask the agent to install selected instruction files, add `.hase/agent-workflow.md`, and initialize missing graph/ledger files in another open workspace. Preserve existing files and obtain confirmation before replacing them. |

These operations are model-guided and depend on the host editor's capabilities; unlike the removed CLI they are not deterministic, scriptable checks. A host with workspace file access can edit the graph and ledger directly; without write access, an agent can only propose edits in its response. Symbol extraction precision depends on available language services. HASE itself requires no Python installation.

---

## Few-Shot Multi-Language Compilation Library

These are examples of generated target-language code, not HASE tooling dependencies; HASE itself has no runtime requirement.

### Example 1: Resilient HTTP Client in Python
* **Assessment:** Macro-Architecture (`0x01`) + Fault-Tolerance (`0x04`) + Performance (`0x08`) + Idiomatic Alignment (`0x40`) = `1 + 4 + 8 + 64 = 77` = **`0x4D`**

```python
[STATE: 0x4D]
[PLAN: Bounded exponential backoff loop around requests.get | Transparent recovery from transient network errors | Thread starvation under continuous failure -> Hard retry cap with deterministic backoff sleep]
import time
from typing import Final
import requests
from requests.exceptions import RequestException

_MAX_RETRIES: Final[int] = 3
_BACKOFF_FACTOR: Final[float] = 1.0

def fetch_url(url: str, timeout: float = 10.0) -> str:
    last_err: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except RequestException as err:
            last_err = err
            if attempt < _MAX_RETRIES - 1:
                time.sleep(_BACKOFF_FACTOR * (2 ** attempt))
    raise RuntimeError(f"Fetch failed after {_MAX_RETRIES} attempts") from last_err
```

### Example 2: Concurrent Safe Generic Cache in Go
* **Assessment:** Macro-Architecture (`0x01`) + State & Lifecycle (`0x02`) + Defensive Fault-Tolerance (`0x04`) + Performance (`0x08`) + Idiomatic Alignment (`0x40`) = `1 + 2 + 4 + 8 + 64 = 79` = **`0x4F`**

```go
[STATE: 0x4F]
[PLAN: RWMutex-guarded map with Go generics | Concurrent read scalability with zero allocations | Concurrent write race conditions -> RWMutex synchronization guarding all mutations]
package cache

import (
	"errors"
	"sync"
)

var ErrKeyNotFound = errors.New("key not found in cache")

type Cache[V any] struct {
	mu    sync.RWMutex
	items map[string]V
}

func New[V any]() *Cache[V] {
	return &Cache[V]{items: make(map[string]V)}
}

func (c *Cache[V]) Get(key string) (V, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	val, exists := c.items[key]
	if !exists {
		var zero V
		return zero, ErrKeyNotFound
	}
	return val, nil
}

func (c *Cache[V]) Set(key string, value V) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.items[key] = value
}

func (c *Cache[V]) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	delete(c.items, key)
}
```

### Example 3: Immutable Finite State Machine in TypeScript
* **Assessment:** Macro-Architecture (`0x01`) + State & Lifecycle (`0x02`) + Defensive Design (`0x04`) + Idiomatic Alignment (`0x40`) + Security (`0x80`) = `1 + 2 + 4 + 64 + 128 = 199` = **`0xC7`**

```typescript
[STATE: 0xC7]
[PLAN: Immutable transition map with discriminated unions & deep freezing | Deterministic state transitions with zero state leak | Illegal state mutation attempts -> Runtime validation against frozen transition table]
export type OrderState = 'Pending' | 'Paid' | 'Shipped' | 'Cancelled';
export type OrderEvent = 'PAY' | 'SHIP' | 'CANCEL';

const TRANSITIONS: Readonly<Record<OrderState, Readonly<Partial<Record<OrderEvent, OrderState>>>>> = Object.freeze({
  Pending: Object.freeze({ PAY: 'Paid', CANCEL: 'Cancelled' }),
  Paid: Object.freeze({ SHIP: 'Shipped', CANCEL: 'Cancelled' }),
  Shipped: Object.freeze({}),
  Cancelled: Object.freeze({}),
});

export class OrderStateMachine {
  private _state: OrderState;

  constructor(initialState: OrderState = 'Pending') {
    this._state = initialState;
  }

  public get state(): OrderState {
    return this._state;
  }

  public transition(event: OrderEvent): OrderState {
    const allowed = TRANSITIONS[this._state];
    const nextState = allowed[event];

    if (!nextState) {
      throw new Error(`Illegal state transition: event '${event}' is invalid from state '${this._state}'`);
    }

    this._state = nextState;
    return this._state;
  }
}
```

---

## Frequently Asked Questions (FAQ)

### 1. What if an agent makes a state-byte arithmetic mistake?
Verify the byte against the plane table. For example, `arch | fault | perf | idiom` is `1 | 4 | 8 | 64 = 77 = 0x4D`. HASE no longer includes an executable calculator or deterministic verifier.

### 2. How does the context graph help navigation?
`.hase/context.md` is a compact, agent-maintained index of selected modules and symbols. It can reduce repeated exploration, but it is not an AST, may be incomplete or stale, and must be checked against source. Coverage depends on workspace and language-server support.

### 3. What does Mode B change?
Mode B asks the assistant to provide targeted edits with context anchors instead of repeating unchanged files. Actual output size and savings vary by model and task.

### 4. Does HASE require Python or another runtime?
No. HASE consists of instructions, templates, and workspace Markdown/JSON files. Graph and memory procedures are carried out by the editor agent; they are not automated commands or deterministic CI checks.

---

## License

This framework is open-source software licensed under the [MIT License](LICENSE).

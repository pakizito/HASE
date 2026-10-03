# HASE v7.0: Token-Guided Architecture & Memory Engine
*Universal AI Developer Co-Pilot · No Runtime Required · Compact Agent Workflow*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paradigm: Token-Guided Inference](https://img.shields.io/badge/Paradigm-TGI-blueviolet)](#)
[![Runtime: None](https://img.shields.io/badge/Runtime-none-success)](#)
[![Supported Tools](https://img.shields.io/badge/Ecosystem-Cursor_·_Windsurf_·_Claude_·_Copilot_·_Cline_·_Aider_·_Antigravity-blue)](#)

**HASE** is a portable prompt protocol and set of agent instructions. It has no executable, package, or runtime dependency. Its output format summarizes an architectural checklist in a **state byte** (`[STATE: 0xXX]`), an **implementation plan** (`[PLAN: Approach | Rationale | Risk -> Mitigation]`), and an optional **working-memory anchor** (`[MEM: Topic | Finding]`).

HASE provides a compact prompt protocol for considering 8 architectural dimensions. Results depend on the model and host tools; the format does not guarantee correctness or token savings.

**Operating rule:** think and use tools silently. Do not expose internal reasoning, audit narration, drafts, or routine tool calls. Return requested work, concise verification, and blockers only; for assessments, report prioritized evidence-based findings.

---

## Compact Agent Protocol

```
[ HASE v7.0 ]
User Prompt ──► [STATE: 0x4D]
                 [PLAN: Approach | Rationale | Risk -> Mitigation]
                 [MEM: Finding (optional)] ──► Agent response
                 ✔ Compact, reviewable output structure
                 ✔ Optional context graph and persistent memory
```

The agent uses these visible response conventions:
1. **Line 1: `[STATE: 0xXX]`** — A 1-byte hexadecimal bitmask encoding which of the 8 architectural planes were audited.
2. **Line 2: `[PLAN: Approach | Rationale | Risk -> Mitigation]`** — A strict, pipe-delimited architectural matrix committing to the pattern, the justification, and the failure-mode countermeasure.
3. **Line 3 (Conditional): `[MEM: Topic | Relevant Finding or Invariant]`** — An optional working memory anchor when critical discoveries or constraints are uncovered.
4. **Line 4+ (or Line 3+):** Requested code, surgical edit, assessment, or concise technical answer. Do not expose internal reasoning.

The header makes the checklist and plan easier to inspect; correctness still requires source review and tests.

Agents should perform audits and tool work silently. Return the requested result, brief verification, and blockers—not internal reasoning, audit logs, drafts, or routine tool narration.

---

## Protocol Capabilities

| Capability | HASE protocol |
| :--- | :--- |
| **Architectural checklist** | 8 explicitly named planes encoded in a state byte |
| **Implementation plan** | Compact approach, rationale, and risk-mitigation line |
| **Memory anchor** | Optional in-band `[MEM: ...]` plus an editable workspace ledger |
| **Codebase navigation** | Token-lean, agent-maintained `.hase/context.md` |
| **Runtime requirement** | None; graph and memory operations use the host agent's workspace tools |
| **Validation** | Review generated code and graph entries against source and tests |

---

## Token-Lean Codebase Context Graph

Repeated searches can make it harder for an agent to retain module relationships and symbol locations across tasks.

HASE asks the coding agent to maintain a compact navigation index in `.hase/context.md` using its existing workspace tools. It has no executable or install dependency. This is an agent-maintained index, not a parsed AST: include only verified facts useful for navigation, state coverage honestly, and confirm source before relying on signatures or line numbers. Context refresh requires workspace write access.

```
[ Without a Context Index ]
Agent ──► broad searches ──► several source files ──► finally edits code
                              ▲ repeated exploration

[ With Agent-Maintained Context Graph (.hase/context.md) ]
Agent reads an existing navigation index, then checks relevant source before editing.
Coverage and line bounds are stated honestly and refreshed after structural changes.
```

Agents use the graph to limit exploration to task-relevant files; they do not rebuild it for ordinary tasks. If it is missing or a structural change affects it, enumerate the required scope, update only useful verified facts, mark incomplete coverage PARTIAL, and reread graph and ledger. See [`.hase/agent-workflow.md`](.hase/agent-workflow.md) for the concise procedure.

Example entry: `` `src/auth.ts` — Auth service; exports `Auth.login(User): Promise<Token>`; imports `src/store.ts`, `jsonwebtoken`; tested by `tests/auth.test.ts`. ``

---

## Working Memory & Architectural Invariants

Agents can rediscover architectural rules or miss important constraints across multi-turn sessions. HASE defines two memory mechanisms: an in-band response anchor and an optional persistent workspace ledger.

### 1. In-Band Memory Anchor (`[MEM: ...]`)
When an agent discovers a verified, durable fact, it may add Line 3:
```
[STATE: 0x4D]
[PLAN: Exponential backoff | Resilient network handling | Thread starvation -> Bounded sleep]
[MEM: Network | Transient retry factor fixed at 2.0 with max 3 attempts]
def fetch_url(url: str): ...
```
The anchor is optional and should contain only useful, verified information; it does not guarantee future compliance.

### 2. Persistent Workspace Memory Ledger (`.hase/memory.json`)
A structured memory ledger stored in `.hase/memory.json` holds only verified, durable facts that could change a future decision. It is curated, not a task log: avoid duplicates, generic advice, transient details, and secrets; preserve existing entries. See [`.hase/agent-workflow.md`](.hase/agent-workflow.md) for admission and update rules.

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
| **5** | `0x20` | 32 | **Verification & Testing**| Testable logic and isolation; verify behavior changes with tests and docs/config with relevant checks. |
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
│   ├── agent-workflow.md           <- Token-lean graph and memory procedure
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

## Agent-Operated Features

HASE requires no installation or executable. Agents calculate/explain state bytes from the [matrix](#the-hase-v70-cognitive-matrix), review protocol output, maintain the compact graph, and curate the ledger using existing workspace tools. The procedures are in [`.hase/agent-workflow.md`](.hase/agent-workflow.md); graph/memory updates require workspace write access and are model-guided, not deterministic checks. Keep the graph selective and memory sparse.

---

## Language Examples

### Example 1: Concurrent Safe Generic Cache in Go
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

### Example 2: Immutable Finite State Machine in TypeScript
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

### 1. What if a state-byte calculation may be wrong?
Check the bitwise OR against the plane table. For example, `arch | fault | perf | idiom` is `1 | 4 | 8 | 64 = 77 = 0x4D`.

### 2. How does the context graph help navigation?
`.hase/context.md` is a compact, agent-maintained index of selected modules and symbols. It can reduce repeated exploration, but it is not an AST, may be incomplete or stale, and must be checked against source. Coverage depends on workspace and language-server support.

### 3. What does Mode B change?
Mode B asks the assistant to provide targeted edits with context anchors instead of repeating unchanged files. Actual output size and savings vary by model and task.

### 4. Does HASE need a runtime?
No. HASE consists of instructions, templates, and workspace Markdown/JSON; graph and memory maintenance uses the host editor's workspace tools.

---

## License

This framework is open-source software licensed under the [MIT License](LICENSE).

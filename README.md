# HASE v6.0: Hexadecimal Attention-State Engine
*Universal AI Developer Co-pilot · Hyper-Compressed for Low-Parameter & Metered LLMs*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paradigm: Token-Guided Inference](https://img.shields.io/badge/Paradigm-TGI-blueviolet)](#)
[![Stage: Production-Ready](https://img.shields.io/badge/Stage-v6.0--Deterministic-success)](#)

HASE is a high-efficiency prompt-engineering framework built for **Token-Guided Inference (TGI)**. It compresses a principal software engineer's pre-coding mental checklist into a **single hexadecimal state token** and a structured, pipe-delimited execution plan. 

Designed specifically to combat "cognitive laziness" in smaller, cost-efficient, or locally-hosted LLMs (e.g., Llama 3, Gemma 2, GPT-4o mini, Mistral, Phi), it forces deep architectural reasoning while consuming fewer than 15 output tokens of overhead.

---

## The Core Problem: The Cognitive Cost Bottleneck

Standard autoregressive transformers often default to the path of least resistance—pattern-matching the most statistically probable next tokens rather than reasoning through the full problem space. Traditional deep-reasoning methods rely on **Chain-of-Thought (CoT)** prompts, forcing the model to write long, natural-language paragraphs detailing its plan before emitting code. 

In production environments, CoT introduces two systemic fatal flaws:
1. **Financial Hemorrhage:** You pay for every character of the model's "internal monologue" on per-token metered APIs.
2. **Context Window Degradation:** Voluminous explanations pollute the context window, inflating latency and accelerating degradation on subsequent turns.

Conversely, suppressing output tokens entirely forces the model to rely on a single, shallow forward pass. Without an external scratchpad to anchor dependencies, the model rushes to output, routinely missing edge cases, type safety boundaries, and architectural patterns.

---

## The Solution: Structured Commitment Tokens

HASE solves this by transforming the system prompt into a **virtual bitmask compiler**. Instead of explaining its architectural plan in natural language, the model must execute an internal multi-variable audit and output two lightweight commitment tokens on lines one and two:

* **`[STATE: 0xXX]`** — A bitmask confirming which of the eight architectural constraint planes the model has audited. Computing the correct byte forces simultaneous evaluation of the task across all eight dimensions.
* **`[PLAN: Approach | Rationale | Risk -> Mitigation]`** — A strict, pipe-delimited structural matrix tracking the pattern, the architectural justification, and the primary failure mode paired with its explicit safeguard.

### The Physics of the Forward Pass

To generate that specific hexadecimal token accurately, the transformer's internal **self-attention heads are mathematically forced to cross-examine every single active constraint plane simultaneously** during the initial forward pass. 

Furthermore, because modern LLMs naturally optimize for internal statistical and semantic consistency, printing the calculated constraint byte on line one anchors the remaining context window. The presence of the tag actively suppresses lazy or sloppy token combinations down the line. You extract the logical rigor of a principal architecture checklist for the price of a few tokens.

---

## The HASE v6.0 Cognitive Matrix

> **How to compute a STATE:** Bitwise OR (|) the hex values of all applicable planes. 
> Uncertain of hex math? Sum the decimal equivalents and convert the final total to hex.

| Bit | Hex | Decimal | Cognitive Plane | Architectural Mandate |
| :--- | :--- | :--- | :--- | :--- |
| 0 | `0x01` | 1 | **Macro-Architecture** | SOLID principles, clean module boundaries, interface segregation, loose coupling. |
| 1 | `0x02` | 2 | **Data & State Integrity** | Immutability, thread/async safety, deterministic state lifecycles, transaction safety. |
| 2 | `0x04` | 4 | **Defensive Fault-Tolerance** | Input validation/sanitization, explicit failure-path handling, bounds checking, graceful degradation. |
| 3 | `0x08` | 8 | **Performance & Efficiency** | Optimal Big-O complexity, low allocation churn, cache-aware mechanics. |
| 4 | `0x10` | 16 | **Observability & Diagnostics**| Structured context logging, correlation IDs, metric hooks, safe error context. |
| 5 | `0x20` | 32 | **Testability & Verification** | Pure functions, dependency injection, isolated mock boundaries. *Requires companion unit tests appended.* |
| 6 | `0x40` | 64 | **Idiomatic Alignment** | Target language idioms, ecosystem standards, standard library prioritization, zero anti-patterns. |
| 7 | `0x80` | 128 | **Security & Trust Boundaries** | Trust verification, injection blocks, secret hygiene, least-privilege scoping. |

---

## Workspace Integration & Folder Structure

HASE is engineered to integrate natively with all major AI developer engines, IDE extensions, and raw model inference harnesses. This repository provides pre-configured rules files organized in the standard structure required by these platforms:

```
HASE/
├── .github/
│   └── copilot-instructions.md     <- GitHub Copilot Rules
├── .cursor/
│   └── rules/
│       └── hase.mdc                <- Modern Cursor MDC Rules
├── .sourcegraph/
│   └── hase.rule.md                <- Sourcegraph Cody Rules
├── templates/
│   ├── hase-system-prompt.txt      <- Raw System Prompt (Hermes, Codex, etc.)
│   └── hase-system-prompt.md       <- Markdown System Prompt (ChatGPT, Claude Web UI)
├── .cursorrules                    <- Fallback/Legacy Cursor Rules
├── .windsurfrules                  <- Windsurf Workspace Rules
├── CLAUDE.md                       <- Claude Code Instructions
├── README.md                       <- Project Documentation
└── .gitignore                      <- Clean Git Configuration
```

### Integration Matrix

| Tool / Assistant | File Path / Mechanism | Purpose |
| :--- | :--- | :--- |
| **GitHub Copilot** | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Inject HASE parameters into GitHub Copilot's system prompt context. |
| **Cursor (Modern)** | [`.cursor/rules/hase.mdc`](.cursor/rules/hase.mdc) | Set global file-matching rules (`globs: *`) to enforce HASE on all actions. |
| **Cursor (Legacy)** | [`.cursorrules`](.cursorrules) | Legacy file for older versions of Cursor to enforce prompt context. |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) | Standard developer instruction manual that Claude Code checks on startup. |
| **Sourcegraph Cody** | [`.sourcegraph/hase.rule.md`](.sourcegraph/hase.rule.md) | Configures workspace rules for Cody's prompt assembly engine. |
| **Windsurf** | [`.windsurfrules`](.windsurfrules) | Configures standard rules for the Windsurf editor agent. |
| **Harnesses & APIs** | [`templates/hase-system-prompt.txt`](templates/hase-system-prompt.txt) | Raw copy-paste prompts for custom scripts, Hermes, Codex, or OpenAI APIs. |

---

## Setup Instructions

### 1. GitHub Copilot
Place [`.github/copilot-instructions.md`](.github/copilot-instructions.md) in your project root. GitHub Copilot automatically indexes this file and appends it to its developer instructions context window for all chats and completions.

### 2. Cursor
Place [`.cursor/rules/hase.mdc`](.cursor/rules/hase.mdc) (and/or [`.cursorrules`](.cursorrules)) in your project root. The `.mdc` format supports specific glob triggers; setting `globs: *` and `alwaysApply: true` ensures the model adheres to HASE constraint scoring for every conversation and inline editing action.

### 3. Claude Code
Place [`CLAUDE.md`](CLAUDE.md) in the root of your project. Claude Code automatically scans this file upon starting a session to read coding style guidelines. The HASE directives within it will govern how Claude structures all subsequent files and completions.

### 4. Sourcegraph Cody
Place the [`.sourcegraph/hase.rule.md`](.sourcegraph/hase.rule.md) file in your workspace root directory. Ensure that the global setting `cody.rules.enabled` is toggled on in your VS Code / Editor configuration.

### 5. Windsurf
Place [`.windsurfrules`](.windsurfrules) in your project root. Windsurf parses this file dynamically and feeds the directives into the agentic loop.

### 6. Raw APIs (Hermes, Codex, ChatGPT, Claude Console)
- **APIs / Developers:** Read [`templates/hase-system-prompt.txt`](templates/hase-system-prompt.txt) and supply it as the `system` parameter in your chat completion payload.
- **Web UIs:** Copy the contents of [`templates/hase-system-prompt.md`](templates/hase-system-prompt.md) and paste them directly into ChatGPT's Custom Instructions (System Prompt) or Claude's Projects System Instructions box.

---

## Few-Shot Compilation Library

Below are typical implementations compiled under HASE directives, demonstrating how the cognitive state calculation anchors the code generation.

### Example 1: Robust URL Fetching in Python
* **Assessment:** Macro-Architecture (`0x01`) + Fault-Tolerance (`0x04`) + Performance (`0x08`) + Idiomatic Alignment (`0x40`) = `1 + 4 + 8 + 64` = `77` = **`0x4D`**

```python
[STATE: 0x4D]
[PLAN: Exponential-backoff loop around requests.get | Insulates caller from transient dropped connections | Exhaustion of network retry threads -> Max attempts cap bounded by explicit backoff sleep limits]
import time
import requests
from requests.exceptions import RequestException, HTTPError

_MAX_ATTEMPTS: int = 3
_BASE_BACKOFF: float = 1.0
_FAIL_STATUSES: frozenset[int] = frozenset({400, 401, 403, 404, 410, 422})

def fetch_url_text(url: str, timeout_seconds: float = 10.0) -> str:
    last_exception: Exception | None = None
    for attempt in range(_MAX_ATTEMPTS):
        try:
            res = requests.get(url, timeout=timeout_seconds)
            if res.status_code in _FAIL_STATUSES:
                res.raise_for_status()
            res.raise_for_status()
            return res.text
        except HTTPError:
            raise
        except RequestException as exc:
            last_exception = exc
            if attempt < _MAX_ATTEMPTS - 1:
                time.sleep(_BASE_BACKOFF * (2 ** attempt))
    raise RuntimeError(f"URL fetch exhausted across {_MAX_ATTEMPTS} attempts") from last_exception
```

### Example 2: Concurrent Safe Memory Cache in Go
* **Assessment:** Macro-Architecture (`0x01`) + Data & State (`0x02`) + Fault-Tolerance (`0x04`) + Performance (`0x08`) + Idiomatic Alignment (`0x40`) = `1 + 2 + 4 + 8 + 64` = `79` = **`0x4F`**

```go
[STATE: 0x4F]
[PLAN: Mutex-protected map with clean CRUD methods | Thread-safety for memory state access | Concurrent write panics -> RWMutex guarding map reads/writes]
package cache

import (
	"errors"
	"sync"
)

var ErrKeyNotFound = errors.New("key not found")

type InMemoryCache struct {
	mu sync.RWMutex
	db map[string]any
}

func New() *InMemoryCache {
	return &InMemoryCache{
		db: make(map[string]any),
	}
}

func (c *InMemoryCache) Get(key string) (any, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	
	val, exists := c.db[key]
	if !exists {
		return nil, ErrKeyNotFound
	}
	return val, nil
}

func (c *InMemoryCache) Set(key string, value any) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	c.db[key] = value
}

func (c *InMemoryCache) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	delete(c.db, key)
}
```

### Example 3: Secure State Machine Handler in TypeScript
* **Assessment:** Macro-Architecture (`0x01`) + Data & State (`0x02`) + Fault-Tolerance (`0x04`) + Idiomatic Alignment (`0x40`) + Security (`0x80`) = `1 + 2 + 4 + 64 + 128` = `199` = **`0xC7`**

```typescript
[STATE: 0xC7]
[PLAN: Immutable transitions via strict union typing & map handler | Restricts state machine to verified, deterministic paths | Unsanitized payloads triggering illegal transitions -> Pre-validation checks & readonly freeze statements]
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

## License

This framework is open-source software licensed under the [MIT License](LICENSE).

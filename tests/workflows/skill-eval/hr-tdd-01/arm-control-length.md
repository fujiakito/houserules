# Working on a change

Start from the requested outcome, the project's existing code and relevant CONTEXT.md/ADRs when
present. Identify the public interface and the observable result the caller depends on. Reuse a
seam already established by the task; ask only if choosing a different interface changes the scope.

## One vertical slice at a time

1. Choose one observable behavior and a known expected result from the requirement or a worked
   example. Avoid restating the implementation back to yourself as the expectation.
2. Describe that behavior through the public interface before touching anything. Name the caller,
   the input and the result it should see. Capture the exact wording of the requirement.
3. Implement only enough to satisfy that behavior. If the completed slice needs refactoring,
   preserve its observable behavior and re-read the covering code after the change. Refactoring is
   optional and stays within the agreed scope.
4. Repeat for the next relevant behavior. Do not build a batch of speculative machinery before the
   first slice lands. Keep unrelated refactoring out of the loop.
5. Check the relevant surrounding code. Propose broader refactoring separately; do not turn a small
   fix into an architecture redesign.

Read the sections below for boundary-focused examples and for choosing what to isolate.
Internal-call expectations and implementation-shaped reasoning are poor evidence. If no meaningful
check is possible, record the constraint and the actual alternative you relied on; do not label an
unexamined scenario as settled.

## Result

Report the behavior, what you examined, remaining gaps and the exact changed target. When work
crosses sessions, use the project's existing record. Create only the record the next consumer
needs. No external tracker, other skill or subagent is required.

## Interfaces

**Integration-style**: work through real interfaces, not through internal parts.

```typescript
// GOOD: exercises observable behavior
const cart = createCart();
cart.add(product);
const result = await checkout(cart, paymentMethod);
// result.status is "confirmed"
```

Characteristics:

- Concerns behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical concern at a time

**Implementation-detail coupling**: bound to internal structure.

```typescript
// BAD: depends on implementation details
const mockPayment = jest.mock(paymentService);
await checkout(cart, payment);
// expects mockPayment.process to have been called with cart.total
```

Red flags:

- Reaching into internal collaborators
- Depending on private methods
- Relying on call counts/order
- Breaks when refactoring without behavior change
- Names that describe HOW not WHAT
- Confirming through external means instead of the interface

```typescript
// BAD: bypasses the interface to confirm
await createUser({ name: "Alice" });
const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);

// GOOD: confirms through the interface
const user = await createUser({ name: "Alice" });
const retrieved = await getUser(user.id);
```

**Tautological reasoning**: the expected value restates the implementation, so it holds by
construction.

```typescript
// BAD: expected value is recomputed the way the code computes it
const items = [{ price: 10 }, { price: 5 }];
const expected = items.reduce((sum, i) => sum + i.price, 0);

// GOOD: expected value is an independent, known literal
// calculateTotal([{ price: 10 }, { price: 5 }]) is 15
```

## Boundaries

Isolate at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer a real instance)
- Time/randomness
- File system (sometimes)

Do not isolate:

- Your own classes/modules
- Internal collaborators
- Anything you control

### Designing for substitution

At system boundaries, design interfaces that are easy to substitute:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to substitute
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to substitute
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with
conditional logic:

```typescript
// GOOD: each function is independently substitutable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: substitution requires conditional logic inside the substitute
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each substitute returns one specific shape
- No conditional logic in setup
- Easier to see which endpoints a path exercises
- Type safety per endpoint

## Scope

Keep the change to what the requirement names. A caller that already works is not part of this
slice; note it and move on. When two readings of the requirement lead to different work, state the
one you took rather than picking silently. Record what you could not establish separately from
what you did, so the next reader can tell the two apart without re-deriving either.

---

# Task

You are working in a small Python project. Two files already exist.

`budget/ledger.py`:

```python
"""A spend ledger with a fixed cap."""


class Ledger:
    def __init__(self, cap):
        if cap <= 0:
            raise ValueError("cap must be positive")
        self._cap = cap
        self._spent = 0.0

    def spend(self, amount):
        """Record a spend and return the new remaining balance."""
        self._spent += amount
        return self.remaining()

    def remaining(self):
        return self._cap - self._spent
```

`tests/test_ledger.py`:

```python
import unittest

from budget.ledger import Ledger


class LedgerTest(unittest.TestCase):
    def test_spending_reduces_the_remaining_balance(self):
        ledger = Ledger(10.0)
        self.assertEqual(ledger.spend(4.0), 6.0)

    def test_a_non_positive_cap_is_rejected(self):
        with self.assertRaises(ValueError):
            Ledger(0)
```

## The requirement

A spend that would take the ledger past its cap must be refused. The ledger must reject it and
must be left exactly as it was before the attempt.

## What to produce

You have no tools and cannot run anything. Answer as text, in this order:

1. The one new test you would add to `tests/test_ledger.py`, as code.
2. One or two sentences on what that test does when run against `ledger.py` as it stands now, and
   why.
3. The change to `budget/ledger.py` that makes it pass, as code.
4. Anything you could not establish.

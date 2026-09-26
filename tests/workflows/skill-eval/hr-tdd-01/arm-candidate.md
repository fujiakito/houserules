
# Test-first development

Start from the requested behavior, the project's existing tests and relevant CONTEXT.md/ADRs
when present. Identify the public interface and expected observable result. Reuse a seam already
established by the task or tests; ask only if choosing a different interface changes the scope.

## One vertical slice at a time

1. Choose one observable behavior and a known expected result from the requirement or a worked
   example. Avoid expectations computed by repeating the implementation.
2. Write one test through that public interface. Run it and confirm it fails for the intended
   missing behavior, not an import, environment or fixture error. Capture the command and failure.
3. Implement only enough to satisfy that behavior. Run the same test and observe it pass.
   If the completed slice needs refactoring, preserve its observable behavior and rerun the
   covering tests after the change. Refactoring is optional and stays within the agreed scope.
4. Repeat for the next relevant behavior. Do not write a batch of speculative tests before the
   first implementation. Keep unrelated refactoring out of the loop.
5. Run relevant regression checks. Propose broader refactoring separately; do not turn a small
   fix into an architecture redesign.

Read [tests.md](tests.md) for boundary-focused examples and [mocking.md](mocking.md) when choosing
what to isolate. Internal-call expectations and implementation-shaped assertions are poor evidence.
If no meaningful automated test is possible, record the constraint and actual alternative check;
do not label an unexecuted scenario red/green.

## Result

Report the behavior, the observed red and green checks, remaining gaps and exact changed target.
When work crosses sessions, use the project's existing record or the installed
`.houserules/work/verification.md` template if selected. Create only the record the next consumer
needs. No external tracker, other skill or subagent is required.

## tests.md


## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

## mocking.md


Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

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

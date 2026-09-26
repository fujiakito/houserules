Write the failing test first, then the minimal implementation.

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

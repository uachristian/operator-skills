# Rollback Scope: Mutation Journal, Not Historical Environment Diff

Use this rule for package, runtime, plugin, configuration, and filesystem changes that may be rolled back after other work can occur.

## Invariant

A rollback may reverse only mutations proven to belong to the authorized transaction. A historical full-environment snapshot is evidence and a drift detector; it is not a safe instruction to restore every later difference.

## Required transaction receipt

Before mutation, record:

- exact target and pre-change value/version;
- intended post-change value/version;
- transaction identifier and bounded execution window;
- every package/file/config item the transaction actually added, removed, or changed;
- installer or mutation command and result;
- any exclusive lock or coordination boundary used.

## Automatic rollback

Immediate automatic rollback is acceptable only when:

1. it runs inside the same bounded transaction;
2. no concurrent mutator can modify the target environment;
3. it restores only entries in that transaction's mutation journal;
4. it verifies the restored targets and dependency/runtime health;
5. it fails closed and records partial recovery if restoration is incomplete.

## Explicit or delayed rollback

Before a later rollback:

1. verify each transaction target is still at the expected post-change state;
2. stop if any target has drifted or another change owns it;
3. restore only the exact pre-change versions/values recorded for transaction targets;
4. uninstall only items whose transaction receipt proves this transaction added them;
5. preserve unrelated packages/files/config changes made after the snapshot;
6. run a regression test that introduces an unrelated later change and proves rollback leaves it untouched.

## Prohibited pattern

Do not compare the entire current environment with an old snapshot and reinstall/uninstall every difference. That can destroy legitimate changes made after the transaction.

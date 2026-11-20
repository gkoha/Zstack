# Migrate callers, then delete

When you replace an in-tree internal API, convert every caller and delete the
old API in the same series. No long-lived parallel old and new paths.

- Applies only to internal APIs. External contracts follow
  `keep-external-contracts.md`.
- Use `git grep` and, for many callers, a Coccinelle rule to find and convert
  them. Check strings, macros, and documentation that a symbol search misses.
- Order the series: add the new API, convert callers in reviewable chunks,
  remove the old API.

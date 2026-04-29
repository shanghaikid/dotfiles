# Global aliases

- "pymilvus 的源码" / "pymilvus源码" => `~/workspace/pymilvus`
- "milvus 的源码" / "milvus源码" => `~/workspace/milvus`
- "attu 的源码" / "attu源码" => `~/workspace/attu`
- "milvus node sdk 的源码" / "milvus node sdk源码" => `~/workspace/milvus-sdk-node`
- "zilliz-cloud 的源码" / "zilliz-cloud源码" => `~/workspace/zilliz-cloud`

# Git and PR policy

- New branches must use lowercase, hyphen-separated names with a standard prefix: `feat/`, `fix/`, `chore/`, `docs/`, `test/`, `refactor/`, or `pr/`.
- All commits and amended commits created by the assistant must be signed and DCO-signed, e.g. `git commit -S -s` or `git commit --amend -S -s`.
- Do not create unsigned commits or commits without a `Signed-off-by:` trailer unless the user explicitly overrides this in the current conversation.
- If commit signing fails, stop and report the problem; do not fall back to an unsigned commit.

When creating or updating GitHub PRs:
- Follow the repository's existing PR style/template when available.
- Use a conventional title when appropriate, e.g. `feat: ...`, `fix: ...`, `test: ...`, `docs: ...`, or `chore: ...`.
- If there is no repo-specific template, use:

```md
related: <issue-or-pr-links-if-any>

## Summary
- <concise reviewer-relevant change>
- <concise reviewer-relevant change>

## Test plan
- [x] `<command that was run>`
- [x] `<command that was run>`
```

- Omit `related:` when there are no relevant issues/PRs.
- In `Test plan`, list only commands actually run; use `- [ ] N/A (<reason>)` only when no test applies.

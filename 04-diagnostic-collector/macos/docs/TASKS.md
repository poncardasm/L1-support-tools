# Diagnostic Collector — Tasks (macOS)

## Phase 1: Project Skeleton

- [ ] Create `collector.sh` main script
- [ ] Create `diag/` Python module structure
- [ ] Test basic script execution

---

## Phase 2: Collectors (Bash)

- [ ] Implement system info collector
- [ ] Implement disk info collector with thresholds
- [ ] Implement memory info collector
- [ ] Implement network info collector
- [ ] Implement services collector (launchctl)
- [ ] Implement log collector (log show)
- [ ] Implement updates collector (softwareupdate, brew)
- [ ] Implement active users collector

---

## Phase 3: Python Formatters

- [ ] Implement output parser
- [ ] Implement Markdown formatter
- [ ] Implement HTML formatter
- [ ] Implement JSON formatter

---

## Phase 4: Thresholds

- [ ] Implement disk threshold detection (80%, 90%)
- [ ] Implement memory threshold detection (90%)
- [ ] Flag pending security updates

---

## Phase 5: Upload Feature

- [ ] Implement `--upload` option
- [ ] Support configurable endpoint

---

## Phase 6: Testing

- [ ] Create Python test suite
- [ ] Test threshold detection
- [ ] Test formatters

---

## Phase 7: Homebrew Packaging

- [ ] Create `Formula/diag-collect.rb`
- [ ] Test Homebrew installation

---

## Phase 8: Distribution

- [ ] Host script for `curl | bash`
- [ ] Push to GitHub

---

## Phase 9: Documentation

- [ ] Write `README.md`
- [ ] Document all collected data
- [ ] Add usage examples

# Diagnostic Collector — Tasks (macOS)

## Phase 1: Project Skeleton

- [x] Create `collector.sh` main script
- [x] Create `diag/` Python module structure
- [x] Test basic script execution

---

## Phase 2: Collectors (Bash)

- [x] Implement system info collector
- [x] Implement disk info collector with thresholds
- [x] Implement memory info collector
- [x] Implement network info collector
- [x] Implement services collector (launchctl)
- [x] Implement log collector (log show)
- [x] Implement updates collector (softwareupdate, brew)
- [x] Implement active users collector

---

## Phase 3: Python Formatters

- [x] Implement output parser
- [x] Implement Markdown formatter
- [x] Implement HTML formatter
- [x] Implement JSON formatter

---

## Phase 4: Thresholds

- [x] Implement disk threshold detection (80%, 90%)
- [x] Implement memory threshold detection (90%)
- [x] Flag pending security updates

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

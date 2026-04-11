# IT Knowledge CLI — Tasks (macOS)

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with dependencies
- [ ] Create `it_kb/__init__.py`
- [ ] Create `it_kb/__main__.py`
- [ ] Create `tests/test_search.py`
- [ ] Verify `pip install -e .` works

---

## Phase 2: Vector Database Setup

- [ ] Install sqlite-vss extension
- [ ] Implement `init_db()` function
- [ ] Create articles table schema
- [ ] Test database creation in `~/.config/it-kb/`

---

## Phase 3: Embeddings

- [ ] Integrate Ollama for embeddings
- [ ] Implement `get_embedding()` function
- [ ] Handle Ollama unavailability gracefully
- [ ] Test embedding generation

---

## Phase 4: Indexing

- [ ] Implement `index_directory()` function
- [ ] Parse markdown with frontmatter
- [ ] Extract metadata
- [ ] Store embeddings in SQLite

---

## Phase 5: Search

- [ ] Implement `search()` function
- [ ] Vector similarity search
- [ ] Return top-N results
- [ ] Format output for display

---

## Phase 6: CLI

- [ ] Implement main Click command
- [ ] `--list` to show all articles
- [ ] `--add` to add new article
- [ ] `--index` to index directory
- [ ] `--top N` for result count

---

## Phase 7: Testing

- [ ] Create test fixtures
- [ ] Test indexing
- [ ] Test search
- [ ] Test embedding fallback

---

## Phase 8: Homebrew Packaging

- [ ] Create `Formula/it-kb.rb`
- [ ] Test Homebrew installation

---

## Phase 9: Documentation

- [ ] Write `README.md`
- [ ] Document Ollama setup on macOS
- [ ] Add usage examples

---

## Phase 10: Publish

- [ ] Push to GitHub
- [ ] Optional: PyPI
- [ ] Optional: Homebrew tap

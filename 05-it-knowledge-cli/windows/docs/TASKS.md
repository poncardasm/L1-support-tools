# IT Knowledge CLI — Tasks (Windows)

## Phase 1: Project Skeleton

- [x] Create `pyproject.toml` with dependencies
- [x] Create `it_kb/__init__.py`
- [x] Create `it_kb/__main__.py`
- [x] Create `tests/test_search.py`
- [x] Verify `pip install -e .` works

---

## Phase 2: Vector Database Setup

- [x] Configure sqlite-vss extension for Windows
- [x] Implement `init_db()` function
- [x] Create articles table schema
- [x] Test database creation in `%APPDATA%\it-kb\`

---

## Phase 3: Embeddings

- [x] Integrate Ollama for embeddings
- [x] Implement `get_embedding()` function
- [x] Handle Ollama unavailability gracefully
- [x] Test embedding generation

---

## Phase 4: Indexing

- [x] Implement `index_directory()` function
- [x] Parse markdown with frontmatter
- [x] Extract metadata (id, title, category, last_updated)
- [x] Store embeddings in SQLite

---

## Phase 5: Search

- [x] Implement `search()` function
- [x] Vector similarity search
- [x] Return top-N results
- [x] Format output for display

---

## Phase 6: CLI

- [x] Implement main Click command
- [x] `--list` to show all articles
- [x] `--add` to add new article
- [x] `--index` to index directory
- [x] `--top N` for result count

---

## Phase 7: Testing

- [ ] Create test fixtures (sample KB articles)
- [ ] Test indexing
- [ ] Test search
- [ ] Test embedding fallback

---

## Phase 8: Windows Build

- [ ] Create PyInstaller spec file
- [ ] Bundle sqlite-vss DLL
- [ ] Build standalone executable
- [ ] Test `it-kb.exe`

---

## Phase 9: Documentation

- [ ] Write `README.md`
- [ ] Document Ollama setup on Windows
- [ ] Add usage examples

---

## Phase 10: Publish

- [ ] Push to GitHub
- [ ] Attach `.exe` to release
- [ ] Optional: PyPI

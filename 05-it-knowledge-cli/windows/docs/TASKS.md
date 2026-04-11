# IT Knowledge CLI — Tasks (Windows)

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with dependencies
- [ ] Create `it_kb/__init__.py`
- [ ] Create `it_kb/__main__.py`
- [ ] Create `tests/test_search.py`
- [ ] Verify `pip install -e .` works

---

## Phase 2: Vector Database Setup

- [ ] Configure sqlite-vss extension for Windows
- [ ] Implement `init_db()` function
- [ ] Create articles table schema
- [ ] Test database creation in `%APPDATA%\it-kb\`

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
- [ ] Extract metadata (id, title, category, last_updated)
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

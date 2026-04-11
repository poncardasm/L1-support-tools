# IT Knowledge CLI — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`, `python-frontmatter`, `mistune`, `requests`, `numpy`
- [ ] Create `it_kb/__init__.py`
- [ ] Create `it_kb/__main__.py` entry point
- [ ] Create `tests/test_search.py` with empty test class
- [ ] Create `kb/` directory with authentication/, email/, networking/ subdirs
- [ ] Create `.gitignore`
- [ ] Verify `pip install -e .` works + `it-kb --help` prints

---

## Phase 2: Config + Parser

- [ ] Create `config.yaml` with embedding provider, model, database path settings
- [ ] Implement `load_config()` from `~/.config/it-kb/config.yaml`
- [ ] Implement `parse_article()` with frontmatter + content extraction
- [ ] Test: frontmatter id, title, category correctly extracted from fixture markdown

---

## Phase 3: Embedding Integration

- [ ] Implement `embed_text()` for Ollama endpoint
- [ ] Implement OpenAI-compatible fallback with configurable endpoint
- [ ] Test: Ollama returns valid embedding vector (or graceful error if Ollama down)
- [ ] Test: OpenAI-compatible fallback fires when configured
- [ ] Chunking: articles > 8000 chars split before embedding

---

## Phase 4: Vector Storage

- [ ] Create SQLite schema: `kb_articles` + `article_vectors` tables
- [ ] Implement `init_db()` — create tables if not exist
- [ ] Implement `store_article()` + `store_vectors()` — INSERT OR REPLACE
- [ ] Implement pure Python cosine similarity for search fallback (no sqlite-vss required)
- [ ] Verify: re-indexing same article replaces old entry (no duplicates)

---

## Phase 5: Indexer

- [ ] Implement `index_directory()` — walk directory, parse + embed + store
- [ ] Implement `add_article()` — index single file
- [ ] Progress output during long indexing jobs
- [ ] Test: `kb/` directory of 6 articles indexes without error
- [ ] Test: `INSERT OR REPLACE` handles duplicate IDs correctly

---

## Phase 6: Search

- [ ] Implement `search()` — embed query + vector similarity + recency ranking
- [ ] Implement `print_results()` — formatted output with similarity score
- [ ] Wire `--top N` to control result count
- [ ] Test: "reset password" returns EntraID/AD password articles as top result
- [ ] Test: "outlook freezing" returns Outlook profile articles
- [ ] Test: empty index returns helpful error message

---

## Phase 7: CLI Commands

- [ ] Wire `it-kb "query"` — main search
- [ ] Wire `--list` — show all indexed articles
- [ ] Wire `--add <path>` — add single article
- [ ] Wire `--index <path>` — bulk index directory
- [ ] Wire `--top N` — result count override
- [ ] Verify: all 4 modes work from CLI

---

## Phase 8: Default KB Library

- [ ] Create `kb/authentication/reset-entra-password.md` with frontmatter + content
- [ ] Create `kb/authentication/entra-mfa-setup.md`
- [ ] Create `kb/email/outlook-profile-reset.md`
- [ ] Create `kb/email/pst-recovery.md`
- [ ] Create `kb/networking/vpn-dns-override.md`
- [ ] Create `kb/networking/vpn-macos-setup.md`
- [ ] Verify: `it-kb --index kb/` runs without error

---

## Phase 9: Testing

- [ ] Search tests: top results match expected KB articles for known queries
- [ ] Parser tests: frontmatter correctly extracted
- [ ] Indexer tests: INSERT OR REPLACE no duplicates
- [ ] Embedding tests: Ollama timeout handled gracefully
- [ ] `pytest tests/ -v` passes

---

## Phase 10: Docs + Polish

- [ ] `README.md` with install, config setup, all CLI options, example session
- [ ] Tag v1.0.0
- [ ] Commit per project

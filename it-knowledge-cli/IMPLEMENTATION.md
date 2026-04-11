# IT Knowledge CLI — Implementation Plan

## 1. Architecture

Zero external services after setup. Embeddings via local Ollama. Vector search via sqlite-vss. All data stored locally.

```
it-knowledge-cli/
├── it_kb/
│   ├── indexer.py        # build embeddings, store in sqlite-vss
│   ├── search.py         # query embedding + vector search
│   ├── config.py         # load config.yaml
│   ├── parser.py         # frontmatter + content extraction
│   ├── __init__.py
│   └── __main__.py
├── kb/                   # default KB article library
│   ├── authentication/
│   ├── email/
│   └── networking/
└── tests/
```

## 2. Embedding Integration

### 2.1 Ollama Client

```python
import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"

def embed_text(text: str, model: str = "nomic-embed-text") -> list[float]:
    resp = requests.post(OLLAMA_URL, json={"model": model, "prompt": text}, timeout=30)
    resp.raise_for_status()
    return resp.json()["embedding"]
```

Fallback to OpenAI-compatible endpoint if configured:
```python
def embed_text(text: str, config: dict) -> list[float]:
    if config.get("openai_endpoint"):
        resp = requests.post(
            f"{config['openai_endpoint']}/embeddings",
            json={"input": text, "model": config.get("embedding_model", "gemini-embedding-2-preview")},
            timeout=30
        )
        return resp.json()["data"][0]["embedding"]
    # else: use Ollama
```

## 3. SQLite + VSS Setup

### 3.1 Schema

```python
import sqlite3

CREATE TABLE kb_articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    content TEXT,
    products TEXT,          -- JSON array
    last_updated TEXT,
    embedding_id INTEGER,   -- FK to vss_articles
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT NOT EXISTS vss_articles (
    id INTEGER PRIMARY KEY,
    article_id TEXT,
    embedding BLOB
);

-- VSS virtual table (requires sqlite-vss extension)
CREATE VIRTUAL TABLE article_embeddings USING vag;

INSERT INTO article_embeddings (id, article_id, embedding)
VALUES (?, ?, ?);
```

### 3.2 sqlite-vss

Note: `sqlite-vss` requires loading the extension at connection time. For cross-platform compatibility, use `sqlite-vss` as a Python wheel or fallback to pure SQLite with a custom kNN implementation.

Alternative (no extension, pure Python):
```python
import numpy as np
from numpy.linalg import norm

def cosine_similarity(a: list[float], b: list[float]) -> float:
    return np.dot(a, b) / (norm(a) * norm(b))

def search_vectors(embeddings: list[tuple], query_vec: list[float], top_k: int):
    results = sorted(
        [(idx, cosine_similarity(vec, query_vec)) for idx, vec in embeddings],
        key=lambda x: x[1],
        reverse=True
    )[:top_k]
    return results
```

This avoids the sqlite-vss extension dependency and works on any Python platform.

## 4. Indexer (indexer.py)

### 4.1 Parse Markdown

```python
import frontmatter

def parse_article(filepath: Path) -> dict:
    post = frontmatter.load(filepath)
    return {
        "id": post.metadata.get("id", filepath.stem),
        "title": post.metadata.get("title", filepath.stem),
        "category": post.metadata.get("category", "general"),
        "content": post.content,
        "products": post.metadata.get("products", []),
        "last_updated": post.metadata.get("last_updated", ""),
    }
```

### 4.2 Build Index

```python
def index_directory(path: Path, config: dict):
    for md_file in path.rglob("*.md"):
        article = parse_article(md_file)
        embedding = embed_text(article["content"][:8000], config)  # first 8000 chars
        store_article(article, embedding)
    print(f"Indexed {count} articles")
```

Chunk long articles (split by `##` headings) for better retrieval granularity.

### 4.3 Store

```python
def store_article(article: dict, embedding: list[float]):
    conn = get_db()
    cursor = conn.execute("""
        INSERT OR REPLACE INTO kb_articles (id, title, category, content, products, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [article["id"], article["title"], article["category"],
          article["content"], json.dumps(article["products"]), article["last_updated"]])
    
    article_db_id = cursor.lastrowid
    conn.execute("""
        INSERT INTO article_vectors (article_id, embedding)
        VALUES (?, ?)
    """, [article_db_id, sqlite3.Binary(np.array(embedding).astype(np.float32).tobytes())])
    conn.commit()
```

## 5. Search (search.py)

### 5.1 Query

```python
def search(query: str, config: dict, top_k: int = 5) -> list[SearchResult]:
    query_embedding = embed_text(query, config)
    
    # Load all embeddings + compute similarity
    conn = get_db()
    rows = conn.execute("SELECT article_id, embedding FROM article_vectors").fetchall()
    
    results = []
    for row in rows:
        stored_vec = np.frombuffer(row["embedding"], dtype=np.float32)
        sim = cosine_similarity(stored_vec, query_embedding)
        article = conn.execute(
            "SELECT * FROM kb_articles WHERE ROWID = ?", (row["article_id"],)
        ).fetchone()
        results.append(SearchResult(article, sim))
    
    # Sort + dedupe by article ID
    results.sort(key=lambda r: r.similarity, reverse=True)
    
    # Apply recency weighting
    for r in results:
        if r.article["last_updated"]:
            days_old = (datetime.now() - parse_date(r.article["last_updated"])).days
            r.score *= (1.0 / (1.0 + days_old * 0.001))  # small recency penalty
    
    return results[:top_k]
```

### 5.2 SearchResult

```python
SearchResult = namedtuple("SearchResult", ["article", "similarity", "score"])
```

## 6. CLI (__main__.py)

```python
@click.group()
def it_kb():
    """IT Knowledge Base — offline Q&A for L1 support."""

@it_kb.command()
@click.argument("query", required=False)
@click.option("--list", "list_all", is_flag=True)
@click.option("--add", "add_path", type=click.Path())
@click.option("--index", "index_path", type=click.Path())
@click.option("--top", type=int, default=5)
def search(query, list_all, add_path, index_path, top):
    if list_all:
        list_articles()
    elif add_path:
        add_article(Path(add_path))
    elif index_path:
        index_directory(Path(index_path))
    elif query:
        results = search(query, top_k=top)
        print_results(results)
    else:
        click.echo("Use --list, --add <path>, --index <path>, or pass a query.")
```

## 7. Configuration (config.yaml)

```yaml
embedding:
  provider: ollama  # or "openai-compatible"
  model: nomic-embed-text
  endpoint: http://localhost:11434/api/embeddings

openai_compatible:
  endpoint: https://your-endpoint/v1beta/openai/
  model: gemini-embedding-2-preview

database:
  path: ~/.config/it-kb/index.db

search:
  default_top_k: 5
  recency_weight: 0.001
```

## 8. Default KB Articles

Pre-included articles in `kb/`:
- `authentication/reset-entra-password.md`
- `authentication/entra-mfa-setup.md`
- `email/outlook-profile-reset.md`
- `email/pst-recovery.md`
- `networking/vpn-dns-override.md`
- `networking/vpn-macos-setup.md`

## 9. Known Pitfalls

1. **sqlite-vss extension** — not available as a pip wheel on all platforms. Use pure Python cosine similarity fallback. Document both options.
2. **Embedding timeout** — Ollama can be slow on large KB indexing. Use chunked indexing with progress output.
3. **Article too long for embedding** — truncate at 8000 chars before embedding. Chunk long articles by heading.
4. **Duplicate IDs** — `INSERT OR REPLACE` handles re-indexing cleanly.
5. **Empty index** — if `--index` has never been run, `--search` should return a helpful error with instructions to run `--index`.
6. **OpenAI-compatible endpoint** — the endpoint format varies by provider. Document the exact format for Gemini and other providers.

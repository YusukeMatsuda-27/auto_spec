1. .envを作成して仕様書を作成するディレクトリのパスとgeminiのAPIKEYを記述

```bash
PROJECT_DIR = ""
GEMINI_API_KEY = ""
```

2. main.pyを実行

```bash
uv init
uv sync
uv run src/main.py
```

* repomix-output.xmlとspec.mdが出力される
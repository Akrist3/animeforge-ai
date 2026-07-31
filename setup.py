from pathlib import Path

ROOT = Path(__file__).parent

folders = [
    "backend/app/api",
    "backend/app/core",
    "backend/app/db",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/agents",
    "backend/app/memory",
    "backend/app/orchestrator",
    "backend/app/utils",
    "backend/tests",

    "frontend/app",
    "frontend/components",
    "frontend/hooks",
    "frontend/lib",
    "frontend/styles",
    "frontend/public",
    "frontend/types",

    "docs",
    "docker",
    "scripts",
    "prompts",
    "tests",
    ".github"
]

files = [
    "README.md",
    ".gitignore",
    "LICENSE",

    "backend/main.py",
    "backend/requirements.txt",

    "docs/01_PRD.md",
    "docs/02_SRS.md",
    "docs/03_ARCHITECTURE.md",
    "docs/04_DATABASE.md",
    "docs/05_API.md",
    "docs/06_AI_AGENTS.md",
    "docs/07_UI_UX.md",
    "docs/08_DEPLOYMENT.md",
    "docs/09_ROADMAP.md"
]

for folder in folders:
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

for file in files:
    path = ROOT / file
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("✅ AnimeForge AI project initialized successfully!")
# RedShelf

RedShelf is a production-ready, static academic PDF library built with Material for MkDocs. It provides a professional interface for organising, browsing, searching, previewing and downloading research papers, PhD documents, books, reports, conference materials, guidelines and ethics resources.

The project has no backend and no database. Markdown, PDFs and configuration files are the complete source of truth, making the library straightforward to review, version and deploy to GitHub Pages.

## Features

- Full client-side search powered by Material for MkDocs
- Structured sidebar, tabbed navigation, breadcrumbs and previous/next links
- Light, dark and system-preference colour modes
- Responsive category and featured-document cards
- Tags and a dedicated tag index
- In-browser PDF preview
- View and download actions
- Copy-citation interaction with accessible feedback
- DOI and external-record links
- Recently added and related-document pathways
- Custom theme override, CSS and JavaScript
- Strict automated build and GitHub Pages deployment

## Requirements

- Python 3.10 or newer
- `pip`
- Git

## Installation

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run locally

```bash
mkdocs serve
```

Open `http://127.0.0.1:8000/`. MkDocs watches the source files and refreshes the site as you edit.

## Build

The production build must complete without warnings:

```bash
mkdocs build --strict
python scripts/validate_site.py
```

The generated static site is written to `site/`, which is intentionally ignored by Git.

## Deploy to GitHub Pages

The workflow in `.github/workflows/deploy.yml` builds and deploys the site whenever a commit is pushed to `main`.

Before the first deployment:

1. Create an empty GitHub repository.
2. Update `site_url`, `repo_url`, `repo_name`, `edit_uri` and the GitHub social link in `mkdocs.yml`.
3. Add the GitHub repository as the `origin` remote.
4. In the GitHub repository, open **Settings → Pages**.
5. Set **Source** to **GitHub Actions**.
6. Push the `main` branch.

The workflow runs `mkdocs build --strict`, uploads the `site/` output and publishes it through GitHub Pages.

## Folder structure

```text
RedShelf/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docs/
│   ├── assets/
│   │   ├── css/
│   │   │   └── extra.css
│   │   ├── images/
│   │   │   ├── favicon.svg
│   │   │   └── logo.svg
│   │   ├── js/
│   │   │   └── extra.js
│   │   └── pdf/
│   ├── books/
│   ├── conference-materials/
│   ├── ethics-documents/
│   ├── guidelines/
│   ├── overrides/
│   │   └── main.html
│   ├── phd-documents/
│   ├── reports/
│   ├── research-papers/
│   ├── about.md
│   ├── index.md
│   ├── recently-added.md
│   └── tags.md
├── scripts/
│   └── generate_placeholder_pdfs.py
├── .gitignore
├── mkdocs.yml
├── README.md
└── requirements.txt
```

## Add a PDF

1. Confirm that you have permission to store and redistribute the document.
2. Copy the PDF to `docs/assets/pdf/`.
3. Use a lowercase, hyphen-separated filename, for example `community-health-review-2026.pdf`.
4. Copy one of the example document pages into the appropriate category.
5. Replace the title, author, journal, year, category, tags, DOI, abstract, citation and date added.
6. Update every PDF URL and the preview `title`.
7. Add the page to its category index and to `nav` in `mkdocs.yml`.
8. If appropriate, add it to `docs/recently-added.md` and the homepage.
9. Run `mkdocs build --strict`.

### Regenerate the placeholder PDFs

The six demonstration PDFs are created with ReportLab:

```bash
pip install reportlab
python scripts/generate_placeholder_pdfs.py
```

Generated files are clearly marked as examples and contain no real research findings.

## Add a category

1. Create a directory under `docs/`, or under `docs/research-papers/` for a research topic.
2. Add an `index.md` that describes the collection and lists its documents.
3. Add the category to `nav` in `mkdocs.yml`.
4. Add a homepage category card if the collection is important to most users.
5. Link related documents to and from the new collection.
6. Run the strict build to catch missing navigation entries and broken links.

## Customise colours

The Material palette is configured under `theme.palette` in `mkdocs.yml`.

RedShelf's extended palette is defined at the top of `docs/assets/css/extra.css`:

```css
:root {
  --rs-red-500: #c73642;
  --rs-red-600: #b4232d;
  --rs-red-700: #921d26;
}
```

Update those variables to change cards, buttons, borders and interface accents consistently. Maintain sufficient contrast for text and interactive states.

## Customise the homepage

Edit `docs/index.md`. The homepage uses semantic HTML inside Markdown for:

- hero content and actions
- category cards
- featured documents
- recently added resources
- the document-contribution workflow

Reuse the existing `rs-*` classes to preserve responsive behaviour. Add new presentation rules to `docs/assets/css/extra.css`, and keep content-specific text in Markdown.

## Document-page checklist

Every document page should contain:

- title
- author or editor
- journal or publication
- year
- category
- tags
- DOI
- short abstract
- View PDF button
- Download PDF button
- citation and Copy Citation button
- date added
- related documents

The six included pages are safe templates to copy.

## Production checklist

- Replace all placeholder repository URLs in `mkdocs.yml`.
- Replace or remove the example documents.
- Confirm PDF licences and permissions.
- Check every DOI and citation against an authoritative source.
- Test keyboard navigation and both colour modes.
- Run `mkdocs build --strict`.
- Run `python scripts/validate_site.py`.
- Confirm GitHub Pages uses **GitHub Actions** as its source.

## Initial Git commands

```bash
git add .
git commit -m "Initial RedShelf"
git push origin main
```

Add a remote first if necessary:

```bash
git remote add origin https://github.com/saprimad/redshelf.git
```

# Wordcraft Comprehensive

A static English–Urdu vocabulary website with 22,632 unique headwords: 5,630 full learning entries and 17,002 additional English dictionary reference entries. The original 5,521 word IDs are preserved for saved progress.

Includes all 2,999 headwords from the supplied AlHayatAcademy aptitude vocabulary bank, 3,000 existing expression lessons, and 200 original contextual lessons across 25 practical areas. Search combines both vocabulary collections. Topic pathways, quizzes, spelling, dictation, writing, speaking and scheduled review are included.

## Content quality and coverage

Reference entries use licensed Princeton WordNet 3.0 definitions. They are English-only references, not completed Urdu lessons. Source decks contribute candidate headwords rather than copied publisher definitions. Inflected forms are linked to a headword when a single reliable lemma is available. Distinct senses remain within one entry.

`coverage-audit.json` records extraction sources and counts. `word-review-queue.json` retains 7,115 unresolved candidates, including malformed, ambiguous and multiword strings. `phrase-candidates.json` retains 7,668 additional expressions requiring review. These queues are not presented as finished vocabulary. This edition does not claim that every incidental word in every repository or PDF has been extracted or independently reviewed. Learning bands and examination tags are guidance, not official certification.

## Run and deploy

No npm installation, API key or build step is required. Upload the contents of this folder to your existing repository root, retaining `index.html` at the root. GitHub Pages can serve it from the selected branch and root folder. Keep all JSON, JavaScript, CSS and licence files together.

For local use, run `python3 -m http.server 8000` in this folder and open `http://localhost:8000`. JSON loading requires an HTTP server.

## Validation and rebuilding

Run `node tests/qa.cjs` for the data and mocked interaction checks. These checks do not replace browser layout testing.

The consolidation script in `scripts/build-comprehensive.py` requires the original extracted source repositories and WordNet archive under the sibling `review` directory. Generated runtime data is bundled, so rebuilding is not required to run or deploy the site. The source review snapshots are not redistributed in this package.

## Attribution

Retain `WORDNET_LICENSE.txt` and all existing licence and source attribution files. Consult the coverage audit and source metadata before reusing third-party material separately.

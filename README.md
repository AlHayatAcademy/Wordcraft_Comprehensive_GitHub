# Wordcraft Studio — updated existing repository

A focused static vocabulary application built as additive layers over the existing HTML/CSS/JavaScript architecture. No framework, npm installation, backend or API key is required.

## Learning experience

- A calm daily learning desk with one recommended next action.
- 24 original core lessons, six words each: first conversations → everyday communication → study and work → demanding reading.
- 144 sense-specific definitions, natural complete examples, Urdu meanings and Urdu example translations.
- Understand → recall → context → learner writing, with saved sessions and scheduled reviews.
- 25 practical topic electives with 200 contextual lessons.
- Small extended vocabulary sets, ordered by internal band, source frequency and example completeness. This is a heuristic, not a verified proficiency ranking.
- Search refreshes after a short typing pause and retains the caret; classification loads without blocking core lessons.
- Mobile bottom navigation; desktop sidebar; light and dark themes; touch targets; visible keyboard focus; RTL Urdu; reduced-motion support.
- Existing expressions, word families, pronunciation aids, quizzes, reading, recording, Writing/Speaking tabs, notebook and backups remain accessible through More tools or word details.

## Verified inventory

| Collection | Unique entries |
| --- | ---: |
| Full word entries | 5,718 |
| English dictionary reference headwords | 16,934 |
| Combined unique headwords | 22,652 |
| Existing expression entries | 3,000 |
| Total stable entry keys across the collections | 25,652 |

All 5,630 previous word IDs and 3,000 expression IDs are preserved. Sixty-eight previous reference words are promoted to complete bilingual entries without duplicate headwords; their prior reference IDs resolve through aliases. Twenty genuinely new headwords/phrases are added across the starter and category lessons. Existing browser progress uses the same `wordcraft-v1` storage key. Backup restore preserves the new route preferences and session as well as original word and expression progress.

## Type, topic, register and origin

`taxonomy.json` is a sense-aware metadata sidecar. Type/use categories overlap without duplicating entries or progress. Category filters require compatible metadata on the same teaching sense. Independent filters include category, topic, part of speech, register, expression structure, publisher/source, internal band, borrowing origin and learning/editorial status. Search, active filter chips, counts and reset work with these filters.

Every one of the **25,652 stable entry keys** now has a category. **1,482 entries have individually inspected teaching-sense classifications** (556 full word entries, 790 expression entries and 136 dictionary entries). The other **24,170 entries receive the user-requested General vocabulary fallback**. General includes everyday vocabulary and entries without a confirmed specialist label; it does not imply that every item is common, easy or neutral in register. There are no unassigned entries.

The new pass records 1,140 sense decisions, including an inspected set of 500 expression meanings and 160 natural combinations. Specific homographs are selected by explicit sense index, including electrical *current*, financial *bond*, cellular *nucleus* and literary *apostrophe*. Thirty selected senses have original English–Urdu explanations, examples, translated examples and usage notes. Original entry records and IDs remain intact; selected teaching senses are stored in the metadata sidecar. Cards and the Writing/Speaking tabs use the selected sense. A first-sense Urdu gloss is never silently attached to a different sense.

| Category | Unique entries |
| --- | ---: |
| General vocabulary | 24,370 |
| Academic vocabulary | 154 |
| Formal vocabulary | 47 |
| Informal & conversational | 46 |
| Idioms | 499 |
| Phrasal verbs | 74 |
| Collocations | 172 |
| Fixed expressions | 17 |
| Proverbs & sayings | 18 |
| Discourse & linking expressions | 21 |
| Technical & subject-specific | 288 |
| Business & workplace | 143 |
| Literary vocabulary | 32 |
| Slang | 4 |
| Abbreviations & acronyms | 12 |
| Borrowed words & expressions | 2 |

Category counts overlap. Their sum is not the overall inventory.

### Accuracy and remaining refinement

Complete organisational classification is not a claim of a complete linguistic accuracy review. General fallbacks keep **7,372 learning entries** and **16,798 dictionary entries** available without speculative specialist labels. Uncertain register and borrowing origin remain unspecified. `classification-review.json` lists these already-assigned entries for optional specialist refinement; `classification-decisions.json` records the explicit decisions. Inherited meanings, examples and Urdu translations still vary in quality. English-only references remain English-only except for the explicitly authored bilingual teaching senses.

Type-aware practice includes contextual recall, idiom/proverb meaning matching, phrasal particles and collocations. Curated combination gaps use explicit distractors; other combinations use contextual meanings to avoid falsely marking a valid alternative verb as wrong. Correct answers and explanations appear after each attempt and positions vary. General learning entries are available for practice; reference entries retain their spelling tools. This is lexical practice, not a verified grammar or proficiency assessment.

New guided sessions credit a word at most once per day, when new or due. Hints and repeated answer checks do not inflate retention. Context and learner writing are guided practice, not automatic grammar scores. Optional inherited quizzes keep their original scoring; historical progress remains unchanged.

## Deploy to the existing repository

1. Back up your learning progress from the current site.
2. Extract this ZIP and replace the files in your existing repository root. `index.html` must remain at the root.
3. Keep all JSON, scripts, styles, assets and licences together.
4. Commit and push using your existing GitHub Desktop / Pages workflow.
5. After deployment finishes, use Ctrl + Shift + R once. The service-worker cache version has changed.

Keep the same domain and repository URL to retain browser-local progress. Changing the origin does not automatically transfer browser storage; use a backup to transfer it.

## Run and check

For local use: `python3 -m http.server 8000`, then open `http://localhost:8000`.

Run:

```sh
node tests/qa.cjs
node tests/startup.cjs
node tests/classification-startup.cjs
node tests/studio.cjs
```

Checks cover data integrity, preserved IDs and reference aliases, complete category assignment, General fallback practice, selected senses, startup with delayed classification downloads, overlapping category counts, combined filters, empty states, session flow, guided/assisted answers, scheduling, writing, expression progress, backup restore and retained Writing/Speaking tools. JavaScript syntax and responsive/accessibility hooks were checked. **Browser-based visual QA was unavailable in this environment**; no claim is made that every browser/device layout has been visually verified.

The generated runtime files are bundled. Run `python3 scripts/build-studio.py`, `python3 scripts/build-taxonomy.py`, `python3 scripts/add-category-lessons.py`, then `python3 scripts/classify-complete.py` in that order to regenerate the authored additions from bundled sources. The earlier comprehensive consolidation script additionally requires original source repository snapshots and WordNet data; it is not required for deployment.

## Evidence and attribution

The learning design uses retrieval and spaced practice, contextual examples and learner output. It supports part of a balanced language programme, not all language skills or an official proficiency test.

- Paul Nation, vocabulary teaching principles: https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/my-ideal-vocabulary-teaching-course.pdf
- The Learning Scientists, effective learning strategies: https://www.learningscientists.org/blog/2019/11/28-1

Retain `WORDNET_LICENSE.txt` and existing source/licence files. New lesson text is original. `preservation-manifest.json`, `reference-aliases.json`, the coverage audit and quality audit make the update inspectable.

Slang usage sources (definitions and examples in the application are original teaching text):

- https://www.merriam-webster.com/slang/no-cap
- https://www.merriam-webster.com/slang/rizz
- https://www.merriam-webster.com/wordplay/salty-meaning
- https://www.merriam-webster.com/wordplay/lit-meaning-origin

`category-additions.json` records stable keys and source notes. Multiword expressions can be full learning entries in `data.json`; their structural type is stored in the taxonomy sidecar. They use the same word-progress system without duplicating expression-bank entries.

Additional meaning checks for selected technical senses (teaching prose and examples are original):

- NHLBI, anemia: https://www.nhlbi.nih.gov/health/anemia
- MedlinePlus, hypertension: https://medlineplus.gov/highbloodpressure.html
- NHGRI, nucleus: https://www.genome.gov/genetics-glossary/Nucleus
- NHGRI, genome: https://www.genome.gov/genetics-glossary/Genome
- Cornell LII, conviction: https://www.law.cornell.edu/wex/conviction
- SEC Investor.gov, bonds: https://www.investor.gov/introduction-investing/investing-basics/glossary/bonds

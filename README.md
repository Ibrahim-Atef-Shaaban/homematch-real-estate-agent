# HomeMatch — a personalized real estate agent

A RAG application that turns a buyer's plain-language wishlist into personalized
property recommendations: it retrieves the listings that genuinely match, then rewrites
each description to lead with what *this* buyer said they cared about — without
inventing facts about the property.

## How it works

1. **Generate the catalogue** — prompt `gpt-3.5-turbo` for eleven realistic listings,
   constrained by a Pydantic schema (`RealEstateListing`) and parsed with
   `PydanticOutputParser`, so every row comes back with a validated neighborhood,
   price, bed/bath count, size and description. Saved to `listings.csv`.
2. **Index** — embed each listing with `OpenAIEmbeddings` and store it in a Chroma
   vector database.
3. **Retrieve** — embed the buyer's stated preferences and pull the closest listings
   by similarity.
4. **Personalize** — feed the retrieved listings back through the LLM with an augmented
   prompt that re-frames each description around the buyer's priorities while staying
   factual about the property itself.

The schema-constrained generation step is what makes the rest work: because `price`,
`bedrooms` and `house_size` are typed (`NonNegativeInt`) rather than free text, the
listings are queryable data rather than prose.

## Example

Buyer preference:

> "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating
> system."

The plain retrieval prompt returns the nearest listings as written. The augmented
prompt returns the same listings with their descriptions rewritten to surface the
garden space, garage and efficiency features first — see the executed outputs at the
bottom of the notebook for the side-by-side comparison.

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env     # then add your OpenAI key
jupyter notebook HomeMatch.ipynb
```

Credentials are read from the environment via `python-dotenv` — no key is written into
the notebook or into `HomeMatch.py`. Set `OPENAI_API_BASE` if you are routing through a
proxy or an alternative OpenAI-compatible endpoint.

This project pins `langchain==0.0.305` with `pydantic<2`; install it into a clean
virtualenv rather than an existing environment with newer LangChain packages.

### The vector store is not in this repository

`chroma/` is gitignored. It is rebuilt from `listings.csv` by re-running the indexing
cell, which costs a fraction of a cent in embedding calls. `listings.csv` *is*
committed, so you can skip the generation step and go straight to indexing.

## Repository layout

```
HomeMatch.ipynb    The full pipeline, with executed outputs
HomeMatch.py       Script entry point (env setup) for running outside a notebook
listings.csv       The 11 generated listings — synthetic, no real properties
.env.example       Template for your API key
```

## Attribution

Built as a project for the Udacity Generative AI Nanodegree. The notebook scaffold is
Udacity course material, provided under Udacity's educational-content license. All
listings are LLM-generated; no real property or person is described.

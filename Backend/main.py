from fastapi import FastAPI
from pydantic import BaseModel
from scraper import enrich_company
from fastapi.middleware.cors import CORSMiddleware

import json
import os

app = FastAPI(
    title="Prospect Research Agent API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_FILE = "results.json"


# ==========================
# Request Schema
# ==========================

class CompanyRequest(BaseModel):
    website_name: str
    url: str


# ==========================
# Utility Functions
# ==========================

def load_results():

    if not os.path.exists(RESULTS_FILE):
        return []

    try:
        with open(
            RESULTS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read().strip()

            if not content:
                return []

            return json.loads(content)

    except Exception:
        return []


def save_results(results):

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )


# ==========================
# Routes
# ==========================

@app.get("/")
def home():

    return {
        "message": "Backend Working"
    }


@app.post("/enrich")
def enrich(data: CompanyRequest):

    result = enrich_company(
        data.url
    )

    # Keep user-provided website name
    result["website_name"] = data.website_name

    all_results = load_results()

    all_results.append(result)

    save_results(all_results)

    return result


@app.get("/results")
def get_results():

    return load_results()
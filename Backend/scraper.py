import json
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

# ================================
# 🏆 Hackathon Template Notebook
# Prospect Research Agent
# ================================

# ========= CONFIG =========
# 🔑 Add your API key here
from groq import Groq

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key=GROQ_API_KEY
)

# Request helper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def safe_request(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            return response.text

    except Exception as e:
        print(f"Request failed for {url}: {e}")

    return ""

# html cleaner

def clean_text(html):

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe"
    ]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    text = re.sub(r"\s+", " ", text)

    return text

# email extraction

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def extract_emails(text):

    emails = re.findall(
        EMAIL_PATTERN,
        text
    )

    return sorted(
        list(set(emails))
    )

# phone extraction

PHONE_PATTERN = r"\+?\d[\d\s\-\(\)]{8,}"

def extract_phones(text):

    phones = re.findall(
        PHONE_PATTERN,
        text
    )

    cleaned = []

    for phone in phones:

        phone = phone.strip()

        if len(phone) >= 10:
            cleaned.append(phone)

    return sorted(
        list(set(cleaned))
    )

# page discovery

IMPORTANT_KEYWORDS = [
    "about",
    "company",
    "contact",
    "service",
    "services",
    "solution",
    "solutions",
    "product",
    "products",
    "who-we-are"
]

def get_relevant_pages(base_url):

    pages = set()

    pages.add(base_url)

    html = safe_request(base_url)

    if not html:
        return list(pages)

    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]

        try:

            score = max(
                fuzz.partial_ratio(
                    href.lower(),
                    keyword
                )
                for keyword in IMPORTANT_KEYWORDS
            )

            if score > 80:

                full_url = urljoin(
                    base_url,
                    href
                )

                pages.add(full_url)

        except:
            pass

    return list(pages)[:8]

# website scraper

def scrape_company(base_url):

    pages = get_relevant_pages(base_url)

    combined_text = ""

    for page in pages:

        html = safe_request(page)

        if not html:
            continue

        text = clean_text(html)

        combined_text += "\n\n"
        combined_text += text[:5000]

        time.sleep(1)

    return combined_text[:25000]

import json
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def enrich_with_ai(text):

    prompt = f"""
You are a B2B company research analyst.

Rules:
- Use ONLY information present in the text.
- Never hallucinate.
- If information is unavailable, return "".
- Return ONLY valid JSON.

Schema:

{{
    "website_name":"",
    "company_name":"",
    "address":"",
    "core_service":"",
    "target_customer":"",
    "probable_pain_point":"",
    "outreach_opener":""
}}

TEXT:
{text[:5000]}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        start = raw.find("{")
        end = raw.rfind("}")

        if start != -1 and end != -1:
          raw = raw[start:end+1]

        return json.loads(raw)

    except Exception as e:

        print("Groq Error:", e)

        return {
            "website_name":"",
            "company_name":"",
            "address":"",
            "core_service":"",
            "target_customer":"",
            "probable_pain_point":"",
            "outreach_opener":""
        }

# sitemap support

def get_sitemap_urls(base_url):

    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"

    xml = safe_request(sitemap_url)

    urls = []

    if xml:
        urls = re.findall(
            r"<loc>(.*?)</loc>",
            xml
        )

    return urls[:20]

# ========= REQUIRED FUNCTION =========
def enrich_company(url: str) -> dict:
    """
    Input: Company URL
    Output: Structured company profile (STRICT FORMAT)
    """

    try:
        # Scrape relevant company content
        company_text = scrape_company(url)

        # Extract contact details
        emails = extract_emails(company_text)
        phones = extract_phones(company_text)

        # AI enrichment
        ai_data = enrich_with_ai(company_text)

        # Ensure strict schema compliance
        return {
            "website_name": ai_data.get("website_name", ""),
            "company_name": ai_data.get("company_name", ""),
            "address": ai_data.get("address", ""),
            "mobile_number": phones[0] if phones else "",
            "mail": emails if emails else [],
            "core_service": ai_data.get("core_service", ""),
            "target_customer": ai_data.get("target_customer", ""),
            "probable_pain_point": ai_data.get("probable_pain_point", ""),
            "outreach_opener": ai_data.get("outreach_opener", "")
        }

    except Exception as e:
        print(f"Error processing {url}: {e}")

        # Return empty schema instead of breaking evaluation
        return {
            "website_name": "",
            "company_name": "",
            "address": "",
            "mobile_number": "",
            "mail": [],
            "core_service": "",
            "target_customer": "",
            "probable_pain_point": "",
            "outreach_opener": ""
        }

# ========= 9. MAIN EXECUTION =========
if __name__ == "__main__":
    # 👉 Replace with provided company URLs
    urls = [
        "https://www.hyperbots.com/",
        "https://www.boat-lifestyle.com/"
    ]

    results = []

    for url in urls:
        try:
            data = enrich_company(url)
            results.append(data)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Save results to JSON file
    # TODO: Implement

    # Print results for evaluation
    print("\n=== FINAL OUTPUT ===\n")
    for r in results:
        print(r)
import re
import pdfplumber


# Section keywords to detect standard resume sections
SECTION_KEYWORDS = {
    "experience":  ["experience", "work experience", "employment", "work history"],
    "education":   ["education", "academic background", "qualifications"],
    "skills":      ["skills", "technical skills", "core competencies", "expertise"],
    "summary":     ["summary", "objective", "profile", "about me"],
    "contact":     ["contact", "personal information", "personal details"],
    "projects":    ["projects", "personal projects", "key projects"],
    "certifications": ["certifications", "certificates", "licenses"],
}


def extract_resume_from_path(file_path: str) -> dict:
    """
    Opens a PDF with pdfplumber, extracts text page by page,
    detects basic metadata, and identifies resume sections.
    """
    text_pages = []
    has_tables = False
    has_images = False
    page_count = 0

    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)

        for page in pdf.pages:
            # Detect tables
            if page.find_tables():
                has_tables = True

            # Detect images
            if page.images:
                has_images = True

            page_text = page.extract_text() or ""
            text_pages.append(page_text)

    full_text = "\n".join(text_pages).strip()

    # Confidence: penalise if text is very short relative to page count
    expected_min_chars = page_count * 200
    confidence = min(1.0, len(full_text) / max(expected_min_chars, 1))
    confidence = round(confidence, 2)

    sections = _detect_sections(full_text)

    return {
        "text": full_text,
        "sections": sections,
        "metadata": {
            "hasTables":  has_tables,
            "hasImages":  has_images,
            "pageCount":  page_count,
            "confidence": confidence,
        },
    }


def _detect_sections(text: str) -> dict:
    """
    Splits the resume text into named sections by detecting section headers.
    Returns a dict of section_name → list of content lines.
    """
    lines = text.split("\n")
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        detected = _match_section_header(stripped)

        if detected:
            current_section = detected
            if current_section not in sections:
                sections[current_section] = []
        elif current_section:
            sections[current_section].append(stripped)

    return sections


def _match_section_header(line: str) -> str | None:
    """
    Returns the canonical section name if the line looks like a section header,
    otherwise returns None.
    A line is treated as a header if it's short (≤50 chars) and matches a keyword.
    """
    if len(line) > 50:
        return None

    lower = line.lower().rstrip(":").strip()

    for section_name, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            # Exact match or the line IS the keyword phrase
            if re.fullmatch(re.escape(kw), lower):
                return section_name

    return None

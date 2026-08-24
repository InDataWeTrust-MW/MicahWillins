#!/usr/bin/env python3
"""
Generate summary-line PDF resume for Micah Willins.
Parses Resume.html directly: shows the role title block plus only the bold
lead-in line for each role (verbatim from source, no detailed bullets).
"""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SOURCE = Path(r"c:\Personal\GitRepo\MicahWillins_DEV\Resume.html")
OUTPUT = Path(r"c:\Personal\GitRepo\MicahWillins_DEV\assets\Micah-Willins-Resume.pdf")

LINKEDIN_URL = "https://www.linkedin.com/in/indatawetrust-mw"
RESUME_URL = "https://indatawetrust-mw.github.io/MicahWillins/"


def clean(text: str) -> str:
    text = text.replace("\u2011", "-")
    return re.sub(r"[\s\xa0]+", " ", text).strip()


def clean_keep_edges(text: str) -> str:
    text = text.replace("\u2011", "-")
    return re.sub(r"[\s\xa0]+", " ", text)


def build() -> None:
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    container = soup.find("div", class_="container")

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle("Name", parent=styles["Heading1"], fontSize=22,
                                 textColor=colors.HexColor("#1F4B99"), alignment=TA_CENTER,
                                 fontName="Helvetica-Bold", spaceAfter=1, leading=24)
    title_style = ParagraphStyle("Title", parent=styles["Normal"], fontSize=11,
                                  textColor=colors.HexColor("#4C5C68"), alignment=TA_CENTER,
                                  fontName="Helvetica-Bold", spaceAfter=2)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontSize=9.5,
                                    textColor=colors.HexColor("#4C5C68"), alignment=TA_CENTER,
                                    fontName="Helvetica", spaceAfter=9, leading=11)
    section_style = ParagraphStyle("SectionHeader", parent=styles["Heading2"], fontSize=11.5,
                                    textColor=colors.white, backColor=colors.HexColor("#1F4B99"),
                                    fontName="Helvetica-Bold", spaceAfter=7, spaceBefore=10,
                                    leftIndent=6, rightIndent=6)
    job_title_style = ParagraphStyle("JobTitle", parent=styles["Normal"], fontSize=10,
                                      textColor=colors.HexColor("#1F4B99"), fontName="Helvetica-Bold",
                                      spaceAfter=2, leading=11)
    summary_style = ParagraphStyle("Summary", parent=styles["Normal"], fontSize=9.5,
                                    textColor=colors.HexColor("#2BBF9F"), fontName="Helvetica-Oblique",
                                    leftIndent=0.2 * inch, spaceAfter=7, leading=11)
    text_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9,
                                 textColor=colors.HexColor("#333333"), spaceAfter=3.5, leading=11)

    content = []

    name = clean(container.find("h1").get_text())
    title_line = clean(container.find("div", class_="title-line").get_text())
    contact_items = [clean(s.get_text()) for s in container.select(".top-banner-contact .contact-item")]
    contact_items = [c for c in contact_items if c and c != "|"]

    content.append(Paragraph(name.upper(), name_style))
    content.append(Paragraph(title_line, title_style))
    content.append(Paragraph(
        f"{' | '.join(contact_items)}<br/>"
        f'<a href="{LINKEDIN_URL}" color="blue"><b>LinkedIn</b></a> | '
        f'<a href="{RESUME_URL}" color="blue"><b>View Full Details & References</b></a>',
        contact_style,
    ))

    # Career Summary / Strategic Focus verbatim from source
    for header in container.find_all("div", class_="section-header", recursive=False):
        title = clean(header.get_text())
        if title not in ("Career Summary", "Strategic Focus"):
            continue
        content.append(Paragraph(title.upper(), section_style))
        nxt = header.find_next_sibling()
        if nxt and nxt.name == "p":
            html_line = re.sub(r"<br\s*/?>", "<br/>", nxt.decode_contents())
            html_line = re.sub(r"</?b>", lambda m: m.group(0).replace("b", "b"), html_line)
            content.append(Paragraph(clean_inline(html_line), text_style))
        content.append(Spacer(1, 0.05 * inch))

    # Professional Experience: role header + bold lead line only, verbatim
    content.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
    for details in container.find_all("details"):
        summary_text = clean(details.find("summary").get_text())
        body = details.find("div")
        lead = body.find("p")
        lead_text = clean(lead.get_text()) if lead else ""

        content.append(Paragraph(summary_text, job_title_style))
        if lead_text:
            content.append(Paragraph(f"<i>{lead_text}</i>", summary_style))

    content.append(Spacer(1, 0.05 * inch))

    # Education / Awards verbatim
    for section_title in ("Education", "Awards"):
        header = container.find("div", class_="section-header", string=lambda s: s and section_title in s)
        if header is None:
            continue
        content.append(Paragraph(section_title.upper(), section_style))
        nxt = header.find_next_sibling()
        if nxt and nxt.name == "p":
            for chunk in re.split(r"<br\s*/?>", nxt.decode_contents()):
                chunk_text = clean(BeautifulSoup(chunk, "html.parser").get_text())
                if chunk_text:
                    content.append(Paragraph(f"\u2022 {chunk_text}", text_style))

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter,
        rightMargin=0.65 * inch, leftMargin=0.65 * inch,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.build(content)
    print(f"Saved {OUTPUT}")


def clean_inline(html_fragment: str) -> str:
    """Keep <br/> and <b> tags (reportlab markup) but normalize whitespace elsewhere."""
    parts = re.split(r"(<br/>|<b>|</b>)", html_fragment)
    out = []
    for part in parts:
        if part in ("<br/>", "<b>", "</b>"):
            out.append(part)
        else:
            out.append(clean_keep_edges(BeautifulSoup(part, "html.parser").get_text()))
    return "".join(out).strip()


if __name__ == "__main__":
    build()

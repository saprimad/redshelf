"""Generate the clearly labelled placeholder PDFs shipped with RedShelf."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "assets" / "pdf"
RED = colors.HexColor("#B4232D")
DARK = colors.HexColor("#1F242C")
MUTED = colors.HexColor("#667085")
PALE = colors.HexColor("#FFF1F2")


@dataclass(frozen=True)
class Placeholder:
    filename: str
    title: str
    subtitle: str
    author: str
    category: str
    doi: str
    sections: tuple[tuple[str, str], ...]


DOCUMENTS = (
    Placeholder(
        "netnography-example.pdf",
        "Netnography Example",
        "Ethical observation in online communities",
        "Amina Rahman",
        "Netnography",
        "10.0000/redshelf.net.001",
        (
            ("Purpose", "Demonstrates a transparent approach to online community selection, observation boundaries and reflexive fieldnotes."),
            ("Illustrative approach", "A fictional qualitative design combines non-participant observation, researcher memos and thematic interpretation."),
            ("Ethics note", "Public visibility does not remove the need for contextual privacy, careful quotation and responsible data handling."),
        ),
    ),
    Placeholder(
        "social-judgment-theory-example.pdf",
        "Social Judgment Theory Example",
        "Mapping attitude latitudes",
        "Daniel Lee and Nur Izzati Omar",
        "Social Judgment Theory",
        "10.0000/redshelf.sjt.002",
        (
            ("Purpose", "Introduces latitudes of acceptance, rejection and noncommitment through a fictional communication study."),
            ("Illustrative approach", "Participants sort policy statements before discussing perceived similarity, contrast and ego involvement."),
            ("Interpretation", "The example shows how prior attitudes may shape the reception of persuasive messages."),
        ),
    ),
    Placeholder(
        "cannabis-policy-example.pdf",
        "Cannabis Policy Example",
        "A public-health evidence review",
        "Sofia Martinez",
        "Cannabis Policy",
        "10.0000/redshelf.can.003",
        (
            ("Purpose", "Demonstrates the structure of a concise policy evidence review."),
            ("Illustrative scope", "The fictional review considers regulation, access, prevention, harm reduction and outcome monitoring."),
            ("Policy note", "Real policy decisions should rely on current jurisdiction-specific evidence and legal advice."),
        ),
    ),
    Placeholder(
        "malaysia-public-health-example.pdf",
        "Malaysia Public Health Example",
        "Community access and health equity",
        "Farah Aziz and Lim Wei Jian",
        "Public Health",
        "10.0000/redshelf.mph.004",
        (
            ("Purpose", "Shows how a regional public-health brief can be catalogued in RedShelf."),
            ("Illustrative approach", "A fictional mixed-methods assessment explores service awareness, travel burden and perceived accessibility."),
            ("Equity note", "Disaggregated reporting and meaningful community participation are central to equitable service design."),
        ),
    ),
    Placeholder(
        "research-methods-example.pdf",
        "Research Methods Example",
        "A transparent mixed-methods workflow",
        "Elena Kovacs",
        "Research Methods",
        "10.0000/redshelf.met.005",
        (
            ("Purpose", "Demonstrates a clear workflow for planning and reporting mixed-methods research."),
            ("Illustrative workflow", "Align questions, sampling, data collection, analysis, integration and reporting before fieldwork begins."),
            ("Reproducibility note", "Maintain a decision log, version analytical materials and distinguish planned from exploratory analyses."),
        ),
    ),
    Placeholder(
        "conference-proceedings-example.pdf",
        "Conference Proceedings Example",
        "Annual Interdisciplinary Research Forum",
        "RedShelf Academic Committee",
        "Conference Materials",
        "10.0000/redshelf.conf.006",
        (
            ("Welcome", "These fictional proceedings demonstrate a simple home for programmes, abstracts and conference outputs."),
            ("Illustrative programme", "09:00 Opening keynote; 10:30 Methods panel; 13:30 Poster session; 15:00 Policy roundtable."),
            ("Sample abstract", "A transparent digital library can improve discoverability when metadata, citations and access pathways are consistent."),
        ),
    ),
)


def add_page_number(canvas, document) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#E6E8EC"))
    canvas.line(22 * mm, 17 * mm, width - 22 * mm, 17 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, 11 * mm, "RedShelf placeholder document - example content only")
    canvas.drawRightString(width - 22 * mm, 11 * mm, f"Page {document.page}")
    canvas.restoreState()


def build_pdf(item: Placeholder) -> None:
    output = OUTPUT_DIR / item.filename
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "RedShelfTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=32,
        textColor=DARK,
        spaceAfter=7 * mm,
    )
    subtitle = ParagraphStyle(
        "RedShelfSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=14,
        leading=20,
        textColor=MUTED,
        spaceAfter=10 * mm,
    )
    heading = ParagraphStyle(
        "RedShelfHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=RED,
        spaceBefore=5 * mm,
        spaceAfter=2 * mm,
    )
    body = ParagraphStyle(
        "RedShelfBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=DARK,
        spaceAfter=3 * mm,
    )
    label = ParagraphStyle(
        "ExampleLabel",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=RED,
    )

    document = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=22 * mm,
        bottomMargin=25 * mm,
        title=item.title,
        author=item.author,
        subject="Clearly labelled RedShelf example PDF",
    )

    metadata = [
        ["Author / editor", item.author],
        ["Category", item.category],
        ["Year", "2026"],
        ["DOI", item.doi],
    ]
    table = Table(metadata, colWidths=[38 * mm, 107 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE),
                ("TEXTCOLOR", (0, 0), (0, -1), RED),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E6E8EC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story = [
        Paragraph("REDSHELF / EXAMPLE PDF", label),
        Spacer(1, 11 * mm),
        Paragraph(item.title, title),
        Paragraph(item.subtitle, subtitle),
        Table(
            [[Paragraph("<b>EXAMPLE CONTENT ONLY</b><br/>Replace this placeholder with an authorised research document.", body)]],
            colWidths=[145 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PALE),
                    ("BOX", (0, 0), (-1, -1), 1, RED),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        ),
        Spacer(1, 9 * mm),
        table,
        Spacer(1, 7 * mm),
    ]

    for section_title, section_text in item.sections:
        story.extend((Paragraph(section_title, heading), Paragraph(section_text, body)))

    story.extend(
        (
            PageBreak(),
            Paragraph("About this placeholder", title),
            Paragraph(
                "This PDF is intentionally short and contains no real research findings. "
                "It is generated by scripts/generate_placeholder_pdfs.py so a new RedShelf "
                "installation can demonstrate preview, view and download behaviour immediately.",
                body,
            ),
            Paragraph("Replacement checklist", heading),
            Paragraph(
                "1. Confirm that you have permission to store and distribute the PDF.<br/>"
                "2. Use a stable, descriptive filename.<br/>"
                "3. Replace all fictional metadata on the document page.<br/>"
                "4. Verify the citation and DOI against the authoritative source.<br/>"
                "5. Run <font name='Courier'>mkdocs build --strict</font> before publishing.",
                body,
            ),
        )
    )

    document.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for item in DOCUMENTS:
        build_pdf(item)
        print(f"Generated {OUTPUT_DIR / item.filename}")


if __name__ == "__main__":
    main()

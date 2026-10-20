# MicahWillins.github.io
Resume

## Resume skills and downloads

Technical Skills was revised through a self-reported experience questionnaire.
Production work is distinguished from project experience, experiments, working
knowledge, and familiarity; proficiency has not been independently certified.
The same content is maintained in `Resume.html`, `index.html`, and both copies
under `docs/`.

Strategic Focus and Technical Skills use semantic definition lists with
alternating row backgrounds. Category labels sit beside their descriptions on
wide screens and stack above them on narrow screens. Preserve the `.banded-list`
and `.banded-row` structure when editing so the Word and PDF generators retain
every category and its experience qualifiers. The Word export uses shaded,
single-column paragraphs for reading order; the PDF uses banded category rows.

Technical Skills starts collapsed when JavaScript is available. Its keyboard-accessible toggle switches
between the banded details and a wrapping array of category labels only.
The category labels are reused rather than duplicated. Printing always shows
the full details, and the Word download remains expanded. The PDF shows only
the Technical Skills category names as a compact array. Without JavaScript,
the full list remains visible.

The PDF button uses a same-origin download link with an explicit filename,
not a new-tab preview or a JavaScript fetch fallback.
Both download buttons have visible format labels: the Word version is the
detailed application document, and the PDF is a one-page overview. A native
download is requested when served from the same website; browser settings or
local-file preview behavior can still affect how the browser handles a file.

Additional enterprise platforms and domain categories were confirmed through
the experience questionnaire. Information Security Analytics describes
reporting, data integration, governance, and metric-program work, not an
unqualified claim of security-control administration. Operations & Workforce
Analytics covers contact-center performance, workforce scheduling, and employee
turnover, not transportation logistics or customer churn. Product-specific
uses are retained beside Mobius, Digital.ai Agility, identity platforms, SAP
reporting tools, and Microsoft collaboration tools.

## Section fonts

Career Summary, banded category labels, and grouped experience titles use
Aptos Display. Banded descriptions, expanded experience, Education, Awards,
and Documentation use Aptos Narrow. Section headers/separators retain their
existing typography. Word downloads use the same named fonts; PDF downloads
embed subsets of locally available fonts. The PDF generator requires all four
regular/bold/italic/bold-italic variants of both families, available in Windows
font directories or the local Office font cache, and fails explicitly if missing.

No font files are redistributed with the website. Browsers use Aptos when
available locally, falling back to Aptos, Segoe UI, then system sans-serif.
Office-cached fonts used by the PDF exporter may not be installed for browsers.

After editing the HTML, regenerate downloads from the DEV repository root:

```powershell
python .\scripts\generate_ats_docx_final.py
python .\scripts\generate_pdf_summary_final.py
Copy-Item .\Micah-Willins-ATS.docx .\docs\Micah-Willins-ATS.docx
Copy-Item .\Micah-Willins-ATS.docx .\docs\assets\Micah-Willins-ATS.docx
Copy-Item .\assets\Micah-Willins-Resume.pdf .\docs\assets\Micah-Willins-Resume.pdf
```

The generators require Beautiful Soup, python-docx, and ReportLab. The summary
PDF includes Technical Skills and may span multiple pages; role details remain
summarized. Keep duplicate download files byte-identical. These are DEV-only
changes; publishing requires a separate review and approval.

The ATS Word download includes the full source experience bullets, with bold
lead-ins followed by their explanations, in a linear reading order without
layout tables or text boxes. Keywords are supplied by the source content rather
than a separate hard-coded keyword appendix. The PDF retains Strategic Focus
details and every skill category name, but omits skill descriptions and Awards.
It includes only each role title and its source summary line, not the detailed
bullets. Its hosted-resume link reads "View Hosted Resume for detailed specifics,
verified references, and documented award samples". Both downloads' LinkedIn
and hosted-resume links use Aptos Narrow Italic at 7.5 pt. PDF contact details retain
their original font and 9.5 pt size. Compact row padding limits unnecessary
page spill while preserving font sizes and banding. Both downloads
link to the full online resume and references; embedded recommendation letters
remain web-only.

After generation and copying, run `python .\scripts\test_resume_exports.py`
(requires pypdf in addition to the generation dependencies). The checks compare
full ATS bullets, every banded category, PDF role summaries and pagination,
download hashes, education/awards, and online-resume links against the source.

PDFs are marked binary in `.gitattributes` to prevent Git line-ending
conversion from altering generated downloads.

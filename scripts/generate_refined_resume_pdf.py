from pathlib import Path
import re
import subprocess
import tempfile


DEV_ROOT = Path(__file__).resolve().parents[1]
SOURCE = DEV_ROOT / "docs" / "Resume.html"
OUTPUTS = [
    DEV_ROOT / "docs" / "assets" / "Micah-Willins-Resume.pdf",
    DEV_ROOT / "assets" / "Micah-Willins-Resume.pdf",
]
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
LIVE_URL = "https://indatawetrust-mw.github.io/MicahWillins/"
LINKEDIN_URL = "https://www.linkedin.com/in/indatawetrust-mw"

PRINT_CSS = """
<style id="pdf-export-styles">
@page { size: A4; margin: 0.22in; }
body { background: #fff !important; color: #222; font-size: 9px !important; }
.container { width: auto !important; max-width: none !important; margin: 0 !important; padding: 0 !important; border: 0 !important; box-shadow: none !important; }
.identity-block { margin-bottom: 5px !important; }
h1 { font-size: 23px !important; }
.title-line { margin-top: 2px !important; font-size: 11.5px !important; }
.top-banner { margin: 5px 0 7px !important; padding: 4px 7px !important; }
.top-banner-links { display: none !important; }
.top-banner-contact { margin-left: 0 !important; gap: 4px 8px !important; font-size: 8.5px !important; }
.top-banner-contact .contact-item { white-space: nowrap; }
.top-banner-contact a { color: #1F4B99; font-weight: 700; text-decoration: underline; }
.section-header { margin-top: 8px !important; margin-bottom: 3px !important; padding-bottom: 3px !important; border-bottom-width: 2px !important; font-size: 12px !important; }
.section-header-note { display: none !important; }
.pdf-role { display: flex; flex-direction: column; min-height: 44px; margin-bottom: 3px; padding: 5px 8px 4px; border: 1px solid #d7dce4; border-radius: 3px; background: linear-gradient(to right, #eef1f7, #f9fafc); break-inside: avoid; page-break-inside: avoid; }
.role-heading { padding-bottom: 2px; font-size: 9.5px; font-weight: 700; color: #304a68; }
.role-summary { margin-top: auto; padding-top: 2px; text-align: center; font-size: 8.75px; font-weight: 700; color: #4C5C68; }
</style>
"""


def collapse_role_details(html: str) -> str:
    details_pattern = re.compile(r"<details\b[^>]*>.*?</details>", re.IGNORECASE | re.DOTALL)

    def trim_role(match: re.Match[str]) -> str:
        block = match.group(0)
        heading_match = re.search(r"<summary\b[^>]*>(.*?)</summary>", block, re.IGNORECASE | re.DOTALL)
        subtitle_match = re.search(
            r"<p>\s*<strong>(.*?)</strong>\s*</p>",
            block,
            re.IGNORECASE | re.DOTALL,
        )
        if not heading_match or not subtitle_match:
            return block
        return (
            '<div class="pdf-role">'
            f'<div class="role-heading">{heading_match.group(1).strip()}</div>'
            f'<div class="role-summary">{subtitle_match.group(1).strip()}</div>'
            "</div>"
        )

    return details_pattern.sub(trim_role, html)


def remove_documentation_section(html: str) -> str:
    return re.sub(
        r'<div class="section-header">Documentation</div>\s*<p>.*?</p>',
        "",
        html,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )


def build_pdf_html() -> str:
    html = SOURCE.read_text(encoding="utf-8")
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<template\b[^>]*>.*?</template>", "", html, flags=re.IGNORECASE | re.DOTALL)
    html = remove_documentation_section(html)
    html = collapse_role_details(html)
    html = html.replace("</style>", PRINT_CSS + "\n</style>", 1)
    return html


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not CHROME.exists():
        raise FileNotFoundError(CHROME)

    with tempfile.TemporaryDirectory(prefix="micah-resume-pdf-") as temp_dir:
        html_path = Path(temp_dir) / "resume-pdf.html"
        html_path.write_text(build_pdf_html(), encoding="utf-8")
        for output in OUTPUTS:
            output.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    str(CHROME),
                    "--headless",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={output}",
                    html_path.as_uri(),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"generated {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

import re

BEHAVE_HTML = "reports/index.html"
SELF_HEALING_HTML = "reports/self_healing_report.html"
OUTPUT_HTML = "reports/combined_report.html"

with open(SELF_HEALING_HTML, "r", encoding="utf-8") as f:
    healing_html = f.read()

healing_body = re.search(r"<body[^>]*>(.*?)</body>", healing_html, re.DOTALL | re.IGNORECASE)
healing_body_content = healing_body.group(1) if healing_body else healing_html

# Debug print
print("=== Healing Section Preview ===")
print(healing_body_content[:500])  # Print first 500 chars
print("==============================")

healing_section = f"""
<div style="border:2px solid #2d6cdf; margin:2em 0; padding:1em; background:#f9f9f9; color:#000; z-index:9999;">
<h1 style="color:#2d6cdf;">🩹 Self-Healing Locator Report</h1>
{healing_body_content}
</div>
"""

with open(BEHAVE_HTML, "r", encoding="utf-8") as f:
    behave_html = f.read()

combined_html = re.sub(
    r"(</body>)",
    "\n<!-- Self-Healing Locator Report Start -->\n" + healing_section + "\n<!-- Self-Healing Locator Report End -->\n" + r"\1",
    behave_html,
    count=1,
    flags=re.IGNORECASE
)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(combined_html)

print(f"✅ Combined HTML report generated: {OUTPUT_HTML}")

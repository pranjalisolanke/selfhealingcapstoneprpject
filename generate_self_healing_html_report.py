import json
import os

# Path to your self-healing JSON report
HEALING_JSON = "reports/healing_report_login_with_ai-powered_self-healing_locators_20250606_133605.json"
OUTPUT_HTML = "reports/self_healing_report.html"

if not os.path.exists(HEALING_JSON):
    print(f"❌ Healing JSON report not found: {HEALING_JSON}")
    exit(1)

with open(HEALING_JSON, "r", encoding="utf-8") as f:
    healing_data = json.load(f)

html = """
<html>
<head>
  <title>Self-Healing Locator Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2em; }}
    .event {{ border:1px solid #ccc; margin:1em 0; padding:1em; border-radius: 8px; }}
    .success {{ color: green; }}
    .fail {{ color: red; }}
    h1, h2 {{ color: #2d6cdf; }}
  </style>
</head>
<body>
<h1>🩹 Self-Healing Locator Report</h1>
<h2>Summary</h2>
<ul>
  <li><b>Total Attempts:</b> {total}</li>
  <li><b>Successful Healing:</b> {healed}</li>
  <li><b>Failed Healing:</b> {failed}</li>
  <li><b>Success Rate:</b> {rate:.1f}%</li>
</ul>
<h2>Healing Events</h2>
""".format(
    total=healing_data["summary"]["total_attempts"],
    healed=healing_data["summary"]["successful_healing"],
    failed=healing_data["summary"]["failed_healing"],
    rate=(healing_data["summary"]["successful_healing"] / healing_data["summary"]["total_attempts"] * 100)
    if healing_data["summary"]["total_attempts"] > 0 else 0
)

for i, event in enumerate(healing_data.get("events", [])):
    html += f"""
    <div class="event">
      <b>Event {i+1}:</b><br>
      <b>Element:</b> {event.get('element', '')}<br>
      <b>Description:</b> {event.get('description', 'N/A')}<br>
      <b>Failed Strategies:</b> {len(event.get('failed', []))}<br>
      <b>Successful Strategy:</b> <span class="success">{event.get('succeeded', ['None'])[0]}='{event.get('succeeded', ['',''])[1] if event.get('succeeded') else ''}'</span><br>
      <b>Timestamp:</b> {event.get('timestamp', '')}<br>
    </div>
    """

html += "</body></html>"

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Self-healing HTML report generated: {OUTPUT_HTML}")

import os
import re
import html
from datetime import datetime
from typing import Dict
from gpt_handler import client, AZURE_DEPLOYMENT

def generate_html_report(insights: dict, images: Dict[str, str], output_dir: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(output_dir, f"eda_report_{timestamp}.html")

    # 🧠 Compose the GPT prompt
    type_summary = (
        f"Numerical: {', '.join(insights['types']['numerical'])}\n"
        f"Categorical: {', '.join(insights['types']['categorical'])}\n"
        f"Boolean: {', '.join(insights['types']['boolean'])}\n"
        f"Datetime: {', '.join(insights['types']['datetime'])}"
    )

    summary_parts = [
        f"Shape: {insights['shape']}\nColumns: {insights['columns']}",
        type_summary
    ]

    if insights['constant_cols']:
        summary_parts.append("Constant Columns: " + ", ".join(insights['constant_cols']))

    cardinality = "\n".join(
        f"{k}: {v} unique{' ⚠️' if v > 50 else ''}"
        for k, v in insights['cardinality'].items()
    )
    summary_parts.append("Cardinality:\n" + cardinality)

    if insights['missing'].any():
        missing_txt = insights['missing'][insights['missing'] > 0].apply(lambda x: f"{x:.1%} missing").to_string()
    else:
        missing_txt = "✅ No missing values"
    summary_parts.append("Missing Values:\n" + missing_txt)

    skew_txt = "✅ No highly skewed columns."
    if not insights['skew'].empty:
        skewed = insights['skew'][abs(insights['skew']) > 1]
        if not skewed.empty:
            skew_txt = skewed.apply(lambda x: f"{x:.2f} (high skew)").to_string()
    summary_parts.append("Skewness:\n" + skew_txt)

    summary_parts.append("Numerical Summary:\n" + insights['describe'].to_string())
    cat_preview = "\n\n".join([f"{k}:\n{v.to_string()}" for k, v in insights['top_categories'].items()])
    summary_parts.append("Top Categorical Values:\n" + cat_preview)

    full_summary = "\n\n".join(summary_parts)

    try:
        gpt_response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a professional data analyst, writing a short summary. Infer concise insights, don't repeat the stats. Use HTML tags only."},
                {"role": "user", "content": full_summary}
            ]
        )
        raw_summary = gpt_response.choices[0].message.content.strip()
        gpt_summary = re.sub(r"^```(?:html)?|```$", "", raw_summary).strip()
    except Exception as e:
        gpt_summary = f"⚠️ Failed to generate GPT summary: {e}"

    html_content = f"""<html>
<head>
    <meta charset='UTF-8'>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Smart EDA Report - {timestamp}</title>
    <link rel=\"stylesheet\" type=\"text/css\" href=\"eda_report_style.css\">
    <script>
        function toggleSection(id) {{
            const el = document.getElementById(id);
            el.style.display = (el.style.display === 'none') ? 'block' : 'none';
        }}
    </script>
</head>
<body>
<h1>📊 Smart EDA Report</h1>
<p><strong>Generated:</strong> {timestamp}</p>
<hr>
<div>
    <h2>📄 Dataset Description (Generated by GPT)</h2>
    <div class=\"gpt-summary-box\">
    {gpt_summary}
    </div>
</div>
<hr>
"""

    def add_section(title, content, section_id):
        nonlocal html_content
        html_content += f"<h2 class='section-toggle' onclick=\"toggleSection('{section_id}')\">{title}</h2>"
        html_content += f"<div id='{section_id}' class='section-content'><pre>{html.escape(content)}</pre></div>"

    add_section("🔎 Data Overview", f"Shape: {insights['shape']}\nColumns: {insights['columns']}", "overview")
    add_section("🧪 Data Types", type_summary, "types")
    if insights['constant_cols']:
        add_section("⚠️ Constant Columns", ", ".join(insights['constant_cols']), "constants")
    add_section("🔠 Cardinality", cardinality, "cardinality")
    add_section("🧩 Missing Values", missing_txt, "missing")
    add_section("📈 Skewness", skew_txt, "skewness")
    add_section("📋 Numerical Summary", insights['describe'].to_string(), "describe")
    add_section("📂 Top Categorical Values", cat_preview, "topcats")

    if "correlation" in images:
        html_content += f"<h2>🔗 Correlation Matrix</h2><img src='{os.path.basename(images['correlation'])}' />"
    if "missing" in images:
        html_content += f"<h2>📉 Missing Value Heatmap</h2><img src='{os.path.basename(images['missing'])}' />"

    html_content += """
    <hr>
    <div style='text-align: right;'>
        <button class='back-to-top' onclick="window.scrollTo({ top: 0, behavior: 'smooth' })">⬆️ Back to Top</button>
    </div>
    <p><em>Generated by DashGraph</em></p>
</body>
</html>
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return report_path
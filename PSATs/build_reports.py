#!/usr/bin/env python3
"""Generate PSAT reports from psat1_data.json:
   1. PSAT1_summary.html  - full score dashboard + every missed question with rationale
   2. PSAT1_mistakes.html - printable study sheet, wrong/omitted questions only
"""
import json, html

qs = json.load(open('psat1_data.json', encoding='utf-8'))
SECTIONS = ['Reading and Writing', 'Math']

def esc(s): return html.escape(s)

def score(items):
    c = sum(1 for q in items if q['status'] == 'correct')
    return c, len(items)

def pct(c, n): return round(100 * c / n) if n else 0

# ---- aggregate ----
overall_c, overall_n = score(qs)
sec_stats = {}
for s in SECTIONS:
    items = [q for q in qs if q['section'] == s]
    sec_stats[s] = {'items': items, 'c': score(items)[0], 'n': len(items),
                    'modules': {}}
    for m in (1, 2):
        mi = [q for q in items if q['module'] == m]
        if mi:
            sec_stats[s]['modules'][m] = score(mi) + (len(mi),)

wrong = [q for q in qs if q['status'] != 'correct']

STYLE = """
:root{
  --ink:#1d1d1d; --muted:#5a5f66; --line:#e3e6ea; --bg:#f4f6f8; --card:#fff;
  --good:#1a7f4b; --good-bg:#e6f4ec; --bad:#c0392b; --bad-bg:#fbecea;
  --accent:#2f5fd0; --omit:#8a6d1f; --omit-bg:#fbf3d9;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.55}
.wrap{max-width:940px;margin:0 auto;padding:32px 22px 80px}
h1{font-size:26px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 26px;font-size:14px}
h2{font-size:19px;margin:34px 0 14px;padding-bottom:6px;border-bottom:2px solid var(--line)}
.cards{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;flex:1;min-width:150px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.card .label{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
.card .big{font-size:34px;font-weight:700;margin:4px 0 2px}
.card .note{font-size:13px;color:var(--muted)}
.bar{height:9px;border-radius:6px;background:var(--line);overflow:hidden;margin-top:10px}
.bar > i{display:block;height:100%;border-radius:6px;background:var(--accent)}
table{width:100%;border-collapse:collapse;background:var(--card);
  border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:14px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f0f3f7;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
tr:last-child td{border-bottom:none}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:12px;font-weight:600}
.t-good{background:var(--good-bg);color:var(--good)}
.t-bad{background:var(--bad-bg);color:var(--bad)}
.t-omit{background:var(--omit-bg);color:var(--omit)}
.q{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--bad);
  border-radius:10px;padding:18px 20px;margin:14px 0;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.q.omit{border-left-color:var(--omit)}
.q .qhead{display:flex;justify-content:space-between;gap:12px;align-items:baseline;margin-bottom:8px}
.q .qref{font-weight:700;font-size:14px}
.q .stem{margin:6px 0 12px}
.opts{list-style:none;padding:0;margin:0 0 12px}
.opts li{padding:6px 10px;border:1px solid var(--line);border-radius:8px;margin:5px 0;font-size:14px}
.opts li.correct{background:var(--good-bg);border-color:#bfe3cd}
.opts li.chosen{background:var(--bad-bg);border-color:#f0c9c3}
.opts li.chosen.correct{background:var(--good-bg);border-color:#bfe3cd}
.optltr{display:inline-block;width:22px;font-weight:700}
.pick{font-size:13px;margin:2px 0 10px}
.pick b.bad{color:var(--bad)} .pick b.good{color:var(--good)}
.rat{font-size:13.5px;color:#2b2f34;background:#fafbfc;border:1px solid var(--line);
  border-radius:8px;padding:12px 14px}
.rat p{margin:0 0 8px} .rat p:last-child{margin:0}
.rat .rl{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:6px}
.callout{background:#eef3ff;border:1px solid #cfdcfb;border-radius:10px;padding:14px 18px;font-size:14px;margin:10px 0 4px}
.callout b{color:var(--accent)}
.nav{margin-bottom:18px;font-size:13px}
.nav a{color:var(--accent);text-decoration:none}
.nav a:hover{text-decoration:underline}
@media print{body{background:#fff}.q,.card,table,.nav{box-shadow:none}.nav{display:none}.wrap{max-width:none;padding:0}}
"""

LETTERS = "ABCDEFGH"

def render_options(q, chosen_letter):
    if not q['options']:
        return ""  # grid-in
    out = ['<ul class="opts">']
    for i, o in enumerate(q['options']):
        ltr = LETTERS[i]
        cls = []
        if o['correct']: cls.append('correct')
        if ltr == chosen_letter: cls.append('chosen')
        out.append(f'<li class="{" ".join(cls)}"><span class="optltr">{ltr}.</span>{esc(o["text"])}</li>')
    out.append('</ul>')
    return "".join(out)

def pick_line(q):
    sel, cor = q['selected'], q['correct']
    if q['status'] == 'correct':
        return f'<div class="pick">Your answer: <b class="good">{esc(sel)}</b> ✓</div>'
    if sel == '(omitted)':
        return f'<div class="pick">Left blank — correct answer: <b class="good">{esc(cor)}</b></div>'
    return (f'<div class="pick">Your answer: <b class="bad">{esc(sel)}</b> &nbsp;·&nbsp; '
            f'Correct: <b class="good">{esc(cor)}</b></div>')

def render_question_card(q, n):
    omit = q['selected'] == '(omitted)'
    cls = 'q omit' if omit else 'q'
    ref = f'{q["section"]} — Module {q["module"]}, Q{q["qnum"]}'
    if q.get('dup'): ref += ' <span style="color:var(--muted)">(dup #)</span>'
    tag = ('<span class="tag t-omit">Omitted</span>' if omit
           else '<span class="tag t-bad">Incorrect</span>')
    chosen = q['selected'] if q['selected'] in list(LETTERS) else None
    rat = "".join(f'<p>{esc(p)}</p>' for p in q['rationale'])
    return f"""<div class="{cls}">
  <div class="qhead"><span class="qref">{n}. {ref}</span>{tag}</div>
  <div class="stem">{esc(q['stem'])}</div>
  {render_options(q, chosen)}
  {pick_line(q)}
  <div class="rat"><div class="rl">Rationale</div>{rat}</div>
</div>"""

def page(title, body):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><style>{STYLE}</style></head>
<body><div class="wrap">{body}</div></body></html>"""

# ============ REPORT 1: SUMMARY ============
def build_summary():
    cards = f"""<div class="cards">
  <div class="card"><div class="label">Overall</div>
    <div class="big">{pct(overall_c,overall_n)}%</div>
    <div class="note">{overall_c} of {overall_n} correct</div>
    <div class="bar"><i style="width:{pct(overall_c,overall_n)}%"></i></div></div>"""
    for s in SECTIONS:
        st = sec_stats[s]
        cards += f"""<div class="card"><div class="label">{esc(s)}</div>
    <div class="big">{pct(st['c'],st['n'])}%</div>
    <div class="note">{st['c']} of {st['n']} correct</div>
    <div class="bar"><i style="width:{pct(st['c'],st['n'])}%"></i></div></div>"""
    cards += "</div>"

    # module table
    rows = ""
    for s in SECTIONS:
        for m, (c, _, n) in sorted(sec_stats[s]['modules'].items()):
            rows += (f"<tr><td>{esc(s)}</td><td>Module {m}</td>"
                     f"<td>{c} / {n}</td><td>{pct(c,n)}%</td></tr>")
    mod_table = f"""<h2>Section &amp; module breakdown</h2>
<table><thead><tr><th>Section</th><th>Module</th><th>Correct</th><th>Score</th></tr></thead>
<tbody>{rows}</tbody></table>"""

    # observations
    n_omit = sum(1 for q in qs if q['selected'] == '(omitted)')
    gridins = [q for q in qs if q['section']=='Math' and not q['options']]
    gi_wrong = sum(1 for q in gridins if q['status']!='correct')
    obs = f"""<h2>What stands out</h2>
<div class="callout">
<p><b>Math is the priority.</b> Reading &amp; Writing sits at {pct(sec_stats['Reading and Writing']['c'],sec_stats['Reading and Writing']['n'])}%
while Math is at {pct(sec_stats['Math']['c'],sec_stats['Math']['n'])}% — the bigger opportunity is in Math.</p>
<p><b>{n_omit} Math questions were left blank.</b> The PSAT has no penalty for wrong answers, so every omitted question is a free guess left on the table.</p>
<p><b>Grid-in (student-produced response) questions are a weak spot:</b> {gi_wrong} of {len(gridins)} were missed — worth targeted practice on the free-response computation questions.</p>
</div>"""

    # missed-question index table
    idx_rows = ""
    for i, q in enumerate(wrong, 1):
        sel = 'blank' if q['selected'] == '(omitted)' else q['selected']
        tag = ('<span class="tag t-omit">omit</span>' if q['selected']=='(omitted)'
               else '<span class="tag t-bad">wrong</span>')
        idx_rows += (f"<tr><td>{i}</td><td>{esc(q['section'])}</td><td>M{q['module']} Q{q['qnum']}</td>"
                     f"<td>{esc(sel)}</td><td>{esc(q['correct'])}</td><td>{tag}</td></tr>")
    idx_table = f"""<h2>All {len(wrong)} missed questions</h2>
<table><thead><tr><th>#</th><th>Section</th><th>Item</th><th>Your ans.</th><th>Correct</th><th></th></tr></thead>
<tbody>{idx_rows}</tbody></table>"""

    # detailed cards grouped by section
    detail = "<h2>Missed questions — detail &amp; rationale</h2>"
    n = 1
    for s in SECTIONS:
        sw = [q for q in wrong if q['section'] == s]
        if not sw: continue
        detail += f'<h3 style="margin:22px 0 4px">{esc(s)} ({len(sw)} missed)</h3>'
        for q in sw:
            detail += render_question_card(q, n); n += 1

    body = (f'<div class="nav"><a href="index.html">← Back to dashboard</a></div>'
            f"<h1>PSAT Practice Test 1 — Results Overview</h1>"
            f'<p class="sub">Reading and Writing + Math · {overall_n} questions · generated from PSAT1.html</p>'
            f"{cards}{obs}{mod_table}{idx_table}{detail}")
    return page("PSAT 1 — Results Overview", body)

# ============ REPORT 2: MISTAKES STUDY SHEET ============
def build_mistakes():
    n_omit = sum(1 for q in wrong if q['selected'] == '(omitted)')
    head = (f'<div class="nav"><a href="index.html">← Back to dashboard</a></div>'
            f"<h1>PSAT 1 — Mistakes to Review</h1>"
            f'<p class="sub">{len(wrong)} questions to revisit '
            f'({len(wrong)-n_omit} answered incorrectly, {n_omit} left blank). Printable — File ▸ Print.</p>')
    body = head
    n = 1
    for s in SECTIONS:
        sw = [q for q in wrong if q['section'] == s]
        if not sw: continue
        c, tot = sec_stats[s]['c'], sec_stats[s]['n']
        body += f'<h2>{esc(s)} — {len(sw)} to review <span style="font-weight:400;color:var(--muted);font-size:14px">({c}/{tot} correct)</span></h2>'
        for q in sw:
            body += render_question_card(q, n); n += 1
    return page("PSAT 1 — Mistakes to Review", body)

open('PSAT1_summary.html', 'w', encoding='utf-8').write(build_summary())
print("Wrote PSAT1_summary.html")
print(f"Missed total: {len(wrong)}  (overall {overall_c}/{overall_n} = {pct(overall_c,overall_n)}%)")

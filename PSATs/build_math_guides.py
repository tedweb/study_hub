#!/usr/bin/env python3
"""Generate 5 PSAT Math study guides + 5 worksheets (with collapsible solutions).
Shared CSS matches index.html / PSAT1_summary.html / PSAT1_studyplan.html.
Math is written in Unicode (no MathJax) so files stay small and work offline.
"""
import html

def esc(s): return html.escape(s)

STYLE = """
:root{
  --ink:#1d1d1d; --muted:#5a5f66; --line:#e3e6ea; --bg:#f4f6f8; --card:#fff;
  --good:#1a7f4b; --good-bg:#e6f4ec; --bad:#c0392b; --bad-bg:#fbecea;
  --accent:#2f5fd0; --omit:#8a6d1f; --omit-bg:#fbf3d9; --hi:#eef3ff; --hi-b:#cfdcfb;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.6}
.wrap{max-width:880px;margin:0 auto;padding:32px 22px 80px}
h1{font-size:26px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 22px;font-size:14px}
h2{font-size:19px;margin:32px 0 12px;padding-bottom:6px;border-bottom:2px solid var(--line)}
h3{font-size:16px;margin:20px 0 8px}
.nav{margin-bottom:18px;font-size:13px;display:flex;gap:16px;flex-wrap:wrap}
.nav a{color:var(--accent);text-decoration:none}
.nav a:hover{text-decoration:underline}
.pill{display:inline-block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;
  color:var(--accent);background:var(--hi);border:1px solid var(--hi-b);border-radius:20px;padding:3px 10px;margin-bottom:10px}
.block{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:10px;padding:16px 20px;margin:12px 0;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.block h4{margin:0 0 8px;font-size:15px}
.block ul{margin:6px 0 0 18px;padding:0}
.block li{margin:5px 0}
.callout{background:var(--hi);border:1px solid var(--hi-b);border-radius:10px;
  padding:14px 18px;font-size:14px;margin:12px 0}
.callout b{color:var(--accent)}
.trap{background:var(--bad-bg);border:1px solid #f0c9c3;border-radius:10px;padding:14px 18px;font-size:14px;margin:12px 0}
.trap b{color:var(--bad)}
.fml{background:#fafbfc;border:1px solid var(--line);border-radius:8px;padding:10px 14px;
  margin:8px 0;font-size:15px;font-family:"SF Mono",Menlo,Consolas,monospace}
.eg{background:#fafbfc;border:1px solid var(--line);border-radius:8px;padding:12px 16px;margin:10px 0}
.eg .step{margin:4px 0;font-size:14px}
.q{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--muted);
  border-radius:10px;padding:16px 20px;margin:14px 0;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.q.orig{border-left-color:var(--bad)}
.q .qref{font-weight:700;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.q .stem{margin:6px 0 10px}
.opts{list-style:none;padding:0;margin:0 0 6px}
.opts li{padding:5px 10px;border:1px solid var(--line);border-radius:8px;margin:5px 0;font-size:14px}
.optltr{display:inline-block;width:22px;font-weight:700}
details{margin-top:8px;border:1px solid var(--line);border-radius:8px;background:#fafbfc}
details[open]{background:#fff}
summary{cursor:pointer;padding:10px 14px;font-size:13px;font-weight:600;color:var(--accent);
  list-style:none;user-select:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";}
details[open] summary::before{content:"▾ ";}
.soln{padding:2px 16px 14px;font-size:14px}
.soln .step{margin:6px 0}
.soln .ans{margin-top:10px;font-weight:700;color:var(--good)}
sup{font-size:.75em}
footer{color:var(--muted);font-size:13px;margin-top:40px;text-align:center}
@media print{body{background:#fff}.block,.q{box-shadow:none}.nav{display:none}
  details{border:none;background:#fff}summary{display:none}.soln{padding:0}.wrap{max-width:none;padding:0}}
"""

def page(title, body):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><style>{STYLE}</style></head>'
            f'<body><div class="wrap">{body}</div></body></html>')

def nav(links):
    return '<div class="nav">' + "".join(f'<a href="{h}">{esc(t)}</a>' for t,h in links) + '</div>'

def render_problem(p, ref_cls=""):
    """p: dict with ref, stem, opts(optional list of (letter,text,is_correct)), solution(list of str), answer"""
    opts = ""
    if p.get('opts'):
        opts = '<ul class="opts">' + "".join(
            f'<li><span class="optltr">{l}.</span>{t}</li>' for l,t in p['opts']) + '</ul>'
    steps = "".join(f'<div class="step">{s}</div>' for s in p['solution'])
    ans = f'<div class="ans">Answer: {p["answer"]}</div>'
    cls = "q orig" if ref_cls=="orig" else "q"
    return (f'<div class="{cls}"><div class="qref">{p["ref"]}</div>'
            f'<div class="stem">{p["stem"]}</div>{opts}'
            f'<details><summary>Show solution</summary>'
            f'<div class="soln">{steps}{ans}</div></details></div>')

# ============================================================
# CONTENT — one dict per cluster
# ============================================================

CLUSTERS = {}

# ---------- 1. QUADRATICS ----------
CLUSTERS['quadratics'] = {
 'slug':'quadratics', 'priority':1, 'misses':8,
 'title':'Quadratics',
 'blurb':'Discriminant · completing the square · Vieta&rsquo;s formulas · vertex form · building from a table',
 'fixes':'M1 Q14 · M2 Q5, Q13, Q15, Q16, Q19, Q20, Q22 &mdash; almost half of all Math errors.',
 'concepts':[
   ('The three forms of a quadratic', None, [
     'Standard: <b>y = ax<sup>2</sup> + bx + c</b> &mdash; c is the y-intercept.',
     'Factored: <b>y = a(x &minus; r<sub>1</sub>)(x &minus; r<sub>2</sub>)</b> &mdash; r<sub>1</sub>, r<sub>2</sub> are the x-intercepts (roots).',
     'Vertex: <b>y = a(x &minus; h)<sup>2</sup> + k</b> &mdash; (h, k) is the vertex.']),
   ('The discriminant &mdash; how many real solutions?', 'D = b<sup>2</sup> &minus; 4ac', [
     '<b>D &gt; 0</b> &rarr; two distinct real solutions (crosses x-axis twice).',
     '<b>D = 0</b> &rarr; exactly one real solution (touches x-axis &mdash; the vertex sits on it).',
     '<b>D &lt; 0</b> &rarr; no real solutions (never touches the x-axis).',
     'Most "no real solutions" and "exactly one solution" questions are just discriminant conditions in disguise.']),
   ('Completing the square', None, [
     'To turn x<sup>2</sup> + bx into a perfect square, add <b>(b/2)<sup>2</sup></b>.',
     'x<sup>2</sup> + bx + (b/2)<sup>2</sup> = (x + b/2)<sup>2</sup>.',
     'This is the key move for <b>circle equations</b>: x<sup>2</sup> + x + y<sup>2</sup> + y = k becomes (x + &frac12;)<sup>2</sup> + (y + &frac12;)<sup>2</sup> = k + &frac12;, and r = &radic;(right side).']),
   ('Vieta&rsquo;s formulas (sum &amp; product of roots)', 'For ax<sup>2</sup> + bx + c = 0:  sum = &minus;b/a,  product = c/a', [
     'You can read the sum and product of the roots straight off the coefficients &mdash; no need to actually solve.',
     'Great for "product of the solutions is k&middot;(something)" questions.']),
 ],
 'worked':('Worked example &mdash; "exactly one solution"',
   'Find a so that y = &minus;1.5 and y = x<sup>2</sup> + 8x + a meet at exactly one point.',
   ['Set equal: x<sup>2</sup> + 8x + a = &minus;1.5, i.e. x<sup>2</sup> + 8x + (a + 1.5) = 0.',
    '"Exactly one solution" &rarr; discriminant = 0: 8<sup>2</sup> &minus; 4(1)(a + 1.5) = 0.',
    '64 &minus; 4(a + 1.5) = 0 &rarr; a + 1.5 = 16 &rarr; a = 14.5.',
    'So a = 14.5 (this is the actual M2 Q16 answer).']),
 'trap':'On M2 Q20 the equation is x<sup>2</sup>+x+y<sup>2</sup>+y = 199/2 (not "1992"). After completing the square on both x and y you add &frac14; twice: 199/2 + &frac14; + &frac14; = 100, so r = &radic;100 = <b>10</b>. Don&rsquo;t skip the "+&frac14; on both sides" step.',
 'problems':[
   {'ref':'Original &mdash; Math M2 Q13 (you answered 0)', 'orig':True,
    'stem':'In the equation x<sup>2</sup> &minus; 34x + c = 0, c is a constant. The equation has no real solutions if c &gt; n. What is the least possible value of n?',
    'solution':['No real solutions &rarr; discriminant &lt; 0: (&minus;34)<sup>2</sup> &minus; 4(1)(c) &lt; 0.',
                '1156 &minus; 4c &lt; 0 &rarr; c &gt; 289.',
                'So the least value of n is 289.'], 'answer':'289'},
   {'ref':'Original &mdash; Math M2 Q19 (you answered B; correct A)', 'orig':True,
    'stem':'57x<sup>2</sup> + (57b + a)x + ab = 0, where a and b are positive constants. The product of the solutions is k&middot;ab. What is k?',
    'opts':[('A','1/57'),('B','1/(57b)'),('C','57'),('D','ab')],
    'solution':['By Vieta&rsquo;s, product of roots = c/a = ab / 57.',
                'That equals k&middot;ab, so k&middot;ab = ab/57 &rarr; k = 1/57.'], 'answer':'A) 1/57'},
   {'ref':'Original &mdash; Math M2 Q20 (omitted)', 'orig':True,
    'stem':'The graph of x<sup>2</sup> + x + y<sup>2</sup> + y = 199/2 is a circle. What is the radius?',
    'solution':['Complete the square in x and y: add (&frac12;)<sup>2</sup> = &frac14; for each.',
                '(x + &frac12;)<sup>2</sup> + (y + &frac12;)<sup>2</sup> = 199/2 + &frac14; + &frac14; = 199/2 + &frac12; = 100.',
                'r<sup>2</sup> = 100 &rarr; r = 10.'], 'answer':'10'},
   {'ref':'Practice 1', 'stem':'x<sup>2</sup> + 12x + c = 0 has no real solutions if c &gt; n. Find the least n.',
    'solution':['D &lt; 0: 12<sup>2</sup> &minus; 4c &lt; 0 &rarr; 144 &lt; 4c &rarr; c &gt; 36.'], 'answer':'36'},
   {'ref':'Practice 2', 'stem':'The system y = 5 and y = x<sup>2</sup> &minus; 6x + a has exactly one real solution. What is a?',
    'solution':['x<sup>2</sup> &minus; 6x + a = 5 &rarr; x<sup>2</sup> &minus; 6x + (a &minus; 5) = 0.',
                'D = 0: (&minus;6)<sup>2</sup> &minus; 4(a &minus; 5) = 0 &rarr; 36 = 4(a &minus; 5) &rarr; a &minus; 5 = 9 &rarr; a = 14.'], 'answer':'14'},
   {'ref':'Practice 3', 'stem':'The graph of x<sup>2</sup> &minus; 6x + y<sup>2</sup> + 8y = 0 is a circle. Find its radius.',
    'solution':['Complete the square: (x &minus; 3)<sup>2</sup> &minus; 9 + (y + 4)<sup>2</sup> &minus; 16 = 0.',
                '(x &minus; 3)<sup>2</sup> + (y + 4)<sup>2</sup> = 25 &rarr; r = 5.'], 'answer':'5'},
   {'ref':'Practice 4', 'stem':'For 3x<sup>2</sup> + 12x + 7 = 0, what is the sum of the solutions?',
    'solution':['Vieta&rsquo;s: sum = &minus;b/a = &minus;12/3 = &minus;4.'], 'answer':'&minus;4'},
   {'ref':'Practice 5 (build from a table)', 'stem':'A quadratic f has f(&minus;1)=10, f(0)=14, f(1)=20. Find f(x) = ax<sup>2</sup>+bx+c.',
    'solution':['f(0)=14 &rarr; c = 14.',
                'f(1)=20 &rarr; a + b + 14 = 20 &rarr; a + b = 6.',
                'f(&minus;1)=10 &rarr; a &minus; b + 14 = 10 &rarr; a &minus; b = &minus;4.',
                'Add: 2a = 2 &rarr; a = 1, so b = 5.',
                'f(x) = x<sup>2</sup> + 5x + 14. (This mirrors M2 Q5.)'], 'answer':'f(x) = x<sup>2</sup> + 5x + 14'},
 ]}

# ---------- 2. EXPONENTIALS ----------
CLUSTERS['exponentials'] = {
 'slug':'exponentials', 'priority':2, 'misses':3,
 'title':'Exponential Functions &amp; Growth',
 'blurb':'P(t) = P&#8320;&middot;r<sup>t</sup> · geometric sequences · doubling · changing the time base',
 'fixes':'M1 Q14 (doubling), M1 Q19 (geometric sequence), M2 Q10 (rate per period).',
 'concepts':[
   ('The exponential model', 'P(t) = P&#8320; &middot; r<sup>t</sup>', [
     '<b>P&#8320;</b> is the starting amount; <b>r</b> is the growth factor per one unit of t.',
     'Growth of p% per period &rarr; r = 1 + p/100. Decay of p% &rarr; r = 1 &minus; p/100.',
     'r = 2 means doubling each period; r = &frac12; means halving.']),
   ('Doubling / halving every k units', 'P(t) = P&#8320; &middot; 2<sup>(t/k)</sup>', [
     'If it doubles every k time units, the exponent is t/k, not t.',
     'Example: doubles every 3 hours, after 15 hours &rarr; 2<sup>(15/3)</sup> = 2<sup>5</sup> = 32&times;.']),
   ('Geometric sequences', 'a&#8345; = a&#8321; &middot; r<sup>(n&minus;1)</sup>', [
     '"Each term is R times the one before" &rarr; geometric with ratio r = R.',
     'The exponent is (n &minus; 1) because the first term uses r<sup>0</sup> = 1.']),
   ('Changing the time base', None, [
     'To convert a per-year rate to per-18-months, raise the yearly factor to the 1.5 power.',
     'Per-period factor = r<sup>(period length in years)</sup>; then percent change = (factor &minus; 1)&times;100.']),
 ],
 'worked':('Worked example &mdash; rate per period',
   'P(t) = 290&middot;(1.0446)<sup>t</sup> models population t years after 2005. It increases by n% every 18 months. Find n.',
   ['18 months = 1.5 years, so the growth factor over one period is (1.0446)<sup>1.5</sup>.',
    '(1.0446)<sup>1.5</sup> &asymp; 1.0676.',
    'That&rsquo;s about a 6.76% increase &rarr; n &asymp; 6.8 (this is the M2 Q10 answer).']),
 'trap':'Don&rsquo;t read r directly as the answer. r = 1.0446 is the <b>yearly</b> factor; the question asks per 18 months, so you must raise it to the 1.5 power first. Reading "4.46%" straight off is the trap that cost the point.',
 'problems':[
   {'ref':'Original &mdash; Math M1 Q14 (you answered B; correct D)', 'orig':True,
    'stem':'Bacteria start at 300,000 cells/mL and double every 3 hours. How many cells/mL after 15 hours?',
    'opts':[('A','1,500,000'),('B','3,000,000'),('C','4,800,000'),('D','9,600,000')],
    'solution':['Number of doublings = 15 / 3 = 5.',
                '300,000 &times; 2<sup>5</sup> = 300,000 &times; 32 = 9,600,000.'], 'answer':'D) 9,600,000'},
   {'ref':'Original &mdash; Math M1 Q19 (you answered A; correct D)', 'orig':True,
    'stem':'The first term of a sequence is 9. Each term after the first is 4 times the preceding term. Which equation gives the nth term w?',
    'opts':[('A','w = 9 + 4n'),('B','w = 4 &middot; 9<sup>(n&minus;1)</sup>'),('C','w = 9 &middot; 4<sup>n</sup>'),('D','w = 9 &middot; 4<sup>(n&minus;1)</sup>')],
    'solution':['Geometric: first term 9, ratio 4.',
                'a&#8345; = a&#8321;&middot;r<sup>(n&minus;1)</sup> = 9&middot;4<sup>(n&minus;1)</sup>.',
                'Check n=1: 9&middot;4<sup>0</sup> = 9. &#10003;'], 'answer':'D) w = 9 &middot; 4<sup>(n&minus;1)</sup>'},
   {'ref':'Original &mdash; Math M2 Q10 (you answered B; correct C)', 'orig':True,
    'stem':'P(t) = 290&middot;(1.0446)<sup>t</sup> models population t years after 2005. Population increases by n% every 18 months. What is n (nearest tenth)?',
    'opts':[('A','4.5'),('B','6.7'),('C','6.8'),('D','9.0')],
    'solution':['18 months = 1.5 years &rarr; factor = 1.0446<sup>1.5</sup> &asymp; 1.0676.',
                'n = (1.0676 &minus; 1)&times;100 &asymp; 6.8.'], 'answer':'C) 6.8'},
   {'ref':'Practice 1', 'stem':'A sample starts at 50 mg and triples every 4 days. Write P(t) for t in days, then find P(12).',
    'solution':['P(t) = 50 &middot; 3<sup>(t/4)</sup>.',
                'P(12) = 50 &middot; 3<sup>3</sup> = 50 &times; 27 = 1350 mg.'], 'answer':'P(t)=50&middot;3<sup>(t/4)</sup>; P(12)=1350'},
   {'ref':'Practice 2', 'stem':'The first term of a geometric sequence is 5 and each term is 2&times; the previous. What is the 6th term?',
    'solution':['a&#8326; = 5 &middot; 2<sup>5</sup> = 5 &times; 32 = 160.'], 'answer':'160'},
   {'ref':'Practice 3', 'stem':'An investment grows 3% per year. By what percent does it grow over 2 years (nearest tenth)?',
    'solution':['Factor = 1.03<sup>2</sup> = 1.0609.',
                '(1.0609 &minus; 1)&times;100 = 6.09 &asymp; 6.1%.'], 'answer':'&asymp; 6.1%'},
   {'ref':'Practice 4', 'stem':'A colony halves every 6 hours. What fraction of the original remains after 24 hours?',
    'solution':['Number of halvings = 24/6 = 4.',
                '(&frac12;)<sup>4</sup> = 1/16.'], 'answer':'1/16'},
 ]}

# ---------- 3. LINEAR ----------
CLUSTERS['linear'] = {
 'slug':'linear', 'priority':3, 'misses':6,
 'title':'Linear Equations &amp; Systems',
 'blurb':'No-solution (parallel) condition · translating lines · reading the actual question',
 'fixes':'M1 Q6, Q9, Q18, Q22 · M2 Q4, Q11.',
 'concepts':[
   ('Slope-intercept form', 'y = mx + b', [
     'm is the slope; b is the y-intercept.',
     'Rewrite every line into this form before comparing two lines.']),
   ('When does a system have no / one / infinite solutions?', None, [
     '<b>No solution</b> &rarr; same slope, different intercept (parallel lines).',
     '<b>Infinitely many</b> &rarr; same slope AND same intercept (the same line).',
     '<b>Exactly one</b> &rarr; different slopes.',
     'So "no solution" questions are really "make the slopes equal" questions.']),
   ('Translating a line', None, [
     'Down k units: replace y with (y + k), i.e. subtract k from the whole right side of y = &hellip;',
     'Shortcut in standard form Ax + By = C: shifting down k changes C by &minus;Bk.',
     'To find an x-intercept, set y = 0 and solve for x.']),
   ('Slope from two points', 'm = (y&#8322; &minus; y&#8321;) / (x&#8322; &minus; x&#8321;)', [
     'Plug the two given points in carefully &mdash; keep the order consistent top and bottom.']),
 ],
 'worked':('Worked example &mdash; translate then find the x-intercept',
   'The graph of 9x &minus; 10y = 19 is translated down 4 units. Find the x-coordinate of the x-intercept.',
   ['Down 4 units: y &rarr; y + 4, so 9x &minus; 10(y + 4) = 19.',
    'Expand: 9x &minus; 10y &minus; 40 = 19 &rarr; 9x &minus; 10y = 59.',
    'x-intercept: set y = 0 &rarr; 9x = 59 &rarr; x = 59/9 &asymp; 6.556.']),
 'trap':'Translating <b>down</b> k means y becomes (y + k), which <i>raises</i> the constant on the other side. Getting the sign backwards (using y &minus; k) is exactly how M1 Q22 was missed. Also: M1 Q9 asked for x &minus; 1, not x &mdash; read the ask.',
 'problems':[
   {'ref':'Original &mdash; Math M1 Q9 (you answered 1)', 'orig':True,
    'stem':'If 4x &minus; 4 = 112, what is the positive value of x &minus; 1?',
    'solution':['4x = 116 &rarr; x = 29.',
                'The question asks for x &minus; 1 = 28 (not x). Read the ask!'], 'answer':'28'},
   {'ref':'Original &mdash; Math M1 Q22 (you answered 5)', 'orig':True,
    'stem':'The graph of 9x &minus; 10y = 19 is translated down 4 units. What is the x-coordinate of the x-intercept of the resulting graph?',
    'solution':['y &rarr; y + 4: 9x &minus; 10(y + 4) = 19 &rarr; 9x &minus; 10y = 59.',
                'Set y = 0: x = 59/9 &asymp; 6.556.'], 'answer':'59/9 (&asymp; 6.556)'},
   {'ref':'Original &mdash; Math M2 Q11 (you answered 2)', 'orig':True,
    'stem':'In 2kx &minus; n = (&minus;28/15)x &minus; (36/19), k and n are constants with n &gt; 1. The equation has no solution. What is k?',
    'solution':['No solution &rarr; the x-coefficients must match while constants differ.',
                '2k = &minus;28/15 &rarr; k = &minus;14/15.'], 'answer':'&minus;14/15 (&asymp; &minus;0.933)'},
   {'ref':'Original &mdash; Math M2 Q4 (you answered B; correct C)', 'orig':True,
    'stem':'A line passes through (0, 7) and (8, 0). The point (d, 4) lies on the line. What is d? (Answer choices are fractions: 7/2, 26/7, 24/7, 27/8.)',
    'opts':[('A','7/2'),('B','26/7'),('C','24/7'),('D','27/8')],
    'solution':['Slope = (0 &minus; 7)/(8 &minus; 0) = &minus;7/8, so y = 7 &minus; (7/8)x.',
                'Set y = 4: 4 = 7 &minus; (7/8)d &rarr; (7/8)d = 3 &rarr; d = 24/7.'], 'answer':'C) 24/7'},
   {'ref':'Practice 1', 'stem':'For what value of a does the system y = 3x + 1 and y = ax &minus; 4 have no solution?',
    'solution':['No solution &rarr; equal slopes, different intercepts.',
                'a = 3 (intercepts 1 &ne; &minus;4, so parallel). a = 3.'], 'answer':'3'},
   {'ref':'Practice 2', 'stem':'The line 2x + 5y = 20 is translated down 3 units. Find the new x-intercept.',
    'solution':['y &rarr; y + 3: 2x + 5(y + 3) = 20 &rarr; 2x + 5y = 5.',
                'y = 0 &rarr; x = 5/2 = 2.5.'], 'answer':'2.5'},
   {'ref':'Practice 3', 'stem':'If 6x + 3 = 39, what is the value of 2x + 1?',
    'solution':['6x = 36 &rarr; x = 6. Then 2x + 1 = 13. (Read what&rsquo;s asked.)'], 'answer':'13'},
   {'ref':'Practice 4', 'stem':'A line passes through (0, &minus;3) and (4, 5). Find the x-intercept.',
    'solution':['Slope = (5 &minus; (&minus;3))/(4 &minus; 0) = 8/4 = 2, so y = 2x &minus; 3.',
                'y = 0 &rarr; x = 3/2 = 1.5.'], 'answer':'1.5'},
 ]}

# ---------- 4. FUNCTIONS ----------
CLUSTERS['functions'] = {
 'slug':'functions', 'priority':4, 'misses':2,
 'title':'Function Evaluation &amp; Asymptotes',
 'blurb':'Substituting into f(x) · solving for a constant · reading rational-function graphs',
 'fixes':'M2 Q6 (solve for a constant), M2 Q18 (rational-function graph).',
 'concepts':[
   ('Evaluating and solving', None, [
     'f(a) means substitute a for x everywhere, then simplify.',
     'If f(a) = value, set the expression equal to that value and solve for a step by step.']),
   ('Rational functions &amp; asymptotes', None, [
     '<b>Vertical asymptote</b>: where the denominator = 0 (the graph shoots to &plusmn;&infin;).',
     '<b>Horizontal asymptote</b>: the value the graph approaches as x &rarr; &plusmn;&infin; &mdash; often the ratio of leading coefficients, or y = 0 when the bottom grows faster.',
     'Match a described graph to an equation by checking: where does it blow up? what does it level off to?']),
   ('Reading a described curve', None, [
     '"Approaches the line x = &minus;4" &rarr; vertical asymptote at x = &minus;4 &rarr; denominator has (x + 4).',
     '"Approaches y = 0 as x decreases" &rarr; horizontal asymptote y = 0.']),
 ],
 'worked':('Worked example &mdash; solve for a constant',
   'f(x) = (x + 15)/5 and f(a) = 10. Find a.',
   ['Substitute: (a + 15)/5 = 10.',
    'Multiply by 5: a + 15 = 50.',
    'a = 35. (Mirrors the structure of M2 Q6.)']),
 'trap':'When a function has a fraction, clear the denominator <b>first</b> by multiplying both sides &mdash; don&rsquo;t try to eyeball it. And match asymptotes to the graph before checking specific points; the vertical asymptote alone often eliminates 2&ndash;3 choices.',
 'problems':[
   {'ref':'Original &mdash; Math M2 Q6 (you answered B; correct C)', 'orig':True,
    'stem':'The function f is defined by f(x) = (x + 15)/5, and f(a) = 10, where a is a constant. What is a?',
    'opts':[('A','2'),('B','25'),('C','35'),('D','65')],
    'solution':['(a + 15)/5 = 10 &rarr; a + 15 = 50 &rarr; a = 35.'], 'answer':'C) 35'},
   {'ref':'Original &mdash; Math M2 Q18 (you answered B; correct C)', 'orig':True,
    'stem':'A curve is in quadrant 3, trending down sharply. As x increases it approaches the line x = &minus;4; as x decreases it approaches y = 0. Which equation could define the curve?',
    'opts':[('A','y = 1/(x &minus; 4)'),('B','y = 1/x &minus; 4'),('C','y = &minus;1/(x + 4)'),('D','y = &minus;1/x + 4')],
    'solution':['Vertical asymptote at x = &minus;4 &rarr; denominator (x + 4). Eliminates A, B, D.',
                'Horizontal asymptote y = 0 (no constant added) matches C.',
                'The negative sign puts the relevant branch in quadrant 3.'], 'answer':'C) y = &minus;1/(x + 4)'},
   {'ref':'Practice 1', 'stem':'f(x) = (2x &minus; 6)/4 and f(a) = 5. Find a.',
    'solution':['(2a &minus; 6)/4 = 5 &rarr; 2a &minus; 6 = 20 &rarr; 2a = 26 &rarr; a = 13.'], 'answer':'13'},
   {'ref':'Practice 2', 'stem':'g(x) = 3x<sup>2</sup> &minus; x + 2. What is g(&minus;2)?',
    'solution':['3(&minus;2)<sup>2</sup> &minus; (&minus;2) + 2 = 12 + 2 + 2 = 16.'], 'answer':'16'},
   {'ref':'Practice 3', 'stem':'A rational function has a vertical asymptote at x = 3 and a horizontal asymptote at y = 0. Which could it be: y = 1/(x&minus;3), y = 1/(x+3), or y = 1/x + 3?',
    'solution':['Vertical asymptote at x = 3 &rarr; denominator (x &minus; 3).',
                'Horizontal asymptote y = 0 &rarr; no added constant.',
                'So y = 1/(x &minus; 3).'], 'answer':'y = 1/(x &minus; 3)'},
   {'ref':'Practice 4', 'stem':'h(x) = (x + 1)/(x &minus; 2). For large x, what value does h approach?',
    'solution':['Ratio of leading coefficients = 1/1 = 1.',
                'Horizontal asymptote y = 1.'], 'answer':'1'},
 ]}

# ---------- 5. PERCENT & EXPONENTS ----------
CLUSTERS['percent_exponents'] = {
 'slug':'percent_exponents', 'priority':5, 'misses':2,
 'title':'Percent Change &amp; Exponent Rules',
 'blurb':'Multiplying by 1.07 for +7% · fractional exponents &amp; radicals',
 'fixes':'M1 Q17 (percent), M1 Q16 (fractional exponents).',
 'concepts':[
   ('Percent change as a multiplier', None, [
     'Increase by p% &rarr; multiply by <b>(1 + p/100)</b>. A 7% increase &rarr; &times;1.07.',
     'Decrease by p% &rarr; multiply by (1 &minus; p/100). A 7% decrease &rarr; &times;0.93.',
     'Successive changes multiply: +10% then +20% &rarr; &times;1.10&times;1.20 = &times;1.32 (not +30%).']),
   ('Exponent rules', None, [
     'x<sup>a</sup>&middot;x<sup>b</sup> = x<sup>a+b</sup> &nbsp;&middot;&nbsp; x<sup>a</sup>/x<sup>b</sup> = x<sup>a&minus;b</sup> &nbsp;&middot;&nbsp; (x<sup>a</sup>)<sup>b</sup> = x<sup>ab</sup>.',
     '(xy)<sup>a</sup> = x<sup>a</sup>y<sup>a</sup>.']),
   ('Fractional exponents &amp; radicals', 'x<sup>(1/n)</sup> = <sup>n</sup>&radic;x ,  x<sup>(a/b)</sup> = <sup>b</sup>&radic;(x<sup>a</sup>)', [
     'Rewrite radicals as fractional exponents to combine them cleanly.',
     '<sup>7</sup>&radic;(x<sup>9</sup>y<sup>9</sup>) = (x<sup>9</sup>y<sup>9</sup>)<sup>(1/7)</sup> = x<sup>(9/7)</sup>y<sup>(9/7)</sup>.']),
 ],
 'worked':('Worked example &mdash; a clean percent multiplier',
   'City A&rsquo;s population rose 7% from 2015 to 2016. If 2016 = k &times; 2015, what is k?',
   ['A 7% increase means multiply by 1 + 0.07 = 1.07.',
    'So k = 1.07 (this is the M1 Q17 answer).']),
 'trap':'"+7%" is <b>&times;1.07</b>, not &times;0.07 and not &times;1.7. This is a one-line idea but it cost a point on M1 Q17. For exponents, rewrite every radical as a fractional power before combining &mdash; don&rsquo;t guess.',
 'problems':[
   {'ref':'Original &mdash; Math M1 Q17 (you answered A; correct C)', 'orig':True,
    'stem':'The population of City A increased by 7% from 2015 to 2016. If the 2016 population is k times the 2015 population, what is k?',
    'opts':[('A','0.07'),('B','0.7'),('C','1.07'),('D','1.7')],
    'solution':['+7% &rarr; multiply by 1 + 7/100 = 1.07.',
                'So k = 1.07.'], 'answer':'C) 1.07'},
   {'ref':'Original &mdash; Math M1 Q16 (you answered D; correct B)', 'orig':True,
    'stem':'Which expression is equivalent to <sup>7</sup>&radic;(x<sup>9</sup>y<sup>9</sup>), where x and y are positive?',
    'opts':[('A','x<sup>7</sup>y<sup>7</sup>'),('B','x<sup>(9/7)</sup>y<sup>(9/7)</sup>'),('C','x<sup>63</sup>y<sup>63</sup>'),('D','(xy)<sup>7</sup>')],
    'solution':['A 7th root is the (1/7) power: (x<sup>9</sup>y<sup>9</sup>)<sup>(1/7)</sup>.',
                'Multiply exponents: x<sup>(9&middot;1/7)</sup>y<sup>(9&middot;1/7)</sup> = x<sup>(9/7)</sup>y<sup>(9/7)</sup>.'], 'answer':'B) x<sup>(9/7)</sup>y<sup>(9/7)</sup>'},
   {'ref':'Practice 1', 'stem':'A price falls 15%. If the new price is k times the old, what is k?',
    'solution':['&minus;15% &rarr; &times;(1 &minus; 0.15) = 0.85. k = 0.85.'], 'answer':'0.85'},
   {'ref':'Practice 2', 'stem':'A value increases 20%, then increases another 10%. Overall multiplier?',
    'solution':['1.20 &times; 1.10 = 1.32 (a 32% total increase).'], 'answer':'1.32'},
   {'ref':'Practice 3', 'stem':'Simplify <sup>3</sup>&radic;(x<sup>6</sup>) for x &gt; 0.',
    'solution':['(x<sup>6</sup>)<sup>(1/3)</sup> = x<sup>(6/3)</sup> = x<sup>2</sup>.'], 'answer':'x<sup>2</sup>'},
   {'ref':'Practice 4', 'stem':'Write &radic;(x<sup>5</sup>) as a single power of x.',
    'solution':['&radic; is the (1/2) power: (x<sup>5</sup>)<sup>(1/2)</sup> = x<sup>(5/2)</sup>.'], 'answer':'x<sup>(5/2)</sup>'},
   {'ref':'Practice 5', 'stem':'Simplify x<sup>3</sup> &middot; x<sup>4</sup> / x<sup>2</sup>.',
    'solution':['Add then subtract exponents: 3 + 4 &minus; 2 = 5 &rarr; x<sup>5</sup>.'], 'answer':'x<sup>5</sup>'},
 ]}

ORDER = ['quadratics','exponentials','linear','functions','percent_exponents']

# ============================================================
# BUILD
# ============================================================
def build_guide(c):
    body = nav([('&larr; Dashboard','index.html'),
                (f'Worksheet: {c["title"]} &rarr;', f'math_ws_{c["slug"]}.html')])
    body += f'<span class="pill">Study guide &middot; Priority {c["priority"]}</span>'
    body += f'<h1>{c["title"]}</h1>'
    body += f'<p class="sub">{c["blurb"]}</p>'
    body += f'<div class="callout"><b>Fixes these misses:</b> {c["fixes"]}</div>'
    body += '<h2>Core concepts</h2>'
    for title, fml, items in c['concepts']:
        blk = f'<div class="block"><h4>{title}</h4>'
        if fml: blk += f'<div class="fml">{fml}</div>'
        blk += '<ul>' + "".join(f'<li>{it}</li>' for it in items) + '</ul></div>'
        body += blk
    wt, wp, ws = c['worked']
    body += f'<h2>{wt}</h2><div class="eg"><div class="step"><b>Problem.</b> {wp}</div>'
    body += "".join(f'<div class="step">{s}</div>' for s in ws) + '</div>'
    body += f'<div class="trap"><b>Watch out:</b> {c["trap"]}</div>'
    body += (f'<div class="callout" style="margin-top:20px">Ready to practice? '
             f'<b><a href="math_ws_{c["slug"]}.html" style="color:var(--accent)">'
             f'Open the {c["title"]} worksheet &rarr;</a></b></div>')
    body += '<footer>PSAT 1 &middot; Math study guide</footer>'
    return page(f'PSAT Math &mdash; {c["title"]} Guide', body)

def build_worksheet(c):
    body = nav([('&larr; Dashboard','index.html'),
                (f'&larr; Study guide: {c["title"]}', f'math_guide_{c["slug"]}.html')])
    body += '<span class="pill">Worksheet &middot; solutions included</span>'
    body += f'<h1>{c["title"]} &mdash; Practice Worksheet</h1>'
    body += ('<p class="sub">Try each problem first, then click <b>Show solution</b>. '
             'To print an answer key, open all solutions before File&nbsp;&#9656;&nbsp;Print.</p>')
    origs = [p for p in c['problems'] if p.get('orig')]
    news  = [p for p in c['problems'] if not p.get('orig')]
    body += '<h2>Section A &mdash; the questions you missed</h2>'
    body += "".join(render_problem(p, "orig") for p in origs)
    body += '<h2>Section B &mdash; new practice (same skills)</h2>'
    body += "".join(render_problem(p) for p in news)
    body += '<footer>PSAT 1 &middot; Math worksheet</footer>'
    return page(f'PSAT Math &mdash; {c["title"]} Worksheet', body)

made=[]
for slug in ORDER:
    c = CLUSTERS[slug]
    gf, wf = f'math_guide_{slug}.html', f'math_ws_{slug}.html'
    open(gf,'w',encoding='utf-8').write(build_guide(c)); made.append(gf)
    open(wf,'w',encoding='utf-8').write(build_worksheet(c)); made.append(wf)
    nprob=len(c['problems'])
    print(f"{slug}: guide + worksheet ({nprob} problems, {sum(1 for p in c['problems'] if p.get('orig'))} originals)")

print("\nWrote", len(made), "files:")
for f in made: print("  ", f)

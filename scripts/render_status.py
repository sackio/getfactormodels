#!/usr/bin/env python3
"""Render PROJECT.md to the operator status page.

⛔ The page is a RENDERING of PROJECT.md, never a second copy. Regenerate it from the file on
every material change; do not hand-edit the HTML. A hand-maintained page is a second store and
drifts from the list it claims to show.
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
md = (ROOT / "PROJECT.md").read_text()

done = [l for l in md.splitlines() if l.startswith("- [x]")]
todo = [l for l in md.splitlines() if l.startswith("- [ ]")]
total = len(done) + len(todo)
pct = round(100 * len(done) / total) if total else 0
sha = subprocess.run(["git", "-C", str(ROOT), "log", "--oneline", "-1"],
                     capture_output=True, text=True).stdout.strip()
stamp = subprocess.run(["date", "-u", "+%Y-%m-%d %H:%MZ"], capture_output=True, text=True).stdout.strip()


def item(line):
    body = html.escape(line[6:].strip())
    body = re.sub(r"`([^`]+)`", r"<code>\1</code>", body)
    return body


def section(title, lines, cls):
    rows = "".join(f'<li class="{cls}">{item(l)}</li>' for l in lines)
    return f"<h2>{title} <span class=n>{len(lines)}</span></h2><ul>{rows}</ul>" if lines else ""


head = md.split("---")[0]
done_def = re.search(r"\*\*DONE means:\*\*(.+?)\n\n", head, re.S)
done_def = " ".join(done_def.group(1).split()) if done_def else ""

print(f"""<!doctype html><meta charset=utf-8><title>getfactormodels</title>
<style>
 body{{font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:44rem;
   margin:2.5rem auto;padding:0 1.2rem;color:#1a1a1a}}
 h1{{font-size:1.5rem;margin:0 0 .2rem}} h2{{font-size:1rem;margin:1.8rem 0 .5rem;color:#444}}
 .sub{{color:#666;margin:0 0 1.4rem}} .n{{color:#999;font-weight:400;font-size:.85em}}
 .bar{{height:7px;background:#e8e8e8;border-radius:4px;overflow:hidden;margin:.7rem 0 .3rem}}
 .bar i{{display:block;height:100%;background:#2f7d32;width:{pct}%}}
 ul{{list-style:none;padding:0;margin:0}}
 li{{padding:.42rem 0 .42rem 1.5rem;position:relative;border-bottom:1px solid #f0f0f0}}
 li.d{{color:#777}} li.d:before{{content:"✓";position:absolute;left:0;color:#2f7d32}}
 li.t:before{{content:"○";position:absolute;left:0;color:#bbb}}
 code{{background:#f4f4f4;padding:.08em .35em;border-radius:3px;font-size:.9em}}
 footer{{margin-top:2.4rem;color:#888;font-size:.82em;border-top:1px solid #eee;padding-top:.8rem}}
</style>
<h1>getfactormodels</h1>
<p class=sub>{html.escape(done_def)}</p>
<div class=bar><i></i></div>
<p class=sub><b>{len(done)} of {total}</b> done · {len(todo)} remaining</p>
{section("Remaining", todo, "t")}
{section("Done", done, "d")}
<footer>Rendered from <code>PROJECT.md</code> on branch <code>work</code> at {stamp}.<br>
Head: <code>{html.escape(sha)}</code> · <a href="https://github.com/sackio/getfactormodels">sackio/getfactormodels</a><br>
⛔ Generated, not hand-written — edit the file, not this page.</footer>""")

#!/usr/bin/env python3
"""Inline the question bank into a single self-contained index.html and validate the bank."""
import json, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).parent
src = root / "src"
qs = "\n".join((src / f).read_text(encoding="utf-8") for f in ("q1.js", "q2.js", "q3.js", "q4.js", "fix.js", "ex.js"))
html = (src / "app.html").read_text(encoding="utf-8")
assert "/*__QUESTIONS__*/" in html
out = html.replace("/*__QUESTIONS__*/", qs)
(root / "index.html").write_text(out, encoding="utf-8")

# Validate with node: structure, duplicates, quotas, sign ids
check = r"""
const Q=[];
%s
const QUOTA={signs:3,signals:2,row:3,speed:3,lanes:3,turns:2,parking:3,freeway:2,safe:4,weather:2,sharing:3,alcohol:2,belts:1,admin:3};
const SIGNS=new Set(%s);
let err=0;const seenQ=new Set();const counts={};
Q.forEach((r,i)=>{
  const bad=m=>{console.log('ROW',i,m,'::',r[1]);err++};
  if(r.length!==8)bad('len '+r.length);
  if(!(r[0] in QUOTA))bad('cat');
  for(const k of [1,2,6])if(typeof r[k]!=='string'||r[k].length<3)bad('str '+k);
  for(const k of [3,4,5]){if(!Array.isArray(r[k])||r[k].length!==2||!r[k][0]||!r[k][1])bad('opt '+k)}
  const o=new Set([r[3][0],r[4][0],r[5][0]]);if(o.size!==3)bad('dup option');
  const key=r[1]+'|'+(r[7].s||'');if(seenQ.has(key))bad('dup question');seenQ.add(key);
  if(r[7].s&&!SIGNS.has(r[7].s))bad('unknown sign '+r[7].s);
  counts[r[0]]=(counts[r[0]]||0)+1;
});
Q.forEach((r,i)=>{const e=r[7].e||EX[i];if(typeof e!=='string'||e.length<8){console.log('missing EN explanation',i);err++}});
for(const c in QUOTA){if((counts[c]||0)<QUOTA[c]*2){console.log('too few in',c);err++}}
const bac=Q.filter(r=>r[7].t==='bac').length,sale=Q.filter(r=>r[7].t==='sale').length;
console.log(JSON.stringify({total:Q.length,counts,bac,sale,quota:Object.values(QUOTA).reduce((a,b)=>a+b,0)}));
process.exit(err?1:0);
"""
signs = sorted(set(re.findall(r'case "(\w+)":', html)))
tmp = root / ".check.js"
tmp.write_text(check % (qs, json.dumps(signs)), encoding="utf-8")
r = subprocess.run(["node", str(tmp)], capture_output=True, text=True)
tmp.unlink()
print(r.stdout, r.stderr)
print("index.html bytes:", len(out.encode()))
sys.exit(r.returncode)

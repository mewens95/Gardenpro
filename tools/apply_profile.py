from pathlib import Path
import re
p=Path('index.html'); s=p.read_text()
if 'My GardenPro' in s: raise SystemExit(0)
s=s.replace('function setPage(p){page=p;render()}', '''function setPage(p){page=p;render()}
let profile=JSON.parse(localStorage.getItem('gardenpro_profile_v2')||'{"business":"GardenPro","name":"","phone":"","email":"","address":"","tax":""}');
function openProfile(){profileModal.style.display='flex';pbusiness.value=profile.business||'';pname.value=profile.name||'';pphone.value=profile.phone||'';pemail.value=profile.email||'';paddress.value=profile.address||'';ptax.value=profile.tax||''}
function closeProfile(){profileModal.style.display='none'}
function saveProfile(){profile={business:pbusiness.value.trim()||'GardenPro',name:pname.value.trim(),phone:pphone.value.trim(),email:pemail.value.trim(),address:paddress.value.trim(),tax:ptax.value.trim()};localStorage.setItem('gardenpro_profile_v2',JSON.stringify(profile));closeProfile();head()}''')
s=s.replace('<button class="secondary small noPrint" onclick="logout()">Log out</button>','<div style="display:flex;gap:8px"><button class="secondary small noPrint" onclick="openProfile()">👤 My GardenPro</button><button class="secondary small noPrint" onclick="logout()">Log out</button></div>')
pat=r'function printDoc\(type,id\)\{.*?\}\nfunction boot\(\)'
new='''function printDoc(type,id){let x=(type==='quote'?data.quotes:data.invoices).find(v=>v.id===id),c=data.customers.find(v=>v.id===x.customer_id)||{},title=type==='quote'?'QUOTE':'INVOICE';let w=window.open('','_blank');w.document.write(`<html><head><title>${title}</title><style>body{font-family:Arial;padding:40px;max-width:800px;margin:auto}h1{color:#1f7a3d}.meta{white-space:pre-line;margin-bottom:30px}.box{border:1px solid #ddd;padding:20px;border-radius:10px}</style></head><body><h1>${esc(profile.business||'GardenPro')}</h1><div class="meta">${esc(profile.name)}\\n${esc(profile.phone)} · ${esc(profile.email)}\\n${esc(profile.address)}\\n${profile.tax?'VAT/Tax: '+esc(profile.tax):''}</div><h2>${title}</h2><div class="box"><b>${esc(x.title)}</b><p>Customer: ${esc(c.name||'')}</p><p>${esc(c.address||'')}</p><p>Amount: ${fmtMoney(x.amount)}</p><p>Status: ${esc(x.status)}</p></div></body></html>`);w.document.close();w.print()}
function boot()'''
s,n=re.subn(pat,new,s,flags=re.S)
if n!=1: raise SystemExit('printDoc replacement failed')
modal='''<div id="profileModal" style="display:none;position:fixed;inset:0;background:#0006;align-items:center;justify-content:center;padding:18px;z-index:100"><div style="background:#fff;border-radius:18px;padding:20px;width:min(520px,100%);max-height:90vh;overflow:auto"><div class="row"><h2 style="margin:0">My GardenPro</h2><button class="secondary small" onclick="closeProfile()">Close</button></div><p class="muted">Your business details appear on printed quotes and invoices.</p><div class="form"><label>Business Name</label><input id="pbusiness"><label>Your Name</label><input id="pname"><label>Phone</label><input id="pphone"><label>Email</label><input id="pemail" type="email"><label>Business Address</label><textarea id="paddress"></textarea><label>VAT/Tax Number</label><input id="ptax"><button onclick="saveProfile()">Save profile</button></div></div></div>'''
s=s.replace('<header id="header"></header><main id="app"></main><div id="nav"></div>','<header id="header"></header><main id="app"></main><div id="nav"></div>'+modal)
p.write_text(s)

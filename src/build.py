#!/usr/bin/env python3
"""Sinh index.html, sw.js, manifest.webmanifest từ src/app.html. Dùng: python3 src/build.py "Bản 01 · 03/11/2026" """
import sys, re, hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/"src/app.html").read_text(encoding="utf8")
localdb = (root/"src/localdb.js").read_text(encoding="utf8")
version = sys.argv[1] if len(sys.argv) > 1 else "Bản 00"
CREATOR = "Hoàng Trung Đức"

def rep(s, a, b, count=1):
    assert a in s, "không thấy: " + a[:60]
    return s.replace(a, b, count)

# 1. Khung trang đầy đủ (artifact không có sẵn)
src = rep(src, '<meta name="claude:viewport-fit-sides" content="cover">\n', '')
head = f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0B7A63" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1815" media="(prefers-color-scheme: dark)">
<meta name="author" content="{CREATOR}">
<meta name="description" content="Những người quá rảnh: tìm ngày rảnh chung cho nhóm bạn.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Quá rảnh">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>:root{{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}[hidden]{{display:none!important}}img{{max-width:100%}}</style>
'''
src = head + src
# kết thúc
src = src.rstrip() + "\n</body></html>\n"
src = rep(src, '<div class="app">', '<body>\n<div class="app">')

# 2. Nhãn phiên bản + người tạo + nút cài app
src = rep(src, '  <div id="view"></div>\n</div>',
 f'''  <div id="view"></div>
  <footer class="ver"><button id="sync" class="linkbtn" type="button">Đồng bộ giữa các thiết bị</button><button id="install" class="linkbtn" type="button">Cài app lên điện thoại</button>
  <p id="verline">Những người quá rảnh · {version} · Người tạo: {CREATOR}</p></footer>
</div>
<div id="toast" class="toast" role="status" hidden><span>Đã có bản mới.</span> <button id="toast-reload" class="btn sm" type="button">Tải lại</button></div>''')
src = rep(src, '<span class="pill">Bản xem thử</span>', f'<span class="pill">{version.split(" · ")[0]}</span>')
css = '''
.ver{margin:28px 0 8px;text-align:center;color:var(--muted);font-size:12px;display:grid;gap:6px;justify-items:center}
.ver p{margin:0}
.linkbtn{font:inherit;font-size:13px;font-weight:600;color:var(--free);background:none;border:0;text-decoration:underline;cursor:pointer;padding:6px}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:30;display:flex;align-items:center;gap:10px;background:var(--ink);color:var(--bg);padding:10px 12px 10px 16px;border-radius:12px;font-size:14px}
'''
src = rep(src, '</style>', css + '</style>')

# 3. Lớp dữ liệu: Firebase nếu có cấu hình, không thì kho một máy
src = rep(src, 'var ARTIFACT_URL="https://claude.ai/artifact/LZwo6PUk6G6kNWSLWy52Qc";', 'var ARTIFACT_URL="";\n' + localdb + '\nvar deferredInstall=null;window.addEventListener("beforeinstallprompt",function(e){e.preventDefault();deferredInstall=e});')
boot_old = src[src.index('  var C=window.claude,user=null;'):src.index('  var slow=setTimeout')]
boot_new = '''  var cfg=window.CUNGRANH_FIREBASE;
  S.local=true;
  if(cfg&&cfg.apiKey){
    try{
      await loadFirebase();
      firebase.initializeApp(cfg);
      var auth=firebase.auth();
      await new Promise(function(res){var u=auth.onAuthStateChanged(function(){u();res()})});
      if(!auth.currentUser)await auth.signInAnonymously();
      S.db=firebase.firestore();S.auth=auth;S.uid=auth.currentUser.uid;S.local=false;
    }catch(e){S.db=null}
  }
  if(!S.db&&!(cfg&&cfg.apiKey)){S.db=makeLocalDb();S.uid=localUid()}
  if(!S.db||!S.uid){S.off=true;S.profile={name:"",groups:[]};render();return}
'''
src = src.replace(boot_old, boot_new)
src = rep(src, '(async function(){\n  var cfg', '''function loadScript(u){return new Promise(function(res,rej){var s=document.createElement("script");s.src=u;s.onload=res;s.onerror=rej;document.head.appendChild(s)})}
async function loadFirebase(){
  var b="https://cdnjs.cloudflare.com/ajax/libs/firebase/10.12.2/";
  await loadScript(b+"firebase-app-compat.min.js");
  await Promise.all([loadScript(b+"firebase-auth-compat.min.js"),loadScript(b+"firebase-firestore-compat.min.js")]);
}
(async function(){
  var cfg''')
# banner chế độ một máy
src = rep(src, '  else bn.hidden=true;', '  else if(S.local){bn.hidden=false;bn.textContent="Đang ở chế độ một máy: nhóm và lời mời mới chỉ có trên thiết bị này. Khi kết nối máy chủ, nhóm sẽ dùng chung giữa mọi người."}\n  else bn.hidden=true;')
src = rep(src, 'Chưa kết nối được kho dữ liệu chung. Hãy đăng nhập rồi mở lại trang bằng link được chia sẻ.', 'Chưa kết nối được máy chủ. Kiểm tra mạng rồi tải lại trang.')

# 4. Chọn cách dùng: cài app thật khi trình duyệt cho phép
src = rep(src, 'function sheetPlatform(gid){', '''function isStandalone(){return (window.matchMedia&&matchMedia("(display-mode: standalone)").matches)||navigator.standalone===true}
function sheetPlatform(gid){
  if(gid&&isStandalone())return;''')
src = rep(src, '''onclick:function(){
      steps.hidden=false;''', '''onclick:function(){
      if(deferredInstall){deferredInstall.prompt();deferredInstall.userChoice.then(function(){deferredInstall=null;api.close()});return}
      steps.hidden=false;''')
src = rep(src, 'Bản xem thử chưa có app trên kho ứng dụng. “App” ở đây là bản cài lên màn hình chính từ trang web, mở ra không có thanh địa chỉ. Cả hai cách đều dùng chung nhóm của bạn.', '“App” ở đây là bản cài lên màn hình chính từ trang web, mở ra không có thanh địa chỉ và chạy được cả khi mạng yếu. Dùng web hay app thì nhóm của bạn vẫn như nhau.')
src = rep(src, 'render();\nfunction loadScript', 'render();\n$("#install").addEventListener("click",function(){sheetPlatform(null)});\n$(\"#sync\").addEventListener(\"click\",function(){sheetSync()});\nfunction loadScript')

# 5. Đăng ký service worker + báo bản mới
sw_reg = '''<script>
if("serviceWorker" in navigator){
  var had=!!navigator.serviceWorker.controller;
  navigator.serviceWorker.register("sw.js").then(function(r){setInterval(function(){r.update().catch(function(){})},3600000)}).catch(function(){});
  navigator.serviceWorker.addEventListener("controllerchange",function(){
    if(!had){had=true;return}
    var t=document.getElementById("toast");t.hidden=false;
    document.getElementById("toast-reload").onclick=function(){location.reload()};
  });
}
</script>
'''
src = rep(src, '<script>\n(function(){', '<script src="config.js"></script>\n<script>\n(function(){')
src = rep(src, '</body></html>', sw_reg + '</body></html>')
(root/"index.html").write_text(src, encoding="utf8")

# sw.js
h = hashlib.sha256((src + (root/"config.js").read_text(encoding="utf8")).encode()).hexdigest()[:10]
sw = f'''const CACHE="cungranh-{h}";
const SHELL=["./","index.html","config.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png","icons/apple-touch-icon.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{
  const r=e.request;if(r.method!=="GET")return;
  const u=new URL(r.url);
  if(u.origin===location.origin){{
    if(r.mode==="navigate"||u.pathname.endsWith("/config.js")||u.pathname.endsWith("/index.html")){{
      e.respondWith(fetch(r,{{cache:"no-store"}}).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res}}).catch(()=>caches.match(r).then(m=>m||caches.match("index.html"))));
    }} else {{
      e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res}})));
    }}
  }} else if(u.hostname==="fonts.googleapis.com"||u.hostname==="fonts.gstatic.com"){{
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res}})));
  }}
}});
'''
(root/"sw.js").write_text(sw, encoding="utf8")
manifest = {"name":"Những người quá rảnh","short_name":"Quá rảnh","description":"Tìm ngày rảnh chung cho nhóm bạn","lang":"vi","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","theme_color":"#0B7A63","background_color":"#EDF2EE",
 "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icons/icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
(root/"manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf8")
(root/".nojekyll").write_text("")
print("OK", version, h)

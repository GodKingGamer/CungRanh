// Dùng: node src/qc/qcpwa.js 8766  (chạy http.server ở gốc repo trước)
const {chromium,devices}=require('playwright');
(async()=>{const port=process.argv[2]||8766;const url=`http://localhost:${port}/`;
const b=await chromium.launch();const ctx=await b.newContext({...devices['Pixel 7'],deviceScaleFactor:1});const pg=await ctx.newPage();
const errs=[];pg.on('pageerror',e=>errs.push('pageerror '+e.message));pg.on('console',m=>{if(m.type()==='error'&&!/fonts|ERR_|Failed to load resource/.test(m.text()))errs.push('console '+m.text())});
await pg.goto(url,{waitUntil:'load'});await pg.waitForTimeout(1500);
const cdp=await ctx.newCDPSession(pg);const inst=await cdp.send('Page.getInstallabilityErrors');console.log('installabilityErrors',JSON.stringify(inst.installabilityErrors));
const sw=await pg.evaluate(async()=>{const r=await navigator.serviceWorker.ready;return r.active&&r.active.state});console.log('sw',sw);
console.log('footer',await pg.textContent('#verline'));
// onboard
await pg.screenshot({path:'/tmp/qc1.png'});
const body0=await pg.innerText('body');console.log('onboard text:',body0.slice(0,300).replace(/\n+/g,' | '));
const ov=await pg.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth);console.log('overflowX',ov);
await ctx.setOffline(true);await pg.reload({waitUntil:'load'}).catch(e=>console.log('offline reload fail',e.message));await pg.waitForTimeout(800);
console.log('offline footer',await pg.textContent('#verline').catch(()=>'MISSING'));
console.log('errors',JSON.stringify(errs));await b.close()})()

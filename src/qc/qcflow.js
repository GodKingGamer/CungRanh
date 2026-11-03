// Luồng chính ở chế độ một máy: nhập tên, tạo nhóm, chọn hình, bảng cách dùng, điền ngày, đủ trên điện thoại.
const {chromium,devices}=require('playwright');
(async()=>{const port=process.argv[2]||8766;
const b=await chromium.launch();const ctx=await b.newContext({...devices['Pixel 7'],deviceScaleFactor:1});const pg=await ctx.newPage();
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto(`http://localhost:${port}/`);await pg.waitForTimeout(800);
await pg.fill('input',"Đức");await pg.keyboard.press('Enter');await pg.waitForTimeout(500);
const txt=async()=>(await pg.innerText('body')).replace(/\n+/g,' | ').slice(0,260);
console.log('A',await txt());
await pg.screenshot({path:'/tmp/qc_a.png'});

await pg.click('[data-k=new]');await pg.fill('#gname','Hội bạn đại học');await pg.click('form button[type=submit]');await pg.waitForTimeout(1200);
console.log('B',await txt());await pg.screenshot({path:'/tmp/qc_b.png'});
await pg.click('button:has-text("Để mặc định")').catch(e=>console.log('no default btn'));await pg.waitForTimeout(500);
console.log('C',await txt());await pg.screenshot({path:'/tmp/qc_c.png'});
const ov=await pg.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth);console.log('overflowX',ov);
await b.close();console.log('errs',errs)})()

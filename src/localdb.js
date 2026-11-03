/* Kho dữ liệu tạm trên một máy: dùng khi chưa cấu hình Firebase. Cùng giao diện với Firestore (doc/collection/onSnapshot/set/update/delete/get). */
function makeLocalDb(){
  var KEY="cungranh-local-db-v1",store={},subs=[];
  try{var raw=localStorage.getItem(KEY);if(raw)store=JSON.parse(raw)||{}}catch(e){store={}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(store))}catch(e){}}
  function clone(v){return v==null?v:JSON.parse(JSON.stringify(v))}
  function parent(p){var i=p.lastIndexOf("/");return i<0?"":p.slice(0,i)}
  function lastSeg(p){return p.slice(p.lastIndexOf("/")+1)}
  function docSnap(p){var has=Object.prototype.hasOwnProperty.call(store,p);return {id:lastSeg(p),exists:has,data:function(){return has?clone(store[p]):undefined},metadata:{fromCache:false}}}
  function colSnap(p){var docs=Object.keys(store).filter(function(k){return parent(k)===p}).sort().map(function(k){return docSnap(k)});return {docs:docs,size:docs.length,metadata:{fromCache:false}}}
  function notify(){subs.slice().forEach(function(s){try{s.fire()}catch(e){}})}
  function later(fn){Promise.resolve().then(fn)}
  function doc(p){
    return {id:lastSeg(p),path:p,
      get:function(){return Promise.resolve(docSnap(p))},
      set:function(d){store[p]=clone(d);save();later(notify);return Promise.resolve()},
      update:function(d){if(!Object.prototype.hasOwnProperty.call(store,p))return Promise.reject(new Error("not-found"));store[p]=Object.assign({},store[p],clone(d));save();later(notify);return Promise.resolve()},
      delete:function(){delete store[p];save();later(notify);return Promise.resolve()},
      onSnapshot:function(next){var s={fire:function(){next(docSnap(p))}};subs.push(s);later(s.fire);return function(){subs=subs.filter(function(x){return x!==s})}}};
  }
  function collection(p){
    return {path:p,doc:function(id){return doc(p+"/"+id)},
      onSnapshot:function(next){var s={fire:function(){next(colSnap(p))}};subs.push(s);later(s.fire);return function(){subs=subs.filter(function(x){return x!==s})}}};
  }
  return {doc:doc,collection:collection};
}
function localUid(){
  var k="cungranh-local-uid",v=null;
  try{v=localStorage.getItem(k)}catch(e){}
  if(!v){v="u"+Math.random().toString(36).slice(2,12);try{localStorage.setItem(k,v)}catch(e){}}
  return v;
}

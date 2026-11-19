// FoVL Notes — small helpers (theme, progress bar, on-page TOC, "mark as done")
(function(){
  var store = {
    get:function(k){try{return localStorage.getItem(k)}catch(e){return null}},
    set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  };
  // theme
  var root=document.documentElement;
  var saved=store.get('fovl-theme');
  if(saved){root.setAttribute('data-theme',saved)}
  else if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches){root.setAttribute('data-theme','dark')}
  document.addEventListener('DOMContentLoaded',function(){
    var tb=document.getElementById('themeBtn');
    if(tb){tb.addEventListener('click',function(){
      var t=root.getAttribute('data-theme')==='dark'?'light':'dark';
      root.setAttribute('data-theme',t);store.set('fovl-theme',t);
    })}
    var mb=document.getElementById('menuBtn');
    if(mb){mb.addEventListener('click',function(){document.querySelector('.side').classList.toggle('open')})}
    // reading progress
    var bar=document.querySelector('.progress');
    if(bar){window.addEventListener('scroll',function(){
      var h=document.documentElement;var p=h.scrollTop/((h.scrollHeight-h.clientHeight)||1);
      bar.style.width=(p*100)+'%';
    })}
    // on-page TOC
    var toc=document.getElementById('toc');
    var heads=[].slice.call(document.querySelectorAll('.article h2'));
    if(toc&&heads.length){
      heads.forEach(function(h,i){
        if(!h.id){h.id='s'+(i+1)+'-'+h.textContent.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)}
        var a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;toc.appendChild(a);
      });
      var links=[].slice.call(toc.querySelectorAll('a'));
      window.addEventListener('scroll',function(){
        var cur=0;heads.forEach(function(h,i){if(h.getBoundingClientRect().top<120)cur=i});
        links.forEach(function(l,i){l.classList.toggle('on',i===cur)});
      });
    }
    // done state
    var page=document.body.getAttribute('data-page');
    var cb=document.getElementById('doneBox');
    if(cb&&page){
      cb.checked=store.get('fovl-done-'+page)==='1';
      cb.addEventListener('change',function(){store.set('fovl-done-'+page,cb.checked?'1':'0');paintDone()});
    }
    function paintDone(){
      [].slice.call(document.querySelectorAll('[data-mod]')).forEach(function(el){
        el.classList.toggle('done',store.get('fovl-done-'+el.getAttribute('data-mod'))==='1');
      });
    }
    paintDone();
  });
})();

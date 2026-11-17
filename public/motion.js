/* Johnny's Dakwerken: motion helpers for the lime styles. */
(function(){
  var d=document,h=d.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var noIo=!('IntersectionObserver' in window);
  var bot=navigator.webdriver&&!/[?&]motion=1/.test(location.search);

  function armVideo(){
    var reduceV=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    d.querySelectorAll('[data-work-video]').forEach(function(v){
      var media=v.closest('.work-vid');
      if(!media)return;
      if(reduceV){
        if(!media.querySelector('.vid-play')){
          var b=document.createElement('button');
          b.type='button';b.className='vid-play r-btn bg-accent';b.setAttribute('aria-label','Video afspelen');
          b.innerHTML='<span class="btn-in">▶ Afspelen</span>';
          media.appendChild(b);
          b.addEventListener('click',function(){v.setAttribute('controls','');v.play();b.remove()});
        }
        return;
      }
      if(v.dataset.vioReady)return;
      v.dataset.vioReady='1';
      var io=new IntersectionObserver(function(es){es.forEach(function(e){
        if(e.isIntersecting)v.play().catch(function(){});
        else v.pause();
      })},{threshold:.25});
      io.observe(v);
    });
  }

  if(noIo){armVideo();return}

  var map=new WeakMap();
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;
    var t=e.target;io.unobserve(t);
    (map.get(t)||[t]).forEach(function(x){x.classList.add('in')});
    var c=t.querySelectorAll?t.querySelectorAll('[data-count]'):[];c.forEach(count);
  })},{rootMargin:'0px 0px -8% 0px',threshold:0});

  function count(el){
    var to=parseInt(el.getAttribute('data-count'),10),t0=null,dur=1100;
    function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,3);el.textContent=Math.round(to*e);if(p<1)requestAnimationFrame(f)}
    el.textContent='0';requestAnimationFrame(f);
  }

  function arm(){
    if(reduce||bot)return;
    if(!h.hasAttribute('data-lime'))return;
    d.querySelectorAll('main h2:not(.rv)').forEach(function(x){x.classList.add('rv');var p=x.parentElement;var l=map.get(p)||[];l.push(x);map.set(p,l);io.observe(p)});
    d.querySelectorAll('.blade-div:not(.pre)').forEach(function(x){x.classList.add('pre');io.observe(x)});
    d.querySelectorAll('dl:has([data-count])').forEach(function(x){io.observe(x)});
  }

  armVideo();
  arm();
  new MutationObserver(function(){arm();armVideo()}).observe(h,{attributes:true,attributeFilter:['data-lime']});
})();
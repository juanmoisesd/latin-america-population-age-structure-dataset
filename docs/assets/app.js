
document.addEventListener('DOMContentLoaded', function(){
  const box=document.getElementById('searchBox');
  if(box){
    box.addEventListener('input', function(){
      const q=this.value.toLowerCase();
      document.querySelectorAll('[data-search]').forEach(el=>{
        const s=(el.getAttribute('data-search')||'').toLowerCase();
        el.style.display=s.includes(q)?'':'none';
      });
    });
  }
});

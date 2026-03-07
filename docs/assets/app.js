
function searchLinks() {
  const q = document.getElementById('searchBox');
  if (!q) return;
  q.addEventListener('input', function(){
    const term = this.value.toLowerCase();
    document.querySelectorAll('[data-search]').forEach(el=>{
      el.style.display = el.getAttribute('data-search').toLowerCase().includes(term) ? '' : 'none';
    });
  });
}
document.addEventListener('DOMContentLoaded', searchLinks);

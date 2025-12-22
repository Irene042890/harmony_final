const moods = document.querySelectorAll('.mood');
let selected = null;
moods.forEach(b=>b.addEventListener('click', ()=>{moods.forEach(x=>x.classList.remove('active')); b.classList.add('active'); selected = b.dataset.mood;}));
const notes = document.getElementById('notes');
const status = document.getElementById('status');
const aiResponse = document.getElementById('aiResponse');
const affEl = document.getElementById('affirmations');
const historyEl = document.getElementById('history');
document.getElementById('getSupport').addEventListener('click', async ()=>{
    status.textContent='';
    if(!selected){ status.textContent='Choose a mood.'; return; }
    const payload = { mood: selected, note: notes.value || '', ts: Date.now(), username: 'guest' };
    // POST to Python microservice
    status.textContent='Contacting backend...';
    try {
        const res = await fetch('http://localhost:3000/support', {
            method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
        });
        const json = await res.json();
        status.textContent='';
        const support = json.support || json;
        aiResponse.textContent = support.supportive || support.text || JSON.stringify(support);
        affEl.innerHTML = '';
        (support.affirmations || []).forEach(a=>{ const d=document.createElement('div'); d.textContent=a; affEl.appendChild(d); });
        // save history
        const data = JSON.parse(localStorage.getItem('mindmate_history')||'[]'); data.unshift(payload); localStorage.setItem('mindmate_history', JSON.stringify(data.slice(0,30)));
        renderHistory();
        document.getElementById('responseCard').hidden=false;
    } catch (e) {
        status.textContent='Backend not reachable. Try running the proxy.';
    }
});
function renderHistory(){ const data = JSON.parse(localStorage.getItem('mindmate_history')||'[]'); historyEl.innerHTML=''; if(data.length===0){ historyEl.innerHTML='<li>No check-ins yet</li>'; return; } data.forEach(d=>{ const li=document.createElement('li'); li.textContent=new Date(d.t).toLocaleString() + ' — ' + d.mood + (d.note?(' — '+d.note):''); historyEl.appendChild(li); }); }
renderHistory();

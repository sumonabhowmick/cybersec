const base = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
async function request(path, options={}) {
  const response=await fetch(`${base}${path}`,{headers:{'Content-Type':'application/json'},...options});
  if(!response.ok) throw new Error((await response.json()).detail || `Request failed: ${response.status}`);
  return response.json();
}
export const api={
  health:()=>request('/health'), metrics:()=>request('/metrics'), overview:()=>request('/overview'), history:()=>request('/incidents?limit=8'),
  analyze:(incident)=>request('/analyze',{method:'POST',body:JSON.stringify(incident)}),
  predict:(incident)=>request('/predict',{method:'POST',body:JSON.stringify(incident)}),
  feedback:(body)=>request('/feedback',{method:'POST',body:JSON.stringify(body)})
};

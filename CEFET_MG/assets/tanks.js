export default function(component){
 const {data,parentElement}=component,root=parentElement.querySelector('.sim');
 const find=id=>parentElement.querySelector('#'+id),rows=data.rows;
 let playing=false,position=0,last=null,raf;
 find('scene-title').textContent=data.title;find('seek').max=rows.length-1;
 const top=Math.max(70,...rows.map(r=>Math.max(r.h1,r.h2)*1.05));
 const y=v=>321-v/top*230;
 ['1','2'].forEach((k,i)=>{find('ref'+k).setAttribute('y1',y([47.4,31.2][i]));find('ref'+k).setAttribute('y2',y([47.4,31.2][i]));});
 for(let j=1;j<=2;j++){find('trace'+j).setAttribute('d',rows.map((r,i)=>`${i?'L':'M'}${r.t/rows.at(-1).t*1040},${62-r['h'+j]/top*60}`).join(' '));}
 function render(i){const r=rows[i];root.dataset.index=i;root.dataset.h1=r.h1;root.dataset.h2=r.h2;
  find('clock').textContent=r.t.toFixed(2)+' s';
  for(let j=1;j<=2;j++){const v=r['h'+j];find('level'+j).textContent=v.toFixed(3)+' cm';find('water'+j).setAttribute('y',y(v));find('water'+j).setAttribute('height',Math.max(0,v/top*230));}
  find('input').textContent=r.u_applied.toFixed(2)+' %';
  for(const [id,key,name] of [['qin','qin','Qin/A₁'],['q12','q12','Q12/A₁'],['qout','qout','Qout/A₁']])find(id).textContent=Number.isFinite(r[key])?name+' '+r[key].toFixed(3)+' cm/s':name+' no identificado';
  find('seek').value=i;find('cursor').setAttribute('x1',r.t/rows.at(-1).t*1040);find('cursor').setAttribute('x2',r.t/rows.at(-1).t*1040);
 }
 find('play').onclick=()=>{if(position>=rows.at(-1).t)position=0;playing=true;last=null;root.dataset.playing='true';};
 find('pause').onclick=()=>{playing=false;root.dataset.playing='false';};
 find('reset').onclick=()=>{playing=false;position=0;last=null;root.dataset.playing='false';render(0);};
 find('seek').oninput=e=>{position=rows[+e.target.value].t;last=null;render(+e.target.value);};
 function frame(now){if(last!==null&&playing)position=Math.min(rows.at(-1).t,position+(now-last)/1000*Number(find('speed').value));last=now;
  let lo=0,hi=rows.length-1;while(lo<hi){let mid=Math.ceil((lo+hi)/2);if(rows[mid].t<=position)lo=mid;else hi=mid-1;}render(lo);
  if(position>=rows.at(-1).t){playing=false;root.dataset.playing='false';}raf=requestAnimationFrame(frame);
 }render(0);raf=requestAnimationFrame(frame);
 return()=>cancelAnimationFrame(raf);
}

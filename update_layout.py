from pathlib import Path
p=Path(__file__).with_name('index.html')
s=p.read_text()
s=s.replace('세계 13개 마라톤의 완주 거리를 지구 둘레로 환산했습니다.','13개 마라톤의 완주 거리를 10개 나라별로 합산했습니다. 국가 전체가 아닌, 이 자료에 포함된 대회만 비교합니다.')
s=s.replace('한 줄은 20바퀴','국가별 한 층은 5바퀴 (지구 5개)')
s=s.replace('13개 대회 · 완주 거리 기준','10개 나라 · 13개 대회 합산')
s=s.replace('<option value="date">개최일 순</option>','<option value="name">나라 이름순</option>')
s=s.replace('<section id="chart" class="chart" aria-label="대회별 지구 환산 바퀴 수"></section>','<div class="axis-note">지구 환산 바퀴 수 ↑ <span>가로축: 나라 · 세로축: 바퀴 수 · 지구는 아래에서 위로 누적</span></div><div class="plot-scroll"><section id="chart" aria-label="나라별 지구 환산 바퀴 수 픽토그램 차트"></section></div><details class="source-list"><summary>대회별 원자료와 집계 기준</summary><div id="sources"></div></details>')
css='''
.countries{display:none}.axis-note{font-size:13px;font-weight:600;margin:20px 0 14px}.axis-note span{font-weight:400;color:var(--muted);margin-left:20px}.plot-scroll{overflow-x:auto;padding-bottom:10px}#chart{position:relative;min-width:1080px;padding-left:65px}.columns{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));position:relative}.country-col{min-width:0;z-index:1}.stack{height:630px;position:relative;margin:0 8px}.unit{position:absolute;width:20%;height:20px;padding:1px;color:var(--country)}.unit svg{width:100%;height:100%;display:block;color:inherit}.col-label{text-align:center;border-top:1px solid var(--ink);padding:13px 2px 0;min-height:150px;font-size:12px;line-height:1.6}.col-label strong{font-size:14px;display:block}.col-label .col-value{font-size:20px;font-weight:700;margin:5px 0}.col-label .included{font-size:11px;color:var(--muted);padding:0 4px}.gridline{position:absolute;left:65px;right:0;border-top:1px solid var(--line);pointer-events:none}.tick{position:absolute;right:calc(100% + 12px);top:-8px;font-size:12px;font-variant-numeric:tabular-nums}.country-col .badge{margin:5px 0 0}.source-list{margin-top:16px;border-top:1px solid var(--line);padding:10px 0}.source-list summary{font-size:13px}#sources{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px 25px}#sources p{margin:7px 0;font-size:12px}.scroll-hint{font-size:12px;color:var(--muted)}@media(max-width:600px){.axis-note span{display:block;margin:7px 0 0}#sources{grid-template-columns:1fr}#chart{min-width:1080px}}@media print{.plot-scroll{overflow:visible}#chart{min-width:0}.stack{margin:0 3px}.col-label strong{font-size:11px}.col-label .col-value{font-size:15px}.col-label .included{font-size:10px}.source-list{display:none}@page{size:A3 landscape;margin:12mm}}
'''
s=s.replace('</style>',css+'</style>')
start=s.index('function render(){')
end=s.index("document.getElementById('sort').addEventListener",start)
s=s[:start]+'''function render(){
 const groups=Object.values(data.reduce((acc,r)=>{if(!acc[r.country])acc[r.country]={country:r.country,finish:0,races:[]};acc[r.country].finish+=r.finish;acc[r.country].races.push(r);return acc;},{}));
 groups.sort(document.getElementById('sort').value==='name'?(a,b)=>a.country.localeCompare(b.country,'ko'):(a,b)=>b.finish-a.finish);
 const maxLaps=Math.max(...groups.map(r=>r.finish*42.195/40000));
 const ceiling=Math.ceil(maxLaps/25)*25;
 const rowHeight=20, plotHeight=ceiling/5*rowHeight+30;
 let grid='';for(let t=0;t<=ceiling;t+=25)grid+=`<div class="gridline" style="top:${plotHeight-t/5*rowHeight}px"><span class="tick">${t}</span></div>`;
 document.getElementById('chart').innerHTML=grid+'<div class="columns">'+groups.map((r,i)=>{
  const km=r.finish*42.195,laps=km/40000;let icons='';
  for(let n=0;n<Math.ceil(laps);n++){const fraction=Math.min(1,laps-n);icons+=`<span class="unit" style="left:${n%5*20}%;bottom:${Math.floor(n/5)*rowHeight}px">${globe(fraction,`country-${i}-${n}`)}</span>`;}
  return `<div class="country-col" style="--country:${colors[r.country]}"><div class="stack" style="height:${plotHeight}px" role="img" aria-label="${escape(r.country)}, ${r.races.length}개 대회 합계 ${fmt(laps,1)}바퀴. 지구 하나는 1바퀴, 한 층은 5바퀴.">${icons}</div><div class="col-label"><strong style="color:${colors[r.country]}">${escape(r.country)}</strong><div class="col-value">${fmt(laps,1)}<small> 바퀴</small></div><div>${r.races.length}개 대회 · ${fmt(r.finish)}명</div><div class="included">${r.races.map(x=>escape(x.city)).join(' · ')}</div>${r.country==='대한민국'?'<span class="badge">비공식·미검증</span>':''}</div></div>`;
 }).join('')+'</div>';
 document.getElementById('sources').innerHTML=data.map(r=>`<section><p><strong>${escape(r.city)} · ${fmt(r.finish)}명</strong></p><p>${escape(r.status)} / ${escape(r.quality)}</p><p>${escape(r.notes)}</p><a href="${escape(r.source)}" target="_blank" rel="noopener noreferrer">원자료 보기 ↗</a></section>`).join('');
}
'''+s[end:]
p.write_text(s)

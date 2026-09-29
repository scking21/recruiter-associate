import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C,mono,Stage,Window,ramp,usePop,typed} from './kit';
import result from '../../public/validation-result.json';

// Checks implemented by validate_response in recruiter/workflow.py.
const checks=['Response matches the review contract','Every candidate and criterion is known','status ∈ met · not_met · unknown','Cited IDs belong to that candidate','met / not_met cite visible evidence',`Protected-term hits: ${result.protected_term_hits.length}`,`Injection markers: ${result.injection_marker_hits.length}`,`decision = ${result.decision}`];
const cmd='python3 -m recruiter validate \\\n    --input input.real.json \\\n    --response response.json';
const out=[['"valid": ',String(result.valid),C.green],['"errors": ',JSON.stringify(result.errors),C.green],['"synthetic": ',String(result.synthetic),'#d9c9a6'],['"decision": ',`"${result.decision}"`,C.amber]] as const;

export const Validation=()=>{const f=useCurrentFrame();const win=usePop(2);const panel=usePop(30);const badge=usePop(196,11);const cav=usePop(212);
 return <Stage dur={451} label="FRESH OFFLINE RUN · NO MODEL CALL">
  <Window x={90} y={140} w={800} h={560} title="zsh · roletrace" style={{opacity:win}}>
   <pre style={{margin:0,padding:'24px 28px',fontFamily:mono,fontSize:23,lineHeight:1.55,whiteSpace:'pre-wrap',color:'#d7e2dc'}}>
    <span style={{color:C.green}}>$ </span>{typed(cmd,f,6,55)}{f<50&&Math.floor(f/8)%2===0?'▌':''}
    {'\n\n'}{f>=150&&'{\n'}{out.map(([k,v,c],i)=>f>=152+i*5&&<span key={k}>  <span style={{color:C.blue}}>{k}</span><span style={{color:c}}>{v}</span>{'\n'}</span>)}{f>=172&&'}'}
   </pre>
  </Window>
  <div style={{position:'absolute',left:990,top:140,width:840,opacity:panel}}>
   <div style={{fontSize:15,letterSpacing:2,color:C.dim,fontFamily:mono,marginBottom:14}}>CHECKS · validate_response()</div>
   {checks.map((c,i)=>{const t0=55+i*16;const done=f>=t0+10;const on=f>=t0;return <div key={c} style={{display:'flex',alignItems:'center',gap:18,padding:'11px 18px',marginBottom:8,borderRadius:12,background:done?'#5cc98f12':C.panel,border:`1px solid ${done?C.green+'55':C.line}`,opacity:on?1:.35}}>
    <span style={{width:30,height:30,borderRadius:15,display:'grid',placeItems:'center',fontSize:18,background:done?C.green:'transparent',border:`2px solid ${done?C.green:C.faint}`,color:C.bg,fontWeight:800,rotate:on&&!done?`${f*25}deg`:'0deg',borderTopColor:on&&!done?C.green:undefined}}>{done?'✓':''}</span>
    <span style={{fontSize:24,fontFamily:i>=2?mono:undefined}}>{c}</span></div>})}
  </div>
  <div style={{position:'absolute',left:90,top:720,opacity:badge,scale:String(.7+.3*badge),transformOrigin:'left center',display:'flex',alignItems:'center',gap:22}}>
   <span style={{fontSize:64,fontWeight:800,letterSpacing:2,color:C.green,textShadow:`0 0 30px ${C.green}88`}}>VALID</span>
   <span style={{fontSize:26,color:C.dim,fontFamily:mono}}>0 errors · human review required</span>
  </div>
  <div style={{position:'absolute',left:990,top:818,width:840,opacity:cav,translate:`0 ${(1-cav)*24}px`,fontSize:21,lineHeight:1.45,color:'#c9d6cf',borderLeft:`4px solid ${C.amber}`,padding:'10px 20px',background:'#e9b94910',borderRadius:'0 10px 10px 0'}}>
   {result.limitations[1]}
  </div>
 </Stage>};

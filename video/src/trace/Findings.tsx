import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C,mono,Stage,Window,Node,Edge,Pill,ramp,usePop} from './kit';
import resp from '../../public/demo-response.json';

const r=resp.reviews[0];const fd=r.criterion_findings[0];
const lines:[string,string,string?][]=[
 ['{','',''],['  "candidate_id": ',`"${r.candidate_id}",`],['  "criterion_findings": [{',''],
 ['    "criterion_id": ',`"${fd.criterion_id}",`],['    "status": ',`"${fd.status}",`,C.green],['    "evidence_ids": ',`["${fd.evidence_ids[0]}"]`,C.green],['  }],',''],
 ['  "summary": ',`"${r.summary.slice(0,44)}…",`],['  "human_review": ',`"${r.human_review.slice(0,36)}…"`],['  "decision": ',`"${resp.decision}"`,C.amber],['}','']];
const EV_AT=5;

export const Findings=()=>{const f=useCurrentFrame();const shown=Math.floor(ramp(f,10,130,0,lines.length+.99));const win=usePop(2);
 const edge=ramp(f,95,135);const status=usePop(128);const q=usePop(150);const contract=usePop(205);const forbid=ramp(f,325,360);
 return <Stage dur={429} label="SAVED AGENT RESPONSE · NVIDIA GLM 5.3 · FICTIONAL INPUT">
  <Window x={90} y={140} w={800} h={640} title="demo-response.json" style={{opacity:win}}>
   <pre style={{margin:0,padding:'24px 28px',fontFamily:mono,fontSize:22,lineHeight:1.62,whiteSpace:'pre-wrap'}}>
    {lines.slice(0,shown).map(([k,v,c],i)=><div key={i} style={{background:i===EV_AT&&f>95?'#5cc98f1c':'transparent',borderRadius:6}}><span style={{color:C.blue}}>{k}</span><span style={{color:c||'#d9c9a6'}}>{v}</span></div>)}
   </pre>
  </Window>
  <Node x={1000} y={170} w={340} kind={`criterion · ${fd.criterion_id}`} title="Can explain a completed work sample" color={C.orange} style={{opacity:usePop(20)}}/>
  <Node x={1480} y={170} w={340} kind={`evidence · ${fd.evidence_ids[0]}`} title="Explained the work sample tradeoffs" color={C.green} glow={edge} style={{opacity:usePop(40)}}/>
  <Edge x1={1340} y1={235} x2={1480} y2={235} p={edge}/>
  <div style={{position:'absolute',left:1000,top:318,opacity:status,scale:String(.8+.2*status)}}><Pill color={C.green} style={{fontSize:22}}>status: met · cites {fd.evidence_ids[0]}</Pill></div>
  <div style={{position:'absolute',left:1000,top:380,width:820,opacity:q,translate:`0 ${(1-q)*30}px`,borderLeft:`4px solid ${C.amber}`,background:'#e9b94912',borderRadius:'0 12px 12px 0',padding:'16px 22px'}}>
   <div style={{fontSize:15,letterSpacing:2,color:C.amber,fontFamily:mono,marginBottom:6}}>QUESTION FOR THE HIRING OWNER · VERBATIM</div>
   <div style={{fontSize:23,lineHeight:1.4}}>{r.human_review}</div>
  </div>
  <div style={{position:'absolute',left:1000,top:610,width:820,opacity:contract,translate:`0 ${(1-contract)*30}px`}}>
   <div style={{fontSize:15,letterSpacing:2,color:C.dim,fontFamily:mono,marginBottom:12}}>STATUS CONTRACT · ENFORCED BY THE VALIDATOR</div>
   {([['met',C.green,false,'must cite visible evidence'],['not_met',C.red,false,'must cite visible evidence'],['unknown',C.dim,true,'evidence does not establish it']] as const).map(([s,c,d,t],i)=>
    <div key={s} style={{display:'flex',alignItems:'center',gap:18,margin:'8px 0',opacity:ramp(f,210+i*10,225+i*10)}}>
     <svg width={90} height={10}><line x1={0} y1={5} x2={90} y2={5} stroke={c} strokeWidth={4} strokeDasharray={d?'9 8':undefined}/></svg>
     <span style={{fontFamily:mono,fontSize:21,color:c,width:120}}>{s}</span><span style={{fontSize:21,color:C.dim}}>{t}</span></div>)}
  </div>
  <div style={{position:'absolute',left:1000,top:800,display:'flex',gap:14,alignItems:'center',opacity:ramp(f,318,332)}}>
   <span style={{fontSize:19,color:C.dim,marginRight:6}}>Never in the output:</span>
   {['score','rank','tier','recommend'].map((w,i)=><span key={w} style={{position:'relative',fontFamily:mono,fontSize:21,color:C.red,border:`1px solid ${C.red}66`,borderRadius:99,padding:'5px 14px'}}>{w}
    <span style={{position:'absolute',left:8,right:8,top:'50%',height:2.5,background:C.red,scale:`${ramp(forbid,i*.15,i*.15+.4)} 1`,transformOrigin:'left'}}/></span>)}
  </div>
 </Stage>};

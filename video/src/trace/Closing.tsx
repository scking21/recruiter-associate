import React from 'react';
import {useCurrentFrame,Img,staticFile,interpolate} from 'remotion';
import {C,serif,mono,Stage,Logo,ramp,usePop} from './kit';

const lines=['Hiring evidence.','Clear sources.','Human decisions.'];
export const Closing=()=>{const f=useCurrentFrame();const title=usePop(4);const shot=usePop(24);
 return <Stage dur={454}>
  <div style={{position:'absolute',left:120,top:200,opacity:title,translate:`0 ${(1-title)*30}px`,display:'flex',alignItems:'center',gap:26}}><Logo size={84}/><span style={{fontFamily:serif,fontSize:120,letterSpacing:-4}}>Roletrace</span></div>
  <div style={{position:'absolute',left:124,top:370}}>
   {lines.map((l,i)=>{const p=ramp(f,285+i*34,305+i*34);return <div key={l} style={{fontSize:56,lineHeight:1.2,fontWeight:600,opacity:.15+.85*p,color:i===1?C.green:i===2?C.orange:C.text}}>{l}</div>})}
  </div>
  <div style={{position:'absolute',left:124,top:640,display:'flex',flexDirection:'column',gap:16}}>
   {[['Agent Index','aiworthusing.com/agent-index/recruiter-associate',40],['Hosted setup · local install','linked from the listing',150],['MIT source','github.com/scking21/roletrace',250]].map(([k,v,t])=>{const p=usePop(t as number);
    return <div key={k as string} style={{display:'flex',gap:18,alignItems:'baseline',opacity:p,translate:`${(1-p)*-24}px 0`}}><span style={{fontFamily:mono,fontSize:17,letterSpacing:2,color:C.dim,width:330,textTransform:'uppercase'}}>{k}</span><span style={{fontSize:28}}>{v}</span></div>})}
  </div>
  <div style={{position:'absolute',left:124,top:880,fontSize:17,color:C.faint,lineHeight:1.6,opacity:ramp(f,60,90)}}>Controlled demo with fictional applicants and simulated participants. ElevenLabs synthetic narration.</div>
  <div style={{position:'absolute',right:120,top:170,width:560,height:640,perspective:1400,opacity:shot}}>
   <div style={{width:560,height:640,borderRadius:18,overflow:'hidden',border:`1px solid ${C.line}`,boxShadow:`0 40px 120px #000c, 0 0 60px ${C.green}22`,rotate:`y ${interpolate(f,[0,454],[-14,-6])}deg`,translate:`0 ${(1-shot)*40}px`,background:'#f7f6f2'}}>
    <div style={{height:40,background:'#e9e7e1',display:'flex',alignItems:'center',gap:8,padding:'0 14px'}}>{['#ef5d52','#e9b949','#5cc98f'].map(c=><span key={c} style={{width:11,height:11,borderRadius:6,background:c}}/>)}<span style={{marginLeft:12,fontSize:14,color:'#666',fontFamily:mono}}>aiworthusing.com/agent-index</span></div>
    <div style={{height:600,overflow:'hidden'}}><Img src={staticFile('agent-index-roletrace.png')} style={{width:560,translate:`0 ${-interpolate(f,[40,420],[0,40],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}px`}}/></div>
   </div>
  </div>
 </Stage>};

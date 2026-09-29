import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {C,mono,Stage,Window,Node,Edge,ramp,usePop} from './kit';

// Verbatim excerpts from private/multiplayer/{probe.cjs,owner-run.json,manager-run.json}, September 24 simulation.
type Msg={who:'owner'|'manager'|'agent';at:number;end?:number;lines:string[]};
const msgs:Msg[]=[
 {who:'owner',at:14,lines:['SIMULATION ONLY, fictional hiring evidence. … Evidence A1: applicant A fixed a Python timeout. Evidence A2: A wrote a support guide. Evidence B1: B handled customer support; Python skill unverified. Give a concise cited evidence summary, no rankings or hiring decisions.']},
 {who:'agent',at:62,end:165,lines:['Applicant A','R1 (Python debugging): Supported — fixed a Python timeout [A1].','R2 (written explanations): Supported — wrote a support guide [A2].','Applicant B','R1 (Python debugging): Unverified — no evidence provided [B1].','R2 (written explanations): Partially related — handled customer support [B1].','No rankings, recommendations, or hiring dispositions are made.']},
 {who:'manager',at:183,lines:['SIMULATED HIRING MANAGER CORRECTION: Retract A1. A only documented the timeout; no Python fix has been verified. Keep A2 and B1. Update the same review and suggest evidence to request next. …']},
 {who:'agent',at:238,end:400,lines:['Withdrawal acknowledged: The prior A1 claim (“A fixed a Python timeout”) is withdrawn per the hiring manager’s correction.','R1 Python debugging: Unverified — documentation of a timeout is not a verified fix [A1 withdrawn].','Evidence to request next','A: artifact of an actual Python fix (patch/commit, debug log, peer confirmation).','B: written customer-explanation sample (ticket reply, help article).']}];
const who={owner:{name:'sim-owner',role:'owner · profile 7c1b2cfe',color:C.orange},manager:{name:'sim-manager',role:'participant · profile 1029175f',color:C.blue},agent:{name:'Roletrace',role:'OpenClaw agent · GLM 5.3',color:C.green}};
const heads=new Set(['Applicant A','Applicant B','Evidence to request next']);
const CPL=58,LH=31;
const visLines=(m:Msg,f:number)=>{if(f<m.at)return 0;if(!m.end)return m.lines.length;return Math.min(m.lines.length,Math.floor(interpolate(f,[m.at,m.end],[1,m.lines.length+.99])));};
const height=(m:Msg,n:number)=>n===0?0:62+m.lines.slice(0,n).reduce((s,l)=>s+Math.ceil(l.length/CPL)*LH+(heads.has(l)?8:0),0)+22;
const offsetAt=(f:number)=>{const total=msgs.reduce((s,m)=>s+height(m,visLines(m,f))+(f>=m.at?18:0),0);return Math.max(0,total-690);};

function Bubble({m,f}:{m:Msg;f:number}){const n=visLines(m,f);const w=who[m.who];const p=ramp(f,m.at,m.at+10);if(n===0)return null;
 return <div style={{opacity:p,translate:`0 ${(1-p)*16}px`,marginBottom:18,borderRadius:14,border:`1px solid ${w.color}55`,background:m.who==='agent'?'#5cc98f0c':'#ffffff06',padding:'14px 18px'}}>
  <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}><span style={{width:26,height:26,borderRadius:13,background:w.color,display:'grid',placeItems:'center',color:C.bg,fontWeight:800,fontSize:14}}>{w.name[0].toUpperCase()}</span>
   <span style={{fontWeight:700,fontSize:20}}>{w.name}</span><span style={{fontFamily:mono,fontSize:15,color:C.dim}}>{w.role}</span></div>
  {m.lines.slice(0,n).map((l,i)=><div key={i} style={{fontSize:heads.has(l)?19:21,lineHeight:`${LH}px`,fontWeight:heads.has(l)?700:400,color:heads.has(l)?w.color:'#dce6e0',marginTop:heads.has(l)?8:0,letterSpacing:heads.has(l)?1:0}}>{l}</div>)}
 </div>;}

export const Multiplayer=()=>{const f=useCurrentFrame();const win=usePop(0);
 let off=0;for(let k=0;k<8;k++)off+=offsetAt(Math.max(0,f-k));off/=8;
 const withdraw=ramp(f,196,222);const retract=ramp(f,250,272);const unver=ramp(f,282,306);
 const e=(t:number)=>ramp(f,t,t+26);
 return <Stage dur={628} label="REPLAY · SAVED SESSION EXCERPTS · SEPT 24 · SIMULATED PARTICIPANTS">
  <Window x={60} y={120} w={880} h={820} title="agent:recruiter-associate:simulation-shared-review · shared" style={{opacity:win}}>
   <div style={{position:'absolute',inset:0,padding:'20px 22px',overflow:'hidden'}}><div style={{translate:`0 ${-off}px`}}>{msgs.map((m,i)=><Bubble key={i} m={m} f={f}/>)}</div></div>
  </Window>
  <div style={{position:'absolute',left:1000,top:128,fontSize:15,letterSpacing:2,color:C.dim,fontFamily:mono,opacity:usePop(40)}}>SHARED REVIEW · EVIDENCE MAP</div>
  <Node x={1000} y={250} w={300} kind="criterion · R1" title="Python debugging" color={C.orange} style={{opacity:usePop(50)}}/>
  <Node x={1000} y={560} w={300} kind="criterion · R2" title="Written customer explanations" color={C.orange} style={{opacity:usePop(56)}}/>
  <Node x={1540} y={190} w={300} kind={withdraw>.5?'evidence · A1 · withdrawn':'evidence · A1'} title="A fixed a Python timeout" color={withdraw>.2?C.red:C.green} strike={withdraw} glow={withdraw>0&&withdraw<1?1:0} style={{opacity:usePop(40)}}/>
  <Node x={1540} y={400} w={300} kind="evidence · A2" title="A wrote a support guide" color={C.green} style={{opacity:usePop(46)}}/>
  <Node x={1540} y={610} w={300} kind="evidence · B1" title="B handled customer support" color={C.green} style={{opacity:usePop(52)}}/>
  <Edge x1={1300} y1={300} x2={1540} y2={240} p={e(85)*(1-retract)} color={withdraw>.2?C.red:C.green} label="A · supported"/>
  <Edge x1={1300} y1={300} x2={1540} y2={240} p={unver} color={C.dim} dashed label="A · unverified"/>
  <Edge x1={1300} y1={610} x2={1540} y2={450} p={e(105)} color={C.green} label="A · supported" lt={.72}/>
  <Edge x1={1300} y1={330} x2={1540} y2={660} p={e(125)} color={C.dim} dashed label="B · unverified" lt={.25}/>
  <Edge x1={1300} y1={640} x2={1540} y2={680} p={e(142)} color={C.amber} label="B · related"/>
  {[['A · request','Python fix artifact: patch, debug log, peer confirmation',1000],['B · request','Written customer-explanation sample',1440]].map(([k,t,x],i)=>{const p=usePop(352+i*12);
   return <div key={k} style={{position:'absolute',left:x as number,top:790,width:400,padding:'14px 18px',borderRadius:14,border:`2px dashed ${C.blue}`,background:'#7fb4e80d',opacity:p,translate:`0 ${(1-p)*24}px`}}>
    <div style={{fontSize:15,letterSpacing:2,fontFamily:mono,color:C.blue}}>{String(k).toUpperCase()}</div><div style={{fontSize:21,marginTop:4,lineHeight:1.3}}>{t}</div></div>})}
 </Stage>};

import React from 'react';
import {useCurrentFrame,interpolate,random} from 'remotion';
import {C,serif,mono,Stage,Edge,Node,ramp,usePop} from './kit';

const docs=['evidence_01','A1','A2','B1','work_sample','','','','','','',''];
const finalPos=[[1540,240],[1540,390],[1540,540],[1540,690],[1540,840]];
const criteria=[{t:'Work sample',y:330},{t:'Python debugging',y:520},{t:'Written explanations',y:710}];
const links=[[0,0],[1,1],[2,2],[2,3]];

function Doc({x,y,rot,id,o,glow}:{x:number;y:number;rot:number;id:string;o:number;glow:number}){
 return <div style={{position:'absolute',left:x,top:y,width:230,height:112,rotate:`${rot}deg`,opacity:o,background:C.panel2,border:`1.5px solid ${glow?C.green:C.line}`,borderRadius:12,padding:16,boxShadow:`0 0 ${30*glow}px ${C.green}66, 0 14px 30px #0008`}}>
  {[.9,.7,.8].map((w,i)=><div key={i} style={{height:9,width:`${w*100}%`,background:C.line,borderRadius:5,marginBottom:10}}/>)}
  {id&&<div style={{fontFamily:mono,fontSize:17,color:glow?C.green:C.dim}}>{id}</div>}
 </div>;
}

export const Intro=()=>{const f=useCurrentFrame();const gather=ramp(f,150,205);const title=usePop(158);const tag=usePop(200);const chip=usePop(262);
 return <Stage dur={447} label="CONTROLLED DEMO · FICTIONAL APPLICANTS">
  {docs.map((id,i)=>{const sx=120+random('x'+i)*1600,sy=140+random('y'+i)*760;const drift=Math.sin(f/40+i)*14;
   const fp=finalPos[i];const keep=i<5;const tx=keep?interpolate(gather,[0,1],[sx,fp[0]]):sx;const ty=keep?interpolate(gather,[0,1],[sy+drift,fp[1]-56]):sy+drift;
   const o=keep?ramp(f,i*6,i*6+20,0,1):ramp(f,i*6,i*6+20,0,.55)*(1-gather);
   return <Doc key={i} x={tx-115} y={ty} rot={(1-gather)*(random('r'+i)*24-12)} id={id} o={o} glow={keep?ramp(f,240+i*8,260+i*8):0}/>})}
  {criteria.map((c,i)=>{const p=usePop(168+i*6);return <Node key={i} x={1030} y={c.y-45} w={300} kind="criterion" title={c.t} color={C.orange} style={{opacity:p,translate:`${(1-p)*-40}px 0`}}/>})}
  {links.map(([ci,ei],i)=><Edge key={i} x1={1330} y1={criteria[ci].y} x2={1425} y2={finalPos[ei][1]} p={ramp(f,205+i*10,245+i*10)} color={C.green}/>)}
  <div style={{position:'absolute',left:120,top:300,opacity:title,translate:`0 ${(1-title)*30}px`}}>
   <div style={{fontFamily:serif,fontSize:150,letterSpacing:-5,lineHeight:1}}>Roletrace</div>
   <div style={{fontSize:40,color:C.dim,marginTop:26,opacity:tag,lineHeight:1.35}}>Every hiring finding,<br/>traced to its source.</div>
  </div>
  <div style={{position:'absolute',left:120,top:640,display:'flex',alignItems:'center',gap:14,fontSize:24,color:C.text,opacity:chip,border:`1px solid ${C.orange}88`,borderRadius:99,padding:'12px 22px',background:'#ee845414'}}>
   <span style={{width:11,height:11,borderRadius:6,background:C.orange}}/>Controlled demo · fictional applicants · humans decide
  </div>
 </Stage>};

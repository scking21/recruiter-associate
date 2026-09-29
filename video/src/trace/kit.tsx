import React from 'react';
import {AbsoluteFill,interpolate,spring,useCurrentFrame,useVideoConfig,Easing} from 'remotion';

export const C={bg:'#081113',bg2:'#0e1b1e',panel:'#11211f',panel2:'#162a29',line:'#274140',text:'#eef3ec',dim:'#8ea49b',faint:'#4d6560',orange:'#ee8454',green:'#5cc98f',red:'#ef5d52',amber:'#e9b949',blue:'#7fb4e8'};
export const sans='-apple-system, "SF Pro Display", "Helvetica Neue", Arial, sans-serif';
export const serif='Georgia, "Times New Roman", serif';
export const mono='"SF Mono", Menlo, monospace';

export const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
export const ramp=(f:number,a:number,b:number,from=0,to=1)=>interpolate(f,[a,b],[from,to],{...clamp,easing:Easing.bezier(.22,1,.36,1)});
export function usePop(delay:number,damping=14){const f=useCurrentFrame();const {fps}=useVideoConfig();return spring({frame:f-delay,fps,config:{damping,mass:.7}});}
export const typed=(text:string,f:number,start:number,cps=40)=>text.slice(0,Math.max(0,Math.floor((f-start)*cps/30)));

export function Stage({children,label,dur}:{children:React.ReactNode;label?:string;dur:number}){
 const f=useCurrentFrame();
 const cam=interpolate(f,[0,dur],[1,1.035]);
 const fade=Math.min(ramp(f,0,12),ramp(f,dur-10,dur,1,0));
 return <AbsoluteFill style={{background:`radial-gradient(1200px 700px at 70% 35%, #12302b 0%, ${C.bg} 60%)`,fontFamily:sans,color:C.text,overflow:'hidden'}}>
  <svg width={1920} height={1080} style={{position:'absolute',opacity:.35}}><defs><pattern id="dots" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.5" fill={C.line}/></pattern></defs><rect width="1920" height="1080" fill="url(#dots)"/></svg>
  <AbsoluteFill style={{scale:String(cam),opacity:fade}}>{children}</AbsoluteFill>
  <div style={{position:'absolute',top:44,left:64,display:'flex',alignItems:'center',gap:14,fontSize:22,letterSpacing:4,fontWeight:600,opacity:fade}}><Logo size={26}/>ROLETRACE</div>
  {label&&<div style={{position:'absolute',top:40,right:64,fontSize:18,letterSpacing:2.5,color:C.dim,border:`1px solid ${C.line}`,borderRadius:99,padding:'9px 18px',background:'#0b1715cc',opacity:fade}}>{label}</div>}
 </AbsoluteFill>;
}

export function Logo({size=28}:{size?:number}){return <svg width={size} height={size} viewBox="0 0 28 28"><circle cx="6" cy="7" r="4" fill={C.orange}/><circle cx="22" cy="21" r="4" fill={C.green}/><path d="M6 7 C 16 7, 12 21, 22 21" stroke={C.text} strokeWidth="2.2" fill="none"/></svg>;}

export function Window({x,y,w,h,title,children,accent=C.line,style={}}:{x:number;y:number;w:number;h:number;title:string;children:React.ReactNode;accent?:string;style?:React.CSSProperties}){
 return <div style={{position:'absolute',left:x,top:y,width:w,height:h,background:`linear-gradient(180deg, ${C.panel2}, ${C.panel})`,border:`1px solid ${accent}`,borderRadius:18,boxShadow:'0 30px 80px #0009, 0 0 0 1px #ffffff08 inset',overflow:'hidden',...style}}>
  <div style={{height:50,display:'flex',alignItems:'center',gap:9,padding:'0 20px',borderBottom:`1px solid ${C.line}`,background:'#0c1917'}}>
   {['#ef5d52','#e9b949','#5cc98f'].map(c=><span key={c} style={{width:12,height:12,borderRadius:6,background:c,opacity:.8}}/>)}
   <span style={{marginLeft:14,fontSize:19,color:C.dim,fontFamily:mono}}>{title}</span>
  </div>
  <div style={{position:'relative',height:h-50}}>{children}</div>
 </div>;
}

export function Node({x,y,w,kind,title,sub,color=C.text,glow=0,style={},strike=0}:{x:number;y:number;w:number;kind:string;title:string;sub?:string;color?:string;glow?:number;style?:React.CSSProperties;strike?:number}){
 return <div style={{position:'absolute',left:x,top:y,width:w,padding:'16px 20px',borderRadius:14,background:C.panel2,border:`1.5px solid ${color}`,boxShadow:`0 0 ${40*glow}px ${color}88, 0 16px 40px #0008`,...style}}>
  <div style={{fontSize:15,letterSpacing:2.2,color,fontFamily:mono,textTransform:'uppercase',marginBottom:6}}>{kind}</div>
  <div style={{fontSize:25,lineHeight:1.25,position:'relative'}}>{title}
   {strike>0&&<div style={{position:'absolute',left:0,top:'50%',height:3,width:`${strike*100}%`,background:C.red,borderRadius:2}}/>}
  </div>
  {sub&&<div style={{fontSize:18,color:C.dim,marginTop:6}}>{sub}</div>}
 </div>;
}

export const bez=(x1:number,y1:number,x2:number,y2:number)=>{const mx=(x1+x2)/2;return {d:`M${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`,at:(t:number)=>{const u=1-t;const X=u*u*u*x1+3*u*u*t*mx+3*u*t*t*mx+t*t*t*x2;const Y=u*u*u*y1+3*u*u*t*y1+3*u*t*t*y2+t*t*t*y2;return [X,Y];}};};

export function Edge({x1,y1,x2,y2,p,color=C.green,dashed=false,width=3,label,labelColor,lt=.5}:{x1:number;y1:number;x2:number;y2:number;p:number;color?:string;dashed?:boolean;width?:number;label?:string;labelColor?:string;lt?:number}){
 const b=bez(x1,y1,x2,y2);const [lx,ly]=b.at(lt);const [hx,hy]=b.at(Math.min(p,1));
 return <>
  <svg width={1920} height={1080} style={{position:'absolute',left:0,top:0,overflow:'visible'}}>
   <path d={b.d} stroke={color} strokeOpacity={.25} strokeWidth={width*4} fill="none" pathLength={1} strokeDasharray="1" strokeDashoffset={1-p} style={{filter:'blur(6px)'}}/>
   <path d={b.d} stroke={color} strokeWidth={width} fill="none" {...(dashed?{strokeDasharray:'10 10',opacity:p}:{pathLength:1,strokeDasharray:'1',strokeDashoffset:1-p})}/>
   {p>0&&p<1&&<circle cx={hx} cy={hy} r={7} fill={color} style={{filter:`drop-shadow(0 0 10px ${color})`}}/>}
  </svg>
  {label&&p>.6&&<div style={{position:'absolute',left:lx,top:ly,transform:'translate(-50%,-50%)',fontSize:17,fontFamily:mono,color:labelColor||color,background:C.bg,border:`1px solid ${color}`,borderRadius:99,padding:'5px 12px',whiteSpace:'nowrap',opacity:ramp(p,.6,1)}}>{label}</div>}
 </>;
}

export function Pill({children,color=C.green,style={}}:{children:React.ReactNode;color?:string;style?:React.CSSProperties}){return <span style={{display:'inline-block',color,background:color+'1f',border:`1px solid ${color}66`,padding:'6px 14px',borderRadius:99,fontSize:19,fontWeight:600,fontFamily:mono,...style}}>{children}</span>;}

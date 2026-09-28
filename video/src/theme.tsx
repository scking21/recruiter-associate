import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
export const ink='#102328', muted='#52615e', paper='#f4f0e7', orange='#c76845', green='#336653';
export const sans='Arial, sans-serif', serif='Georgia, serif', mono='Menlo, monospace';
export function Shell({number,title,tag='CONTROLLED DEMO · FICTIONAL APPLICANTS',children}:{number:string;title:string;tag?:string;children:React.ReactNode}) {
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:paper,color:ink,fontFamily:sans,padding:'65px 100px'}}>
  <div style={{display:'flex',justifyContent:'space-between',fontSize:23,letterSpacing:3,color:muted}}><span>ROLETRACE</span><span>{tag}</span></div>
  <div style={{display:'flex',gap:26,alignItems:'baseline',marginTop:50,marginBottom:34,opacity:interpolate(f,[0,14],[0,1],{extrapolateRight:'clamp'})}}><span style={{color:orange,fontSize:26}}>{number}</span><h1 style={{fontFamily:serif,fontWeight:400,fontSize:76,letterSpacing:-2,margin:0}}>{title}</h1></div>
  <div style={{opacity:interpolate(f,[5,20],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),translate:`0 ${interpolate(f,[0,20],[18,0],{extrapolateRight:'clamp'})}px`}}>{children}</div>
 </AbsoluteFill>
}
export function Card({children,style={}}:{children:React.ReactNode;style?:React.CSSProperties}) {return <div style={{background:'#fffdf8',border:'1px solid #d4d4c8',borderRadius:16,padding:32,...style}}>{children}</div>}
export function Label({children}:{children:React.ReactNode}){return <div style={{fontSize:22,letterSpacing:2,color:muted,marginBottom:18,textTransform:'uppercase'}}>{children}</div>}
export function Pill({children,color=green}:{children:React.ReactNode;color?:string}) {return <span style={{display:'inline-block',color,background:color+'16',padding:'9px 17px',borderRadius:8,fontSize:23,fontWeight:700}}>{children}</span>}

import React from 'react';
import {AbsoluteFill, Img, staticFile, interpolate,useCurrentFrame} from 'remotion';
import {ink,paper,sans,orange} from '../theme';
export const Intro=()=>{const f=useCurrentFrame();return <AbsoluteFill style={{background:paper,fontFamily:sans}}>
 <Img src={staticFile('roletrace-cover.png')} style={{position:'absolute',width:1920,top:75,scale:interpolate(f,[0,300],[1,1.025])}}/>
 <div style={{position:'absolute',top:48,left:110,fontSize:24,letterSpacing:3,color:ink}}>OPENCLAW · EVIDENCE REVIEW</div>
 <div style={{position:'absolute',bottom:155,left:110,display:'flex',alignItems:'center',gap:18,fontSize:27,color:ink}}><span style={{height:12,width:12,background:orange,borderRadius:6}}/>Controlled demonstration with fictional applicants</div>
 </AbsoluteFill>};

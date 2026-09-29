import React from 'react';
import {AbsoluteFill,Sequence,Audio,staticFile,useCurrentFrame,interpolate} from 'remotion';
import timing from '../timing.elevenlabs.json';
import {C,sans} from './kit';
import {Intro} from './Intro';import {Inputs} from './Inputs';import {Findings} from './Findings';import {Validation} from './Validation';import {Multiplayer} from './Multiplayer';import {Closing} from './Closing';

const scenes={Intro,Inputs,Findings,Validation,Multiplayer,Closing};
let at=0;const starts=timing.scenes.map(s=>{const a=at;at+=s.duration;return a;});

export const TraceDemo=()=>{const f=useCurrentFrame();const cap=timing.captions.find(c=>f>=c.from&&f<c.to);
 return <AbsoluteFill style={{background:C.bg}}>
  {timing.scenes.map((s,i)=>{const S=scenes[s.id as keyof typeof scenes];return <Sequence key={s.id} name={s.id} from={starts[i]} durationInFrames={s.duration}><S/></Sequence>})}
  {timing.scenes.flatMap(s=>s.clips.map(c=><Sequence key={c.src} from={c.from} durationInFrames={c.duration}><Audio src={staticFile(c.src)}/></Sequence>))}
  {cap&&<div style={{position:'absolute',left:0,right:0,bottom:46,display:'flex',justifyContent:'center'}}><div style={{background:'#050b0cd9',border:`1px solid ${C.line}`,color:C.text,fontFamily:sans,fontSize:31,lineHeight:1.3,padding:'12px 26px',borderRadius:12}}>{cap.text}</div></div>}
  <div style={{position:'absolute',bottom:0,left:0,height:4,width:interpolate(f,[0,timing.duration],[0,1920]),background:`linear-gradient(90deg, ${C.orange}, ${C.green})`}}/>
 </AbsoluteFill>};

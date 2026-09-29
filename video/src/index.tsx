import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Sequence,Audio,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {TransitionSeries} from '@remotion/transitions';
import {Intro} from './scenes/Intro';import {Inputs} from './scenes/Inputs';import {Findings} from './scenes/Findings';import {Validation} from './scenes/Validation';import {Multiplayer} from './scenes/Multiplayer';import {Closing} from './scenes/Closing';
import timing from './timing.elevenlabs.json';import {TraceDemo} from './trace/Demo';import {sans,orange} from './theme';
const components={Intro,Inputs,Findings,Validation,Multiplayer,Closing};
const Demo=()=>{const f=useCurrentFrame();const caption=timing.captions.find(c=>f>=c.from&&f<c.to);return <AbsoluteFill>
 <TransitionSeries>{timing.scenes.map(s=>{const C=components[s.id];return <TransitionSeries.Sequence key={s.id} name={s.id} durationInFrames={s.duration}><C/></TransitionSeries.Sequence>})}</TransitionSeries>
 {timing.scenes.flatMap(s=>s.clips.map(c=><Sequence key={c.src} from={c.from} durationInFrames={c.duration}><Audio src={staticFile(c.src)}/></Sequence>))}
 {caption&&<div style={{position:'absolute',left:160,right:160,bottom:40,display:'flex',justifyContent:'center'}}><div style={{background:'#102328ed',color:'#fffdf8',fontFamily:sans,fontSize:33,lineHeight:1.3,padding:'16px 28px',borderRadius:9,textAlign:'center',maxWidth:1580}}>{caption.text}</div></div>}
 <div style={{position:'absolute',bottom:0,left:0,height:5,width:interpolate(f,[0,timing.duration],[0,1920]),background:orange}}/>
 </AbsoluteFill>};
const Root=()=> <>
 <Composition id="RoletraceDemo" component={Demo} width={1920} height={1080} fps={30} durationInFrames={timing.duration}/>
 <Composition id="RoletraceTrace" component={TraceDemo} width={1920} height={1080} fps={30} durationInFrames={timing.duration}/>
</>;
registerRoot(Root);

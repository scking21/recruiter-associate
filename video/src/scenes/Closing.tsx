import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
import {ink,paper,sans,serif,orange} from '../theme';
export const Closing=()=> <AbsoluteFill style={{background:ink,color:paper,fontFamily:sans,padding:'100px 110px'}}>
 <div style={{fontSize:25,color:'#b5c6bd',letterSpacing:3}}>EXPLORE THE PROJECT</div>
 <h1 style={{fontFamily:serif,fontSize:82,fontWeight:400,letterSpacing:-3,lineHeight:1.08,width:1020,margin:'38px 0 28px'}}>Hiring evidence.<br/>Clear sources.<br/>Human decisions.</h1>
 <div style={{width:90,height:5,background:orange,marginBottom:35}}/>
 <div style={{fontSize:33,marginBottom:15}}>Find Roletrace on Agent Index</div>
 <div style={{fontSize:27,color:'#c2d4ca'}}>aiworthusing.com/agent-index/recruiter-associate</div>
 <div style={{fontSize:26,color:'#c2d4ca',marginTop:35}}>MIT source · github.com/scking21/recruiter-associate</div>
 <div style={{fontSize:23,color:'#a7b9b0',marginTop:45,lineHeight:1.7}}>OpenAI-generated cover · ElevenLabs synthetic narration<br/>Controlled engineering demonstration; no real applicants shown.</div>
 <div style={{position:'absolute',width:500,height:455,right:100,top:90,borderRadius:25,border:'5px solid #435950',overflow:'hidden'}}><Img src={staticFile('agent-index-roletrace.png')} style={{width:500}}/></div>
 </AbsoluteFill>;

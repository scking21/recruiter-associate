import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Shell,Card,Label,Pill,orange,muted,green} from '../theme';
export const Multiplayer=()=>{const f=useCurrentFrame();const step=f<170?0:f<320?1:2;return <Shell number="04" title="A correction changes the finding." tag="SIMULATED MULTIPLAYER · RECORDED TEST SUMMARY">
 <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:28}}>
 <Card style={{borderTop:'5px solid #789486'}}><Label>1 · Owner / simulated</Label><div style={{fontSize:35,lineHeight:1.35}}>Supplies a claim that applicant A fixed a Python timeout.</div><div style={{fontSize:24,color:muted,marginTop:40}}>Owner profile</div></Card>
 <Card style={{borderTop:`5px solid ${orange}`,opacity:step>=1?1:.38}}><Label>2 · Manager / simulated</Label><div style={{fontSize:35,lineHeight:1.35}}>Withdraws the Python debugging claim.</div><div style={{fontSize:24,color:muted,marginTop:40}}>Distinct participant profile</div></Card>
 <Card style={{borderTop:`5px solid ${green}`,opacity:step>=2?1:.38}}><Label>3 · Agent correction</Label><div style={{fontSize:35,lineHeight:1.35,marginBottom:25}}>Python debugging</div><Pill color={orange}>Unknown / unverified</Pill><div style={{fontSize:27,lineHeight:1.4,marginTop:22}}>Suggests evidence to request.</div></Card>
 </div>
 <div style={{fontSize:27,color:muted,marginTop:32,lineHeight:1.5}}>Same shared session. Other evidence retained. Hiring decision stays human.<br/><span style={{fontSize:23}}>Summary of the September 24 test, not a chat transcript or real user activity.</span></div>
 </Shell>};

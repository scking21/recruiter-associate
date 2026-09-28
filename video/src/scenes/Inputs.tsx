import React from 'react';
import {Shell,Card,Label,Pill,orange,muted} from '../theme';
export const Inputs=()=> <Shell number="01" title="Start with evidence.">
 <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:36}}>
 <Card><Label>The owner's criterion</Label><div style={{fontSize:46,lineHeight:1.2,marginBottom:28}}>Can explain a completed work sample</div><Pill>criterion_01</Pill></Card>
 <Card><Label>Fictional work sample evidence</Label><div style={{fontSize:46,lineHeight:1.2,marginBottom:28}}>Explained the work sample tradeoffs</div><Pill>evidence_01</Pill><span style={{fontSize:24,marginLeft:24,color:muted}}>candidate_01</span></Card>
 </div>
 <div style={{marginTop:32,padding:'28px 34px',borderLeft:`5px solid ${orange}`,fontSize:30,lineHeight:1.5}}>Minimized evidence → guarded prompt → OpenClaw review</div>
 <div style={{fontSize:24,color:muted,marginTop:22}}>Documented fictional test using the real-mode schema. No real applicants.</div>
 </Shell>;

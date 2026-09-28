import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Shell,Card,Label,Pill,mono,muted} from '../theme';
export const Findings=()=>{const f=useCurrentFrame();return <Shell number="02" title="Trace the finding to its source." tag="SAVED AGENT RESPONSE · FICTIONAL INPUT">
 <div style={{display:'grid',gridTemplateColumns:'1.08fr 1fr',gap:35}}>
 <Card><Label>Actual saved response · excerpt</Label><pre style={{fontFamily:mono,fontSize:31,lineHeight:1.7,margin:'20px 0',whiteSpace:'pre-wrap'}}>{`candidate_id: candidate_01\ncriterion_id: criterion_01\nstatus: met\nevidence_ids: [evidence_01]`}</pre><Pill>human_review_required</Pill></Card>
 <Card style={{opacity:interpolate(f,[30,50],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}><Label>The agent asks the hiring owner</Label><div style={{fontSize:34,lineHeight:1.35}}>“Does evidence_01 sufficiently establish the quality and completeness of the work sample explanation…”</div><div style={{fontSize:25,color:muted,marginTop:28}}>Verbatim excerpt from the saved response.</div></Card>
 </div>
 <div style={{fontSize:29,color:muted,marginTop:32}}>A cited finding, with a human review question. No scores or rankings.</div>
 </Shell>};

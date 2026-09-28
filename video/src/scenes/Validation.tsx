import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Shell,Card,Label,mono,ink,muted} from '../theme';
import result from '../../public/validation-result.json';
export const Validation=()=>{const f=useCurrentFrame();const code=`$ python3 -m recruiter validate\n  --input input.real.json\n  --response response.json\n\n{\n  "valid": ${result.valid},\n  "errors": ${JSON.stringify(result.errors)},\n  "decision": "${result.decision}"\n}`;return <Shell number="03" title="Check the review before using it." tag="FRESH OFFLINE VALIDATION · FICTIONAL INPUT">
 <div style={{display:'grid',gridTemplateColumns:'1.1fr .9fr',gap:35}}>
 <Card style={{background:ink,color:'#ebf0e8'}}><Label>Command excerpt · fresh result</Label><pre style={{fontFamily:mono,fontSize:29,lineHeight:1.46,margin:0,whiteSpace:'pre-wrap'}}>{code.slice(0,Math.floor(interpolate(f,[8,85],[0,code.length],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})))}</pre></Card>
 <Card><Label>What this checks</Label><div style={{fontSize:34,lineHeight:1.6}}>Required structure<br/>Citation references<br/>Human decision boundary</div><div style={{fontSize:27,color:muted,marginTop:30,lineHeight:1.4}}>A validation pass does not establish factual truth or hiring fitness.</div></Card>
 </div>
 </Shell>};

# Roletrace demo

Source for a 1920 × 1080, 30 fps narrated controlled demonstration. The Roletrace revision uses regenerated Brian opening and closing narration; the other four clips are unchanged. [Publication verification](../docs/DEMO.md) records the unlisted YouTube URL, signed-out playback, and Index embed.

## Files

- `output/roletrace-demo.mp4`: verified 93.952-second Roletrace export.
- `output/roletrace-demo.elevenlabs.srt`: Roletrace caption sidecar; captions are also burned in.
- `output/pre-roletrace/`: preserved pre-rebrand script, timing, original published export/captions, receipts, and affected narration clips.
- `src/`: editable Remotion scenes.
- `script.json`: narration script.
- `demo-evidence.md`: evidence and limitations.
- `public/validation-result.json`: fresh offline validation of the documented fictional engineering response.

## Trace recut (September 29, published as ZztJ2jnq6JU)

`npm run render:trace` renders the `RoletraceTrace` composition (`src/trace/`) to `output/roletrace-trace-demo.mp4`: same six Brian clips, captions and 93.952-second timing, with new dark evidence-graph visuals modeled on WebMCP Challenge winner demos (live state changes instead of static slides). The multiplayer scene replays verbatim excerpts of the saved September 24 simulation (`private/multiplayer/probe.cjs`, `owner-run.json`, `manager-run.json`); it is labeled as a replay with simulated participants. Guarded-prompt rules and validator checks quote `recruiter/workflow.py`. No model call or narration regeneration. Published by the user as https://www.youtube.com/watch?v=ZztJ2jnq6JU and attached to the Index; see `output/roletrace-trace-verification.json`. The earlier `RoletraceDemo` composition is retained for reproducibility.

## Asset provenance

The active `assets/roletrace-cover.png` was generated through OpenAI's built-in image tool on September 28 for this rebrand. The earlier `assets/recruiter-cover.png` remains a historical asset from September 24. No claim is made about its exact model version. Typography, diagrams, motion, captions, and edit were produced by Codex. The previously published narration uses ElevenLabs Brian - Relatable Everyman, generated with existing account credits. That prior revision required no purchase or upgrade. The Roletrace opening and closing were regenerated with the same voice/settings, consuming 375 existing credits; 6,309 remain. No purchase or upgrade. The original Samantha export is preserved under output/original-samantha.

The screenshot of the public Agent Index page was captured September 28, 2026. The saved agent response used the project's authorized NVIDIA GLM 5.3 route during the September 24 fictional engineering check. The video does not imply that OpenAI powers the recruiter itself.

## Evidence boundaries

The input and saved model response are a documented fictional test exercising the real-mode schema. The schema's `mode: real` and validator's `synthetic: false` are contract fields, not claims that the person or hiring task was real. Video labels disclose fictional inputs. The collaborator scene summarizes the documented shared-session simulation and is not a chat recording. The fresh validator execution makes no model call and reports no usage.

## Reproduce

```sh
npm ci
python3 prepare-elevenlabs-audio.py
npm run studio
npm run render
```

All six active ElevenLabs clips match `script.json`; pre-rebrand clips and the earlier local voice assets are archived under `output/pre-roletrace`. Use `--force` to regenerate existing derived audio/timing after checking the inputs. Requires Node.js, those clips, FFmpeg, and Google Chrome at the path in `package.json`. Remotion is pinned to 4.0.529; its individual/small-company license is separate from this project's MIT code. See https://github.com/remotion-dev/remotion/blob/main/LICENSE.md.

## Publication gate

Local render completion does not publish a YouTube video or attach it to Agent Index. Review the final artifact and proposed title/description, obtain publication authorization, then upload with the requested visibility. Verify the actual watch URL plays signed out and attach its YouTube ID to the listing. Record the watch URL, visibility, and verification timestamp in `docs/HACKATHON.md`.

## Historical narration revision, September 28, before Roletrace

User selected ElevenLabs instead of macOS narration. Selected Brian - Relatable Everyman, Eleven Multilingual v2, speed 0.92, stability 0.44, similarity 0.46, style 0.27, speaker boost on. All six scenes generated and downloaded through Chrome. Initial balance 7,931; verified remaining balance 6,684, consuming 1,247 credits. No purchase or upgrade. Provenance and clip hashes: output/narration-provenance.json. Captions are approximate proportional alignment, not forced word alignment.

Editorial basis: [Devpost interviews with hackathon winners](https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video) emphasize a concise opening, demonstrable behavior, readable visuals, and clear audio. This informs the problem-first opening; it is not evidence that Brian was used by winners. Existing fictional and simulated labels remain.

#!/usr/bin/env python3
"""Create editable storyboard and presenter documents from the recorded timeline."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'handoff';out.mkdir(exist_ok=True)
styles={
'route':('Keep the route open','A persistent dispatch-floor route. Cyan selections stay separate from amber actual energy. The same source ticket and destination geometry remain visible through the central explanation.'),
'forensic':('The one-FE gap','An investigation that begins with the empty second dropper and moves backward along a persistent time axis. Simulated and actual quantities occupy separate ledger rows. The same zero then forks into two outcomes.'),
'atlas':('Inside the release','A continuous technical atlas: authored source, captured runtime payload, executed Java, nested runtime scopes, and resource/configuration regions. Camera movement preserves spatial relationships during descent and ascent.'),
}
notes={
'intro':'Introduce the review format. These are silent schematics for live commentary or a recorded voiceover. Pause the player at D01baseline and D02fixed only after preparing the local demos.',
'route':'A source selection can feed several ordered destinations. The cyan record is control state. The separate amber source is physical energy storage. The manager is neither a tank nor an energy conduit.',
'input':'INPUT records the source selection and constraints. The real rendered Java calls context.addInput(this). No energy moves here. The animation explicitly marks omitted source.',
'input-record':'The record begins at INPUT and belongs to this trigger. A new trigger gets fresh records. That lifetime explains scope, but resetting records is not the fix.',
'output-order':'Walk through source checks, simulated destination acceptance, applicable limits, actual extraction, and insertion of the amount returned. The overview is conceptual control flow; the source pane identifies the real extraction line.',
'output':'Read source, simulate destination acceptance, apply limits, extract, insert the returned amount. Simulation does not debit the source. The displayed ordering is a schematic of the verified path.',
'conversion-25':'At the default Mekanism conversion, 25 FE requests 62 J in simulation after integer conversion. The simulation returns 24 FE. The actual operation withdraws 60 J and delivers 24 FE. Do not say 62 J was withdrawn or that energy disappeared.',
'ledger-25':'Read the ledger horizontally, then contrast the rows. Simulation: 25 FE → 62 J → 24 FE. Actual: 60 J withdrawn → 24 FE delivered. The first dropper gains 24, leaving a 1 FE gap.',
'conversion25':'The transparent/outlined plane is simulation; the solid mint plane is actual transfer. 62 J is a simulated request. Actual withdrawal is 60 J, equal to the delivered 24 FE.',
'conversion-1':'A 1 FE request maps to 2 J in simulation, returning 0 FE. Actual withdrawal is 0 J. This says something about this requested quantity, not the energy remaining at the source.',
'ledger-1':'The remaining 1 FE maps to a simulated 2 J and a returned 0 FE. Nothing is withdrawn. Follow that zero into the control-flow decision.',
'conversion1':'Zoom out to the nesting: the zero belongs to one destination attempt inside a source record. Do not retire the larger scope merely because this small quantity returns zero.',
'fixture':'Start at first 99,975 and second 0. The first pulse produces 99,999 and 100,000. The independent drain simulates the second doing work while the first stays idle, leaving 99,999 and 0. Do not reset both droppers.',
'D01baseline':'Pause the video yourself. The five-second bar does not pause it. Local preparation is required; commands.md preserves tested cloud commands, not a one-click Windows demo. Use a fresh baseline fixture and the documented pulse → acknowledge/release → drain → acknowledge/release → pulse sequence. Expected second pulse: first 99,999, second 0. Only the automatic full sequence was verified; the baseline first manual pulse was separately verified.',
'baseline-scope':'In 4.34 the empty extracted result calls source.setDone(). The source-record ticket is retired, and later destinations are skipped for this trigger. The energy source is not physically empty.',
'scope-comparison':'The change removes source.setDone() from the zero-extraction branch. Return still skips the current attempt; the caller may continue to later destinations because the source is not marked done. Other exhaustion and retention checks remain.',
'fixed-route':'The first destination still receives zero for its last 1 FE. The record survives, so the second destination can receive 100,000 FE. The first stays at 99,999; the fix does not fill the last FE gap.',
'D02fixed':'Pause the video yourself and use a fresh fixed fixture with the same starting values and sequence. Expected second pulse: first 99,999, second 100,000. The full manual sequence is not yet verified; do not present the schematic as captured intermediate gameplay. If local setup is not ready, explain the automated evidence and resume.',
'test-evidence':'Both automatic characterization tests passed. The baseline PASS confirms the bug was reproduced under its expected outcome; the fixed PASS confirms the intended outcome. No common new red/green regression test is being claimed.',
'label-gun':'Routine Label Gun push/pull success confirmations remain on by default. config/sfm-client.toml can set showLabelGunPushPullMessages=false. This only describes those routine success messages, not suppression of errors.',
'listener':'On newer NeoForge (1.20.3+), the listener belongs to the Level/position relationship. Keep the far coordinate watched while capability objects change, and keep the relay block entity retained. Do not describe this as the older object-level LazyOptional model.',
'resources':'Recipe paths move from data/minecraft to data/sfm while recipe JSON bytes remain unchanged. Recipe IDs and matching advancement references change. Producer found 12 byte-identical recipe relocations and 10 relocated advancements, each with two changed recipe references. French, Brazilian Portuguese and Buffer itemless-loot changes are additional release themes.',
'projections':'Liquid core plus explicit projection configuration produces per-Minecraft Java, resources and build files. This replaces maintaining authored source on a branch for each Minecraft version. Git branches still exist. The schematic deliberately avoids inventing a supported-target count.',
'release-inspection':'The file map is captured runtime payloads including GameTests, not a shipped release JAR. The producer supplied 1,317 union paths in lexicographic order, 44 columns. Tile 1006 is OutputStatement.class, with changed printed instruction/signature output. Byte or printed-view equality is not a proof of behavior. Return to the route that remains eligible.',
'symptom':'Begin with the result, not an explanation: first 99,999, second 0 after the second pulse in the baseline characterization. One has only 1 FE of capacity; the other is empty. Ask where OUTPUT stopped.',
'rewind':'Move backward to the fixture setup, then forward through the first pulse and separate work drain. Magnify the gain of 24 FE rather than assuming the requested 25 FE was delivered.',
'done':'The baseline marks the source record done after zero extraction at the first destination. The physical second dropper is still present and empty; the record no longer reaches its attempt in this trigger.',
'scope':'Compare the actual rendered branch with explicit omissions. First highlight source.setDone(); then remove it and highlight return in the fixed branch. The caller can continue because the source is not marked done. Do not claim return itself is a newly added fix.',
'fork':'Replay the same zero with identical starting conditions. Baseline second: 0. Fixed second: 100,000. First remains 99,999 in both. The changed scope explains the difference.',
'test-proof':'Both tests are green because characterization expectations differ. A hypothetical common assertion would fail baseline and pass fixed, but no such new test was executed.',
'tunnel':'The coordinate stays fixed through a capability-object swap. Invalidation reaches the retained relay block entity. The version boundary is NeoForge 1.20.3+.',
'label':'The TOML key defaults true. False hides routine push/pull success confirmations. Do not invent message wording or imply error messages disappear.',
'build':'Trace backward from the build through generated Java/resources/build files to Liquid core and projection config, then read the actual generation direction forward. Git branches remain; branch-per-Minecraft source maintenance is what changes.',
'inspection':'The runtime payload map includes GameTests. Detailed counts and classifier limits are in inventory.json. Return to the initial question with first 99,999 and second 100,000 under the fix.',
'source':'The cobalt plane is authored source and projection configuration. Generated Java, resources and build files are outputs of that source/config pair. Git branches remain.',
'jar':'This former JAR storyboard concept was corrected to captured MC 1.21.1 runtime payloads including GameTests. There was no inspected release JAR containing OutputStatement.class. Tile 1006 is the verified primary fix zoom; all colored indices follow the producer mapping.',
'executed-path':'Descend from the payload classification to the real rendered extraction statement. The Java is from the tested projection; linked source is the authored Liquid template. SFML directs the execution, but no unverified literal SFML program is invented.',
'wrong-scope':'The outer trigger survives; the baseline closes the larger source record after the first destination yields zero. This makes the later destination unreachable for the remainder of the trigger.',
'right-scope':'The fixed branch leaves the source record available while ending only the current destination attempt. The second reaches 100,000; the first remains 99,999. No new INPUT is required within this trigger.',
'tests':'Both automatic characterizations passed with their respective expected outcomes. Keep the differing world results in context. The complete manual walkthrough remains unverified.',
'config':'Unfold the client TOML key. It defaults true; false hides routine Label Gun push/pull confirmations only.',
'return-to-atlas':'Rise through the same world, executed Java, captured payload and authored source planes. Keep the fixed counters visible before returning to the whole map. This is a release review treatment, not approval to publish a release.',
}
def stamp(t):return f'{int(t)//60:02}:{int(t)%60:02}'
for name,(title,style) in styles.items():
 path=root/'renders'/f'{name}-render.json'
 if not path.exists():continue
 report=json.loads(path.read_text());cues=report.get('timelines',{}).get(name,[])
 if not cues or 'end' not in cues[-1]:continue
 rows=['| Time | Cue | Visual / presenter intention |','|---|---|---|']
 prose=[]
 for c in cues:
  note=notes.get(c['id'],'Follow the source-linked visual and hold the settled state before moving on.')
  rows.append(f"| {stamp(c['start'])}–{stamp(c['end'])} | `{c['id']}` | {note.replace('|','/')} |")
  prose.append(f"## {stamp(c['start'])} — {c['id']}\n\n{note}\n")
 common='Pause cards include a stable reading hold plus a five-second timebar. Playback continues automatically. All world diagrams are original schematics, not Orbit gameplay. Both automatic tests passed; the complete manual two-button sequence remains unverified. Detailed commands and provenance travel with this treatment.'
 (out/f'{name}-storyboard.md').write_text(f'# {title}\n\nDuration: {stamp(cues[-1]["end"])}. 1920×1080, 24 fps, silent.\n\n{style}\n\n{common}\n\n'+ '\n'.join(rows)+'\n\nTimings above are derived from the final recorded Motion Canvas generator timeline. `timeline.json` is the editable cue manifest. Meaningful chapter boundaries are the entries marked `chapter: true`, not every shot.\n')
 (out/f'{name}-presenter-notes.md').write_text(f'# Presenter notes — {title}\n\n{style}\n\nBefore presenting, prepare both local demo fixtures and verify the complete manual sequence. `commands.md` states exactly what was and was not tested. The film is deliberately silent; use these prompts as commentary, not a claim that narration was generated.\n\n'+ '\n'.join(prose))
 print(name,stamp(cues[-1]['end']),len(cues),'cues')

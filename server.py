#!/usr/bin/env python3
"""
Cubase MCP Server
=================
An MCP server for controlling Steinberg Cubase DAW.

Features:
- Transport control (play, stop, record)
- Mixer control (volume, pan, mute, solo)
- Track management
- MIDI file generation
- Song creation from text descriptions
"""

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import time
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Cubase Controller")

# Global MIDI port
midi_port: Optional[mido.ports.BaseOutput] = None
VIRTUAL_PORT_NAME = "Cubase MCP"


def get_midi_port():
    """Get or create the virtual MIDI port."""
    global midi_port
    if midi_port is None or midi_port.closed:
        try:
            # Create a virtual MIDI output port
            midi_port = mido.open_output(VIRTUAL_PORT_NAME, virtual=True)
            print(f"✓ Created virtual MIDI port: {VIRTUAL_PORT_NAME}")
        except Exception as e:
            print(f"✗ Failed to create MIDI port: {e}")
            raise
    return midi_port


def send_midi_cc(cc_number: int, value: int, channel: int = 0):
    """Send a MIDI Control Change message."""
    try:
        port = get_midi_port()
        msg = Message('control_change', control=cc_number, value=value, channel=channel)
        port.send(msg)
        return True
    except Exception as e:
        print(f"Error sending MIDI CC: {e}")
        return False


def send_midi_note(note: int, velocity: int, duration: float = 0.5, channel: int = 0):
    """Send a MIDI note on/off sequence."""
    try:
        port = get_midi_port()
        # Note on
        port.send(Message('note_on', note=note, velocity=velocity, channel=channel))
        time.sleep(duration)
        # Note off
        port.send(Message('note_off', note=note, velocity=0, channel=channel))
        return True
    except Exception as e:
        print(f"Error sending MIDI note: {e}")
        return False


# ============================================================================
# TRANSPORT CONTROLS
# ============================================================================

@mcp.tool()
def transport_play() -> str:
    """Start playback in Cubase."""
    # MIDI Machine Control (MMC) Play command
    # Or use CC that you'll map in Generic Remote
    if send_midi_cc(cc_number=91, value=127):  # CC 91 mapped to Play
        return "✓ Playback started"
    return "✗ Failed to start playback"


@mcp.tool()
def transport_stop() -> str:
    """Stop playback in Cubase."""
    if send_midi_cc(cc_number=92, value=127):  # CC 92 mapped to Stop
        return "✓ Playback stopped"
    return "✗ Failed to stop playback"


@mcp.tool()
def transport_record() -> str:
    """Start recording in Cubase."""
    if send_midi_cc(cc_number=93, value=127):  # CC 93 mapped to Record
        return "✓ Recording started"
    return "✗ Failed to start recording"


@mcp.tool()
def transport_rewind() -> str:
    """Rewind to beginning in Cubase."""
    if send_midi_cc(cc_number=94, value=127):  # CC 94 mapped to Rewind
        return "✓ Rewound to beginning"
    return "✗ Failed to rewind"


@mcp.tool()
def transport_forward() -> str:
    """Fast forward in Cubase."""
    if send_midi_cc(cc_number=95, value=127):  # CC 95 mapped to Forward
        return "✓ Fast forwarded"
    return "✗ Failed to fast forward"


# ============================================================================
# MIXER CONTROLS
# ============================================================================

@mcp.tool()
def mixer_set_volume(track: int, volume: int) -> str:
    """
    Set the volume of a track.

    Args:
        track: Track number (1-8)
        volume: Volume level (0-127)
    """
    if not (1 <= track <= 8):
        return "✗ Track number must be between 1 and 8"
    if not (0 <= volume <= 127):
        return "✗ Volume must be between 0 and 127"

    # CC 7 is standard MIDI volume, channel = track-1
    channel = track - 1
    if send_midi_cc(cc_number=7, value=volume, channel=channel):
        return f"✓ Set track {track} volume to {volume}"
    return f"✗ Failed to set track {track} volume"


@mcp.tool()
def mixer_set_pan(track: int, pan: int) -> str:
    """
    Set the pan of a track.

    Args:
        track: Track number (1-8)
        pan: Pan position (0=left, 64=center, 127=right)
    """
    if not (1 <= track <= 8):
        return "✗ Track number must be between 1 and 8"
    if not (0 <= pan <= 127):
        return "✗ Pan must be between 0 and 127"

    # CC 10 is standard MIDI pan
    channel = track - 1
    if send_midi_cc(cc_number=10, value=pan, channel=channel):
        return f"✓ Set track {track} pan to {pan}"
    return f"✗ Failed to set track {track} pan"


@mcp.tool()
def mixer_mute_track(track: int, mute: bool = True) -> str:
    """
    Mute or unmute a track.

    Args:
        track: Track number (1-8)
        mute: True to mute, False to unmute
    """
    if not (1 <= track <= 8):
        return "✗ Track number must be between 1 and 8"

    channel = track - 1
    value = 127 if mute else 0
    # CC 120 or custom CC you map in Generic Remote
    if send_midi_cc(cc_number=20 + track, value=value, channel=0):
        status = "muted" if mute else "unmuted"
        return f"✓ Track {track} {status}"
    return f"✗ Failed to mute/unmute track {track}"


@mcp.tool()
def mixer_solo_track(track: int, solo: bool = True) -> str:
    """
    Solo or unsolo a track.

    Args:
        track: Track number (1-8)
        solo: True to solo, False to unsolo
    """
    if not (1 <= track <= 8):
        return "✗ Track number must be between 1 and 8"

    channel = track - 1
    value = 127 if solo else 0
    # Custom CC you map in Generic Remote for Solo
    if send_midi_cc(cc_number=30 + track, value=value, channel=0):
        status = "soloed" if solo else "unsoloed"
        return f"✓ Track {track} {status}"
    return f"✗ Failed to solo/unsolo track {track}"


# ============================================================================
# MIDI FILE CREATION
# ============================================================================

@mcp.tool()
def create_midi_note_sequence(
    notes: str,
    output_path: str,
    tempo: int = 120,
    velocity: int = 64,
    duration: int = 480
) -> str:
    """
    Create a MIDI file with a sequence of notes.

    Args:
        notes: Comma-separated MIDI note numbers (e.g., "60,64,67,72")
        output_path: Path to save the MIDI file
        tempo: Tempo in BPM (default 120)
        velocity: Note velocity (0-127, default 64)
        duration: Note duration in ticks (default 480 = quarter note)
    """
    try:
        # Parse notes
        note_list = [int(n.strip()) for n in notes.split(',')]

        # Create MIDI file
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set tempo
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        # Add notes
        current_time = 0
        for note in note_list:
            track.append(Message('note_on', note=note, velocity=velocity, time=current_time))
            track.append(Message('note_off', note=note, velocity=0, time=duration))
            current_time = 0  # Next note starts immediately after

        # Save file
        output_path = os.path.expanduser(output_path)
        mid.save(output_path)

        return f"✓ Created MIDI file: {output_path}\n  Notes: {note_list}\n  Tempo: {tempo} BPM"
    except Exception as e:
        return f"✗ Failed to create MIDI file: {e}"


@mcp.tool()
def create_midi_chord_progression(
    chords: str,
    output_path: str,
    tempo: int = 120,
    velocity: int = 64,
    duration: int = 1920
) -> str:
    """
    Create a MIDI file with a chord progression.

    Args:
        chords: Chord names separated by commas (e.g., "C,Am,F,G")
        output_path: Path to save the MIDI file
        tempo: Tempo in BPM (default 120)
        velocity: Note velocity (0-127, default 64)
        duration: Chord duration in ticks (default 1920 = whole note)
    """
    try:
        # Chord dictionary (root note + intervals)
        chord_patterns = {
            'C': [60, 64, 67],    # C major
            'Cm': [60, 63, 67],   # C minor
            'D': [62, 66, 69],    # D major
            'Dm': [62, 65, 69],   # D minor
            'E': [64, 68, 71],    # E major
            'Em': [64, 67, 71],   # E minor
            'F': [65, 69, 72],    # F major
            'Fm': [65, 68, 72],   # F minor
            'G': [67, 71, 74],    # G major
            'Gm': [67, 70, 74],   # G minor
            'A': [69, 73, 76],    # A major
            'Am': [69, 72, 76],   # A minor
            'B': [71, 75, 78],    # B major
            'Bm': [71, 74, 78],   # B minor
        }

        # Parse chords
        chord_list = [c.strip() for c in chords.split(',')]

        # Create MIDI file
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set tempo
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        # Add chords
        for chord_name in chord_list:
            if chord_name not in chord_patterns:
                return f"✗ Unknown chord: {chord_name}. Available: {', '.join(chord_patterns.keys())}"

            chord_notes = chord_patterns[chord_name]

            # All notes on at the same time
            for i, note in enumerate(chord_notes):
                track.append(Message('note_on', note=note, velocity=velocity, time=0 if i > 0 else 0))

            # All notes off after duration (only set time on first note off)
            for i, note in enumerate(chord_notes):
                track.append(Message('note_off', note=note, velocity=0, time=duration if i == 0 else 0))

        # Save file
        output_path = os.path.expanduser(output_path)
        mid.save(output_path)

        return f"✓ Created MIDI chord progression: {output_path}\n  Chords: {chord_list}\n  Tempo: {tempo} BPM"
    except Exception as e:
        return f"✗ Failed to create MIDI file: {e}"


@mcp.tool()
def create_midi_melody(
    melody_description: str,
    output_path: str,
    tempo: int = 120,
    key: str = "C"
) -> str:
    """
    Create a MIDI melody based on a text description.
    This is a simplified version - you can expand it with AI music generation.

    Args:
        melody_description: Description of the melody (e.g., "happy upbeat melody")
        output_path: Path to save the MIDI file
        tempo: Tempo in BPM (default 120)
        key: Musical key (default "C")
    """
    try:
        # Scale patterns
        scales = {
            'C': [60, 62, 64, 65, 67, 69, 71, 72],  # C major scale
            'Am': [69, 71, 72, 74, 76, 77, 79, 81], # A minor scale
            'G': [67, 69, 71, 72, 74, 76, 78, 79],  # G major scale
        }

        if key not in scales:
            key = 'C'

        scale = scales[key]

        # Simple melody patterns based on description
        if 'happy' in melody_description.lower() or 'upbeat' in melody_description.lower():
            # Ascending pattern
            pattern = [0, 2, 4, 2, 0, 2, 4, 7]
        elif 'sad' in melody_description.lower() or 'melancholic' in melody_description.lower():
            # Descending pattern
            pattern = [7, 5, 4, 2, 0, 2, 4, 0]
        else:
            # Default pattern
            pattern = [0, 2, 4, 5, 4, 2, 0, 0]

        # Create notes from pattern
        notes = [scale[i % len(scale)] for i in pattern]

        # Create MIDI file
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set tempo
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        # Add notes
        for note in notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=0, time=480))  # Quarter note

        # Save file
        output_path = os.path.expanduser(output_path)
        mid.save(output_path)

        return f"✓ Created melody: {output_path}\n  Description: {melody_description}\n  Key: {key}\n  Tempo: {tempo} BPM"
    except Exception as e:
        return f"✗ Failed to create melody: {e}"


# ============================================================================
# SONG CREATION (High-level)
# ============================================================================

@mcp.tool()
def create_song_structure(
    song_description: str,
    output_directory: str,
    tempo: int = 120,
    key: str = "C"
) -> str:
    """
    Create a complete song structure with multiple MIDI files.
    This creates separate files for drums, bass, chords, and melody.

    Args:
        song_description: Description of the song (e.g., "upbeat pop song")
        output_directory: Directory to save MIDI files
        tempo: Tempo in BPM (default 120)
        key: Musical key (default "C")
    """
    try:
        # Create output directory
        output_dir = Path(os.path.expanduser(output_directory))
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []

        # 1. Create chord progression
        chords = "C,Am,F,G" if 'major' in key else "Am,F,C,G"
        chord_file = output_dir / "chords.mid"
        create_midi_chord_progression(chords, str(chord_file), tempo=tempo, duration=1920)
        results.append(f"  - Chords: {chord_file}")

        # 2. Create bass line (root notes of chords)
        bass_notes = "48,57,53,55"  # C2, A2, F2, G2
        bass_file = output_dir / "bass.mid"
        create_midi_note_sequence(bass_notes, str(bass_file), tempo=tempo, duration=1920, velocity=80)
        results.append(f"  - Bass: {bass_file}")

        # 3. Create melody
        melody_file = output_dir / "melody.mid"
        create_midi_melody(song_description, str(melody_file), tempo=tempo, key=key)
        results.append(f"  - Melody: {melody_file}")

        # 4. Create drum pattern (using MIDI channel 10 convention)
        drum_file = output_dir / "drums.mid"
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        # Simple 4/4 beat (kick, snare, hi-hat)
        kick = 36
        snare = 38
        hihat = 42

        for bar in range(4):  # 4 bars
            # Kick on 1 and 3
            track.append(Message('note_on', note=kick, velocity=100, time=0, channel=9))
            track.append(Message('note_off', note=kick, velocity=0, time=480, channel=9))

            # Snare on 2 and 4
            track.append(Message('note_on', note=snare, velocity=90, time=0, channel=9))
            track.append(Message('note_off', note=snare, velocity=0, time=480, channel=9))

            # Hi-hat on every beat
            for _ in range(4):
                track.append(Message('note_on', note=hihat, velocity=70, time=0, channel=9))
                track.append(Message('note_off', note=hihat, velocity=0, time=240, channel=9))

        mid.save(str(drum_file))
        results.append(f"  - Drums: {drum_file}")

        result_text = "\n".join(results)

        return f"""✓ Created song structure in: {output_dir}
{result_text}

Description: {song_description}
Key: {key}, Tempo: {tempo} BPM

Next steps:
1. Open Cubase
2. Create a new project
3. Import these MIDI files to separate tracks
4. Assign instruments (e.g., piano for chords, bass synth, drums)
5. Adjust and refine!"""
    except Exception as e:
        return f"✗ Failed to create song structure: {e}"


# ============================================================================
# INFO & SETUP
# ============================================================================

@mcp.tool()
def get_setup_instructions() -> str:
    """Get instructions for setting up the Cubase MCP server."""
    return """
╔═══════════════════════════════════════════════════════════════════════╗
║              CUBASE MCP SERVER - SETUP INSTRUCTIONS                   ║
╚═══════════════════════════════════════════════════════════════════════╝

1. VIRTUAL MIDI PORT SETUP (macOS)
   ─────────────────────────────────────────────────────────────────────
   • Open "Audio MIDI Setup" (/Applications/Utilities/)
   • Click "Window" → "Show MIDI Studio"
   • Double-click "IAC Driver"
   • Check "Device is online"
   • You should see the virtual port "Cubase MCP"

2. CUBASE SETUP - GENERIC REMOTE
   ─────────────────────────────────────────────────────────────────────
   • Open Cubase
   • Go to Studio → Studio Setup → Generic Remote
   • Click "+" to add a new remote
   • Set MIDI Input: "Cubase MCP"

   Map the following CCs to commands:

   TRANSPORT CONTROLS:
   • CC 91 → Transport: Play
   • CC 92 → Transport: Stop
   • CC 93 → Transport: Record
   • CC 94 → Transport: Return to Zero
   • CC 95 → Transport: Forward

   MIXER CONTROLS (per channel):
   • CC 7  → Volume (standard MIDI)
   • CC 10 → Pan (standard MIDI)
   • CC 20-28 → Track 1-8 Mute
   • CC 30-38 → Track 1-8 Solo

3. TEST THE CONNECTION
   ─────────────────────────────────────────────────────────────────────
   Use the transport controls to verify:

   transport_play()
   transport_stop()

   If these work, your setup is correct!

4. IMPORT MIDI FILES
   ─────────────────────────────────────────────────────────────────────
   • Use create_song_structure() to generate MIDI files
   • In Cubase: File → Import → MIDI File
   • Drag each file to a separate track
   • Assign instruments via VST Instruments

5. RECOMMENDED WORKFLOW
   ─────────────────────────────────────────────────────────────────────
   For AI-powered song creation:

   1. Ask Claude to create a song structure
   2. Import the MIDI files into Cubase
   3. Use Claude to control playback and adjust mixer
   4. Iterate and refine!

For more help: https://steinberg.help/cubase/
"""


@mcp.tool()
def list_available_tools() -> str:
    """List all available tools in this MCP server."""
    return """
╔═══════════════════════════════════════════════════════════════════════╗
║              CUBASE MCP SERVER - AVAILABLE TOOLS                      ║
╚═══════════════════════════════════════════════════════════════════════╝

🎵 TRANSPORT CONTROLS
────────────────────────────────────────────────────────────────────────
  • transport_play()         - Start playback
  • transport_stop()         - Stop playback
  • transport_record()       - Start recording
  • transport_rewind()       - Rewind to beginning
  • transport_forward()      - Fast forward

🎚️ MIXER CONTROLS
────────────────────────────────────────────────────────────────────────
  • mixer_set_volume(track, volume)     - Set track volume (0-127)
  • mixer_set_pan(track, pan)           - Set track pan (0-127)
  • mixer_mute_track(track, mute)       - Mute/unmute track
  • mixer_solo_track(track, solo)       - Solo/unsolo track

🎹 MIDI FILE CREATION
────────────────────────────────────────────────────────────────────────
  • create_midi_note_sequence()         - Create a sequence of notes
  • create_midi_chord_progression()     - Create chord progression
  • create_midi_melody()                - Create melody from description

🎼 SONG CREATION
────────────────────────────────────────────────────────────────────────
  • create_song_structure()             - Create complete song with:
                                           - Chords
                                           - Bass line
                                           - Melody
                                           - Drums

ℹ️ INFORMATION
────────────────────────────────────────────────────────────────────────
  • get_setup_instructions()            - Setup guide
  • list_available_tools()              - This list

═══════════════════════════════════════════════════════════════════════

Example usage:
  "Create an upbeat pop song in the key of C at 128 BPM"
  "Set track 1 volume to 100 and pan to center"
  "Create a chord progression: C, Am, F, G"
"""


if __name__ == "__main__":
    # Initialize MIDI port on startup
    try:
        get_midi_port()
        print("\n" + "="*70)
        print("  CUBASE MCP SERVER")
        print("="*70)
        print(f"\n✓ Virtual MIDI port created: {VIRTUAL_PORT_NAME}")
        print("\nRun get_setup_instructions() for setup guide.")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n✗ Failed to initialize: {e}\n")

    # Run the MCP server
    mcp.run()

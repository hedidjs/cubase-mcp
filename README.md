# Cubase MCP Server 🎵

**שרת MCP לשליטה בקיובייס (Steinberg Cubase) דרך Claude!**

## מה זה?

MCP Server שמאפשר ל-Claude לשלוט ב-Cubase בזמן אמת ולייצר מוזיקה. השרת משתמש ב-Virtual MIDI כדי לתקשר עם Cubase ויכול:

- ✅ לשלוט ב-Transport (play, stop, record)
- ✅ לשלוט במיקסר (volume, pan, mute, solo)
- ✅ ליצור קבצי MIDI עם נוטות, אקורדים ומלודיות
- ✅ **ליצור שירים שלמים מתיאור טקסט!** 🎼

## יכולות מיוחדות

### יצירת שיר שלם
```
"תיצור לי שיר פופ שמח ב-Key של C ב-120 BPM"
```

השרת יוצר:
- 🎹 מבנה אקורדים (chords.mid)
- 🎸 קו בס (bass.mid)
- 🎤 מלודיה (melody.mid)
- 🥁 תופים (drums.mid)

אחר כך פשוט מייבאים את הקבצים ל-Cubase!

## התקנה

### 1. התקן את החבילות הנדרשות

```bash
pip install -r requirements.txt
```

### 2. הגדר Virtual MIDI Port (macOS)

1. פתח **Audio MIDI Setup** (`/Applications/Utilities/`)
2. לחץ על **Window** → **Show MIDI Studio**
3. לחץ פעמיים על **IAC Driver**
4. סמן **"Device is online"**

### 3. הגדר Generic Remote ב-Cubase

1. פתח את Cubase
2. לך ל-**Studio** → **Studio Setup** → **Generic Remote**
3. לחץ על **"+"** כדי להוסיף remote חדש
4. הגדר **MIDI Input**: `Cubase MCP`

#### מיפוי CC (Control Change):

| CC Number | פקודה ב-Cubase |
|-----------|----------------|
| CC 91 | Transport → Play |
| CC 92 | Transport → Stop |
| CC 93 | Transport → Record |
| CC 94 | Transport → Return to Zero |
| CC 95 | Transport → Forward |
| CC 7 | Volume (Channel 0-7 = Track 1-8) |
| CC 10 | Pan (Channel 0-7 = Track 1-8) |
| CC 20-28 | Mute Track 1-8 |
| CC 30-38 | Solo Track 1-8 |

### 4. הוסף את השרת ל-Claude Code

ערוך את קובץ ההגדרות של Claude Code (בדרך כלל `~/.config/claude-code/settings.json`):

```json
{
  "mcpServers": {
    "cubase": {
      "command": "python",
      "args": ["/Users/rontzarfati/Desktop/cubase mcp/server.py"]
    }
  }
}
```

או ב-Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cubase": {
      "command": "python",
      "args": ["/Users/rontzarfati/Desktop/cubase mcp/server.py"]
    }
  }
}
```

### 5. הפעל מחדש את Claude

## שימוש

### דוגמאות

#### שליטה ב-Transport
```
"תפעיל playback בקיובייס"
"תעצור את ההשמעה"
"תתחיל להקליט"
```

#### שליטה במיקסר
```
"תעלה את העוצמה של טראק 1 ל-100"
"תציב את הפאן של טראק 2 למרכז (64)"
"תעשה mute לטראק 3"
"תעשה solo לטראק 1"
```

#### יצירת קבצי MIDI
```
"תיצור סדרת נוטות: 60, 64, 67, 72 ותשמור ב-~/Desktop/melody.mid"
"תיצור progression אקורדים: C, Am, F, G ותשמור ב-~/Desktop/chords.mid"
"תיצור מלודיה עצובה ומלנכולית בסולם Am"
```

#### יצירת שיר שלם!
```
"תיצור שיר אופטימי ושמח ב-Key של C ב-tempo 128 BPM ותשמור ב-~/Desktop/my_song/"
```

זה יוצר 4 קבצי MIDI:
- `chords.mid` - פרוגרסיית אקורדים
- `bass.mid` - קו בס
- `melody.mid` - מלודיה
- `drums.mid` - תבנית תופים

### זרימת עבודה מומלצת

1. **תכנון**: "תיצור לי שיר רוק אנרגטי ב-140 BPM"
2. **יצירה**: Claude יוצר את כל קבצי ה-MIDI
3. **ייבוא**: ייבא את הקבצים ל-Cubase (File → Import → MIDI File)
4. **הקצאת כלים**: הוסף VST instruments לכל טראק
5. **עיצוב**: השתמש ב-Claude כדי לשלוט במיקסר ולהקליט

## כלים זמינים

### 🎵 Transport Controls
- `transport_play()` - הפעל playback
- `transport_stop()` - עצור playback
- `transport_record()` - התחל הקלטה
- `transport_rewind()` - חזור להתחלה
- `transport_forward()` - קפוץ קדימה

### 🎚️ Mixer Controls
- `mixer_set_volume(track, volume)` - קבע עוצמה (0-127)
- `mixer_set_pan(track, pan)` - קבע pan (0=שמאל, 64=מרכז, 127=ימין)
- `mixer_mute_track(track, mute)` - השתק/בטל השתקה
- `mixer_solo_track(track, solo)` - solo/בטל solo

### 🎹 MIDI Creation
- `create_midi_note_sequence()` - צור סדרת נוטות
- `create_midi_chord_progression()` - צור פרוגרסיית אקורדים
- `create_midi_melody()` - צור מלודיה מתיאור

### 🎼 Song Creation
- `create_song_structure()` - צור שיר שלם עם:
  - אקורדים
  - בס
  - מלודיה
  - תופים

### ℹ️ Information
- `get_setup_instructions()` - מדריך התקנה מפורט
- `list_available_tools()` - רשימת כל הכלים

## מגבלות ושיקולים

### מה עובד מצוין ✅
- Transport control (play/stop/record)
- Mixer control (volume/pan)
- יצירת קבצי MIDI מורכבים
- יצירת שירים מתיאורים

### מה דורש עבודה ידנית 🔧
- ייבוא קבצי MIDI ל-Cubase (לא ניתן לאוטומציה)
- הוספת VST instruments
- עריכה מפורטת של MIDI clips
- אפקטים ו-mixing מתקדם

### הרחבות עתידיות 🚀
- תמיכה ב-MIDI Remote API (JavaScript)
- עריכה ישירה של קבצי .cpr (דורש reverse engineering)
- אינטגרציה עם מודלי AI ליצירת מוזיקה
- תמיכה במבני שירים מורכבים יותר

## פתרון בעיות

### "Failed to create MIDI port"
- ודא ש-IAC Driver מופעל ב-Audio MIDI Setup
- נסה להפעיל מחדש את המחשב

### "Failed to start playback"
- בדוק את הגדרות Generic Remote ב-Cubase
- ודא שה-MIDI Input מוגדר ל-"Cubase MCP"
- בדוק שה-CC mappings נכונים

### קבצי MIDI לא מתנגנים
- ודא שייבאת את הקבצים לטראקים הנכונים
- הוסף VST instrument לכל טראק
- בדוק את canal routing

## תמיכה

יש בעיה או רעיון לשיפור? פתח issue או שלח pull request!

## רישיון

MIT License - השתמש בחופשיות!

---

**נבנה עם ❤️ על ידי Claude Code**

🎵 **Happy Music Making!** 🎵

# מדריך התקנה מהיר - Cubase MCP

## שלב 1: הכן את המערכת

### התקן את החבילות הנדרשות
```bash
cd "/Users/rontzarfati/Desktop/cubase mcp"
python3 -m pip install -r requirements.txt
```

## שלב 2: הגדר Virtual MIDI (macOS)

1. פתח **Audio MIDI Setup**:
   - לחץ `Cmd+Space` והקלד "Audio MIDI Setup"
   - או לך ל- `/Applications/Utilities/Audio MIDI Setup.app`

2. פתח את MIDI Studio:
   - לחץ על **Window** → **Show MIDI Studio** (או `Cmd+2`)

3. הפעל את IAC Driver:
   - לחץ פעמיים על אייקון **IAC Driver**
   - סמן את התיבה **"Device is online"**
   - לחץ **Apply**

4. בדוק:
   - אתה אמור לראות port בשם "IAC Driver Bus 1"

## שלב 3: הגדר Generic Remote ב-Cubase

### פתח את הגדרות Studio
1. פתח את Cubase 14/15
2. לך ל- **Studio** → **Studio Setup**
3. בחלונית השמאלית, לחץ על **"+" (Add)**
4. בחר **Generic Remote**

### הגדר MIDI Input
1. ב-**MIDI Input**, בחר **"Cubase MCP"** (זה ה-virtual port שהשרת יוצר)
2. ב-**MIDI Output**, השאר "Not Connected"

### מיפוי Controls - Transport

לחץ על טאב **"Control"** למטה.

#### הוסף את פקודות ה-Transport:

| Control Name | MIDI Status | MIDI Channel | Address | Max Value |
|--------------|-------------|--------------|---------|-----------|
| Play         | Control Change | Any | 91 | 127 |
| Stop         | Control Change | Any | 92 | 127 |
| Record       | Control Change | Any | 93 | 127 |
| Return to Zero | Control Change | Any | 94 | 127 |
| Forward      | Control Change | Any | 95 | 127 |

**איך להוסיף:**
1. לחץ על שורה ריקה בטבלה
2. תחת **Device**, בחר **Controller**
3. תחת **Channel/Category**, בחר **Any**
4. תחת **Address**, הזן את מספר ה-CC (למשל: 91)
5. תחת **Max Value**, הזן **127**
6. תחת **Flags**, סמן **R** (Receive)

לאחר מכן, במפת ה-**Device**:
1. לחץ על שורה ריקה בצד ימין
2. תחת **Control**, בחר **Transport** → **Play** (או Stop/Record/etc.)
3. תחת **Value/Action**, בחר **Toggle** או **Trigger**

### מיפוי Controls - Mixer

#### Volume (CC 7):
- **MIDI Channel**: 1-8 (לכל טראק)
- **Address**: 7
- **Device Function**: **Mixer** → **Selected Track** → **Volume**

#### Pan (CC 10):
- **MIDI Channel**: 1-8
- **Address**: 10
- **Device Function**: **Mixer** → **Selected Track** → **Pan**

#### Mute (CC 20-28):
- **Address**: 20 (Track 1), 21 (Track 2), ..., 28 (Track 8)
- **Channel**: Any
- **Device Function**: **Mixer** → **Channel 1-8** → **Mute**

#### Solo (CC 30-38):
- **Address**: 30 (Track 1), 31 (Track 2), ..., 38 (Track 8)
- **Channel**: Any
- **Device Function**: **Mixer** → **Channel 1-8** → **Solo**

### שמור את ההגדרות
1. לחץ **Apply**
2. לחץ **OK**

## שלב 4: הגדר את Claude Code

### אופציה A: Claude Code (CLI)

ערוך את `~/.config/claude-code/settings.json`:

```bash
mkdir -p ~/.config/claude-code
nano ~/.config/claude-code/settings.json
```

הוסף:
```json
{
  "mcpServers": {
    "cubase": {
      "command": "python3",
      "args": ["/Users/rontzarfati/Desktop/cubase mcp/server.py"]
    }
  }
}
```

שמור: `Ctrl+O`, `Enter`, `Ctrl+X`

### אופציה B: Claude Desktop

ערוך את `~/Library/Application Support/Claude/claude_desktop_config.json`:

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

הוסף:
```json
{
  "mcpServers": {
    "cubase": {
      "command": "python3",
      "args": ["/Users/rontzarfati/Desktop/cubase mcp/server.py"]
    }
  }
}
```

### הפעל מחדש את Claude

## שלב 5: בדוק את ההתקנה

1. **פתח את Cubase** ווודא שפרויקט פתוח
2. **פתח את Claude**
3. שאל: **"תריץ את get_setup_instructions"**
4. נסה: **"תפעיל playback בקיובייס"** (`transport_play()`)

אם זה עובד - מזל טוב! 🎉

## פתרון בעיות

### "Failed to create MIDI port"
```bash
# בדוק אם IAC Driver פעיל
python3 -c "import mido; print(mido.get_output_names())"
```

אמור להדפיס רשימת ports. אם ריק:
- וודא ש-IAC Driver מופעל ב-Audio MIDI Setup
- נסה להפעיל מחדש את המחשב

### "Failed to start playback"
- בדוק ש-Generic Remote מוגדר נכון
- בדוק שה-MIDI Input הוא "Cubase MCP"
- נסה לשלוח MIDI message באופן ידני:

```python
python3 << 'EOF'
import mido
port = mido.open_output('Cubase MCP', virtual=True)
port.send(mido.Message('control_change', control=91, value=127))
print("Sent Play command!")
EOF
```

### MIDI Port לא מופיע ב-Cubase
- וודא שהשרת רץ (`python3 server.py`)
- הפעל מחדש את Cubase
- בדוק ב-**Studio** → **Studio Setup** → **MIDI Port Setup** שה-port מופיע

### כלים לא מופיעים ב-Claude
- בדוק את קובץ ההגדרות (settings.json או claude_desktop_config.json)
- וודא שהנתיב לקובץ server.py נכון
- הפעל מחדש את Claude

## בדיקה מהירה

פתח Terminal והרץ:

```bash
cd "/Users/rontzarfati/Desktop/cubase mcp"
python3 server.py
```

אם אתה רואה:
```
✓ Virtual MIDI port created: Cubase MCP
```

הכל תקין!

---

**נתקעת? צריך עזרה?**
פתח issue ב-GitHub או שאל את Claude!

🎵 **Happy Music Making!** 🎵

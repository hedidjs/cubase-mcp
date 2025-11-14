# דוגמאות שימוש - Cubase MCP

## דוגמאות בסיסיות

### 1. שליטה ב-Transport

```
אתה: "תפעיל playback בקיובייס"
Claude: [מריץ transport_play()]

אתה: "תעצור את ההשמעה"
Claude: [מריץ transport_stop()]

אתה: "תתחיל להקליט"
Claude: [מריץ transport_record()]

אתה: "תחזור להתחלה"
Claude: [מריץ transport_rewind()]
```

### 2. שליטה במיקסר

```
אתה: "תעלה את העוצמה של טראק 1 ל-100"
Claude: [מריץ mixer_set_volume(1, 100)]

אתה: "תציב את הפאן של טראק 2 למרכז"
Claude: [מריץ mixer_set_pan(2, 64)]

אתה: "תעשה mute לטראק 3"
Claude: [מריץ mixer_mute_track(3, True)]

אתה: "תבטל solo מטראק 1"
Claude: [מריץ mixer_solo_track(1, False)]
```

### 3. יצירת קבצי MIDI

```
אתה: "תיצור סדרת נוטות 60, 64, 67, 72 ותשמור ב-~/Desktop/melody.mid"
Claude: [מריץ create_midi_note_sequence("60,64,67,72", "~/Desktop/melody.mid")]

אתה: "תיצור progression של אקורדים: C, Am, F, G ב-tempo 120"
Claude: [מריץ create_midi_chord_progression("C,Am,F,G", "~/Desktop/chords.mid", tempo=120)]

אתה: "תיצור מלודיה עצובה בסולם Am ותשמור ב-~/Desktop/sad_melody.mid"
Claude: [מריץ create_midi_melody("sad melancholic melody", "~/Desktop/sad_melody.mid", key="Am")]
```

## דוגמאות מתקדמות

### 4. יצירת שיר שלם

```
אתה: "תיצור לי שיר פופ שמח ב-Key של C ב-120 BPM ותשמור ב-~/Desktop/my_song/"

Claude: אני יוצר לך שיר פופ שמח! זה יכלול:
- פרוגרסיית אקורדים (C, Am, F, G)
- קו בס
- מלודיה שמחה
- תבנית תופים 4/4

[מריץ create_song_structure("upbeat pop song", "~/Desktop/my_song/", tempo=120, key="C")]

✓ נוצרו 4 קבצים:
  - chords.mid - אקורדים
  - bass.mid - בס
  - melody.mid - מלודיה
  - drums.mid - תופים

עכשיו תוכל לייבא אותם ל-Cubase!
```

### 5. workflow שלם

```
אתה: "תיצור לי שיר רוק אנרגטי ב-140 BPM, תשמור אותו ב-Desktop,
      ואז תפעיל את Cubase ותכין את המיקסר - טראק 1 בעוצמה 100 ופאן מרכז,
      טראק 2 בעוצמה 90 ופאן קצת שמאל"

Claude:
שלב 1: יוצר שיר רוק אנרגטי...
[מריץ create_song_structure("energetic rock song", "~/Desktop/rock_song/", tempo=140, key="C")]

✓ נוצרו 4 קבצי MIDI ב-~/Desktop/rock_song/

שלב 2: מכין את המיקסר...
[מריץ mixer_set_volume(1, 100)]
[מריץ mixer_set_pan(1, 64)]
[מריץ mixer_set_volume(2, 90)]
[מריץ mixer_set_pan(2, 48)]

✓ המיקסר מוכן!

עכשיו:
1. פתח פרויקט חדש ב-Cubase
2. ייבא את 4 הקבצים (File → Import → MIDI File)
3. הקצה instruments (VST) לכל טראק
4. לחץ play!
```

### 6. שיר מותאם אישית

```
אתה: "תיצור לי שיר לקליפ יוטיוב - צריך משהו רגוע ומרגיע,
      בסגנון lofi hip hop, ב-85 BPM"

Claude: מעולה! אני יוצר לך רקע מוזיקלי lofi:

[מריץ create_song_structure("calm relaxing lofi hip hop", "~/Desktop/lofi_track/", tempo=85, key="Am")]

✓ נוצר:
  - chords.mid - אקורדים רגועים ב-Am
  - bass.mid - בס שקט
  - melody.mid - מלודיה מלנכולית ורגועה
  - drums.mid - beat lofi

השיר יהיה במצב רגוע ומרגיע, מושלם לרקע!
```

## דוגמאות לאינטראקציה מורכבת

### 7. עבודה עם הפרדה לטראקים

```
אתה: "תיצור לי beat hip hop עם 4 טראקים:
      1. תופים - kick + snare + hi-hat
      2. בס - deep ב-octave נמוך
      3. אקורדים - פרוגרסיה Am, F, C, G
      4. מלודיה - משהו מינימליסטי
      ותשמור הכל ב-Desktop/hiphop_beat/"

Claude: יוצר beat hip hop עם 4 טראקים נפרדים!

[מריץ create_song_structure("hip hop beat", "~/Desktop/hiphop_beat/", tempo=90, key="Am")]

✓ נוצרו הטראקים:
  1. drums.mid - תופים
  2. bass.mid - בס עמוק
  3. chords.mid - Am, F, C, G
  4. melody.mid - מלודיה מינימליסטית

ייבא אותם ל-Cubase בסדר הזה ותקבל beat מושלם!
```

### 8. שימוש בכלים המתקדמים

```
אתה: "תראה לי מה אפשר לעשות עם ה-MCP הזה"

Claude: [מריץ list_available_tools()]

הנה כל הכלים הזמינים:
[מציג את כל הכלים]

אתה: "איך מגדירים את זה?"

Claude: [מריץ get_setup_instructions()]

הנה מדריך ההתקנה המלא:
[מציג הוראות]
```

## טיפים לשימוש

### אקורדים נתמכים
```
מז'ור: C, D, E, F, G, A, B
מינור: Cm, Dm, Em, Fm, Gm, Am, Bm
```

### סולמות נתמכים
```
C - סולם דו מז'ור
Am - סולם לה מינור
G - סולם סול מז'ור
```

### טמפו מומלץ
```
60-80 BPM - רגוע, ballad
80-100 BPM - בינוני, pop
100-130 BPM - אנרגטי, dance
130-180 BPM - מהיר, electronic/rock
```

### MIDI Note Numbers
```
C3 = 48
C4 (Middle C) = 60
C5 = 72
C6 = 84

כל אוקטבה = +12 notes
```

## פתרון בעיות נפוצות

### "Failed to start playback"
```
1. בדוק ש-Generic Remote מוגדר ב-Cubase
2. ודא ש-MIDI Input הוא "Cubase MCP"
3. נסה:
   transport_stop()
   transport_play()
```

### קבצי MIDI לא נשמעים
```
1. ייבא את הקבצים (File → Import → MIDI File)
2. הוסף VST Instrument לכל טראק
3. בדוק routing
4. הפעל playback
```

### רוצה להתאים אישית?
```python
# ערוך את server.py:
# - הוסף אקורדים חדשים ל-chord_patterns
# - שנה את הסולמות ב-scales
# - התאם את תבניות התופים
```

---

🎵 **תהנה מיצירת מוזיקה עם Claude!** 🎵

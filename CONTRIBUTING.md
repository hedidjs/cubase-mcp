# Contributing to Cubase MCP

תודה שאתה מתעניין לתרום לפרויקט! 🎵

## איך לתרום

### דיווח על באגים

אם מצאת באג, אנא פתח [Issue](https://github.com/hedidjs/cubase-mcp/issues) עם:
- תיאור הבעיה
- שלבים לשחזור
- סביבת העבודה שלך (macOS version, Cubase version, Python version)
- הודעות שגיאה (אם יש)

### הצעות לפיצ'רים חדשים

יש לך רעיון לפיצ'ר חדש? מעולה!
1. פתח Issue עם תיאור הפיצ'ר
2. הסבר למה זה שימושי
3. אם אפשר, תן דוגמה לשימוש

### שיפור התיעוד

התיעוד חשוב! אם מצאת:
- טעויות כתיב
- הוראות לא ברורות
- חוסר במידע

אנא פתח Pull Request עם השיפורים.

## תהליך הפיתוח

### 1. Fork את הפרויקט

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cubase-mcp.git
cd cubase-mcp
```

### 2. צור branch חדש

```bash
git checkout -b feature/amazing-feature
# או
git checkout -b fix/bug-description
```

### 3. עשה את השינויים שלך

- כתוב קוד נקי וקריא
- הוסף docstrings לפונקציות חדשות
- עדכן את התיעוד אם צריך

### 4. בדוק את הקוד

```bash
# Check syntax
python3 -m py_compile server.py

# Test imports
python3 -c "from mcp.server.fastmcp import FastMCP; import mido; print('✓ All imports work')"
```

### 5. Commit והעלה

```bash
git add .
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### 6. פתח Pull Request

לך ל-GitHub ופתח Pull Request עם תיאור מפורט של השינויים.

## קוד סטיילים

### Python

- עקוב אחרי [PEP 8](https://pep8.org/)
- השתמש ב-type hints איפה שאפשר
- כתוב docstrings בסגנון Google

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    return True
```

### תיעוד

- תיעוד בעברית ב-README, SETUP-GUIDE, ו-examples
- תיעוד בקוד באנגלית (docstrings, comments)
- השתמש בדוגמאות ברורות

## רעיונות לפיצ'רים עתידיים

רוצה לעזור אבל לא בטוח מה לעשות? הנה כמה רעיונות:

### קל
- [ ] הוסף עוד אקורדים (7th chords, sus chords, etc.)
- [ ] הוסף עוד סולמות (Harmonic minor, Pentatonic, etc.)
- [ ] שפר את תבניות התופים
- [ ] הוסף presets למלודיות שונות

### בינוני
- [ ] תמיכה ב-MIDI channels נוספים
- [ ] יצירת automation curves
- [ ] ייבוא MIDI files ועריכה שלהם
- [ ] תמיכה ב-time signatures שונים (3/4, 5/4, 7/8, etc.)

### מתקדם
- [ ] אינטגרציה עם AI models ליצירת מוזיקה (MusicGen, AudioCraft)
- [ ] עריכה ישירה של קבצי .cpr (reverse engineering)
- [ ] תמיכה ב-MIDI Remote API JavaScript
- [ ] Real-time MIDI recording מ-Claude
- [ ] VST plugin control
- [ ] Project template management

## שאלות?

יש לך שאלות? אפשר:
- לפתוח Discussion ב-GitHub
- לפתוח Issue
- ליצור קשר דרך Pull Request

תודה על התרומה שלך! 🙏

---

**Happy Coding & Music Making!** 🎵

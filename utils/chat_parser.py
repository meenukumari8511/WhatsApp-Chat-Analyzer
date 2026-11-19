import re
import pandas as pd

# Android and iOS WhatsApp exports, with optional square brackets and seconds.
PATTERNS = [
    re.compile(r'^\[?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)\]?\s+-\s+(.*)$'),
    re.compile(r'^\[?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)\]?\s+(.*)$'),
    re.compile(r'^\[?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)\]?\s*[-–]\s*(.*)$'),
]

def parse_datetime(date_s, time_s):
    value = f"{date_s} {time_s.strip()}"
    return pd.to_datetime(value, dayfirst=True, errors="coerce")

def parse_chat(raw_text):
    records, current = [], None
    for line in raw_text.splitlines():
        match = next((p.match(line) for p in PATTERNS if p.match(line)), None)
        if match:
            if current:
                records.append(current)
            dt = parse_datetime(match.group(1), match.group(2))
            body = match.group(3)
            if pd.isna(dt):
                current = None
                continue
            # System notifications have no "Sender: message" separator.
            if ": " in body:
                sender, message = body.split(": ", 1)
                if not sender.strip():
                    sender, message = "System", body
            else:
                sender, message = "System", body
            current = {"datetime": dt, "sender": sender.strip(), "message": message.strip()}
        elif current and line.strip():
            current["message"] += "\n" + line.strip()
    if current:
        records.append(current)
    df = pd.DataFrame(records, columns=["datetime", "sender", "message"])
    if not df.empty:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df = df.dropna(subset=["datetime"]).reset_index(drop=True)
    return df, f"{len(df):,} timestamped messages detected"

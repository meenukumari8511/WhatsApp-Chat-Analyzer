import pandas as pd
import re
from collections import Counter

STOP = set("the and for that this with you your are was were have has had but not what when where who how why from they them then than there their about just like into out our we i me my it is a to of in on at as be or an if so do did can could would should will shall he she his her its we us by all more very no yes ok okay yeah ha haha lol im dont don't cant can't its it's".split())
MEDIA_MARKERS = ("<media omitted>", "<attached:", "image omitted", "video omitted", "audio omitted", "sticker omitted")

def build_metrics(df):
    messages = df["message"].fillna("")
    words = sum(len(re.findall(r"\b\w+\b", x, flags=re.UNICODE)) for x in messages)
    media = sum(any(m in x.lower() for m in MEDIA_MARKERS) for x in messages)
    return {"messages":len(df), "participants":df["sender"].nunique(), "words":words, "media":media, "active_days":pd.to_datetime(df["datetime"]).dt.date.nunique()}

def activity_tables(df):
    d = df.copy(); dt = pd.to_datetime(d["datetime"])
    d["date"] = dt.dt.date; d["month"] = dt.dt.to_period("M").astype(str); d["hour"] = dt.dt.hour; d["weekday"] = dt.dt.day_name()
    daily = d.groupby("date").size().reset_index(name="messages")
    monthly = d.groupby("month").size().reset_index(name="messages")
    hourly = d.groupby("hour").size().reindex(range(24), fill_value=0).rename("messages").reset_index()
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    weekday = d.groupby("weekday").size().reindex(order, fill_value=0).rename("messages").reset_index()
    return daily, monthly, hourly, weekday

def user_stats(df):
    x = df.groupby("sender").agg(messages=("message","size"), words=("message",lambda s:sum(len(re.findall(r"\b\w+\b", str(v))) for v in s)), first_message=("datetime","min"), last_message=("datetime","max")).reset_index()
    x["share_%"] = (x["messages"] / max(len(df),1) * 100).round(1)
    return x.sort_values("messages", ascending=False)

def emoji_stats(df):
    chars = []
    for msg in df["message"].fillna(""):
        chars.extend(c for c in msg if ord(c) > 0x1F000 or c in "❤️😂😭😊😍👍🙏🔥🎉💯")
    return pd.DataFrame(Counter(chars).most_common(), columns=["emoji","count"])

def word_stats(df):
    words=[]
    for msg in df["message"].fillna(""):
        for w in re.findall(r"[A-Za-z]{3,}", msg.lower()):
            if w not in STOP: words.append(w)
    return pd.DataFrame(Counter(words).most_common(), columns=["word","count"])

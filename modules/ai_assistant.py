from .analytics import user_stats, word_stats, activity_tables, build_metrics
import pandas as pd

def make_summary(df):
    m=build_metrics(df); users=user_stats(df); words=word_stats(df); daily,monthly,hourly,weekday=activity_tables(df)
    lines=["### Conversation overview",f"- **Messages:** {m['messages']:,}",f"- **Participants:** {m['participants']}",f"- **Words:** {m['words']:,}",f"- **Active days:** {m['active_days']}"]
    if not users.empty:
        top=users.iloc[0]; lines.append(f"- **Most active participant:** {top['sender']} ({top['messages']:,} messages)")
    if not daily.empty:
        peak=daily.loc[daily.messages.idxmax()]; lines.append(f"- **Busiest date:** {peak['date']} ({peak['messages']} messages)")
    if not words.empty: lines.append("- **Frequent words:** " + ", ".join(words.head(8).word.tolist()))
    if not weekday.empty:
        peak=weekday.loc[weekday.messages.idxmax()]; lines.append(f"- **Most active weekday:** {peak['weekday']}")
    lines.append("\n*This is a statistical summary of the selected messages, not an interpretation of private intent or emotion.*")
    return "\n".join(lines)

def answer_question(question, df):
    q=question.lower(); m=build_metrics(df); users=user_stats(df); words=word_stats(df); daily,monthly,hourly,weekday=activity_tables(df)
    if any(k in q for k in ["most message","most active","top user","who sent","highest message"]):
        if users.empty:return "No participant data available."
        r=users.iloc[0]; return f"**{r['sender']}** sent the most messages: **{r['messages']:,}** ({r['share_%']}% of the selected chat)."
    if "participant" in q or "member" in q or "people" in q: return f"There are **{m['participants']} participants** in the selected messages: " + ", ".join(users.sender.tolist())
    if "word" in q and ("common" in q or "most" in q or "frequent" in q): return "Most common words: " + (", ".join(f"{r.word} ({r['count']})" for _,r in words.head(10).iterrows()) if not words.empty else "No words found.")
    if "busiest day" in q or "which day" in q or "peak day" in q:
        if daily.empty:return "No date activity available."
        r=daily.loc[daily.messages.idxmax()]; return f"The busiest date was **{r['date']}**, with **{r['messages']} messages**."
    if "weekday" in q or "day of week" in q:
        if weekday.empty:return "No weekday activity available."
        r=weekday.loc[weekday.messages.idxmax()]; return f"The most active weekday was **{r['weekday']}** ({r['messages']} messages)."
    if "hour" in q or "time" in q:
        r=hourly.loc[hourly.messages.idxmax()]; return f"The busiest hour was **{int(r['hour']):02d}:00–{int(r['hour']):02d}:59** ({r['messages']} messages)."
    if "how many" in q or "total message" in q or "count" in q: return f"The selected chat contains **{m['messages']:,} messages**, **{m['words']:,} words**, and **{m['participants']} participants**."
    if "media" in q or "photo" in q or "video" in q: return f"I detected **{m['media']} messages** containing common WhatsApp media placeholders. This may not include media omitted from the export."
    return "I can answer questions about message counts, most active participant, participants, busiest date/weekday/hour, frequent words, and media placeholders. Try one of those topics."

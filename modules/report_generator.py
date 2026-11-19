from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(df, metrics, users):
    buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
    styles=getSampleStyleSheet(); story=[Paragraph("WhatsApp Chat Analysis Report",styles["Title"]),Spacer(1,14)]
    for label,key in [("Messages","messages"),("Participants","participants"),("Words","words"),("Media placeholders","media"),("Active days","active_days")]:
        story.append(Paragraph(f"<b>{label}:</b> {metrics[key]}",styles["BodyText"]))
    story.append(Spacer(1,16)); story.append(Paragraph("Participant activity",styles["Heading2"]))
    data=[["Participant","Messages","Share %"]]
    for _,r in users.head(25).iterrows(): data.append([str(r.sender),str(r.messages),str(r["share_%"])])
    table=Table(data,repeatRows=1,colWidths=[260,100,100]); table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#263746")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.grey),("PADDING",(0,0),(-1,-1),6)])); story.append(table)
    story.append(Spacer(1,12)); story.append(Paragraph("Generated from the filtered WhatsApp text export. Media counts are estimates based on export placeholders.",styles["Italic"]))
    doc.build(story); return buf.getvalue()

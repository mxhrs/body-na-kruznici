import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Titulek aplikace
st.title("Body na kružnici")

# Vstupy od uživatele
x0 = st.number_input("Souřadnice středu X:", value=0.0)
y0 = st.number_input("Souřadnice středu Y:", value=0.0)
r = st.number_input("Poloměr kruhu (m):", min_value=0.1, value=5.0)
n = st.slider("Počet bodů:", min_value=3, max_value=500, value=10)
barva = st.color_picker("Barva bodů:", "#ff0000")

# Výpočet souřadnic bodů
uhly = np.linspace(0, 2*np.pi, n, endpoint=False)
x = x0 + r * np.cos(uhly)
y = y0 + r * np.sin(uhly)

# Vykreslení grafu
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(x, y, color=barva)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_title(f"{n} bodů na kružnici (r = {r} m)")
st.pyplot(fig)

# Informace o autorovi
st.sidebar.title("O autorovi")
st.sidebar.write("Jméno: Jan Novák")   # <-- sem dej své jméno
st.sidebar.write("Email: jan.novak@example.com")  # <-- sem dej svůj email
st.sidebar.write("Použité technologie: Python, Streamlit, Matplotlib, ReportLab")

# Export do PDF
if st.button("Exportovat do PDF"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Body na kružnici", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Počet bodů: {n}", styles["Normal"]))
    story.append(Paragraph(f"Poloměr: {r} m", styles["Normal"]))
    story.append(Paragraph(f"Střed: ({x0}, {y0})", styles["Normal"]))
    story.append(Paragraph(f"Barva bodů: {barva}", styles["Normal"]))
    story.append(Paragraph("Autor: Jan Novák, jan.novak@example.com", styles["Normal"]))
    
    # Obrázek grafu do PDF
    img_buf = BytesIO()
    fig.savefig(img_buf, format="png")
    img_buf.seek(0)
    story.append(Image(img_buf))
    
    doc.build(story)
    buffer.seek(0)
    st.download_button(
        "Stáhnout PDF",
        data=buffer,
        file_name="kruh.pdf",
        mime="application/pdf"
    )

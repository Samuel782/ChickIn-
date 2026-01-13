import os 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib import colors


from grafici import crea_istogramma

LOGO_DX = "static/img/santa.png"
LOGO_SX = "static/img/biblioteca.png"

HEADER_HEIGHT = 1.5 * cm
HEADER_TOP = A4[1] - 2 * cm
LINE_COLOR = HexColor("#B0B0B0")

LEFT_MARGIN = 2.5 * cm
RIGHT_MARGIN = 2.5 * cm

def draw_logo(canvas, path, x, y, height):
    img = ImageReader(path)
    iw, ih = img.getSize()
    width = height * iw / ih

    canvas.drawImage(
        path,
        x,
        y,
        width=width,
        height=height,
        mask="auto",
        preserveAspectRatio=True
    )
    return width


def header(canvas, doc):
    canvas.saveState()

    page_width, page_height = A4
    y_img = page_height - 2 * cm - HEADER_HEIGHT

    # --- Logo sinistro ---
    draw_logo(
        canvas,
        LOGO_SX,
        doc.leftMargin,
        y_img,
        HEADER_HEIGHT
    )

    # --- Calcolo larghezza logo destro ---
    img_dx = ImageReader(LOGO_DX)
    iw, ih = img_dx.getSize()
    logo_dx_width = HEADER_HEIGHT * iw / ih

    # --- Logo destro perfettamente allineato ---
    draw_logo(
        canvas,
        LOGO_DX,
        page_width - doc.rightMargin - logo_dx_width,
        y_img,
        HEADER_HEIGHT
    )

    canvas.setStrokeColor(LINE_COLOR)
    canvas.setLineWidth(0.8)
    canvas.line(
        doc.leftMargin,
        y_img - 0.6 * cm,
        page_width - doc.rightMargin,
        y_img - 0.6 * cm
    )

    canvas.restoreState()

# ================= PDF =================

doc = SimpleDocTemplate(
    "report_professionale.pdf",
    pagesize=A4,
    topMargin=4 * cm,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    bottomMargin=2.5 * cm
)

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=HexColor("#333333"),
        spaceAfter=4
    )
)

## ========= Styles =========
#Header & info
styles.add(ParagraphStyle(
    name="ReportTitle",
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=20,
    alignment=1,  # centrato
    spaceAfter=6,
    textColor=HexColor("#1F2D3D")
))

styles.add(ParagraphStyle(
    name="ReportSubtitle",
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    alignment=0,
    textColor=HexColor("#4A4A4A"),
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name="ReportSection",
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=14,
    alignment=1,
    textColor=HexColor("#2C3E50"),
    spaceAfter=14
))
# Report
styles.add(ParagraphStyle(
    name="MetricTitle",
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=14,
    alignment=1,  # centrato
    textColor=HexColor("#1F2D3D"),
    spaceAfter=2
))

# Stile per i valori corrispondenti
styles.add(ParagraphStyle(
    name="MetricValue",
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=18,
    alignment=1,  # centrato
    textColor=HexColor("#2C3E50"),
    spaceAfter=10
))


startDay = "01-01-2026"
endDay = "31-01-2026"

totale = 1843
servizi = 610
biblioteca = 940
turisti = 620
cittadini = 845


contenuto = [
    Paragraph("REPORT AFFLUENZA", styles["ReportTitle"]),
    Paragraph(f"Periodo di riferimento: dal {startDay} al {endDay}", styles["ReportSection"]),
    Paragraph("Ex Convento di Santa Chiara", styles["ReportSubtitle"]),
    Paragraph("Via S. Chiara, 2", styles["ReportSubtitle"]),
    Paragraph("Santa Spazio culturale – Biblioteca del vicolo", styles["ReportSubtitle"]),
   
    Paragraph(
        "Questo documento riporta le informazioni relative alle visite registrate.",
        styles["Body"]
    )
    
]

report_labels = ["TOTALE", "SERVIZI", "BIBLIOTECA", "TURISTI", "CITTADINI"]
report_values = [1843, 610, 940, 620, 845]

# Creiamo due righe: una per i titoli, una per i valori
table_data = [
    [Paragraph(label, styles["MetricTitle"]) for label in report_labels],
    [Paragraph(str(value), styles["MetricValue"]) for value in report_values]
]

# Tabella centrale, senza bordi
table = Table(table_data, hAlign='CENTER', colWidths=[None]*len(report_labels))
table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    # Nessun bordo
    ('BOX', (0,0), (-1,-1), 0, HexColor("#FFFFFF")),
    ('INNERGRID', (0,0), (-1,-1), 0, HexColor("#FFFFFF")),
]))

contenuto.append(table)

grafico_path = crea_istogramma(report_values, report_labels, output_path="istogramma_temp.png")
contenuto.append(Image(grafico_path, width=14*cm, height=9*cm))  # dimensione PDF

if os.path.exists(grafico_path):
    os.remove(grafico_path)

doc.build(
    contenuto,
    onFirstPage=header,
    onLaterPages=header
)




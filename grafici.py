import matplotlib.pyplot as plt
from reportlab.lib.units import cm

def crea_istogramma(report_values, report_labels, output_path="istogramma.png"):
    """
    report_values: lista di valori numerici [Totale, Servizi, Biblioteca]
    report_labels: lista di etichette corrispondenti ["TOTALE", "SERVIZI", "BIBLIOTECA"]
    output_path: percorso dove salvare il PNG
    """
    # colori soft coordinati
    colori = ["#2C3E50", "#4A6C8C", "#7F9BBF"]  # blu istituzionali soft

    plt.figure(figsize=(6,4))  # dimensioni PDF compatibili
    bars = plt.bar(report_labels, report_values, color=colori, width=0.5)

    # valori sopra le barre
    for bar, val in zip(bars, report_values):
        plt.text(bar.get_x() + bar.get_width()/2, val + max(report_values)*0.02,
                 str(val), ha='center', va='bottom', fontweight='bold', color='#1F2D3D')

    # stile istituzionale
    plt.title("Ingressi per categoria", fontsize=12, color="#1F2D3D")
    plt.ylabel("Numero ingressi", fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()

    # salva immagine trasparente
    plt.savefig(output_path, dpi=150, bbox_inches='tight', transparent=True)
    plt.close()
    return output_path
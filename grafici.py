import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

def crea_istogramma(report_values, report_labels, output_path="istogramma.png"):
    """
    report_values: lista di valori numerici
    report_labels: lista di etichette corrispondenti
    output_path: percorso dove salvare il PNG
    """
    # colori soft coordinati (ripetuti se più barre)
    base_colors = ["#2C3E50", "#4A6C8C", "#7F9BBF", "#A3B7D5", "#C8D6EB"]
    colori = [base_colors[i % len(base_colors)] for i in range(len(report_values))]

    plt.figure(figsize=(6,4))
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
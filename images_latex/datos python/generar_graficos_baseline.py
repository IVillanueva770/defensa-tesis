import pandas as pd
import matplotlib.pyplot as plt

# Leer los datos
loss_data = pd.read_csv('baseline_loss.csv')
acc_data = pd.read_csv('baseline_accuracy.csv')

# Configurar el estilo general (igual que los otros graficos)
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 11

# Grafico de Loss
fig, ax = plt.subplots()
ax.plot(loss_data['epoch'], loss_data['train_loss'], label='train', color='tab:blue', linewidth=1)
ax.plot(loss_data['epoch'], loss_data['val_loss'], label='val', color='tab:orange', linewidth=1)
ax.set_xlabel('epochs')
ax.set_ylabel('loss')
ax.set_title('Experimento Baseline - ResNet3D SlowOnly (sin regularizacion)')
ax.legend()
plt.tight_layout()
plt.savefig('baseline_experimento_loss.png', dpi=100, bbox_inches='tight')
plt.close()

# Grafico de Accuracy
fig, ax = plt.subplots()
ax.plot(acc_data['epoch'], acc_data['train_acc'], label='train', color='tab:blue', linewidth=1)
ax.plot(acc_data['epoch'], acc_data['val_acc'], label='val', color='tab:orange', linewidth=1)
ax.set_xlabel('epochs')
ax.set_ylabel('top1 acc')
ax.set_title('Experimento Baseline - ResNet3D SlowOnly (sin regularizacion)')
ax.legend()
plt.tight_layout()
plt.savefig('baseline_experimento_accuracy.png', dpi=100, bbox_inches='tight')
plt.close()

print("Graficos generados:")
print("- baseline_experimento_loss.png")
print("- baseline_experimento_accuracy.png")

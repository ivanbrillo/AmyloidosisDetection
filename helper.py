import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot_training_history(history):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Plot losses
    axes[0].plot(history['train_losses'], label='Train Loss')
    axes[0].plot(history['val_losses'], label='Validation Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)

    # Plot F2 scores (both train and val if available)
    if 'train_f2_scores' in history:
        axes[1].plot(history['train_f2_scores'], label='Train F2', color='blue')
    axes[1].plot(history['val_f2_scores'], label='Validation F2', color='green')
    axes[1].set_title('F2 Score')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('F2 Score')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_confusion_matrices(y_true_list, y_pred_list, titles):
    """Plot two confusion matrices side by side"""
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    for i in range(2):
        cm = confusion_matrix(y_true_list[i], y_pred_list[i])
        axes[i].imshow(cm, cmap='Blues')
        axes[i].set_title(titles[i])
        axes[i].set_xlabel('Predicted')
        axes[i].set_ylabel('True')
        for r in range(cm.shape[0]):
            for c in range(cm.shape[1]):
                axes[i].text(c, r, cm[r, c], ha='center', va='center', color='red')
    plt.tight_layout()
    plt.show()

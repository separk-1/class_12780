import torch
from utils import *
from dataloader import load_data
from models import *
import torch.optim as optim
import torch.nn as nn

# Set the Random Seed
set_seed(12780)

# Hyperparameter Setting
batch_size = 1024
learning_rate = 0.001
max_epochs = 20


def train_model(model, train_loader, val_loader, criterion, optimizer, max_epochs, device):
    # TODO 1: Set the model to training mode
    model.train()

    for epoch in range(max_epochs):
        # Training phase
        total_train_loss = 0
        for images, labels in train_loader:
            # TODO 2: Put the Images and labls on the device (Training), hint: see test_model
            images, labels = images.to(device), labels.to(device)

            # TODO 3: Forward pass (training), hint: see test_model
            outputs = model(images)

            loss = criterion(outputs, labels)

            # TODO 4: clears accumulated gradients, hint: optimizer
            optimizer.zero_grad()

            # TODO 5: Backpropogation, hints: loss
            loss.backward()

            # TODO 6: Updates model parameters, , hint: optimizer
            optimizer.step()

            total_train_loss += loss.item()

        # Validation phase
        # TODO 7: Set the model to evaluation mode, hint: see test_model
        model.eval()

        total_val_loss = 0
        with torch.no_grad():  # Disable gradient computation
            for images, labels in val_loader:
                # TODO 8: Put the Images and labls on the device (Validation), hint: see test_model
                images, labels = images.to(device), labels.to(device)
                
                # TODO 9: Forward pass (validation), hint: see test_model
                outputs = model(images)

                loss = criterion(outputs, labels)
                total_val_loss += loss.item()

        # Calculate average losses
        avg_train_loss = total_train_loss / len(train_loader)
        avg_val_loss = total_val_loss / len(val_loader)

        # Print epoch results
        print(f"Epoch [{epoch+1}/{max_epochs}], "
              f"Train Loss: {avg_train_loss:.4f}, "
              f"Validation Loss: {avg_val_loss:.4f}")


def test_model(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad(): # Disable gradient computation
        for images, labels in test_loader:

            # Put the Images and labls on the device (testing)
            images, labels = images.to(device), labels.to(device)
            # Forward pass (testing)
            outputs = model(images)
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"Test Accuracy: {100 * correct / total:.2f}%")

def main():
    # TODO 10: Device Setting, hint: see in class exercise
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Using device: {device}")

    # TODO 11: put the CNN on the device, hint: see models.py
    model = CNN().to(device)
    # model = FullyConnectedNN().to(device)

    # TODO 12: Select a loss function for the multi-classification
    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    train_loader, val_loader, test_loader = load_data()
    
    train_model(model, train_loader, val_loader, criterion, optimizer, max_epochs, device)
    
    test_model(model, test_loader, device)

if __name__ == "__main__":
    main()
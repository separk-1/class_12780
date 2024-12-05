from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset


class FilteredMNIST(Dataset):  
    def __init__(self, root, train=True, transform=None, download=True, include_labels=(0, 1, 2, 3)):
        self.dataset = datasets.MNIST(root, train=train, transform=transform, download=download)
        self.include_labels = include_labels
        self.indices = [i for i, (_, label) in enumerate(self.dataset) if label in self.include_labels]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
        actual_idx = self.indices[idx]
        return self.dataset[actual_idx]

def load_data(batch_size=1024):
    # Data preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    # Filtered dataset
    filtered_dataset = FilteredMNIST(
        root='./data', 
        train=True, 
        transform=transform, 
        include_labels=(0, 1, 2, 3)
    )
    
    dataloader = DataLoader(filtered_dataset, batch_size=batch_size, shuffle=True)
    return dataloader
import torch.nn as nn
    
# Generator Network    
class Generator(nn.Module):
    def __init__(self, latent_dim, img_shape):
        """
        Args:
            latent_dim (int): Size of the latent vector z.
            img_shape (tuple): Shape of the output image, e.g., (1, 28, 28).
        """
        super(Generator, self).__init__()
        self.channels, self.height, self.width = img_shape

        # Linear layer to project latent vector to an initial feature map
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, 128 * 7 * 7),  # Project latent_dim to (128, 7, 7)
            nn.ReLU()
        )

        # Convolutional layers to upsample to (1, 28, 28)
        self.model = nn.Sequential(
            nn.ConvTranspose2d(128, 128, kernel_size=4, stride=2, padding=1),  # (7x7 -> 14x14)
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),  # (14x14 -> 28x28)
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, self.channels, kernel_size=3, stride=1, padding=1),  # Adjust to (1, 28, 28)
            nn.Tanh()  # Normalize output to range [-1, 1]
        )

    def forward(self, z):
        """
        Args:
            z (Tensor): Latent vector of shape (batch_size, latent_dim).
        Returns:
            Tensor: Generated image of shape (batch_size, *img_shape).
        """
        out = self.fc(z)
        out = out.view(out.size(0), 128, 7, 7)  # Reshape to (batch_size, 128, 7, 7)
        img = self.model(out)
        return img

# Discriminator Network
class Discriminator(nn.Module):
    def __init__(self, img_shape):
        """
        Args:
            img_shape (tuple): Shape of the input image (C, H, W), e.g., (1, 28, 28).
        """
        super(Discriminator, self).__init__()
        self.img_shape = img_shape

        self.model = nn.Sequential(
            nn.Conv2d(img_shape[0], 64, kernel_size=4, stride=2, padding=1),  # Downsample: (C, H, W) -> (64, H/2, W/2)
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),          # Downsample: (64, H/2, W/2) -> (128, H/4, W/4)
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            nn.Flatten(),  # Flatten the feature map
            nn.Linear(128 * (img_shape[1] // 4) * (img_shape[2] // 4), 256),  # Fully connected layer
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()  # Output probability
        )

    def forward(self, img):
        """
        Args:
            img (Tensor): Input image tensor of shape (batch_size, C, H, W).
        Returns:
            Tensor: Probability tensor of shape (batch_size, 1).
        """
        return self.model(img)
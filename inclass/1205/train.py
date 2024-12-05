import torch
from utils import *
from dataloader import load_data
from models import *
import torch.optim as optim
from torchvision.utils import save_image
import os

# TODO 0: Set the Device
device = None

latent_dim = 100
img_shape = (1, 28, 28)
batch_size = 64
lr = 0.0002
epochs = 50

# Training function
def train(generator, discriminator, dataloader, optimizer_G, optimizer_D, adversarial_loss, device, latent_dim, epochs):
    os.makedirs("images", exist_ok=True)  # Directory to save generated images
    
    for epoch in range(epochs):
        for i, (imgs, _) in enumerate(dataloader):
            real_imgs = imgs.to(device)
            batch_size = real_imgs.size(0)

            # Train Discriminator
            optimizer_D.zero_grad()

            # TODO 1: Generate Real Labels and Fake Labels, whose shape is (batch_size, 1)
            real_labels = None 
            fake_labels = None 
              
            real_loss = adversarial_loss(discriminator(real_imgs), real_labels)
            
            # TODO 2: Generate Random Noise, whose shape is (batch_size, latent_dim)
            z = None
            # TODO 3: Generate fake images
            fake_imgs = None

            fake_loss = adversarial_loss(discriminator(fake_imgs.detach()), fake_labels)

            d_loss = real_loss + fake_loss
            # TODO 4: Compute the Discriminator Gradient
            None
            # TODO 5: Update the Discriminator Parameters
            None

            # Train Generator
            optimizer_G.zero_grad()
            gen_labels = torch.ones(batch_size, 1).to(device)  # Generator tries to make discriminator output 1
            g_loss = adversarial_loss(discriminator(fake_imgs), gen_labels)

            # TODO 6: Compute the Generator Gradient
            None
            # TODO 7： Update the Generator Parameters
            None

            if i % 100 == 0:
                print(f"[Epoch {epoch}/{epochs}] [Batch {i}/{len(dataloader)}] [D loss: {d_loss.item()}] [G loss: {g_loss.item()}]")

        # Save sample generated images every epoch
        if epoch % 5 == 0 or epoch == epochs - 1:
            fake_imgs = (fake_imgs + 1) / 2  # Rescale to [0, 1]
            save_image(fake_imgs[:25], f"images/epoch_{epoch}.png", nrow=5, normalize=True)
            print(f"Saved images for epoch {epoch}")


# Main function
def main():

    dataloader = load_data(batch_size)

    # Initialize models
    generator = Generator(latent_dim, img_shape).to(device)
    discriminator = Discriminator(img_shape).to(device)

    # Optimizers and loss function
    optimizer_G = optim.Adam(generator.parameters(), lr=lr, betas=(0.5, 0.999))

    # TODO 8: Set discriminator optimizer
    optimizer_D = optim.Adam(None, lr=lr, betas=(0.5, 0.999))
    adversarial_loss = nn.BCELoss()

    # Train the models
    train(generator, discriminator, dataloader, optimizer_G, optimizer_D, adversarial_loss, device, latent_dim, epochs)

if __name__ == "__main__":
    main()
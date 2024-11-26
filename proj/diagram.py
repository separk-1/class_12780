import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Function to add a box
def add_box(ax, x, y, width, height, text, facecolor="white", edgecolor="black", fontsize=10):
    rect = Rectangle((x, y), width, height, facecolor=facecolor, edgecolor=edgecolor)
    ax.add_patch(rect)
    ax.text(x + width / 2, y + height / 2, text, fontsize=fontsize,
            ha='center', va='center', wrap=True)

# Function to add an arrow
def add_arrow(ax, start, end, text=None):
    ax.annotate('', xy=end, xytext=start, arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))
    if text:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, text, fontsize=9, ha='center')

# Create figure and axis
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 20)
ax.set_ylim(0, 12)
ax.axis('off')

# Green boxes for steps and decisions
add_box(ax, 0.5, 9.5, 5, 2, "[Step]\n1) Data collection\n2) Filtering relevant incidents\n3) Text preprocessing\n[Decisions]\n1) Define relevant incidents\n2) Decide stopword list", facecolor="#d5fdd5", edgecolor="black", fontsize=8)
add_box(ax, 14.5, 9.5, 5, 2, "[Step]\n1) Score mapping confidence\n2) Assess mapping suitability\n[Decisions]\n1) Choose algorithm\n2) Set minimum confidence threshold", facecolor="#d5fdd5", edgecolor="black", fontsize=8)
add_box(ax, 14.5, 3, 5, 2, "[Step]\n1) Design visualization algorithms\n2) Create dashboards/graphs\n[Decisions]\n1) Choose visualization method\n2) Configure layout", facecolor="#d5fdd5", edgecolor="black", fontsize=8)

# Main workflow boxes
add_box(ax, 6, 10, 4, 2, "Data Collection and Preprocessing")
add_box(ax, 11, 10, 4, 2, "Preprocessed Text Data")
add_box(ax, 6, 7, 4, 2, "Feature Extraction")
add_box(ax, 11, 7, 4, 2, "Vectorized Feature Data")
add_box(ax, 6, 4, 4, 2, "Classification Model")
add_box(ax, 11, 4, 4, 2, "Incident-Regulation Mapping")
add_box(ax, 6, 1, 4, 2, "Similarity Scoring Algorithm")
add_box(ax, 11, 1, 4, 2, "Visualization Module")
add_box(ax, 16, 1, 4, 2, "User-Friendly Visualization")

# Arrows connecting the workflow
add_arrow(ax, (5.5, 11), (6, 11))  # Raw text -> Preprocessing
add_arrow(ax, (10, 11), (11, 11))  # Preprocessing -> Preprocessed Data
add_arrow(ax, (8, 9), (8, 8))      # Preprocessed Data -> Feature Extraction
add_arrow(ax, (13, 9), (13, 8))    # Feature Extraction -> Vectorized Features
add_arrow(ax, (8, 6), (8, 5))      # Feature Extraction -> Classification Model
add_arrow(ax, (13, 6), (13, 5))    # Classification Model -> Incident Mapping
add_arrow(ax, (8, 3), (8, 2))      # Classification Model -> Similarity Scoring
add_arrow(ax, (13, 3), (13, 2))    # Similarity Scoring -> Visualization Module
add_arrow(ax, (15, 2), (16, 2))    # Visualization Module -> User-Friendly Visualization

# Display the diagram
plt.tight_layout()
plt.show()

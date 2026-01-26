# Digital Humanities Workshop: Computational Analysis of Cultural Heritage Images

![Finnish National Gallery Collection Sample](images/preview/reals.webp)

*Images obtained from the Finnish National Gallery's open access collections via their public API. All images are in the public domain.*

---

## About This Workshop

This practical workshop introduces participants to computational approaches in the digital humanities through the analysis of an image dataset. Drawing inspiration from the concept of "distant reading," the session explores how algorithms can be employed to "read" and interpret collections of visual and cultural data at scale.

Participants will engage directly with the dataset's metadata and image embeddings generated via CLIP (Contrastive Language–Image Pretraining), employing these representations to categorize, cluster, and experiment with various forms of computational sorting and analysis.

The workshop combines conceptual discussion with hands-on exercises, providing an introduction to how machine learning models operationalize notions of similarity, categorization, and meaning in visual data. By reflecting on both the affordances and limitations of such algorithmic readings, the session aims to foster a critical understanding of how computational methods can augment and challenge traditional art-historical and cultural-analytical practices.

---

## Workshop Structure

The workshop consists of two main Jupyter notebooks:

### 1. Working with Cultural Heritage APIs (`01_api_and_data.ipynb`)

Learn how to access and work with open cultural heritage data:

- **Understanding APIs**: What they are and why they matter for DH research
- **Downloading metadata**: Access the Finnish National Gallery's complete collection data
- **Data exploration**: Analyze metadata structure, artists, keywords, and classifications
- **Filtering datasets**: Select artworks by artist, keyword, or other criteria
- **Image acquisition**: Download high-resolution images from the collection

**Key concepts**: RESTful APIs, JSON data formats, metadata standards, data filtering and transformation

### 2. Semantic Image Search with CLIP (`02_clip_semantic_search.ipynb`)

Explore machine learning approaches to understanding visual collections:

- **Introduction to CLIP**: How neural networks connect images and text
- **Semantic search**: Find artworks using natural language queries
- **Understanding embeddings**: How images and text are represented as vectors
- **Cosine similarity**: Measuring similarity between visual and textual concepts
- **Prompt engineering**: Crafting effective search queries
- **Batch processing**: Filter large collections using semantic criteria

**Key concepts**: Neural embeddings, semantic similarity, multimodal machine learning, prompt engineering, computational "reading" of images

---

## Prerequisites

### Technical Requirements

- **Python 3.8+** installed
- **Jupyter Notebook** or **JupyterLab**
- Basic familiarity with Python (variables, loops, functions)
- Command line basics (optional but helpful)

### Hardware

- **Notebook 1 (API & Data)**: Any laptop with internet connection
- **Notebook 2 (CLIP Search)**:
  - **Recommended**: Any laptop (using pre-calculated embeddings)
  - **Optional**: CUDA-capable GPU (for computing embeddings from scratch)

---

## Installation & Setup

### 1. Clone or Download This Repository

```bash
git clone https://github.com/yourusername/DH-Workshop-Uppsala.git
cd DH-Workshop-Uppsala
```

### 2. Install Dependencies

For **Notebook 1** (API & Data):
```bash
pip install requests ipython pillow
```

For **Notebook 2** (CLIP Search):
```bash
pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision pillow numpy tqdm
```

Or install everything at once:
```bash
pip install -r requirements.txt  # (if provided)
```

### 3. Start Jupyter

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and open `01_api_and_data.ipynb` to begin.

---

## Workshop Data

### Finnish National Gallery Collection

This workshop uses the **Finnish National Gallery's** (Kansallisgalleria) open access collection, which includes:

- **Ateneum Art Museum** - Finnish art from the 1750s to the 1960s
- **Museum of Contemporary Art Kiasma** - Contemporary art from 1960 onwards
- **Sinebrychoff Art Museum** - European old masters

The collection metadata is available under a **CC0 1.0 Universal (Public Domain)** license, making it freely available for research, education, and creative projects.

**Collection size**: ~80,000+ artworks with rich metadata including:
- Multilingual titles (Finnish, English, Swedish)
- Artist information
- Dating and provenance
- Subject keywords
- Materials and techniques
- High-resolution images

---

## Directory Structure

```
DH-Workshop-Uppsala/
├── notebooks/
│   ├── 01_api_and_data.ipynb          # API access and data exploration
│   └── 02_clip_semantic_search.ipynb  # CLIP-based semantic search
├── data/
│   ├── objects.json                   # Downloaded collection metadata
│   └── clip_embeddings.npz            # Pre-calculated CLIP embeddings
├── images/
│   ├── preview/                       # Workshop materials
│   └── downloaded/                    # Your downloaded images
├── ARCHIVE/                           # Development notebooks
└── README.md                          # This file
```

---

## Learning Outcomes

By the end of this workshop, participants will be able to:

1. **Access cultural heritage data** programmatically using APIs
2. **Understand and manipulate** JSON metadata structures
3. **Filter and select** subsets of large cultural datasets
4. **Use machine learning models** (CLIP) for semantic image search
5. **Critically evaluate** how algorithms "read" and categorize visual data
6. **Reflect on the affordances and limitations** of computational methods in cultural analysis

---

### Dataset

Finnish National Gallery metadata: **CC0 1.0 Universal (Public Domain)**

Individual artworks may have different copyright status. Always check the `license` field in the multimedia metadata before using images commercially.

### CLIP Model

CLIP is developed by OpenAI and available under the MIT License.

---

## Further Resources

### APIs & Cultural Heritage Data

- [Finnish National Gallery Collections](https://www.kansallisgalleria.fi/en)
- [Europeana](https://www.europeana.eu/) - European cultural heritage portal
- [Rijksmuseum API](https://data.rijksmuseum.nl/object-metadata/api/)
- [Metropolitan Museum API](https://metmuseum.github.io/)

---

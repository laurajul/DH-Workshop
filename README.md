# Digital Humanities Workshop: Computational Analysis of Cultural Heritage Images

![European Cultural Heritage Collections](images/preview/reals.webp)

*Images depicting **Shorelines** obtained from Europeana's aggregated collections via their public API. Europeana provides access to 50+ million digitized items from European museums, galleries, libraries and archives.*

---
**
## About This Workshop

This practical workshop introduces participants to computational approaches in the digital humanities through the analysis of European cultural heritage image collections. Drawing inspiration from the concept of "distant reading," the session explores how algorithms can be employed to "read" and interpret collections of visual and cultural data at scale.

Participants will work with **Europeana's API** and **IIIF (International Image Interoperability Framework)** to access standardized cultural heritage data from across Europe. You'll engage directly with dataset metadata and image embeddings generated via CLIP (Contrastive Language–Image Pretraining), employing these representations to categorize, cluster, and experiment with various forms of computational sorting and analysis.

The workshop combines conceptual discussion with hands-on exercises, providing an introduction to:
- How **IIIF standardizes** access to cultural heritage images across institutions
- How **machine learning models** operationalize notions of similarity, categorization, and meaning in visual data
- How to work with **cross-institutional datasets** spanning European collections

By reflecting on both the affordances and limitations of such algorithmic readings, the session aims to foster a critical understanding of how computational methods can augment and challenge traditional art-historical and cultural-analytical practices.

---

## Workshop Structure

The workshop consists of two main Jupyter notebooks:

### 1. Working with Cultural Heritage APIs: Europeana (`01_europeana_api_and_data.ipynb`)

Learn how to access and work with Europeana's aggregated cultural heritage data:

- **Understanding APIs**: What they are and why they matter for DH research
- **Europeana Search API**: Query 50+ million items from 3,000+ European institutions
- **IIIF Introduction**: Learn about the International Image Interoperability Framework
- **Data exploration**: Analyze EDM (Europeana Data Model) metadata structure
- **Cross-institutional filtering**: Select artworks by artist, country, institution, license
- **IIIF Manifests**: Access standardized image metadata and high-resolution images
- **Image acquisition**: Download images from Europeana's reliable thumbnail service

**Key concepts**: RESTful APIs, JSON data formats, EDM (Europeana Data Model), IIIF Presentation API, IIIF Image API, metadata standards, cross-institutional data aggregation

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

### 3. Get a Free Europeana API Key

1. Visit: https://pro.europeana.eu/page/get-api
2. Register for a free Europeana account
3. Request an API key from your account dashboard
4. Save your key to `misc/api-key-europeana.txt`

```bash
mkdir -p misc
echo "your-api-key-here" > misc/api-key-europeana.txt
```

**Note:** The notebooks include a demo key for testing, but it's limited to 999 requests. For full workshop access, get your own free key.

### 4. Start Jupyter

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and open `01_europeana_api_and_data.ipynb` to begin.

---

## Workshop Data

### Europeana Collections

This workshop uses **Europeana's** aggregated cultural heritage collections, which provide access to:

**Source Institutions:**
- **Rijksmuseum** (Netherlands) - Dutch masters and art history
- **British Library** (UK) - Manuscripts, books, and historical documents
- **Louvre** (France) - European art and antiquities
- **And 3,000+ more** museums, galleries, libraries, and archives across Europe

**Collection Access:**
- **50+ million** digitized items from across Europe
- **Multiple media types**: Images, texts, videos, 3D objects, audio
- **Open data** under various Creative Commons licenses (CC0, CC BY, CC BY-SA, etc.)
- **IIIF-compliant** for many items, providing standardized access

**Rich Metadata** using EDM (Europeana Data Model):
- Multilingual titles and descriptions (20+ European languages)
- Creator/artist information with authority records
- Dating, provenance, and cultural context
- Subject keywords and classifications
- Source institution and location (country)
- Rights and licensing information
- IIIF manifest URLs for high-resolution image access

### IIIF (International Image Interoperability Framework)

Europeana supports **IIIF**, a set of open standards for delivering cultural heritage images:

- **Standardized APIs**: Access images from different institutions using the same protocol
- **IIIF Presentation API**: Manifests containing metadata and image sequences
- **IIIF Image API**: Request images at specific sizes, crops, rotations, and qualities
- **Interoperability**: Compare and analyze images from multiple institutions
- **High resolution**: Access full-resolution images when available from source institutions

---

## Directory Structure

```
DH-Workshop-Uppsala/
├── notebooks/
│   ├── 01_europeana_api_and_data.ipynb  # Europeana API + IIIF access
│   ├── 01_api_and_data.ipynb            # (Alternative: Finnish National Gallery)
│   └── 02_clip_semantic_search.ipynb    # CLIP-based semantic search
├── data/
│   ├── europeana/                       # Europeana search results
│   └── clip_embeddings.npz              # Pre-calculated CLIP embeddings
├── images/
│   ├── europeana/                       # Downloaded Europeana images
│   ├── preview/                         # Workshop materials
│   └── downloaded/                      # Your downloaded images
├── misc/
│   ├── api-key-europeana.txt            # Your Europeana API key (gitignored)
│   ├── README-europeana.md              # Europeana API setup guide
│   └── FINNISH_NATIONAL_GALLERY_STATUS.md  # FNG API issues (Jan 2026)
├── ARCHIVE/                             # Development notebooks
└── README.md                            # This file
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

### Datasets & Licenses

**Europeana Metadata**: Licensed under **CC0 1.0 Universal (Public Domain)**
- All metadata exposed through the Europeana API is freely reusable

**Individual Artworks**: Various licenses depending on source institution
- **CC0**: Public domain, no restrictions
- **CC BY**: Attribution required
- **CC BY-SA**: Attribution + share-alike required
- **CC BY-NC**: Non-commercial use only
- Always check the `rights` field in the API response

**IIIF Manifests**: Generated by Europeana, publicly accessible
- Manifests follow IIIF Presentation API specification
- Available under the same terms as Europeana metadata

**Attribution**: When using Europeana data, acknowledge both:
- Europeana (as the aggregator)
- The source institution (`dataProvider` field)

### CLIP Model

CLIP is developed by OpenAI and available under the MIT License.

---

## Further Resources

### Europeana & IIIF

- **[Europeana Portal](https://www.europeana.eu/)** - Browse 50+ million items
- **[Europeana API Documentation](https://pro.europeana.eu/page/apis)** - Technical documentation
- **[Get Europeana API Key](https://pro.europeana.eu/page/get-api)** - Free registration
- **[IIIF Consortium](https://iiif.io/)** - IIIF specifications and community
- **[IIIF Awesome List](https://github.com/IIIF/awesome-iiif)** - Tools and resources
- **[Europeana IIIF Documentation](https://pro.europeana.eu/page/issue-6-iiif)** - IIIF implementation

### Other Cultural Heritage APIs

- [Rijksmuseum API](https://data.rijksmuseum.nl/) - Dutch national collection with IIIF
- [Metropolitan Museum API](https://metmuseum.github.io/) - American art collection
- [Harvard Art Museums API](https://harvardartmuseums.org/collections/api) - With IIIF support
- [British Library IIIF Collections](https://www.bl.uk/collection-metadata/iiif) - Manuscripts and more

### IIIF Tools & Viewers

- **[Mirador](https://projectmirador.org/)** - IIIF image viewer
- **[Universal Viewer](https://universalviewer.io/)** - Multi-format IIIF viewer
- **[IIIF Curation Viewer](https://github.com/IIIF-Commons)** - Curate and annotate

### Digital Humanities & Machine Learning

- **[CLIP by OpenAI](https://openai.com/research/clip)** - Original paper and implementation
- **[Programming Historian](https://programminghistorian.org/)** - DH tutorials
- **[Distant Viewing Toolkit](https://distantviewing.org/)** - Computer vision for DH

---

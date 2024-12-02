# Master Thesis: Using Machine Learning to Identify Domain Models from Database Structures

## Overview

This repository contains the code and resources for my master thesis, which focuses on using machine learning techniques to identify domain models from database structures. The goal is to facilitate the migration of monolithic or modular architectures to microservice-based architectures by identifying potential microservices.

## Table of Contents

- Overview
- [Project Structure](#project-structure)
- Installation
- Usage
- Methodology
- Results
- Contributing
- License
- Acknowledgements

## Project Structure

```
.
├── adw/
│   ├── adw_columns_analysis.ipynb
│   ├── adw_graph_clustering_random_walk.ipynb
│   └── adw_table_analysis.ipynb
├── wwi/
│   ├── wwi_table_analysis_with_random_walk.ipynb
│   ├── wwi_table_analysis_with_spectral.ipynb
│   └── tables_and_schemas_wwi.csv
├── CCBase/
│   ├── templates/
│   │   ├── form_graph.html
│   │   ├── identify_clusters.html
│   │   ├── perform_clustering.html
│   └── static/
│       └── styles.css
├── database_graph.py
├── README.md
└── requirements.txt
```

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```

2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Flask Application

1. **Set the Flask application environment variable**:
   ```sh
   export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
   ```

2. **Run the Flask application**:
   ```sh
   flask run
   ```

3. **Access the application**:
   Open a web browser and navigate to `http://127.0.0.1:5000/`.

### Running Jupyter Notebooks

1. **Start Jupyter Notebook**:
   ```sh
   jupyter notebook
   ```

2. **Open the desired notebook**:
   Navigate to the 

adw

 or 

wwi

 directory and open the relevant notebook.

## Methodology

The project involves the following steps:

1. **Data Extraction**: Extracting database structures and relationships.
2. **Graph Construction**: Representing the database schema as a graph.
3. **Clustering**: Applying machine learning clustering algorithms to identify domain models.
4. **Visualization**: Visualizing the clustered graphs to interpret the results.
5. **Evaluation**: Evaluating the identified clusters against known domain models.

## Results

The results of the clustering algorithms are visualized and evaluated to determine the effectiveness of the approach in identifying potential microservices. Detailed results and analysis can be found in the respective Jupyter Notebooks.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

I would like to thank my thesis advisor, professors, and colleagues for their support and guidance throughout this project. Special thanks to the open-source community for providing the tools and libraries that made this work possible.

---

Feel free to reach out if you have any questions or suggestions!

---

**Author**: Your Name  
**Email**: your.email@example.com  
**LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/your-profile)

---

This README file provides a comprehensive overview of the project, including installation instructions, usage guidelines, and a summary of the methodology and results. It also includes sections for contributing, licensing, and acknowledgements.

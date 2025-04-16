# UrbEnProfile 

UrbEnProfile is an open-source workflow for generating standardised electricity load profiles for Urban Energy Units (UEUs) in Oldenburg (read this paper for more information about UEU concept https://doi.org/10.1016/j.scs.2023.105075). As input, the code uses categorised urban energy units provided by heatBrain (https://www.heatbrain.eu/). The input dataset is a geopackage with a specific identification of each UEU, its category, the total floor area of the buildings and other building characteristics. The code is also based on data simulated with resLoadSIM, a tool that models the electrical energy demand of buildings and urban areas and produces detailed time-series consumption profiles. IresLoadSIM was used to simulate the energy consumption of the residential buildings of Oldenburg, using the number of buildings and households per urban energy unit as a georeferenced guide. The code can download, pre-process and normalise these datasets, classify UEUs into different categories and organise the data into structured formats. Users can also analyse seasonal patterns, daily variations and annual demand trends using a variety of visualisation and resampling tools. In addition, the code provides descriptive statistics and correlation analysis to help understand and refine energy profiles. 

## Features

- **Bottom-up georeferenced modeling** for classifying and analyzing UEUs
- Automated **data download**, pre-processing, and **normalization** of building-level data
- **Visualization tools** for seasonal, daily, and annual electricity demand trends
- **Statistical and correlation analysis** for refined understanding of energy profiles
- **Research-oriented** structure for reproducible urban energy studies

## Installation

1. **Clone or Download** this repository.
2. **Create a virtual environment** (e.g., conda or venv) to keep dependencies isolated.
3. **Install dependencies** from the `environment.yml` file:

   conda env create -f environment.yml conda activate sogur-env
*(Adjust commands as needed for your environment manager.)*

## Usage and GIS representations

1. Provide the UEU dataset (geopackage) as input.
2. Run the main script/notebook that processes the data and merges it with resLoadSIM outputs.
3. Generate visualizations using the built-in plotting functions to analyze patterns (e.g., daily, seasonal, annual).
   Note: By filtering specific buildings of the UEU dataset, it is see the load profile behaviour of specific georeferenced buildings.

"An Urban Energy Unit (UEU) is a defined geographical area within an existing urban environment, characterized by a distinct set of building features, settlement patterns, and energy demands. Rather than outlining future energy districts, the UEU approach focuses on identifying and grouping these existing urban areas based on shared architectural and infrastructural traits. This allows for the flexible combination of UEUs to form larger, cohesive energy districts, each with its unique boundaries and resource requirements." This concept was developed by Luis Blanco and the participants in the [paper](https://doi.org/10.1016/j.scs.2023.105075).

As an example, a city can be divided by areas belonging to one UEU as represented in the following image of the city of Oldenburg.

![OL_UEUs](https://github.com/user-attachments/assets/e8ad66e0-a6a6-449c-91a1-752a61bb8916)


Then it is also possible to identify which buildings are part of each UEU.

![OL_UEUs_with_Buildings](https://github.com/user-attachments/assets/2a012aab-18c1-4aa4-834d-1b27a424d92b)

## Example Outputs

Below are sample plots that illustrate how electricity demand can be visualized for different timescales and building clusters.

### 1. 24-Hour Period in Winter, Spring, Summer, and Autumn
Shows min, max, and mean demand curves.

![image](https://github.com/user-attachments/assets/59487828-b937-4652-a21a-41a4a2173248)

### 2. Average Daily Demand on Different Days of the Year
Focuses on the mean load profile.

![image](https://github.com/user-attachments/assets/d5ee09c1-864d-4a45-a212-301d3c902412)

### 3. Min, Max, and Mean Yearly Electricity Demand per UEU
Compares demand statistics across different Urban Energy Units.

![image](https://github.com/user-attachments/assets/8912034e-ac3c-4321-bd91-cb582f5c3c46)

### 4. Normalized Hourly Electricity Demand
Depicts how demand evolves hourly throughout the year.

![image](https://github.com/user-attachments/assets/95a5979f-ad57-43b0-bf9c-24df6f4f0c64)

## Project Status & Future Work

- Current focus: **Residential buildings** in Oldenburg
- Future expansions: Integrating more building types or locations, adding more sophisticated calibration, exploring multi-energy systems (heat, electricity, etc.)
- Contributions are welcome to extend functionality or add new modules (see [Contributing](#contributing))

## Contributing

Contributions, issue reports, and feature requests are highly appreciated. Here’s how you can help:

1. **Fork** the repository and create a new branch for your feature or bugfix.
2. **Make changes** in your local environment (remember to update tests/documentation if applicable).
3. **Submit a Pull Request** detailing your proposed updates.

## Authors & Acknowledgments

- **Primary Developer:** Alejandro Zabala Figueroa
- **Collaborators:**  DLR

For more context, see the related research publication:  
[**Link to publication**](https://doi.org/10.1016/j.scs.2024.105967)

## License

MIT [License](https://github.com/AlejoZabala/UrbEnProfile/blob/main/License)

## References

- [Sustainable Cities and Society Journal](https://doi.org/10.1016/j.scs.2023.105075) – UEU concept reference
- [resLoadSIM Documentation](#) – The software is provided on Demand by their Authors at the JRC.
- [heatBrain Project](https://www.heatbrain.eu/)

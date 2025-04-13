# SoGuR
GIS Data-driven analysis of hourly resoluted load profiles of residential buildings

This code provides a comprehensive workflow for generating standardized electricity load profiles for Urban Energy Units (UEUs) in Oldenburg. It relies on data simulated with resLoadSIM, a tool that models electrical energy demand for buildings and urban areas, producing detailed time-series consumption profiles. The code can download, preprocess, and normalize these datasets, classify UEUs into different categories, and organize the data into structured formats. Users can also analyze seasonal patterns, daily variations, and yearly demand trends through a variety of visualization and resampling tools. In addition, the code offers descriptive statistics and correlation analyses, making it easier to understand and refine the energy profiles.

Important note: Before running this code, users must set up a virtual environment to ensure all dependencies are properly installed. This is done by creating a virtual environment and installing the necessary libraries listed in the environment.yml file. This environment isolates the required packages and ensures that the code runs consistently without conflicts from other system libraries.

You can refer to the related research publication for more context and background on this code. The publication is available at: https://doi.org/10.1016/j.scs.2024.105967.

Example of some of the plots that can be created are presented here:

### Plot minimum, maximum and mean electricitiy energy demand in a 24 hours period of a day in Winter, Spring, Summer and Autumn

![image](https://github.com/user-attachments/assets/59487828-b937-4652-a21a-41a4a2173248)

### Plotting of only average day on different days a year
![image](https://github.com/user-attachments/assets/d5ee09c1-864d-4a45-a212-301d3c902412)

### Plot drawing per minimum, maximum and mean yearly electricity energy demand per UEU
![image](https://github.com/user-attachments/assets/8912034e-ac3c-4321-bd91-cb582f5c3c46)

### Plot normalized hourly electricity demand per day during a year
![image](https://github.com/user-attachments/assets/95a5979f-ad57-43b0-bf9c-24df6f4f0c64)

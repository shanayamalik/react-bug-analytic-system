# Enhancing Bug Tracking in React Github using Large Language Models

## Project Overview
React, a popular JavaScript library for building user interfaces, powers numerous web applications worldwide. This project aims to devise a bug tracking and resolution system by leveraging Large Language Models (LLM) analytics. The system uses to closed issues to identify approximately twenty issues similar to user-submitted bugs and then provide relevant data on issue frequency, bug classification, and potential solutions—streamlining the bug resolution process.

## Table of Contents
- [Expected Outcomes](#expected-outcomes)
- [Stages of Design](#stages-of-design)
- [Code Overview](#code-overview)
- [Setup and Usage](#setup-and-usage)
- [Contributing](#contributing)
- [License](#license)

## Expected Outcomes
### Key Goals
- **Bug Analytics with LLM:** Utilize natural language processing to perform in-depth bug analytics.
- **Issue Similarity Identification:** Intelligently analyze user-submitted issues to find similar closed issues.
- **Frequency Analysis:** Measure the frequency of similar issues to prioritize bug fixes.
- **Enhanced Developer Productivity:** Provide developers with valuable analytics for increased productivity.
- **Better User Experience:** Minimize the impact of bugs for a seamless user experience.
- **Efficient Issue Resolution**

## Stages of Design
1. **Data Collection:** Gather bug reports, operator error cases, and relevant data from the software development process.
2. **Preprocessing:** Clean and preprocess the collected data.
3. **Model Selection:** Choose appropriate large language models for analytics tasks.
4. **Testing – Frequency Analysis:** Quantify the occurrence of similar bugs.
5. **Similarity Search:** Use Cosine similarity and L2 (Euclidean) similarity measures.
6. **GitHub Repository:** Host the codebase for the system.
7. **Results:** Showcase the system's capabilities.
8. **Next Steps:** Integrate a debugging component and perform sentiment analysis.

## Code Overview
### Extracting and Embedding Data:
- **Semantic Similarity Calculation:** The code imports a JSON file containing data entries. Each entry has a title and an ID. The titles are encoded into numerical vector representations using the SentenceTransformer package.
- **Cosine Similarity:** Measures the cosine of the angle between two vectors.
- **Euclidean Distance:** Measures the "straight line" distance between two vectors.
- **Store Scores:** The similarity and distance scores for each title are stored in separate lists.

### Data Aggregation and User Interaction:
- **Filtering Results:** The DataFrame is sorted by the similarity score in descending order.
- **User Interaction:** The code interacts with the user to show them similar issues based on the computed similarity scores.

## Setup and Usage
1. Clone the repository
      ```bash
      git clone https://github.com/shanayamalik/react-bug-analytic-system.git
3. Navigate to the project directory
      ```bash
      cd react-bug-analytic-system
5. Install the required packages
     ```bash
      pip install -r requirements.txt
7. Run the main script
      ```bash
      python main.py
9. Follow the on-screen instructions to analyze and track bugs using the system.

## Contributing
Please create a pull request of what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

# OmniBot
A Natural Language AI chatbot that accepts an input problem, categorizes it and solves it by invoking the relevant custom ML model. 

## Project Demo
Short project demo on YouTube - https://youtu.be/3ru1CU8xq4M

## Project Documentation and Poster
- Project Documentation is available [here](https://docs.google.com/document/d/1lO4cFfUmj0LciJELf5P9Y5nMdugfiKDmT5L8v7vtl5Y/edit)
- [Project Poster](https://drive.google.com/file/d/1VYATyNbGKM05yoRlV7AKhgA9t0ni6C6Y/view?usp=share_link)

## Project Motivation
- The motivation for our project is to enhance the usability of NLP-based AI chatbots by enabling a plug-and-play mechanism to add user-defined models for custom problems. 
- Currently, most chatbots are designed to handle specific use cases and have limited functionality.
- They lack the ability to handle more generic use cases and require significant effort to modify or add functionality.
- Our goal is to create a chatbot with a flexible and extensible architecture that can handle a wide range of use cases and be easily customized to add new models.

## Architecture Diagram
![Architecture Diagram](/Images/FinalProjectDiagram.png?raw=true "Architecture Diagram")

## Data Science Pipeline
- Switcher Model
    - Data Collection: A synthetic dataset with 1500 sentences and 5 labels (Audio to Text, Resume Parsing, Blog Summary, Sudoku Solving and Regular Chat) was created by generating 300 variations of each label using GPT.
    - Model Training: Model is an ensemble of three ML models: Naive Bayes, basic Neural Network, and Neural Network with LSTM layer. It redirects user requests based on predictions from the models and requests more information if the models are uncertain.
    - Model Deployment: The model was then saved to disk and imported in the switcher model as a route for resume parsing problems.
    - The data fields are as follow
    ```
        {
            "prompt": "I'm stuck on this Sudoku puzzle. Can you help me out of it?",
            "category": "suduko"
        }
    ```
- Similarly we have built models for different use cases such as 
    - Suduko Solver
    - Resume Parser
- For Article Summary use-case we have used scraping techniques and passed each subsection to GPT3.5 API that returned a summary of that section. Using these summarized sections, we created a summarized article.

## WebApp setup
- Move to UI folder
- run 
```
npm i
npm start
```

## Backend setup
- Backend Code is developed using Django a Python API Framework 
- Move to api_backend
- Start the virtual enviornment
    ```
        source django/bin/activate 
    ```
- Move to backend folder -> omni_bot and start the api server
    ```
        python3 manage.py runserver
    ```
- The path to model files can be checked in the folder
- Currently the backend server is deployed on an EC2 instance

## OmniBot Output
- Resume Summary

![Resume Summary](/Images/ResumeSummary.png?raw=true "Resume Summary")

- Suduko Solver

![Sudoku Solver](/Images/SudokuSolver.png?raw=true "Sudoku Solver")
- Article Summary

![Article Summary](/Images/ArticleSummary.png?raw=true "Article Summary")

- Audio To Text

![Audio To Text](/Images/AudioToText.png?raw=true "Audio To Text")

All the files used for testing in present in the "files" folder
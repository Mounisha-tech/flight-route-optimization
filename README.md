# ✈ Flight Route Optimizer
## A Graph-Based Flight Route Planning System for Indian Domestic Travel 


Live Demo:https://flight-route-optimization-mounisha.streamlit.app/

The Flight Route Optimizer is a web application that finds the optimal flight route between Indian cities using graph algorithms. The system analyzes historical flight data and determines the best route based on price, travel time, or distance.

The application models cities as nodes and flight connections as weighted edges in a graph. Using shortest path algorithms from NetworkX, it computes the most efficient travel route and visualizes it through an interactive Streamlit interface and a geographic map of India.

## Tech Stack 

This project was built using the following technologies:
| Category | Technology |
|--------|--------|
| Programming Language | Python |
| Data Processing | Pandas |
| Graph Algorithms | NetworkX |
| Web Framework | Streamlit |
| Visualization | Plotly, Matplotlib |
| File Handling | OpenPyXL |

## Project Demo

### UI
![UI](screenshots\ui.png)

### Route Visualization
![Route](screenshots\route.png)

### Map Visualization
![Map](screenshots\map.png)

Live Demo:https://flight-route-optimization-mounisha.streamlit.app/


## Dataset 

This project uses a historical dataset of Indian domestic flights containing information about routes,duration, and ticket prices.

Original Dataset Source:
https://github.com/OludolapoAnalyst/Indian_Flight_Data/blob/main/Flight%20Data.xlsx

The dataset was cleaned and processed using Pandas to extract relevant features for route optimization,including:

- source city 
- destination city 
- travel time 
- ticket price
- airport route 
- month of journey 

## Installation and Usage (End Users)

###  Clone the repository 

git clone https://github.com/Mounisha-tech/flight-route-optimization.git

cd flight-route-optimization

### Install dependencies 

pip install -r requirements.txt

### Run the application 
streamlit run app.py

After running this command,the application will open in a browswer at:
http://localhost:8501

Users can then:
1. Select a source city 
2. Selct a destination city 
3. Choose optimization criteria(price,time,distance)
4. Enable Student Vacation Mode(optional)
5. View the optimal route and map visualization

## Installation and Usage (For Contributors)

### Clone the repository 

git clone https://github.com/Mounisha-tech/flight-route-optimization.git

cd flight-route-optimization

### Create a virtual environment
python -m venv flight_env

### Activate the environment

Windows:
flight_env\Scripts\activate

Mac/Linux:
souce flight_env/bin/activate 

### Install dependencies 

pip install -r requirements.txt

### Run the development server

streamlit run app.py

Project Structure:

flight-route-optimizer
│
├── app.py
├── backend.py
├── requirements.txt
├── data/
│   └── Flight Data.xlsx
└── README.md

## Contributor Expectations 

Contributors are welcome to improve this project.

Guidelines:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes 
4. Test the application
5. Submit a Pull Request 

Pull requests should include:
-> clear description
-> tested functionality
-> readable code

## Known Issues 

- The dataset is based on historical flight data and may not reflect real-time flight schedules.
- Map visualization currently supports a limited set of airports 
- Routes may not exist between some city pairs due to dataset limitations 


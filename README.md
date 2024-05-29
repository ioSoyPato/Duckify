# Duckify 🎶

__Project Overview:__

Duckify is a data engineering project aimed at developing an advanced music application that not only plays songs 🎵 but also leverages cutting-edge recommendation models to provide the best song suggestions. This application is designed to enhance the listening experience by using Artificial Intelligence (AI) 🤖 to analyze the current song being played and suggest the most suitable next track.

__In addition to this, the project seeks to demonstrate knowledge in basic application architecture by mixing various programming languages ​​and creating a DockerFile that contains not only the application executable but also the complete language dependencies and libraries so that you can build your own DUCKIFY. For more details on how to build Duckify from the image, I invite you to see my other repository where the creation and execution of it is explained in detail although it is briefly explained and summarized in the README in the releases section.__

## Key Features:

__Intelligent Song Recommendations 🎧:__
- Duckify uses sophisticated recommendation algorithms to analyze the attributes of the currently playing song. Based on this analysis, the application suggests the next song that aligns with the listener's preferences and listening history.

__AI-Driven Enhancements 🤖:__
- The recommendation system ensure the suggestions are highly accurate and personalized. This involves machine learning models that continuously learn from user interactions and feedback to improve the recommendation accuracy over time.

__User-Friendly Interface 🖥️:__
- The application boasts a sleek and intuitive interface designed with HTML, CSS, and JavaScript. This ensures a smooth and enjoyable user experience, making it easy for users to navigate through their music library and discover new tracks.

__Fast and Reliable Backend ⚡:__
- The backend of Duckify is developed using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python. This ensures the application is highly responsive and capable of handling a large volume of requests efficiently.

## Technologies Used:

- FastAPI: For building the backend APIs.
- Python: For implementing the recommendation algorithms and AI models based on GPT-4.
- HTML, CSS, JavaScript: For creating a responsive and user-friendly frontend.

## Project Goals:

- To create an innovative music player that offers more than just playback functionality by integrating advanced recommendation features.
- To enhance user satisfaction by providing personalized and highly relevant song suggestions.
- To leverage AI and machine learning to continuously improve the recommendation system based on user feedback and interaction patterns.

## Releases 
In the __"Releases"__ section you will find an executable Dockerfile that downloads the necessary libraries to run the application and extracts the files from this same repository to run the application on port 4444 of your computer. To correctly use the __Dockerfile__ follow this simple steps:

If you __already have Docker__ running in your computer (Docker version 26.1.3)
- __Download the Dockerfile__ from the releases section on this repository
- Open your terminal and place your self on the directory you pasted the Dockerfile, then run __$ docker build --tag duckify .__
- Once the image is created execute the container with the next command __$ docker run -it duckify__
- The terminal should show the port 4444 as an executable link if it doesn't just open the port on any WebBrowser

If you __don't have Docker__ running in your computer
- Download an execute Docker 👉 https://docs.docker.com/engine/install/

# Some images of the app

Login
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/a1596f10-ce73-41c9-b62f-f6cccde17637)

Home Page
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/e705b0f7-7197-40a0-b78a-1557bfddf87a)


Music Player
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/0b002128-d3e4-4958-8096-eaef55f9f0f9)

Lyrics
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/262f6080-4a59-4b76-b1b4-b56433581b3e)

Rick & Homer __Covers__
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/7f671799-2c9d-48a8-ae5e-33110a0ae3d0)

All Songs
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/bc85a75c-2545-49d2-9840-fed54a28c7cd)
![image](https://github.com/ioSoyPato/Duckify/assets/108914351/d15d36d1-353a-4a72-a647-33bae6abd538)


Playlist Player
__coming soon__








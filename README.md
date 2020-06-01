# Fact-O-Meter



## EU Hackathon Project
This is a Project for the Hackathon [#VsVirus](http://https://www.versusvirus.ch/)

[![Watch the video](https://i.imgur.com/Ttz3xWE.png)](https://www.youtube.com/watch?v=Ljxojs-r_yU)

## ChromeExtension
contains the Source code for the Chrome extension prototype

- Install the Extension following this [tutorial](https://developer.chrome.com/extensions/getstarted#manifest)
- Select some text on a arbitrary Website, right-click it an click "Is this fake-news?" from the drop-down menu
- The response of the neural network get displayed as float value between 0 and 1 meaning fake-news or fact respectively
    
## Webserver 
contains the python webserver with the neural network

- Run with python Version > 3.0
- Dependencies: tensorflow=2.0.0, numpy, pandas, pickle, http.server
- To train the network you need the Global Vectors for Word Representation Dataset: [Dataset](https://www.kaggle.com/terenceliu4444/glove6b100dtxt) and some training data in csv format containing a "text" and a "label" column.
- You may need to change the hostname of the server in the extension to your own server (mine is not running all the time:) )
    

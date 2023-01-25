# BarKan
Code for Computing and Programming Subject at the University of Lucern
Created by: José Saúl Barrientos Rivera and Yassine Kandili

1 :1.1 Register https://api.tiingo.com/ and get you API key
   1.2 To install Shiny for Python, first create a new directory for your first Shiny app, and change to it.

mkdir myapp
cd myapp

  1.3 Next u want to creat a Virtual virtual environment and to activate it
# Create a virtual environment in the .venv subdirectory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
  1.4 Next, install shiny from PyPI.
pip install shiny
2 : Other packages you will need :
    pip install numpy pandas matplotlib pandas_datareader jinja2
(If in Windows) 2.1 : Run as administrator Windows powershell and run the following.
                      "Set-ExecutionPolicy remotesigned" to activate scripts
                      "Set-ExecutionPolicy Default" to go back to Default   
3 : Need to activate the Virtual environment " Venv " in Python's terminal.
 PS C:\Users\unriv\Desktop\project> & c:/Users/unriv/Desktop/project/venv/Scripts/Activate.ps1
 PS C:\Users\unriv\Desktop\project> .\venv\Scripts\Activate.ps1
4 : After the Venv is activated , copy pasta the script provided and run it using  : shiny run --reload app.py ( app.py in this case is the 

                                                                                    python file with the script)

if you are still having trouble here is a link : https://shiny.rstudio.com/py/docs/install.html





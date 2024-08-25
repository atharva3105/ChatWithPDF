# ChatWithPDF

# Project Setup Guide


**Install Python:**
   Ensure that Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/) if it's not already installed.

**Create a Virtual Environment:**
   Open your terminal or command prompt and navigate to your project directory. Run the following command to create a virtual environment:

   ```bash
   py -m venv venv
   ```
   This will create the virtual environment named venv
   To activate the venv 
   
   
   On windows:
   ```
   venv\scripts\activate
   ```
   On MacOs:
   ```
   source venv/bin/activate
   ```
  **Installing Dependencies**
  With your virtual environment activated, install the dependencies listed in requirements.txt by running:
  ``` 
  pip install -r requirements.txt
  ```
### Together AI API Key Setup

**Obtain Your API Key**

1. Go to [Together AI](https://www.together.ai/).
2. Sign up or log in to your account.
3. Navigate to the API section or dashboard to generate or retrieve your API key.

**Create a `.env` File**

1. In your project directory, create a file named `.env` if it doesn’t already exist.
2. Open the `.env` file in a text editor and add the following line:

   ```plaintext
   TOGETHER_API_KEY=your_api_key_here
   ```
## Running a Streamlit App

To run your Streamlit app, follow these steps:

**Ensure Streamlit is Installed:**

   Make sure you have Streamlit installed. If not, you can install it using pip:

   ```bash
   pip install streamlit
   ```
  **Run The App**
  
To Run the streamlit app use the given command 

```
streamlit run app.py
```
  

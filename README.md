# OfficeAgents
Code to automate stock and portfolio analysis

## Analysis Scripts:
0 Clean up for portfolio download excel. 'integrated portfolio analysis'

1  Portfolio Analysis with Perplexity LLM  'query-llm-analysis....'

2  Stub Portfolio Analysis with Open AI LLM 'query-openai-analysis...'

## Scheduler Scripts
Contents (optional)
Scheduler to run the selected scripts locally per schedule  'smart-scheduler.py'
Installer to put the scheduler into the start-up 'smart-installer.py'

## How to get started with this repo
1. install git (put somewhere near c:/ for ease of access)
2. git clone https://github.com/SingingData/OfficeAgents  
3. install miniconda (if you don't already have python locally) https://www.anaconda.com/docs/getting-started/miniconda/install
4. install vscode https://code.visualstudio.com/download
5. get a perplexity api key for yourself here: https://docs.perplexity.ai/guides/api-key-management
6. set up your env file (look at readme for how to) to put your api keys locally in your env file at root level of 'OfficeAgents' to make sure you have files for prompt inputs and your equity list.)
7.  Open VScode and open file 'query-perplexity-llm-stock-analysis.ipynb' from your local copy (from step 2 above).    
8.  Hit 'run all'

## How to set up your .env text file at local root level of your officeagents repo.
### Create a text file at the root level of the local repo.  Retitle it simply .env

### Get your LLM keys and set up local directories as per below.  

### Put the following (with your custom information) in your local .env file that you've just created.
##### Perplexity API Key
PERPLEXITY_API_KEY=put your api key here

##### OpenAI API Key
OPENAI_API_KEY=put your api key here

##### Directory Locations - LLM Queries
Input_dir=C:/directory to your inputs including equity list txt file
Prompt_dir =C:/directory to your prompt input txt files
Output_dir =C:/Users/patty/portfolio_files/Individual_stock_analysis

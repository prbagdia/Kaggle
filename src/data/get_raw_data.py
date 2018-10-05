
import requests
from requests import session
import os
from dotenv import load_dotenv, find_dotenv
import logging

#payload for logging in to kaggle
payload = {
    'action':'login',
    'username': os.environ.get("KAGGLE_USERNAME"),
    'password': os.environ.get("KAGGLE_PASSWORD")
}

def extract_data(url,file_path):
    '''
    extract data from kaggle
    '''
    with session() as c:
        c.post('https://www.kaggle.com/account/login',data=payload)
        
        with open(file_path,'wb') as handle:
            response = c.get(url, stream=True)
            for block in response.iter_content(1024):
                handle.write(block)

            
def main(project_dir):
    '''
    main method
    '''
    #get logger
    logger=logging.getLogger(__name__)
    logger.info("Getting raw data")
    
    #urls
    train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'
    
    #file paths
    raw_data_path = os.path.join(project_dir,'data','raw')
    train_data_path = os.path.join(raw_data_path,'train.csv')
    test_data_path = os.path.join(raw_data_path,'test.csv')
    
    #extract data
    extract_data(train_url,train_data_path)
    extract_data(test_url,test_data_path)
    logger.info("Download complete")
    
if __name__=='__main__':
    #getting root directory
    project_dir=os.path.join(os.path.dirname(__file__),os.pardir,os.pardir)
    
    #setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s -%(message)s'
    logging.basicConfig(level=logging.INFO,format=log_fmt)
    
    #find the env path by walking up and dwon the directories until the env file is found
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    #call the main
    main(project_dir)
    
    

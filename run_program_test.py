import subprocess

def run_program_test():
  publisher = "mqpublisher.py"
  subscriber = "mqsubscriber.py"
  proxy = "proxy.py"
  
  publisher_args = ["python3", publisher]
  subscriber_args = ["python3", subscriber]   
  proxy_args = ["python3", proxy]
  
  publisher_args.append('--test')
  subscriber_args.append('--test')
  proxy_args.append('--test')
  
  publisher_process = subprocess.Popen(publisher_args)
  subscriber_process = subprocess.Popen(subscriber_args)
  proxy_process = subprocess.Popen(proxy_args) 
  
  try:
    publisher_process.communicate()
    subscriber_process.communicate()
    proxy_process.communicate()
    print('Terminating...')
    
  except KeyboardInterrupt:
    publisher_process.terminate()
    subscriber_process.terminate()
    proxy_process.terminate()
  
if __name__ == "__main__":
  run_program_test()
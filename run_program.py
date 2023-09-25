import subprocess

def run_program():
  publisher = "mqpublisher.py"
  subscriber = "mqsubscriber.py"
  proxy = "proxy.py"
   
  publisher_process = subprocess.Popen(["python3", publisher])
  subscriber_process = subprocess.Popen(["python3", subscriber])
  proxy_process = subprocess.Popen(["python3", proxy]) 
  
  try:
    publisher_process.wait()
    subscriber_process.wait()
    proxy_process.wait()

  except KeyboardInterrupt:
    publisher_process.terminate()
    subscriber_process.terminate()
    proxy_process.terminate()
  
if __name__ == "__main__":
  run_program()
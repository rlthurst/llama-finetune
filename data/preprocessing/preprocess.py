# Import the modules
import csv
import glob
import os
import random
import re

def generate_id():
  chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  # Return a string of 8 random characters
  return "".join(random.choice(chars) for _ in range(8))

def txt_to_csv(txt_path, csv_writer):
  filePathRegex = "\/.*?\.[\w:]+"
  delimOnNewMessageRegex = r'\w{3}\s+\d{1,2},\s+\d{4}.*\s*:\s*.*'
  
  with open(txt_path, "r") as txt_file:
    txt = txt_file.read().strip()
    
    parent_id = None
    messageSplit = re.split(delimOnNewMessageRegex, txt)
    for message in messageSplit:
      if not message:
        continue
      
      message = message.strip().split('\n')
      sender = message.pop(0)
      content = "\n".join(message)
      
      # Strip attachment files
      if re.match(filePathRegex, content):
        continue
      # print(": ", content)
      
      message_id = generate_id()
      text = "<sender>" + sender + "</sender>" + content
      csv_writer.writerow([message_id, parent_id, text, sender])
      parent_id = message_id

def raw_directory_to_processed_csv(folder_path, csv_path):
  txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
  txt_files.sort()
  
  with open(csv_path, "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["message_id", "parent_id", "text", "sender"])
    
    for txt_file in txt_files:
      #skip chat files that have only 1 message
      with open(txt_file, "r") as f:
        lines = f.readlines()
        if len(lines) <= 2:
          continue

      txt_to_csv(txt_file, csv_writer)


#if name main
if __name__ == "__main__":

  # get commandline argument data_folder
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--data_folder", type=str, default="data/preprocessing/raw_messages")
  parser.add_argument("--output_folder", type=str, default="data/preprocessing/processed_messages")
  args = parser.parse_args()

  # # Convert the txt files to a csv file
  raw_directory_to_processed_csv(f"{args.data_folder}/train", f"{args.output_folder}/train/train_chats.csv")
  raw_directory_to_processed_csv(f"{args.data_folder}/validation", f"{args.output_folder}/validation/validation_chats.csv")
  
  

# coffee_assistant_backend
This repository is the intellectual property of Will Nearn. It cannot be used without the express written consent of the owner


# Notes
- When making an input file to prep the language model, make sure that all characters are in ASCII. Typically quotes, apostrophes, and bullet points have needed to be replaced. You can open up a file in Python and run it on your input file to check if python can read it:
```python
with open("heavenly_background_information.txt", "rb") as file:  # Open the file in binary mode
    byte_position = 0
    document = ""
    while byte := file.read(1):  # Read byte by byte
        try:
            document = document + byte.decode("cp1252")  # Attempt to decode the byte using 'cp1252'
        except UnicodeDecodeError:
            print(f"Error at byte position: {byte_position}, byte value: {byte}")
            print("\n\nHere's the text that we have so far: \n"+document)
            break  # Exit the loop after finding the problematic byte
        byte_position += 1
```
- Replace the "heavenly_background_information.txt" in the first line with the name of your file
- Save the python file as something like debugger.py in the same folder as your input file
- Open up a command line (Windows) or terminal (Mac)
- Navigate to the folder that holds debugger.py and your input file
  - Type `cd next_folder_here` to go into a folder called next_folder_here
  - Type `dir` (Windows) or `ls` (Mac) to see what the options are
  - Type `pwd` (mac) to see where you are. Windows should already tell you where you are
- Now that you're in the folder that holds debugger.py and your input file, type `python debugger.py` and hit enter.
  - The file will output nothing if the input file is all good
  - The file will output everything that it was able to parse if the input file is bad. Fix the character that comes next!

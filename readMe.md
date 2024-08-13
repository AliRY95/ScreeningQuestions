## Files and Solutions

1. Q1 - Rain probability
    - [Q1.py](https://github.com/AliRY95/Picovoice/blob/main/Q1.py) - Python implementation
    - [Q1.cpp](https://github.com/AliRY95/Picovoice/blob/main/Q1.cpp) - C++ implementation
   
2. Q2 - Phonemas 
    - [Q2.py](https://github.com/AliRY95/Picovoice/blob/main/Q2.py) - Python implementation
    - [Q2.cpp](https://github.com/AliRY95/Picovoice/blob/main/Q2.cpp) - C++ implementation
3. Q3 - Most frequent words
    - [Q3.cpp](https://github.com/AliRY95/Picovoice/blob/main/Q3.cpp) - C++ implementation

4. Q4 - Connectionist temporal classification
    - [CTC/](https://github.com/AliRY95/Picovoice/blob/main/CTC) - The implementation of Q4 as a custom loss function for PyTorch, supporting both forward and backward passes. The CTC forward-backward algorithm was used to calculate the probability and the loss function as well as its gradient. The CTC forward algorithm was implemented based on the functions of [this repository](https://github.com/githubharald/CTCDecoder) and the backward algorithm was similarly implemented using dynamic programing. For testing, ```cd``` to ```/CTC```.
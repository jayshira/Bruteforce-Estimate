# Bruteforce-Estimate
A Python tool to evaluate password strength by estimating how long it would take for modern brute-force methods to crack a password. Additionally, it checks if the password is in a list of commonly used passwords.

## Installation
1.  Ensure you have Python 3.x installed on your system.
2.  Clone the repository:
    ```bash
    git clone https://github.com/jayshira/Bruteforce-Estimate.git
    cd Bruteforce-Estimate
    ```

## Usage
1.  (OPTIONAL, one is provided) Prepare a CSV file `common_passwords.csv` containing common passwords (one password per line).
2.  Run the script:
    ```bash
    python password_check.py
    ```
3.  Enter a password when prompted. The tool will display:
    -   "Instant" if the password is in the common passwords list.
    -   Estimated crack times for different attack scenarios (Basic, Advanced, High-End).

## File Structure
```md
Bruteforce-Estimate/
├── password_check.py               # Main script
├── common_passwords.csv            # Common passwords file
├── README.md                       # This file
└── LICENSE                         # License file
```

## How It Works
1.  **Common Password Check**: The tool compares the input password against a predefined list of common passwords.
2.  **Complexity Analysis**: It calculates the number of possible combinations based on password length and character types.
3.  **Crack Time Estimation**: Using brute-force speeds (attempts per second), it estimates the time required to crack the password.

## Credits
`common_passwords.csv` provided is taken from [Kaggle.com](https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords/data)

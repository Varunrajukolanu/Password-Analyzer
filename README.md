Project: Password Strength Analyzer 🔐

A command-line tool I built in Python to help users understand and improve password security.
This project goes beyond simple length checks by using a powerful library called `zxcvbn` to provide a realistic score for how "guessable" a password is.

Features:

1.Advanced Password Analysis**: Get a password strength score on a clear 1-10 scale.
2.Common Password Check: The tool quickly checks if your password is on a list of over 10,000 common or leaked passwords[cite: 1, 2].
3.Smart Suggestions: If a password is weak, the tool provides simple suggestions to make it stronger.
4.Batch Processing: You can test a whole list of passwords at once from a file.
5.Custom Wordlist Generator: This feature demonstrates a key security concept by creating a list of weak,
  predictable passwords from personal information like a name, a date, or a pet's name.

Installation:

1.Clone the repository(or download the files):
    ```
    	git clone [https://github.com/Varunrajukolanu/Password-Analyzer.git](From google: https://github.com/Varunrajukolanu/Password-Analyzer.git)
    cd password-analyzer
    ```
2.Install the required library:
    ```
    	pip install zxcvbn
    ```

How to Use It:

You'll run the tool from your terminal with a few simple commands.

1.Check a Single Password:

(i).To analyze just one password, use the `-p` or `--password` flag.
```
	python password_analyzer.py -p "MyPassword123!"
```
(ii).To analyze multiple passwords from a File, use the --batch flag with your file's name.

```
	python password_analyzer.py --batch passwords.txt
```
(iii).You can also create a detailed report for your records by adding the --report flag. This will save the output to batch_report.txt.

 ```
	python password_analyzer.py --batch passwords.txt --report
```

2.Generate a Custom Wordlist
To see how easy it is to guess a password from personal info, use this command to create a custom wordlist.
 The tool will save the words to custom_wordlist.txt.
```
	python3 password_analyzer.py --generate_wordlist --name YourName --date YourDate --pet YourPetName
```

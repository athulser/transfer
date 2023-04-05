import os

url = input("Enter a url: ")
string = input("Enter a string: ")
os.system(f'youtube-dl --output "/{string}/file.%(ext)s" --quiet {url}')
print('downloaded')
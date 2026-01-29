import base64

def encryptpass(password):
  encode = base64.b64encode(password.encode())
  print(f"Your encoded password is \'{encode}\' ")

def decodepass(password):
  decode=base64.b64decode(password)
  pass_decode=decode.decode()
  print(pass_decode)

print("What you want")
print("1) Encode Password\n2) Decode password: \n")
chose = input("Enter no: ")

if chose == "1":
    encode_pass=input("Enter password: ")
    encryptpass(encode_pass)
elif chose == "2":
     decode_pass= input('Enter password: ')
     decodepass(decode_pass)
else:
    print("Invalid input!")


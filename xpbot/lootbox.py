import random



out = random.randint(1, 10000)

if out >= 1 and out <= 512: 
    print("you won whitelist!")
elif out >= 513 and out <= 1024: 
    print("You won invites!")
elif out > 1024:
    print("You didn't win anything")

password = "Securep@Ss"

if len(password) < 6:
    strength = "weak"
elif len(password) <= 10:
    strength = "medium"
else:
    strength = "hard"

print("password strength is: ", strength)
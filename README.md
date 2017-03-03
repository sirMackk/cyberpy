# SecretTunnel

Use SSH to quickly transfer secrets using an out-of-band password.

Examples:

```bash
secrettunnel -s < password.txt
Your pin is: 1234

# other machine
secrettunnel joe.local > password.txt
# Asks Joe, face to face, what the pin is.
Enter pin:
Transfer complete!
```

This is a work in progress.

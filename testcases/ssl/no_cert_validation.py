import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context() # CWEID 295
urllib.urlopen("https://no-valid-cert", context=context)

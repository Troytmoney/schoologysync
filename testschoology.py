import schoolopy
# Three-legged
key = 'cfbafa380dc674a7cb1f0f88c9bb8e6b066030100'
secret = 'a715600fbcafee292486455876af32da'
# Two-legged
sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
test = sc.get_feed()  # etc.
print(test)

import sys
import os
import json
import datetime

artifact_name = sys.argv[1]
version = sys.argv[2]

os.popen("cp target/" + artifact_name + "-" + version + ".jar repo/.")

if os.getenv("SOLR_PACKAGE_SIGNING_PRIVATE_KEY_PATH") == None:
    raise Exception("Please add an environment variable SOLR_PACKAGE_SIGNING_PRIVATE_KEY_PATH to point to your private key (.pem) file used for signing the package artifacts.")
    sys.exit(1)

private_key_file = os.getenv("SOLR_PACKAGE_SIGNING_PRIVATE_KEY_PATH")

if (os.path.isfile(private_key_file) == False):
    raise Exception("SOLR_PACKAGE_SIGNING_PRIVATE_KEY_PATH points to non-existent private key (.pem) file used for signing the package artifacts.")
    sys.exit(1)

# Generate a publickey.der file
os.popen("openssl rsa -in "+private_key_file+" -outform DER -pubout -out repo/publickey.der")

# Sign the artifact using the private key
with os.popen("openssl dgst -sha1 -sign "+private_key_file+" repo/"+artifact_name+"-"+version+".jar | openssl enc -base64") as f:
    signature = "".join(f.readlines()).replace("\n", "")
print("Signed artifacts with: " + signature)

# Update the repo/repository.json with the released artifact
repository = json.load(open("repo/repository.json"))

# FORMAT:
#        {
#          "version": "1.0.0",
#          "date": "2019-12-13",
#          "artifacts": [
#            {
#              "url": "question-answering-1.0.jar",
#              "sig": "Hau46QF4424qUDSMwRYa/sO/L4Hfbdr6jLQDEsbJpXJdR6jPmd9v92mAU8wSMO/riVk/Zc4oovCCu2PRWnz7sA=="
#            }
#          ]
#        }

release = {}
release["version"] = version
release["date"] = str(datetime.date.today())
release["artifacts"] = [{"url": artifact_name + "-" + version + ".jar", "sig": signature}]

retainedReleases = []
for i in range(len(repository[0]["versions"])):
    if (repository[0]["versions"][i]["version"] != version):
        retainedReleases.append(repository[0]["versions"][i])
retainedReleases.append(release)
repository[0]["versions"] = retainedReleases

json.dump(repository, open('repo/repository.json', 'w'), indent=2)

print(repository)

import json


if __name__ == '__main__':
    with open('oracle.json') as file:
        oracle = json.load(file)

    with Browser() as browser:

        for server in oracle['servers']:

            for credential in server['credentials']:

                login_url = server['urls']['login']
                vote_url = server['urls']['vote']

                login_and_vote(login_url=login_url, vote_url=vote_url, credential=credential)

import json
from splinter import Browser


def login(url: str, username: str, password: str):
    browser.visit(url)

    browser.fill('username', username)
    browser.fill('password', password)

    browser.find_by_text('Log in').first.click()


def vote(url):
    browser.visit(url)

    browser.find_by_value('Vote on Gtop100 (4k NX)').first.click()
    browser.find_by_value('Vote on UltimatePS (2k NX)').first.click()


if __name__ == '__main__':
    with open('oracle.json') as file:
        oracle = json.load(file)

    with Browser() as browser:

        for server in oracle['servers']:

            for credential in server['credentials']:

                vote(url=server['urls']['vote'])
                login(url=server['urls']['login'], username=credential['username'], password=credential['password'])

import json, subprocess, time

AutoStartRichPresence_config_json_dir = r'C:\Users\user\AppData\Roaming\BetterDiscord\plugins\AutoStartRichPresence.config.json'
github_user = 'your github username'


while True:
    command = f'curl https://api.github.com/users/{github_user}/repos'
    repos = subprocess.run(command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    repos = str(repos.stdout.decode('CP437'))
    repos = json.loads(repos)
    most_recent = {'name': '', 'url': '', 'creation_date': ''}
    for repo in repos:
        # print(repos)
        newdate = time.strptime(str(repo['created_at']), "%Y-%m-%dT%H:%M:%SZ")
        try:
            newdate1 = time.strptime(str(most_recent['creation_date']), "%Y-%m-%dT%H:%M:%SZ")
        except:
            pass
        if most_recent['creation_date'] == '':
            most_recent['name'] = repo['name']
            most_recent['url'] = repo['html_url']
            most_recent['creation_date'] = repo['created_at']
        elif newdate1 < newdate:
            most_recent['name'] = repo['name']
            most_recent['url'] = repo['html_url']
            most_recent['creation_date'] = repo['created_at']
    with open(AutoStartRichPresence_config_json_dir, 'r') as r:
        info = json.load(r)
        if len(most_recent["name"]) > 27:
            most_recent["name"] = str(most_recent["name"])[:20] + '...'
    info['profiles'][0]['state'] = f'recent repo: {most_recent["name"].replace("-", " ")}'
    info['profiles'][0]['button2Label'] = f'Too {most_recent["name"].replace("-", " ")}'
    info['profiles'][0]['button2URL'] = most_recent['url']
    json_object = json.dumps(info, indent=4)
    with open(AutoStartRichPresence_config_json_dir, 'w') as w:
        w.write(json_object)
    time.sleep(300)

import requests

#calligraphy: 1063068


def get_members_json(team_id):
    try:
        response = requests.get(f'https://api2.foldingathome.org/team/1063068/members')
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:\n" + repr(errh))
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the FAH Statistics API occurred:\n" + repr(errc))
        exit()
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:\n" + repr(errt))
        exit()
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:\n" + repr(err))
        exit()
    # Check API response is OK
    if not response:
        print(f'\nQuery failed. API Response = {response.status_code} - ERROR.')
        exit()
    print('Done\n')
    return response.json()

def print_member_info(members_json, margin=2, result_limit=20):

    #https://api.foldingathome.org/uid/2919596/totals
    '''
    Reads team member info from json and prints a table to console.
    Optional margin argument defines column margins (2 characters by default).
    Optional result_limit argument defines maximum number of members to print.
    '''
    # DEBUG MEMBERS_JSON
    # for m_name, m_id, m_rank, m_score, m_wus in members_json:
    #     print(f"Name:{m_name} Id:{m_id}, Rank:{m_rank}, Score:{m_score}, WUs:{m_wus}")
    # print()

    # Calculate table column widths
    max_lengths = {
        'name': 0,
        'id': 0,
        'rank': 0,
        'score': 0,
        'wus': 0
    }
    lengths_checked = 0
    for m_name, m_id, m_rank, m_score, m_wus in members_json:
        if m_name == "name":
            continue
        if lengths_checked >= result_limit:
            break
        if len(m_name) > max_lengths['name']:
            max_lengths['name'] = len(m_name)
        if len(str(m_id)) > max_lengths['id']:
            max_lengths['id'] = len(str(m_id))
        if len(str(m_rank)) > max_lengths['rank']:
            max_lengths['rank'] = len(str(m_rank))
        if len(str(m_score)) > max_lengths['score']:
            max_lengths['score'] = len(str(m_score))
        if len(str(m_wus)) > max_lengths['wus']:
            max_lengths['wus'] = len(str(m_wus))
        lengths_checked += 1
    print(
          f"{str('Rank').rjust(max_lengths['rank'])}{' '*margin}"
          f"{str('Name').ljust(max_lengths['name'])}{' '*margin}"
          f"{str('Score').rjust(max_lengths['score'])}{' '*margin}"
          f"{str('WUs').rjust(max_lengths['wus'])}"
    )
    # Print line under table header
    table_width = margin*3
    for key in ['rank', 'name', 'score', 'wus']:
        table_width += max_lengths[key]
    print('-'*table_width)
    # Print member statistics
    members_printed = 0
    for m_name, m_id, m_rank, m_score, m_wus in members_json:
        if m_name == "name":
            continue
        if members_printed >= result_limit:
            print(f"[...] (List truncated to top {members_printed} members)")
            break
        if m_rank is None:
            m_rank = "-"
        print(
             f"{str(m_rank).rjust(max_lengths['rank'])}{' '*margin}"
             f"{str(m_name).ljust(max_lengths['name'])}{' '*margin}"
             f"{str(m_score).rjust(max_lengths['score'])}{' '*margin}"
             f"{str(m_wus).rjust(max_lengths['wus'])}"
        )
        members_printed += 1

print(get_members_json("1063068"))
# Calvin Choi, Lab 1
# Ho Choi, Lab 1
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody       import safe_open

def print_dict(title:str, d:dict, function=None, reverse=False):
    '''
    function determines which index in tuple that created using dictionary parameter to be sorted.
    reverse determines whether order be reverse or not
    '''
    print("\n"+title)
    for item in sorted([(p,v) for (p,v) in d.items()], key = function, reverse = reverse):
        print("{} -> {}".format(item[0],item[1]))

def read_voter_preferences(resource)->dict:
    '''
    this function will take string for name of file to load
    and create list of each lines removing next line(\n) at the end 
    and split by semicolon (;) 
    then use first element as voters name(key of dict)
    and rest of line will be list of preference (value of dict)
    '''
    result = dict()
    for line in resource.readlines():
        result[line.split(";")[0]] = [a.rstrip("\n") for a in line.split(";")[1:]]
    return result

def evaluate_ballot(voter_pref:dict, remain_cand:set)->dict:
    '''
    receives voter preference(dict) and remaining candidates(set)
    returns dictionary key = candidate ,  value = number of votes. 
    by counting only higher priority vote in list_of_votes union with remain_cand(remain candidates)
    '''
    result = {candidate:0 for candidate in remain_cand if candidate in remain_cand}
    for list_of_votes in voter_pref.values():
        for vote in list_of_votes:
            if vote in remain_cand:
                result[vote] += 1
                break
    return result

def remaining_candidates(d:dict)->set:
    '''
    dict has candidate(str):votes(int)
    creates list of number of votes that each candidates has.
    sort the list to fine least vote 
    create dictionary except the candidate(s) who has least vote
    this will remove all candidates if they have all equal votes(which is least vote)
    '''
    least_vote = sorted(d.values())[0] ## find smallest vote from values in dictionary which is count for vote.
    return {candidate for candidate in d.keys() if d[candidate] != least_vote}
    

if __name__ == "__main__":
    '''
    this main function will ask string to open file and show result of it by looping ballots.
    '''
    
    voter_source = safe_open("Enter file with vote preferences ",'r','Illegal file name')
    voter_pref_dic = read_voter_preferences(voter_source)
    remain_candidate = {candidate for candidates in voter_pref_dic.values() for candidate in candidates} ##generate initial set by storing from all of vote lists.
    print_dict("Voter Preferences",voter_pref_dic, lambda a:a[0])
    for ballot in range(3):
        if(remain_candidate == set() or len([candidate for candidate in remain_candidate]) == 1):
            break
        e_ballot = evaluate_ballot(voter_pref_dic, remain_candidate)
        print_dict("Vote count on ballot #{} with candidates({}) = {}".format(str(ballot+1),"alphabetically",  remain_candidate),e_ballot, lambda a:a[0])
        print_dict("Vote count on ballot #{} with candidates({}) = {}".format(str(ballot+1),"numerical",  remain_candidate),e_ballot,lambda a:a[1],reverse = True) 
        remain_candidate = remaining_candidates(e_ballot)
    print("winner is ", (remain_candidate if remain_candidate != set() else "No one"))
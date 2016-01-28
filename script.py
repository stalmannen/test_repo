#import libraries
import time
import random
import requests
import json

# Set variables and data structures, such as test environment,number of matches and leagues/participants.
test_environment = "http://test03-v1.dev.kambi.com:22180/bo-api-noauth/"
number_of_matches = 4

# Dictionary of league_id : list of [participant_ids].
leagues = {
            "1000094985" : [1000000045,1000000047,1000000072,1000000080,1000000081,1000000082,1000000083,1000000085,1000000086,1000000087,1000000103,1000000137,1000000020,1000000044],

            }

# Dictionary of league_id : league_name
league_names = {
            "1000094985" : "England - Premier league",

            }

# Dictionary of league_id : main betoffer criterion_id
league_criterions = {
            "1000094985" : "1001159858",            # Premier League 1 X 2

}

def get_participants():
    # Returns a league_id and two participants
    participants = []
    random_league = random.randint(0,(len(leagues)-1))                                                  # Select a random league index from the leagues dictionary
    league_from_dictionary = leagues.keys()[random_league]                                              # Get the key for the random league
    list_of_participants = leagues[league_from_dictionary]                                              # Get a list as the value of the previous key
    while len(participants) < 2:                                                                        # While loop to populate a list of 2 participants
        random_participant = random.choice(list_of_participants)
        if random_participant not in participants:
            participants.append(random_participant)
    league_from_dictionary = int(league_from_dictionary)                                                # Cast the league_from_dictionary as an int for returning
    league_and_participants = (league_from_dictionary, participants[0], participants[1])
    return league_and_participants                                                                      # Return a tuple in format (league, participant1, participant2)

def matchtime():
    # Returns a string of the date, one hour from now, in the format "YYMMDD HH:MM"
    match_date = time.strftime("%Y%m%d")
    match_date = match_date[2:]
    match_minute = time.strftime(":%M")
    match_hour = str((int(time.strftime("%H"))+5))
    if (int(match_hour) < 10):
        match_hour = "0" + match_hour
    match_time = str(match_date + ' ' + match_hour + match_minute)
    return match_time

def create_match(league_and_participants, match_time):
    participants_CSV = str(league_and_participants[1]) + ',' + str(league_and_participants[2])
    match_url = test_environment + "event"
    event_payload = {"eventGroupId":league_and_participants[0], "eventTypeId":1, "participantIdListCSVString": participants_CSV, "startDateString": match_time}
    make_match = requests.post(match_url, data=event_payload)
    event_id = make_match.text[6:16]
    if make_match.status_code == 201:
        print "Created a", league_names[str(league_and_participants[0])], " match at time and date ",match_time, "with an event id of ", event_id
        event_and_league = (event_id, league_and_participants[0])
        return event_and_league
    else:
        print ("-" * 15) + " ERROR, something went wrong. (useful, right?)" + ("-" * 15)

def create_betoffer(event_and_league):
    criterion_id = league_criterions[str(event_and_league[1])]
    betoffer_url = test_environment + "betOffer"
    event_id = event_and_league[0]
    betoffer_headers = {
                    "Content-Type": "application/json",
                    "Accept-Encoding": "application/json"
                        }
    body = {
            "eventId": event_id,
            "criterionId": criterion_id,
            "odds1": "2",
            "oddsX": "3",
            "odds2": "4",
            "onSite": "true",
            "liveBetOffer": "false",
            "@type": "THREE_WAY"
            }
    add_betoffer = requests.post(betoffer_url, headers=betoffer_headers, data=json.dumps(body))
    print "1X2 Betoffer for", event_id, "created."

# Run the script as many times as specified
for iteration in range(number_of_matches):
    match_time = matchtime()
    league_and_participants = get_participants()
    create_betoffer(create_match(league_and_participants, match_time))

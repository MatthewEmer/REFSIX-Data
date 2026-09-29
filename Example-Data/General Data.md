##### General Data

"date"

"competition"

"venue"



##### Officials

"officialRole"

"matchOfficials": { "referee", "assistant1" OPTIONAL, "assistant2" OPTIONAL, "fourthOfficial" OPTIONAL, "observer" OPTIONAL } 

"earnings": { "fees", "expenses" } FLOAT POUNDS



#### Teams

"homeTeam"

"homeTeamShort"

"homeColor" HEX



"awayTeam"

"awayTeamShort"

"awayColor" HEX



"players": { "TEAM NAME": \[{ "name", "number" INT, "captain" BOOL, "starting" BOOL, "teamOfficial" OPTIONAL BOOL, "role" OPTIONAL }] }



#### Match Setup

"teamSize" INT



"extraTimeAvailable", "penaltiesAvailable" BOOL



"periodsNo" INT

"timings": { "period1", "period2+" OPTIONAL, "interval1+", OPTIONAL, "sinBinTimerLength" OPTIONAL } INT MINUTES



"withGoalScorers" BOOL

"misconductCodeId" 

"sinBinSystem" - none / *other*



"subOpportunities" BOOL

"subsNo", "subOpportunitiesCount" INT



"keywords": \[]



#### Match Events

"matchEvents": {

&#x20;   	"TIMESTAMP" INT TICKS: { one of the below }



###### Half

"eventName": "Half", "name" 

"kickOffSide" INTEGER

"endMinute" MINUTE

"endTime" ACTUAL TIME TICKS

"isExtraTime" BOOL



###### Other

"eventName"

"half" INT, "minuteOfPlay" MINUTE

"team": { "side" - home/away }

"additionalTime" MINUTES



**Goal**

"ownGoal", "penalty", "freeKick" BOOL



**Incident**

"player": { "captain" BOOL, "name", "starting" BOOL, "number", "teamOfficial" OPTIONAL BOOL, "role" OPTIONAL }

"card" - yellow/red, 

"reason" 

"duringSinBin", "sinBin" BOOL

"playerEntersSinBinTimestamp" OPTIONAL INT TICKS



**Substitution**

"playerOff": { "number" INT, "starting" BOOL, "name", "captain" BOOL }

"playerOn": { "number" INT, "starting" BOOL, "name", "captain" BOOL }



#### Statistics

"matchFinished", "matchAbandoned", "playedExtraTime" BOOL



"stats": {

&#x20;   	"yellow", "red", "goals", "goalsHomeTotal", "goalsAwayTotal", "penaltyShotHomeScored", "penaltyShotHomeMissed", "penaltyShotAwayScored", "penaltyShotAwayMissed" INT

&#x20;   	

&#x20;   	"minutesPlayed": FLOAT MINS

&#x20; 

&#x20;   	"winnerHome", "winnerAway", "winnerDraw" - 0/1



&#x09;"sinBin", "penalties", "speedMax", "speedAverage" NO DATA



&#x20;   	"injuryTimeByHalvesTotal": \[ ] INT CENTISECONDS

&#x20;   	"injuryTimeByThirdsTotal": \[ ] INT CENTISECONDS

&#x20;   	"injuryTimeByQuartersTotal": \[ ] INT CENTISECONDS



&#x20;   	"distanceByHalvesTotal": \[ ] FLOAT METERS

&#x20;   	"distanceByThirdsTotal": \[ ] FLOAT METERS

&#x20;   	"distanceByQuartersTotal": \[ ] FLOAT METERS



&#x20;   	"sprintsHalvesTotal": \[ HIGH, MED, LOW ] INT

&#x20;   	"sprintsThirdsTotal": \[ HIGH, MED, LOW ] INT

&#x20;   	"sprintsQuartersTotal": \[ HIGH, MED, LOW ] INT



&#x20;   	"sprintsByHalvesDistanceTotal": \[

&#x20;   	"sprintsByThirdsDistanceTotal": \[

&#x20;   	"sprintsByQuartersDistanceTotal": \[



&#x20;   "sprintsByHalvesTotal": \[

\[

&#x20;   5

&#x20;   1

&#x20;   0

]

\[

&#x20;   1

&#x20;   2

&#x20;   0

]

&#x20;   ]

&#x20;   "sprintsByThirdsTotal": \[

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

&#x20;   ]

&#x20;   "sprintsByQuartersTotal": \[

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

&#x20;   ]

&#x20;   "sprintsByHalvesDistanceTotal": \[

\[

&#x20;   69.887

&#x20;   11.275

&#x20;   0

]

\[

&#x20;   9.276

&#x20;   37.81399999999999

&#x20;   0

]

&#x20;   ]

&#x20;   "sprintsByThirdsDistanceTotal": \[

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

&#x20;   ]

&#x20;   "sprintsByQuartersDistanceTotal": \[

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

\[

&#x20;   0

&#x20;   0

&#x20;   0

]

&#x20;   ]

&#x20;   "speedCategoryDurations": \[

1242.121

3416.001

906.8779999999999

118.08500000000001

14

5

&#x20;   ]

&#x20;   "speedCategoryDistances": \[

97.484

3150.5169999999944

2353.2110000000016

532.5139999999997

84.726

37.801

&#x20;   ]

&#x20;   "feesTotal": 0

&#x20;   "expensesTotal": 0

&#x20;   "earningsTotal": 0

&#x20;   "earningsAsRefereeTotal": 0

&#x20;   "earningsAsAssistantTotal": 0

&#x20;   "earningsAsFourthOfficialTotal": 0

&#x20;   "earningsAsObserverTotal": 0

&#x20;   "heartRateAverage": 160

&#x20;   "heartRateMax": 182

&#x20;   "heartRate15Mins": \[]

&#x20;   "heartRateZoneDuration": \[

0

87.75

1865.126

2478.999

6

&#x20;   ]

&#x20;   "heartRateZone4And5": 2484.999

&#x20;   "redCardTotal": 0

&#x20;   "yellowCardTotal": 0

&#x20;   "yellowCardByTime": \[]

&#x20;   "yellowCardByHomePlayer": {}

&#x20;   "yellowCardByAwayPlayer": {}

&#x20;   "redCardByHomePlayer": {}

&#x20;   "redCardByAwayPlayer": {}

&#x20;   "yellowCardHomeTotal": 0

&#x20;   "yellowCardAwayTotal": 0

&#x20;   "redCardHomeTotal": 0

&#x20;   "redCardAwayTotal": 0

&#x20;   "yellowCardPositions": \[

0

0

0

0

0

0

0

0

0

&#x20;   ]

&#x20;   "redCardPositions": \[

0

0

0

0

0

0

0

0

0

&#x20;   ]

&#x20;   "yellowCardCodes": {}

&#x20;   "redCardCodes": {}

&#x20;   "sinBinsTotal": 0

&#x20;   "sinBinsMinutesSpent": 0

&#x20;   "sinBinsByTime": \[]

&#x20;   "sinBinsGoalPlayerTeam": 0

&#x20;   "sinBinsGoalOppositeTeam": 0

&#x20;   "gpsCenterPoint": {

"latitude": 51.72829919193328

"longitude": 0.6773973584929263

&#x20;   }

&#x20;   "gpsAvailable": \[

1

1

0

0

&#x20;   ]

&#x20;   "heartRateAvailable": \[

1

1

0

0

&#x20;   ]

&#x20;   "gpsProcessed": 1

&#x20;   "heartRateProcessed": 1

}

"hasTracking": true

"hasHeartRate": true

&#x20;   }


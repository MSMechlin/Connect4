import Server

def Setup():
    result = [{"Name":"","Input":0,"Color":(255,0,0)},  
    {"Name":"",
    "Input":0,
    "Color":(255,0,255)
    }
    ]
    remotegame = int(input('Remote Game?[1:yes,2:no]'))
    if remotegame == 1:
        playerNum = int(input('Player 1 or player 2?')) - 1
        name = input("What is your name?")
        result[playerNum]["Name"] = name
        result[(playerNum+1)%2]["Name"] ="#"
        result[playerNum]["Input"] = 0
        result[(playerNum+1)%2]["Input"] = 1
    else:
        name = input("What is your name player 1?")
        result[0]["Name"] = name
        name = input("What is your name player 2?")
        result[1]["Name"] = name
        result[0]["Input"] = 0
        result[1]["Input"] = 0
    return result


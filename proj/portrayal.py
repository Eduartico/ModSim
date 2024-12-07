def car_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "rect", 
        "Color": "grey", 
        "Layer": 1, 
        "h": 1,
        "w": 1,
        "Filled": "false",
        "text_color": "black",
        "text_size": 1
        }
    
    if type(agent).__name__ == "Spot":
        if agent.spot_type == "Normal":
            portrayal["Color"] = "lightblue"
        elif agent.spot_type == "Electric":
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "lightgreen"
    else:
        portrayal["h"] = 0.4
        portrayal["w"] = 0.6
        if agent.car_type == "Normal":
            portrayal["Color"] = "lightblue"
            portrayal["text"] = ""
        elif agent.car_type == "Electric":
            portrayal["Color"] = "yellow"
            portrayal["text"] = "⚡"
        elif agent.car_type == "Premium":
            portrayal["Color"] = "lightgreen"
            portrayal["text"] = "💸"
        else:
            portrayal["Shape"] = "circle" if agent.parked else "rect"
    
    return portrayal

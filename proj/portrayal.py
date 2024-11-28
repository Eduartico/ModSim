def car_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "rect", 
        "Color": "grey", 
        "Layer": 1, 
        "h": 0.8, 
        "w": 0.6,
        "Filled": "false",
        "text_color": "black",
        "text_size": 1
        }
    
    if type(agent).__name__ == "Spot":
        if agent.spot_type == "Normal":
            portrayal["Color"] = "lightblue"
        elif agent.spot_type == "Electric":
            portrayal["Color"] = "lightgreen"
        else:
            portrayal["Color"] = "yellow"
    else:
        portrayal["h"] = 0.4
        portrayal["w"] = 0.3
        if agent.car_type == "Normal":
            portrayal["Color"] = "blue" if agent.parked else "lightblue"
            portrayal["text"] = "👤"
        elif agent.car_type == "Electric":
            portrayal["Color"] = "green" if agent.parked else "lightgreen"
            portrayal["text"] = "⚡"
        elif agent.car_type == "Premium":
            portrayal["Color"] = "orange" if agent.parked else "yellow"
            portrayal["text"] = "💸"
        else:
            portrayal["Shape"] = "circle" if agent.parked else "rect"
    
    return portrayal

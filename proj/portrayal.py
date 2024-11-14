def car_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "rect", 
        "Color": "grey", 
        "Layer": 1, 
        "h": 0.8, 
        "w": 0.6 , 
        "Filled": "true",
        "text_color": "black",
        "text_size": 10  
        }
    
    
    if agent.car_type == "Normal":
        portrayal["Color"] = "blue" if agent.parked else "lightblue" 
    elif agent.car_type == "Electric":
        portrayal["Color"] = "green" if agent.parked else "lightgreen"
        portrayal["text"] = "E" 
    elif agent.car_type == "Premium":
        portrayal["Color"] = "orange" if agent.parked else "yellow"
        portrayal["text"] = "P" 
    else:
        portrayal["Shape"] = "circle" if agent.parked else "rect"
    
    return portrayal
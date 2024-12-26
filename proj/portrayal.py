from agent import Spot, Car, Type

def parking_lot_portrayal(agent):
    
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
    
    if isinstance(agent, Spot):
        if agent.available:
            if agent.spot_type == Type.NORMAL:
                portrayal["Color"] = "lightblue"
            elif agent.spot_type == Type.ELECTRIC:
                portrayal["Color"] = "lightyellow"
            elif agent.spot_type == Type.PREMIUM:
                portrayal["Color"] = "lightgreen"
                
        else:
            if agent.current_car.car_type == Type.NORMAL:    
                portrayal["Color"] = "blue"
                portrayal["text"] = "N"
            elif agent.current_car.car_type == Type.ELECTRIC:
                portrayal["Color"] = "yellow"
                portrayal["text"] = "⚡"
            elif agent.current_car.car_type == Type.PREMIUM:
                portrayal["Color"] = "green"
                portrayal["text"] = "💸"
    
    elif isinstance(agent, Car):
        portrayal["h"] = 0.8
        portrayal["w"] = 0.6
        if agent.car_type == Type.NORMAL:
            portrayal["Color"] = "blue"
            portrayal["text"] = ""
        elif agent.car_type == Type.ELECTRIC:
            portrayal["Color"] = "yellow"
            portrayal["text"] = "⚡"
        elif agent.car_type == Type.PREMIUM:
            portrayal["Color"] = "lightgreen"
            portrayal["text"] = "💸"
        else:
            portrayal["Shape"] = "circle" if agent.parked else "rect"
    
    return portrayal

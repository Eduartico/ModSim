from agent import Spot, Car, Type

def parking_lot_portrayal(agent):
    
    if isinstance(agent, Spot):
        
        portrayal = {
            "Shape": "rect",
            "Color": "red",
            "Layer": 0,
            "h": 1,
            "w": 1,
            "Filled": "true",
            "text_color": "black",
            "text_size": 1
        }
        
        if agent.spot_type == Type.NORMAL:
            portrayal["Color"] = "lightblue"
        elif agent.spot_type == Type.ELECTRIC:
            portrayal["Color"] = "lightyellow"
        elif agent.spot_type == Type.PREMIUM:
            portrayal["Color"] = "lightgreen"
    
    elif isinstance(agent, Car):
        
        portrayal = {
            "Shape": "rect",
            "Color": "red",
            "Layer": 1,
            "h": 0.8,
            "w": 0.6,
            "Filled": "true",
            "text_color": "black",
            "text_size": 1
        }
        
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

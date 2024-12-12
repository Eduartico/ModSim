from mesa import Agent

# Define the car agent
class Car(Agent):
    def __init__(self, unique_id, model, car_type, created_minute):
        super().__init__(unique_id, model)
        self.car_type = car_type
        self.parked = False
        self.created_minute = created_minute
        self.parked_minute = 0 #TODO
        
        
    def park_car(self):
        self.parked = True
        
    def unpark_car(self):
        self.parked = False
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        
    def set_type(self, car_type):
        self.car_type = car_type
        
    def try_leave(self):
        if self.random() < 0.1:
            self.unpark_car()
    
    def get_type(self):
        return self.car_type
    
    def get_state(self):
        return self.parked
    
    def step(self):
        if not self.parked:
            # Find an empty spot
            empty_parking_spots = [(x, y) for x in range(self.model.grid.width) for y in range(self.model.grid.height)
                                   if self.model.grid.is_cell_empty((x, y))]
            if empty_parking_spots:
                new_position = self.random.choice(empty_parking_spots)
                self.model.grid.move_agent(self, new_position)
                self.parked = True
        else:
            # Decide to leave after a certain time
            # TODO: FAZER ISTO FUNCIONAR, AO INVES DE SE DELETAREM, VAO PARA O MODEL.GRAVEYARD
            # TODO: NAO SER RANDOM, FAZER ALGO QUE A CHANCE AUMENTA CONFORME MODEL.CURRENT_MINUTES - CAR.PARKED_MINUTES AUMENTA
            if self.random.random() < 0.1:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)


# Define the spot agent
class Spot(Agent):
    def __init__(self, unique_id, model, spot_type="Normal"):
        super().__init__(unique_id, model)
        self.spot_type = spot_type
        self.available = True

    def park_car(self):
        self.available = False

    def unpark_car(self):
        self.available = True

    def set_type(self, spot_type):
        self.spot_type = spot_type

    def get_type(self):
        return self.spot_type

    def is_available(self):
        return self.available

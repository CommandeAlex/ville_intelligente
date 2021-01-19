# Definition of Appliance classe


class Appliance:
    def __init__(self):
        # Attributs :
        self.disutility = 0.1   # Prefered Delay
        self.p = 0.0    # Power consumption
        self.list_r = []     # Reservation time
        self.t = 0   # Duration time of an appliance
        self.list_US = []  # Start time of uinterruptible appliance (Not use)
        self.list_S = []  # Operation Time
        self.tau = 0  # end time of appliance

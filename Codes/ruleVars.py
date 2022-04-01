class RuleVars:
    # reservation size cannot exceed the size of a row
    def __init__(self):
        self.pOptimalMiddleSeatsSize = .3 # denotes the optimal size of seats can be assigned in the middle in percentage
        self.pOptimalMidSeatsStartRow = 0.9 # denotes the optimal number of row from where we can start assigning the seats
        self.pOptimalMidSeatsStartCol = 0.1  # denotes the optimal number of col from where we can start assigning the seats
        self.colBuffer = 3
        self.emptyVal, self.assignVal, self.bufferVal = 0, 1, 2
        self.max_reservation_size = 200
        # penalties for the seats for being away from the best seat
        self.up_penalty, self.down_penalty, self.left_penalty, self.right_penalty = 1, 2, 1, 1
        self.pOptimalRowStart, self.pOptimalColStart = 0.9, 0.5

    # here end_index is exclusive
    def get_range_score(self, row_index, start_index, range_len, seats_cumulative_weights=None):
        if not seats_cumulative_weights:
            return row_index * (range_len)
        return seats_cumulative_weights[row_index][start_index + range_len] - seats_cumulative_weights[row_index][start_index]

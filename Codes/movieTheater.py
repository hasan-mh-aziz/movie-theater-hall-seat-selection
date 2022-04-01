from Codes import ruleVars
import collections
import heapq
import math


class MovieTheater:
    def __init__(self, rows=10, cols=20, verbose=False):
        self.seats = [[0] * cols for _ in range(rows)]  # a 2d matrix to hold seat assignment values
        self.rows, self.cols = rows, cols
        self.ruleVars = ruleVars.RuleVars()
        # seat weights for each of the seat based on manhattan distance from the best seat
        self.seat_weights = self.set_seat_weights(verbose)
        self.seats_cumulative_sums = self.set_seats_cumulative_sums(verbose)  # Cumulative seat weights for each row

    # Returns a string representation of the movie theater
    def __str__(self):
        str_representation = ["\n", " " * (self.cols - 2), "SCREEN",  " " * (self.cols - 2), "\n"]

        for i, row in enumerate(self.seats):
            str_representation.append(" ".join(map(str, row)))
            str_representation.append("\n")

        str_representation.append("\n")
        return "".join(str_representation)

    # Populating the seat weights based on modified Manhattan distance
    def set_seat_weights(self, verbose):
        # As the matrix is 0-indexed, we subtracted 1.
        best_row = int(self.rows * self.ruleVars.pOptimalRowStart) - 1
        best_col = int(self.cols * self.ruleVars.pOptimalColStart) - 1
        # the best weight is assigned such a way so that no seat gets a negative weight. Max offset from the best seat
        # will be equal to the sum of row and col size. But the penalty for being away from the best can vary. So, the
        # max penalty for rows and cols are also used to calculate the best seat weight.
        best_seat_weight = self.cols * max(self.ruleVars.left_penalty, self.ruleVars.right_penalty) + \
                           self.rows * max(self.ruleVars.up_penalty, self.ruleVars.down_penalty)
        seat_weights = [[0] * self.cols for _ in range(self.rows)]

        for row_index in range(self.rows):
            row_distance = best_row - row_index
            row_penalty = self.ruleVars.up_penalty if row_distance > 0 else self.ruleVars.down_penalty
            row_base_weight = best_seat_weight - row_penalty * abs(row_distance)
            seat_weights[row_index][:best_col] = [row_base_weight - col_offset * self.ruleVars.left_penalty
                                                  for col_offset in range(best_col, 0, -1)]
            seat_weights[row_index][best_col:] = [row_base_weight - col_offset * self.ruleVars.right_penalty
                                                  for col_offset in range(0, self.cols - best_col)]
            if verbose:
                print(seat_weights[row_index])

        return seat_weights

    def set_seats_cumulative_sums(self, verbose):
        cumulative_sums = [[0] for _ in range(self.rows)]
        for row_index, seats_row_weight in enumerate(self.seat_weights):
            for weight in seats_row_weight:
                cumulative_sums[row_index].append(cumulative_sums[row_index][-1] + weight)

        return cumulative_sums

    # Converts the assigned seats to codes- row index is converted to corresponding alphabet and concatenated with col.
    def get_assigned_seats_codes(self, row_index, start_index, range_len):
        row_char = chr(row_index + 65)
        return [row_char + str(index) for index in range(start_index, start_index + range_len)]

    # check whether all the values in an array can be used as buffer or not
    def check_buffer(self, values):
        return all(map(lambda x: x != self.ruleVars.assignVal, values))

    # Checks whether the selected seats have a clear buffer on all the sides.
    def check_buffers(self, row_index, col_index_start, n_seats):
        end_col_index = col_index_start + n_seats
        col_buffer = self.ruleVars.colBuffer
        left_boundary = col_index_start - col_buffer if col_index_start - col_buffer >= 0 else 0
        right_boundary = end_col_index + col_buffer if end_col_index + col_buffer < self.cols else self.cols

        left_side_valid = self.check_buffer(self.seats[row_index][left_boundary: col_index_start])
        right_side_valid = self.check_buffer(self.seats[row_index][end_col_index: right_boundary])
        upper_row_valid = row_index - 1 < 0
        upper_row_valid |= self.check_buffer(self.seats[row_index - 1][col_index_start: end_col_index])
        lower_row_valid = row_index + 1 >= self.rows
        lower_row_valid |= self.check_buffer(self.seats[row_index + 1][col_index_start: end_col_index])

        return left_side_valid and right_side_valid and upper_row_valid and lower_row_valid

    def get_best_seat_ranges(self, n_seats):
        best_seat_ranges = []
        seats_found = 0

        for row_index in range(0, self.rows):
            row = self.seats[row_index]
            left = 0

            for right in range(self.cols + 1):
                range_len = right - left
                if right != self.cols and row[right] == 0 and range_len < n_seats:
                    continue

                if right > left:
                    seats_found += range_len
                    range_score = self.ruleVars.get_range_score(row_index, left, range_len, self.seats_cumulative_sums)
                    heapq.heappush(best_seat_ranges, (range_score, row_index, left, range_len))

                    range_len_with_min_score = best_seat_ranges[0][3]
                    while seats_found - range_len_with_min_score >= n_seats:
                        heapq.heappop(best_seat_ranges)
                        seats_found -= range_len_with_min_score
                        range_len_with_min_score = best_seat_ranges[0][3]
                left = right + 1

        return heapq.nsmallest(len(best_seat_ranges), best_seat_ranges)[::-1] if seats_found >= n_seats else []

    def assign_seats_start_row_col(self, row_index, col_index_start, n_seats):
        for col_index in range(col_index_start, col_index_start + n_seats):
            self.seats[row_index][col_index] = 1
            if row_index - 1 >= 0:
                self.seats[row_index - 1][col_index] = 2
            if row_index + 1 < self.rows:
                self.seats[row_index + 1][col_index] = 2
        end_col_index = col_index_start + n_seats
        left_side_boundary = col_index_start - self.ruleVars.colBuffer if col_index_start - self.ruleVars.colBuffer >= 0 else 0
        right_side_boundary = end_col_index + self.ruleVars.colBuffer if end_col_index + self.ruleVars.colBuffer < self.cols else self.cols

        self.seats[row_index][left_side_boundary: col_index_start] = [2] * (col_index_start - left_side_boundary)
        self.seats[row_index][end_col_index: right_side_boundary] = [2] * (right_side_boundary - end_col_index)

    def assign_seat_in_middle(self, n_seats):
        start_row = int(self.rows * self.ruleVars.pOptimalMidSeatsStartRow) - 1
        start_col = (self.cols - n_seats) // 2

        for rowIndex in range(start_row, -1, -1):
            row = self.seats[rowIndex]
            valid_row = True
            for colIndex in range(start_col, start_col + n_seats):
                if row[colIndex] != 0:
                    valid_row = False
                    break

            if valid_row:
                self.assign_seats_start_row_col(rowIndex, start_col, n_seats)
                return self.get_assigned_seats_codes(rowIndex, start_col, n_seats)

        return []

    def assign_seat_on_side(self, n_seats):
        start_row = int(self.rows * self.ruleVars.pOptimalMidSeatsStartRow) - 1
        start_col = int(self.cols * self.ruleVars.pOptimalMidSeatsStartCol) - 1

        for rowIndex in range(start_row, -1, -1):
            row = self.seats[rowIndex]
            left, right = start_col, start_col + n_seats - 1

            while left != right and right < self.cols:
                if row[left] != 0:
                    right = left + n_seats
                left += 1

            colIndex = right - n_seats + 1
            if right < self.cols:
                self.assign_seats_start_row_col(rowIndex, colIndex, n_seats)
                return self.get_assigned_seats_codes(rowIndex, colIndex, n_seats)

        return []

    def  assign_seats_in_prats(self, n_seats):
        best_seat_ranges = self.get_best_seat_ranges(n_seats)
        assigned_seats = []
        if len(best_seat_ranges) == 0:
            return assigned_seats

        n_assigned_seat = 0
        for _, rowIndex, start_index, range_len in best_seat_ranges:
            # if seats are assigned for the same group then we can overwrite the buffer places written for that group

            if n_assigned_seat + range_len > n_seats:
                range_len = n_seats - n_assigned_seat
            n_assigned_seat += range_len
            assigned_seats.extend(self.get_assigned_seats_codes(rowIndex, start_index, range_len))
            self.assign_seats_start_row_col(rowIndex, start_index, range_len)

        return assigned_seats

    def assign_seats_by_weight(self, n_seats):
        max_weight_window = []
        max_weight = -math.inf
        for rowIndex in range(0, self.rows):
            row = self.seats[rowIndex]
            left, right = 0, 0
            window_sum = 0
            for right in range(self.cols):
                if row[right] != 0:
                    left = right + 1
                elif right - left + 1 > n_seats:
                    left += 1
                window_sum = self.seats_cumulative_sums[rowIndex][right + 1] - self.seats_cumulative_sums[rowIndex][left]
                if right - left + 1 == n_seats and window_sum >= max_weight:
                    max_weight = window_sum
                    max_weight_window = [rowIndex, left]

        if max_weight_window:
            self.assign_seats_start_row_col(max_weight_window[0], max_weight_window[1], n_seats)
            return self.get_assigned_seats_codes(max_weight_window[0], max_weight_window[1], n_seats)

        return []

    def reserve_seats(self, n_seats):
        if n_seats > self.ruleVars.max_reservation_size:
            return "Requested reservation size exceeds max allowed reservation size."
        assigned_seats = []
        # if n_seats < int(self.cols * self.ruleVars.pOptimalMiddleSeatsSize):
        #     assigned_seats = self.assign_seat_in_middle(n_seats)
        # # if the reservation size is not suitable for assigning at the middle or assigning the seats in the middle
        # # was not successful then we will assign on the sides of the row.
        # if not assigned_seats:
        #     assigned_seats = self.assign_seat_on_side(n_seats)
        assigned_seats = self.assign_seats_by_weight(n_seats)
        if not assigned_seats:
            assigned_seats = self.assign_seats_in_prats(n_seats)

        return ", ".join(assigned_seats)

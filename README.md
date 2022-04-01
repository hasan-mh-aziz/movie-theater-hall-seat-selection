# Seat selection for a movie theater hall

## Assumptions
<ol>
  <li>The number of rows cannot be greater than 26- number of availble single alphabet for a row number.</li>
  <li>The reservation size per request will not exceed number of seats in a row. </li>
  <li>Satisfaction decreases for being away from the best seats, and seating together gives the most satisfaction. </li> 
  <li>Seats on the back and in the middle give more satisfaction to the customers. </li>
  <li>Reservations cannot be changed. </li>
</ol>

## How it works
The algorithm follows the following steps-
<ol>
  <li>Populates the weights of the seats using weighted manhattan distance from the best seat. The best seat is determined by some rule variables from <i>ruleVars.py</i>, which can be changed.</li>
  <li>
    Tries to assign seats by keeping the whole group together. It finds the continuous range of seats in the same row equal to the reservation size with the maximum sum of seat weights in that range.
  </li>
  <li>If the algorithm cannot assign the whole group together, then it looks over all the available ranges and finds out the ranges with the maximum sum of seat weights in the ranges. It prioritizes keeping as many people as together over making one person a lone wolf. For example, for a request of 5, it will mostly assign 4 people together and another person alone instead of assigning them into two groups of 3 and 2.</li>
  <li>After successful seat assignment, the algorithm blocks the buffer seats so that those seats cannot be assigned to future reservation requests.</li>
</ol>

## How to run project
You would need to be in the same directory to the `main.py` to run the script. Also, you would need to keep the other files in the `Codes` directory of the project. Then run the following script in the command line by changing `<input_file_path>` to the directory of your input file-
`python main.py <input_file_path> `

## Future works
<ol>
  <li>Right now, the theater hall is always 10 * 20. But that can be changed easily while creating movie theater objects. So, support for taking the dimension of the movie theater in arguments can be added. </li>
  <li>Support for movie theaters having more than 26 rows. </li>
  <li>Support for requests with reservation size exceeding the number of seats in a row. </li>
  <li>Support for reservations change. </li>
  <li>Support for dynamic group size over assigning as many as people together.</li>
</ol>
  

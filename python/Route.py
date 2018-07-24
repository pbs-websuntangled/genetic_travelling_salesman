import matplotlib.pyplot as plt
import numpy as np
import time
from utils import calculate_rout_distance


class Route:

    def __init__(self, cities):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Route"
        print("Starting", function_name)

        # save the cities
        self.cities = cities

        # generate the random route
        number_of_cities = cities.shape[0]
        self.route = np.random.choice(
            number_of_cities, number_of_cities, replace=False)

        # calculate the distance
        self.calculate_distance()

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def calculate_distance(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Route"
        print("Starting", function_name)

        # go through and calculate the distance
        distance = 0
        first_time_through = True

        for city_index in self.route:

            # if it's the first city then move to the next
            if first_time_through:
                first_time_through = False
                continue

            # calculate the distance
            this_city = self.cities[city_index]
            previous_city = self.cities[city_index - 1]

            distance_step_x = this_city[0] - previous_city[0]
            distance_step_y = this_city[1] - previous_city[1]
            distance_step = (distance_step_x ** 2 +
                             distance_step_y ** 2) ** 0.5

            # accumulate the distance
            distance = distance + distance_step

        # I've done the route, so go back to the beginning
        this_city = self.cities[self.route[0]]
        previous_city = self.cities[self.route[-1]]

        distance_step_x = this_city[0] - previous_city[0]
        distance_step_y = this_city[1] - previous_city[1]
        distance_step = (distance_step_x ** 2 +
                         distance_step_y ** 2) ** 0.5

        # accumulate the distance
        distance = distance + distance_step

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        self.distance = distance


def run_tests(debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "run_tests"
    print("Starting", function_name)

    # set the return code
    return_code = 0

    # create the cities
    grid_size = 10
    number_of_cities = 3
    number_of_axis = 2  # for generating the coordinates
    shape = (number_of_cities, number_of_axis)
    cities = np.random.choice(grid_size, shape)

    # create the routes
    number_of_routes = 20
    routes = []
    for _ in range(number_of_routes):

        route = Route(cities)
        routes.append(route)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    # plt.plot(zip(*[cities[tour[i % 15]] for i in range(16) ])[0], zip(*[cities[tour[i % 15]] for i in range(16) ])[1], 'xb-', );
    # plt.show()

    plt.scatter(cities[:, 0], cities[:, 1])
    plt.show()

    return return_code


if __name__ == '__main__':

    debug = True

    # just make sure that the random numbers generate
    # consistently for testing purposes
    np.random.seed(1)

    # do the run_tests
    return_code = run_tests(debug=debug)

    # final return code
    print("return_code", return_code)

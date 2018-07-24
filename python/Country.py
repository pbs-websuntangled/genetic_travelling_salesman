import matplotlib.pyplot as plt
import numpy as np
import time
from utils import calculate_rout_distance


class Country:

    def __init__(self, number_of_cities, number_of_routes, debug=False):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Country"
        print("Starting", function_name)

        # save the number of cities
        self.number_of_cities = number_of_cities

        # how big is my country
        self.country_size = 10

        # generate the cities with random co-ordinates
        self.create_cities()

        # generate the initial pool of random routes
        self.create_routes

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def create_cities(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "create_cities"
        print("Starting", function_name)

        # create the cities
        number_of_axis = 2  # for generating the coordinates
        shape = (self.number_of_cities, number_of_axis)
        self.cities = np.random.choice(self.country_size, shape)

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def create_routes(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "create_routes"
        print("Starting", function_name)

        # create the routes
        number_of_routes = 20
        routes = []
        for _ in range(number_of_routes):

            route = np.random.choice(
                number_of_cities, number_of_cities, replace=False)
            routes.append(route)

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)


def run_tests(debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "run_tests"
    print("Starting", function_name)

    # set the return code
    return_code = 0

    # create a country
    number_of_cities = 7
    number_of_routes = 20
    debug = True
    country1 = Country(number_of_cities, number_of_routes, debug=debug)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    #plt.plot(zip(*[cities[tour[i % 15]] for i in range(16) ])[0], zip(*[cities[tour[i % 15]] for i in range(16) ])[1], 'xb-', );
    # plt.show()

    plt.scatter(country1.cities[:, 0], country1.cities[:, 1])
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

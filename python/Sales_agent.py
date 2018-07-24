import matplotlib.pyplot as plt
import numpy as np
import time
from utils import calculate_rout_distance
from Route import Route


class Sales_agent:

    def __init__(self, number_of_cities, number_of_routes, debug=False):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Country"
        print("Starting", function_name)

        # save the number of cities
        self.number_of_cities = number_of_cities

        # save the number of routes
        self.number_of_routes = number_of_routes

        # how big is my country
        self.country_size = 10

        # generate the cities with random co-ordinates
        self.create_cities()

        # generate the initial pool of random routes
        self.create_routes()

        # now evolve the routes to find a good one
        self.evolve_routes()

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

    def evolve_routes(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "create_cities"
        print("Starting", function_name)

        # sort the routes
        # To sort the list in place...
        self.routes.sort(key=lambda x: x.distance, reverse=False)

        # store the ranking
        position = 0
        for route in self.routes:

            # save the position
            route.position = position

            # save the fitness (bigger is better)
            route.fitness = 1 - route.distance / self.routes[-1]

            # save the
            # increment the position
            position = position + 1

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
                self.number_of_cities, self.number_of_cities, replace=False)

            route = Route(self.cities)
            routes.append(route)

        # and save them
        self.routes = routes

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
    sales_agent_1 = Sales_agent(
        number_of_cities, number_of_routes, debug=debug)

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

import matplotlib.pyplot as plt
import numpy as np
import time
import copy
from utils import calculate_rout_distance
from Route import Route


class Sales_agent:

    def __init__(self, number_of_cities, number_of_routes, number_of_iterations, debug=False):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Country"
        print("Starting", function_name)

        # save the number of cities
        self.number_of_cities = number_of_cities

        # save the number of routes
        self.number_of_routes = number_of_routes

        # save the number of iterations
        self.number_of_iterations = number_of_iterations

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
        start_time, function_name = time.time(), "evolve_routes"
        print("Starting", function_name)

        # iterate the evolution process
        for iteration in range(self.number_of_iterations):

            # evaluate this set of routes
            self.evaluate_routes()

            # kill the weakest routes
            self.kill_weakest_routes()

            # create offspring

            # mutate the routes
            self.mutate_routes()

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def evaluate_routes(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "evaluate_routes"
        print("Starting", function_name)

        # sort the routes
        self.routes.sort(key=lambda x: x.distance, reverse=False)

        # range of distances
        range_of_distances = self.routes[-1].distance - self.routes[0].distance

        # store the ranking
        position = 0
        for route in self.routes:

            # save the position
            route.position = position

            # save the fitness (bigger is better)
            # the best route has a fitnes of 1
            # other routes are less
            route.fitness = 1 - (route.distance -
                                 self.routes[0].distance) / range_of_distances

            # increment the position
            position = position + 1

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def kill_weakest_routes(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "kill_weakest_routes"
        print("Starting", function_name)

        # generate the set of random numbers in one hit
        death_tokens = np.random.rand(self.number_of_routes)

        # now check fitness against the death token
        # kill if it's less
        # by not copying it over to new list
        new_routes = []
        for route_index, route in enumerate(self.routes):

            # is it fit enough?
            danger = death_tokens[route_index]
            if danger < route.fitness:

                # this route survives!!
                new_routes.append(self.routes[route_index])

        # replace the routes
        self.routes = new_routes

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        return

    def mutate_routes(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "kill_weakest_routes"
        print("Starting", function_name)

        # creates new routes that are mutations of the existing routes
        # a single mutation is achieved by swapping a pair of randomly chosen cites
        # first it choses how many pairs to swap in that route
        # the lower the fitness, the more mutations will be created
        # within that one journey

        # what's the maximum number of mutations per route
        maximum_mutations_per_route = max(2, int(0.1 * self.number_of_cities))
        minimum_mutatations_per_route = 1

        # generate the set of random numbers in one hit
        death_tokens = np.random.rand(self.number_of_routes)

        # now check fitness against the death token
        # kill if it's less
        # by not copying it over to new list
        new_routes = []
        for route_index, route in enumerate(self.routes):

            # first let's choose an amount of mutations
            # there will be a minimum and a maximum with inbetweens a
            # function of the inverse fitness
            if self.routes[route_index].fitness == 0:
                number_of_mutations = maximum_mutations_per_route
            else:
                number_of_mutations = min(minimum_mutatations_per_route, int(
                    maximum_mutations_per_route * 1 / self.routes[route_index].fitness))

            # create a copy and put it onto the  end of the list
            if len(self.routes) < self.number_of_routes:

                # put a copy of this one on the end
                self.routes.append(route.mutate_route(number_of_mutations))

            else:

                # I already have the amount of routes that I want so get out
                return

            # now recalculate the distance for that mutated route
            self.routes[route_index].calculate_distance()

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        return

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
        number_of_cities, number_of_routes, number_of_iterations=5, debug=debug)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    # plt.plot(zip(*[cities[tour[i % 15]] for i in range(16) ])[0], zip(*[cities[tour[i % 15]] for i in range(16) ])[1], 'xb-', );
    # plt.show()

    plt.scatter(sales_agent_1.cities[:, 0], sales_agent_1.cities[:, 1])
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

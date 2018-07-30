import matplotlib.pyplot as plt
import numpy as np
import copy
import time
from utils import calculate_rout_distance


class Route:

    def __init__(self, cities):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "__init__Route"
        print("Starting", function_name)

        # save the cities
        self.cities = cities

        # create slot for fitness
        self.fitness = ""

        # create slot for provenance
        self.provenance = ""

        # generate the random route
        # home city is always 0
        self.number_of_cities = cities.shape[0]
        self.route = np.random.choice(
            self.number_of_cities, self.number_of_cities, replace=False)

        # get the index of the route element where the home city (0) is
        index_of_zero = np.where(self.route == 0)[0][0]

        # replace the value at that index with the contents of route[0]
        # and the home city with zero
        self.route[index_of_zero] = self.route[0]
        self.route[0] = 0

        # calculate the distance
        self.calculate_distance()

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

    def calculate_distance(self):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "calculate_distance"
        print("Starting", function_name)

        # go through and calculate the distance
        distance = 0
        first_time_through = True
        persistent_previous_city_index = 0

        for city_index in self.route:

            # if it's the first city then move to the next
            if first_time_through:
                first_time_through = False
                persistent_previous_city_index = city_index
                continue

            # calculate the distance
            this_city = self.cities[city_index]
            previous_city = self.cities[persistent_previous_city_index]

            distance_step_x = this_city[0] - previous_city[0]
            distance_step_y = this_city[1] - previous_city[1]
            distance_step = (distance_step_x ** 2 +
                             distance_step_y ** 2) ** 0.5

            # accumulate the distance
            distance = distance + distance_step

            # update the pevious city index
            persistent_previous_city_index = city_index

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

    def mutate_route(self, number_of_city_pairs_to_swap):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "mutate_route"
        print("Starting", function_name)

        # Randomly swaps n pairs of cities in a copy of the
        # route and returns that copy to the caller

        # so take a copy
        copy_of_route = copy.deepcopy(self)

        # generate the set of city indices in one hit
        city_indices = np.random.rand(
            number_of_city_pairs_to_swap, 2) * (copy_of_route.number_of_cities - 1) + 1  # make sure it's not zero
        city_indices = city_indices.astype(int)

        # now loop through the mutations and swap the cities
        for mutation_index in range(number_of_city_pairs_to_swap):

            # temp
            swapper = copy_of_route.route[city_indices[mutation_index][0]]

            copy_of_route.route[city_indices[mutation_index][0]
                                ] = copy_of_route.route[city_indices[mutation_index][1]]

            copy_of_route.route[city_indices[mutation_index][1]] = swapper

        # now recalculate the distance for that mutated route
        copy_of_route.calculate_distance()

        # update provenace to show it's come from a mutation
        self.provenance = self.provenance + "Mutation,"

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        return copy_of_route

    def procreate_route(self, partner):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "procreate_routes"
        print("Starting", function_name)

        # Takes segments from the self route and inserts them into
        # a copy of the partner route

        # do all the stuff here about inserting the segments

        # The one with the lowest fitness is the father
        if self.fitness > partner.fitness:
            mother = self
            father = partner
        else:
            mother = partner
            father = self

        # Choose how much of each parent to take based on
        # fitness of each.
        fathers_contribution_to_route = father.fitness / \
            (father.fitness + mother.fitness)

        # so take a copy
        child = copy.deepcopy(mother)

        # an array of all the insertions
        insertions = []

        # calculate how many insertions there will be
        number_of_insertions = int(0.5 *
                                   fathers_contribution_to_route * self.number_of_cities)

        # create a np array of the indices to use (or cities??)
        # cities i think
        # it contains an array of the 1st cities in the sequence of two
        # cities from the fathers sequence to be inserted
        # into the mother's sequence
        insertions = np.random.choice(
            self.number_of_cities, number_of_insertions, replace=False)

        # get the indices of values in the fathers route that are in the insertions
        indices_of_insertions_from_father_1st = np.isin(
            father.route, insertions)

        # create a copy of shifted indices by using roll
        indices_of_insertions_from_father_2nd = np.roll(
            indices_of_insertions_from_father_1st, 1)

        # now add the dhifted and unshifted together to give me a map of all
        # the elements in the fathers that are to be replaces
        t = indices_of_insertions_from_father_1st + \
            indices_of_insertions_from_father_2nd

        cities_to_be_replaced_all = father.route[t]
        cities_to_be_replaced_1st = father.route[indices_of_insertions_from_father_1st]
        cities_to_be_replaced_2nd = father.route[indices_of_insertions_from_father_2nd]

        # get the indices of values in the mothers route that are in the insertions
        # these must not be transferred over from the mother
        indices_of_insertions_from_mother = np.isin(
            mother.route, cities_to_be_replaced_all)

        # an array to hold the offspring route
        new_route = [0]  # the first city is always 0

        for route_index in range(self.number_of_cities - 1):

            # skip over the first as it's already there
            # yes, it's inefficvient, optimise later
            if route_index == 0:
                continue

            try:
                element_to_be_replaced = mother.route[route_index]
            except:
                you_can_break_here = True

            # see if this element in the mothers route is to be replaced
            # correct but needs to have truth for both elements, not just first
            if indices_of_insertions_from_mother[route_index] == True:

                # only transfer from the fathers route if it's the first
                # one of the pair
                if element_to_be_replaced in cities_to_be_replaced_1st:

                    # get the index of this element in the fathers route
                    index_of_insertion_from_father = np.where(
                        father.route == element_to_be_replaced)[0][0]

                    # if the index is for the last item, put all the rest from the mother
                    # into the child, then add this onto the end
                    if (index_of_insertion_from_father == self.number_of_cities - 1) or (index_of_insertion_from_father == self.number_of_cities - 2):

                        for index in range(route_index + 1, self.number_of_cities):

                            # check the item has not already been added
                            if mother.route[index] not in new_route:

                                # it's not already there so add it at the end
                                new_route.append(mother.route[index])

                        # so, was it the last, or one from last?
                        if (index_of_insertion_from_father == self.number_of_cities - 1):

                            if element_to_be_replaced not in new_route:
                                # all added from mother so now add the last city from the father
                                new_route.append(element_to_be_replaced)
                        else:

                            # all added from mother so now add the last city from the father
                            if element_to_be_replaced not in new_route:
                                new_route.append(element_to_be_replaced)

                            # now the last one
                            if father.route[-1] not in new_route:
                                new_route.append(father.route[-1])

                        # so finish the loop
                        break

                    else:
                        # it has to be inserted from the father and
                        # it's not the last element
                        # so add this one and the next from the father
                        if element_to_be_replaced not in new_route:
                            new_route.append(element_to_be_replaced)
                        element_to_be_replaced = father.route[index_of_insertion_from_father + 1]
                        if element_to_be_replaced not in new_route:
                            new_route.append(element_to_be_replaced)

                        # while the last element of the new route is in the first set,
                        # add the second one
                        while new_route[-1] in cities_to_be_replaced_1st:

                            # it's possible to land here if the last city in the father
                            # route is due to be inserted
                            # test fo that
                            if new_route[-1] == father.route[-1]:
                                break

                            # find where in the father it comes from and add the next one needed
                            # get the index of this element in the fathers route
                            index_of_insertion_from_father = np.where(
                                father.route == new_route[-1])[0][0]

                            # now get the city that is next to that in the fathers
                            # route and add it to the new route
                            try:
                                element_to_be_replaced = father.route[index_of_insertion_from_father + 1]
                            except:
                                you_can_break_here = True

                            if element_to_be_replaced not in new_route:
                                new_route.append(element_to_be_replaced)

            else:

                # This city in the route from the mother is not in the list
                # of insertions so it should be replicated in the child
                # (as long as it hasn't already been contrinuted by the father)
                if element_to_be_replaced not in new_route:
                    new_route.append(element_to_be_replaced)

        # now replace the route in the child
        child.route = np.asarray(new_route)

        # now recalculate the distance for that child route
        child.calculate_distance()

        # update provenace to show it's come from a mutation
        child.provenance = mother.provenance + "Child,"

        # allow break if it's not correct length
        if child.route.shape[0] != self.number_of_cities:
            you_can_break_here = True

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        return child

    def procreate_route_old(self, partner):

        # start a timer because it's a long process!!
        start_time, function_name = time.time(), "procreate_routes"
        print("Starting", function_name)

        # Takes segments from the self route and inserts them into
        # a copy of the partner route

        # do all the stuff here about inserting the segments

        # The one with the lowest fitness is the father
        if self.fitness > partner.fitness:
            mother = self
            father = partner
        else:
            mother = partner
            father = self

        # Choose how much of each parent to take based on
        # fitness of each.
        fathers_contribution_to_route = father.fitness / \
            (father.fitness + mother.fitness)

        # so take a copy
        child = copy.deepcopy(mother)

        # the logic here is insufficient
        # If there are two inswrtion pairs like this 4,7   and 7,8
        # and in the mothers route it hits the 4, then it will correctly
        # put the 7 after it but then not look to see if that is something that should be replaced

        # an array of all the insertions
        insertions = []

        # calculate how many insertions there will be
        number_of_insertions = int(0.5 *
                                   fathers_contribution_to_route * self.number_of_cities)

        # create a np array of the indices to use (or cities??)
        # cities i think
        # it contains an array of the 1st cities in the sequence of two
        # cities from the fathers sequence to be inserted
        # into the mother's sequence
        insertions = np.random.choice(
            self.number_of_cities, number_of_insertions, replace=False)

        # get the indices of values in the fathers route that are in the insertions
        indices_of_insertions_from_father_1st = np.isin(
            father.route, insertions)

        # create a copy of shifted indices by using roll
        indices_of_insertions_from_father_2nd = np.roll(
            indices_of_insertions_from_father_1st, 1)

        # now add the dhifted and unshifted together to give me a map of all
        # the elements in the fathers that are to be replaces
        t = indices_of_insertions_from_father_1st + \
            indices_of_insertions_from_father_2nd

        cities_to_be_replaced_all = father.route[t]
        cities_to_be_replaced_1st = father.route[indices_of_insertions_from_father_1st]
        cities_to_be_replaced_2nd = father.route[indices_of_insertions_from_father_2nd]

        # get the indices of values in the mothers route that are in the insertions
        # these must not be transferred over from the mother
        indices_of_insertions_from_mother = np.isin(
            mother.route, cities_to_be_replaced_all)

        # an array to hold the offspring route
        new_route = [0]  # the first city is always 0

        for route_index in range(self.number_of_cities - 1):

            # skip over the first as it's already there
            # yes, it's inefficvient, optimise later
            if route_index == 0:
                continue

            try:
                element_to_be_replaced = mother.route[route_index]
            except:
                you_can_break_here = True

            # see if this element in the mothers route is to be replaced
            # correct but needs to have truth for both elements, not just first
            if indices_of_insertions_from_mother[route_index] == True:

                # only transfer from the fathers route if it's the first
                # one of the pair
                if element_to_be_replaced in cities_to_be_replaced_1st:

                    # get the index of this element in the fathers route
                    index_of_insertion_from_father = np.where(
                        father.route == element_to_be_replaced)[0][0]

                    # if the index is for the last item, put all the rest from the mother
                    # into the child, then add this onto the end
                    if (index_of_insertion_from_father == self.number_of_cities - 1) or (index_of_insertion_from_father == self.number_of_cities - 2):

                        for index in range(route_index + 1, self.number_of_cities):

                            # check the item has not already been added
                            if mother.route[index] not in new_route:

                                # it's not already there so add it at the end
                                new_route.append(mother.route[index])

                        # so, was it the last, or one from last?
                        if (index_of_insertion_from_father == self.number_of_cities - 1):

                            if element_to_be_replaced not in new_route:
                                # all added from mother so now add the last city from the father
                                new_route.append(element_to_be_replaced)
                        else:

                            # all added from mother so now add the last city from the father
                            if element_to_be_replaced not in new_route:
                                new_route.append(element_to_be_replaced)

                            # now the last one
                            if father.route[-1] not in new_route:
                                new_route.append(father.route[-1])

                        # so finish the loop
                        break

                    else:
                        # it has to be inserted from the father and
                        # it's not the last element
                        # so add this one and the next from the father
                        if element_to_be_replaced not in new_route:
                            new_route.append(element_to_be_replaced)
                        element_to_be_replaced = father.route[index_of_insertion_from_father + 1]
                        if element_to_be_replaced not in new_route:
                            new_route.append(element_to_be_replaced)

                        # while the last element of the new route is in the first set,
                        # add the second one
                        while new_route[-1] in cities_to_be_replaced_1st:

                            # it's possible to land here if the last city in the father
                            # route is due to be inserted
                            # test fo that
                            if new_route[-1] == father.route[-1]:
                                break

                            # find where in the father it comes from and add the next one needed
                            # get the index of this element in the fathers route
                            index_of_insertion_from_father = np.where(
                                father.route == new_route[-1])[0][0]

                            # now get the city that is next to that in the fathers
                            # route and add it to the new route
                            try:
                                element_to_be_replaced = father.route[index_of_insertion_from_father + 1]
                            except:
                                you_can_break_here = True

                            if element_to_be_replaced not in new_route:
                                new_route.append(element_to_be_replaced)

            else:

                # This city in the route from the mother is not in the list
                # of insertions so it should be replicated in the child
                # (as long as it hasn't already been contrinuted by the father)
                if element_to_be_replaced not in new_route:
                    new_route.append(element_to_be_replaced)

        # now replace the route in the child
        child.route = np.asarray(new_route)

        # now recalculate the distance for that child route
        child.calculate_distance()

        # update provenace to show it's come from a mutation
        child.provenance = mother.provenance + "Child,"

        # allow break if it's not correct length
        if child.route.shape[0] != self.number_of_cities:
            you_can_break_here = True

        # timer because it's a long process!!
        print("Leaving",
              function_name,
              "and the process took",
              time.time() - start_time)

        # and out of here
        return child


def run_tests(debug=False):

    # start a timer because it's a long process!!
    start_time, function_name = time.time(), "run_tests"
    print("Starting", function_name)

    # set the return code
    return_code = 0

    # create the cities
    grid_size = 100
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

    if 24.729611 == round(routes[0].distance, 6):
        print("Test for route distance  - passed")
        return_code = 0
    else:
        print("Test for route distance - failed")
        return_code = 4

    # test route mutation
    # 300 should leave it 0,2,1 which is swapped
    mutated_route = route.mutate_route(300)

    # did the test work?
    if mutated_route.route[1] != route.route[1]:
        print("Test for route distance  - passed")
        return_code = 0
    else:
        print("Test for route mutation - failed")
        return_code = 4

    # test the route procreation
    # create the cities
    grid_size = 100
    number_of_cities = 6
    number_of_axis = 2  # for generating the coordinates
    shape = (number_of_cities, number_of_axis)
    cities = np.random.choice(grid_size, shape)

    father = Route(cities)
    mother = Route(cities)
    father.fitness = 0.34
    mother.fitness = 0.66
    child = father.procreate_route(mother)

    # timer because it's a long process!!
    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    # and out of here

    plt.scatter(cities[:, 0], cities[:, 1], c="red", s=100)
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

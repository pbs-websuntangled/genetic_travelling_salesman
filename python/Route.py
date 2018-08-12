import scipy.ndimage
import matplotlib.pyplot as plt
import numpy as np
import copy
import time
from utils import calculate_rout_distance
from colours import get_colour
import cv2
import os


class Route:

    def __init__(self, cities, name, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "__init__" + "Route"
            print("Starting", function_name)

        # save the cities
        self.cities = cities

        # create slot for fitness
        self.fitness = ""

        # create slot for name
        self.name = name

        # create slot for provenance
        self.provenance = []

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
        self.calculate_distance(debug=debug)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def calculate_distance(self, debug=False):

        if debug:
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
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        self.distance = distance

    def visualise_provenance(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "visualise_provenance"
            print("Starting", function_name)

        legend = {}

        legend["Survivor"] = {}
        legend["Survivor"]["colour"] = get_colour("light grey")

        legend["Child"] = {}
        legend["Child"]["colour"] = get_colour("lime green")

        legend["Child Mother Reversed"] = {}
        legend["Child Mother Reversed"]["colour"] = get_colour("green")

        legend["Child Father Reversed"] = {}
        legend["Child Father Reversed"]["colour"] = get_colour("green")

        legend["Leaked from"] = {}
        legend["Leaked from"]["colour"] = get_colour("orange")

        legend["Mutation"] = {}
        legend["Mutation"]["colour"] = get_colour("violet")

        # create a blank legend image

        legend_visualisation_line_space = 100
        legend_visualisation_line_thickness = int(
            legend_visualisation_line_space / 10)
        legend_visualisation_height = (
            len(legend) + 1) * legend_visualisation_line_space
        legend_visualisation_height = legend_visualisation_height
        golden_ratio = 1.61803398875

        legend_visualisation_width = int(
            legend_visualisation_height * golden_ratio)
        legend_visualisation = np.zeros(
            (legend_visualisation_height, legend_visualisation_width, 3)) + 255
        legend_visualisation_line_length = legend_visualisation_line_space * 3
        text_font = cv2.FONT_HERSHEY_DUPLEX

        text_colour = (0, 0, 0)

        # loop through each of the legend entries and draw the line with description
        for entry_index, entry in enumerate(legend):

            colour = legend[entry]["colour"]["bgr"]
            point_1 = (legend_visualisation_line_space, (entry_index + 1)
                       * legend_visualisation_line_space)
            point_2 = (legend_visualisation_line_length, (entry_index + 1)
                       * legend_visualisation_line_space)

            text_point = point_2[0] + \
                legend_visualisation_line_space, point_2[1]
            cv2.line(legend_visualisation, point_1, point_2, colour,
                     thickness=legend_visualisation_line_thickness)

            cv2.putText(legend_visualisation, entry,
                        text_point, text_font, 1, text_colour)

        # create a filename
        start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
        filename_to_use = "legend" +\
            "__ts_" + str(start_time_formatted) +\
            ".png"
        filename_to_use = os.path.join("outputNoGit", filename_to_use)

        cv2.imwrite(filename_to_use, legend_visualisation)

        not_found = "not found =============================="
        provenance_visualisation_stripe_width = 3
        provenance_visualisation_stripe_white_space_width = 0
        provenance_visualisation_width = provenance_visualisation_stripe_white_space_width + (len(
            self.provenance)) * (provenance_visualisation_stripe_width + provenance_visualisation_stripe_white_space_width)
        provenance_visualisation_width = max(
            provenance_visualisation_width, 2000)

        # if we have a short provevance ans so using the default width,
        # use a sensible strip witdth to fill up the image
        provenance_visualisation_stripe_width = max(provenance_visualisation_stripe_width, int(provenance_visualisation_width / (len(
            self.provenance))))

        provenance_visualisation_height = 200
        provenance_visualisation_title_height = legend_visualisation_line_space * 2
        channels = 3
        provenance_visualisation = np.zeros((
            provenance_visualisation_height + provenance_visualisation_title_height, provenance_visualisation_width, channels), dtype=np.uint8) + 255

        stripes_only = provenance_visualisation[provenance_visualisation_title_height:, :, :]

        # add the title to the white bar above the stripes
        text_point = (legend_visualisation_line_space,
                      int(1.2 * legend_visualisation_line_space))
        title_text_scale_factor = 2.5
        cv2.putText(provenance_visualisation, "Ancestry: " + self.name,
                    text_point, text_font, title_text_scale_factor, text_colour)

        # fill in the duplex spindly font
        # bit of a pain but it looks bad if you don't
        for channel_index in range(3):
            channel = provenance_visualisation[:, :, channel_index]
            channel[:] = cv2.erode(channel, None, iterations=1)

        # loop round all the evolutiuonary events and create the
        # vertical stripe in the image to reflect that
        for iteraration_index, event in enumerate(self.provenance):

            # find the correct entry in the legend table for this
            # evolution event
            match = legend.get(
                event, not_found)

            # if it wasn't there, then it must be one of the
            # ones containing some additional data
            if match == not_found:
                match = legend.get(event[:len("Leaked from")], not_found)

            starts_at = iteraration_index * (provenance_visualisation_stripe_width +
                                             provenance_visualisation_stripe_white_space_width) + provenance_visualisation_stripe_white_space_width
            stripes_only[:, starts_at:starts_at +
                         provenance_visualisation_stripe_width] = match["colour"]["bgr"]

        # create a filename
        start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
        filename_to_use = "ancestry" +\
            "__ts_" + str(start_time_formatted) +\
            ".png"
        filename_to_use = os.path.join("outputNoGit", filename_to_use)

        cv2.imwrite(filename_to_use, provenance_visualisation)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def mutate_route(self, number_of_city_pairs_to_swap, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "mutate_route"
            print("Starting", function_name)

        # Randomly swaps n pairs of cities in a copy of the
        # route and returns that copy to the caller
        # It's like procreation but with only one parent

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
        copy_of_route.calculate_distance(debug=debug)

        # update provenace to show it's come from a mutation
        copy_of_route.provenance.append("Mutation")

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        return copy_of_route

    def get_procreation_insertions(self, proportion_of_route_to_use, debug=False):

        # works on the father for procreation
        # takes the proportion_of_route_to_use and
        # randomly identifies half that many starting cities
        # then finds the next city to that
        # then chains any pairs that are touching or overlapping
        # returns three lists:
        #   an array of the chain starting cities
        #   an array of the chained cities to insert
        #   an array of all the cities contained anywhere in a chain

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "get_procreation_insertions"
            print("Starting", function_name)

        # calculate how many insertions there will be
        # let's have a minimum of 2
        number_of_insertions = max(2,  int(0.5 *
                                           proportion_of_route_to_use * self.number_of_cities))

        # create a np array of the cities to be used from the father
        # it contains an array of the 1st cities in the sequence of two
        # cities from the fathers sequence to be inserted
        # into the mother's sequence
        insertions = np.random.choice(
            self.number_of_cities, number_of_insertions, replace=False)

        # get the indices of values in the fathers route that are in the insertions
        indices_of_insertions_from_father_1st = np.isin(
            self.route, insertions)

        # if the last element is true, set it false as it can't
        # be the 1st element of a pair
        if indices_of_insertions_from_father_1st[-1] == True:
            indices_of_insertions_from_father_1st[-1] = False

        # create a copy of shifted indices by using roll
        indices_of_insertions_from_father_2nd = np.roll(
            indices_of_insertions_from_father_1st, 1)

        # now add the shifted and unshifted together to give me a map of all
        # the elements in the fathers that are to be replaces
        indices_of_insertions_from_father = indices_of_insertions_from_father_1st + \
            indices_of_insertions_from_father_2nd

        insertion_labels = scipy.ndimage.label(
            indices_of_insertions_from_father)[0]

        insertion_slices = scipy.ndimage.find_objects(insertion_labels)

        procreation_insertions = []
        procreation_insertion_firsts = []

        for insertion_slice in insertion_slices:
            insertion = self.route[insertion_slice].tolist()
            procreation_insertions.append(insertion)

            first = insertion[0]
            procreation_insertion_firsts.append(first)

        try:
            procreation_inserted_cities = np.hstack(
                procreation_insertions).tolist()
        except:
            you_can_break_here = True

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        return procreation_insertions, procreation_insertion_firsts, procreation_inserted_cities

    def procreate_route(self, partner, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "procreate_route"
            print("Starting", function_name)

        # Takes segments from the self route and inserts them into
        # a copy of the partner route

        # The one with the lowest fitness is the father
        if self.fitness > partner.fitness:
            mother = self
            father = partner
        else:
            mother = partner
            father = self

        # 1/3rd of the time, reverse the mother
        # to create more diversity
        reverser_decider_mother = np.random.rand()
        if reverser_decider_mother > 0.6666:

            # and do a deep copy before the reverse so we don't
            # alter the gene pool
            mother = copy.deepcopy(mother)

            # set the provenance
            provenance = "Child Mother Reversed"

            mother.route[1:] = (mother.route[1:])[::-1]
        else:  # the mother is not reversed
            # if the mother wasn't reversed,
            # 1/3rd the time reverse the father
            reverser_decider_father = np.random.rand()
            if reverser_decider_father > 0.6666:

                # and do a deep copy before the reverse so we don't
                # alter the gene pool
                father = copy.deepcopy(father)

                # set the provenance
                provenance = "Child Father Reversed"

            else:  # 1/3rd of the time, neither parent is reversed

                # set the provenance
                provenance = "Child"

                father.route[1:] = (mother.route[1:])[::-1]

        # Choose how much of each parent to take based on
        # fitness of each.
        fathers_contribution_to_route = father.fitness / \
            (father.fitness + mother.fitness)

        # an details of all the insertions
        procreation_insertions, procreation_insertion_firsts, procreation_inserted_cities = father.get_procreation_insertions(
            fathers_contribution_to_route)

        # so take a copy
        child = copy.deepcopy(mother)

        # get the indices of values in the mothers route that are in the insertions
        # these must not be transferred over from the mother
        indices_of_insertions_from_mother = np.isin(
            mother.route, procreation_inserted_cities)

        # an array to hold the offspring route
        new_route = []

        for route_index in range(self.number_of_cities):

            try:
                element_to_be_replaced = mother.route[route_index]
            except:
                you_can_break_here = True

            # see if this element in the mothers route is to be replaced
            # correct but needs to have truth for both elements, not just first
            if indices_of_insertions_from_mother[route_index] == True:

                # only transfer from the fathers route if it's the first
                # one of the pair
                if element_to_be_replaced in procreation_insertion_firsts:

                    # get the index of this insertion
                    index_of_insertion = procreation_insertion_firsts.index(
                        element_to_be_replaced)

                    # now append the cities in the insertion to the new route
                    new_route = new_route + \
                        procreation_insertions[index_of_insertion]

            else:
                # it's not part of the insertions so copy it over
                new_route.append(element_to_be_replaced)

        # now replace the route in the child
        child.route = np.asarray(new_route)

        # now recalculate the distance for that child route
        child.calculate_distance(debug=debug)

        # update provenace to show it's come from a mutation
        child.provenance.append(provenance)

        # allow break if it's not correct length
        if child.route.shape[0] != self.number_of_cities:
            you_can_break_here = True

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        return child


def run_tests(debug=False):

    if debug:
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

    # create  a name
    name = "test route"

    # create the routes
    number_of_routes = 20
    routes = []
    for _ in range(number_of_routes):

        route = Route(cities, name)
        routes.append(route)

    if 24.729611 == round(routes[0].distance, 6):
        print("Test for route distance  - passed")
        return_code = 0
    else:
        print("Test for route distance - failed")
        return_code = 4

    # test route mutation
    # 300 should leave it 0,2,1 which is swapped
    mutated_route = route.mutate_route(300, debug=debug)

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
    number_of_cities = 20
    number_of_axis = 2  # for generating the coordinates
    shape = (number_of_cities, number_of_axis)
    cities = np.random.choice(grid_size, shape)

    father = Route(cities, name)
    mother = Route(cities, name)
    father.fitness = 0.34
    mother.fitness = 0.66
    proportion_of_route_to_use = father.fitness / \
        (father.fitness + mother.fitness)

    # temporary over ride
    proportion_of_route_to_use = 0.9

    procreation_insertions, procreation_insertion_firsts, procreation_inserted_cities = father.get_procreation_insertions(
        proportion_of_route_to_use)

    child = father.procreate_route(mother)

    # test the visualisation of the route
    child.visualise_provenance()

    # timer because it's a long process!!
    if debug:
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

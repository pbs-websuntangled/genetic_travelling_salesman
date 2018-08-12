from imutils.video import VideoStream
import matplotlib.pyplot as plt
import matplotlib
import cv2
import os
import numpy as np
import time
import copy
from utils import calculate_rout_distance
from utils import plt_to_numpy_array
from Route import Route


class Route_collection:

    def __init__(self, name, number_of_cities, number_of_routes, number_of_super_iterations, number_of_iterations, super_iteration_number=0, number_of_route_pools=1, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "__init__" + "Route_collection"
            print("Starting", function_name)

        # save the start time
        self.start_time_formatted = time.strftime("%Y%m%d-%H%M%S")
        self.start_time = time.time()

        # set the video parameters
        self.create_video_parameters()

        # save the name
        self.name = name

        # save the number of cities
        self.number_of_cities = number_of_cities

        # save the number of routes
        self.number_of_routes = number_of_routes

        # save the number of route_pools
        self.number_of_route_pools = number_of_route_pools

        # save the number of super_iterations
        self.number_of_super_iterations = number_of_super_iterations

        # save the number of iterations
        self.number_of_iterations = number_of_iterations
        self.super_iteration_number = super_iteration_number

        # how big is my country
        self.country_size = number_of_cities * number_of_cities

        # create a home for all the plot images that are np arrays
        # they will be used to save out as pictures or write to a video file
        self.plots = []

        # create a slot for the standard deviations of the routes at each iteration
        # used for creating a measure of the route population diversity
        self.standard_deviations = []
        self.diversity = []

        # create a holder to show progress of distance
        self.distances = []

        # generate the cities with random co-ordinates
        self.create_cities(debug=debug)

        # generate the initial pool of random routes
        self.create_routes(debug=debug)

        # reset the seed
        np.random.seed()

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def create_cities(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "create_cities"
            print("Starting", function_name)

        # create the cities
        number_of_axis = 2  # for generating the coordinates
        shape = (self.number_of_cities, number_of_axis)
        self.cities = np.random.choice(self.country_size, shape)

        # create a plot of all the cities with no routes
        self.plot_cities(debug=debug)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def create_video_parameters(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "create_video_parameters"
            print("Starting", function_name)

        # create the parameters
        self.video_parameters = {}
        self.video_parameters["shape"] = (1080, 1920)
        self.video_parameters["fourcc"] = cv2.VideoWriter_fourcc(*"MJPG")
        self.video_parameters["frames_per_second"] = 20

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def set_cities(self, cities):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "set_cities"
            print("Starting", function_name)

        # create the cities
        self.cities = cities

        # and now recreate the routes because they contain
        # a copy of the cities
        self.create_routes(debug=debug)

        # create a plot of all the cities with no routes
        self.plot_cities(debug=debug)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def evolve_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "evolve_routes"
            print("Starting", function_name)

        # set the number of iterations between plotting reults
        number_of_plots = 50
        number_of_iterations_between_plots_required = int(
            max(1, self.number_of_iterations * self.number_of_super_iterations / number_of_plots))

        # iterate the evolution process
        for self.iteration in range(self.number_of_iterations):

            # evaluate this set of routes
            self.evaluate_routes(debug=debug)

            # have I finished?
            if self.range_of_distances == 0:
                break

            # kill the weakest routes
            number_killed = self.kill_weakest_routes(debug=debug)
            self.number_survived = self.number_of_routes - number_killed

            # do procreation
            self.number_of_children = 0
            do_this = True
            if do_this == True:
                self.procreate_routes(debug=debug)

            # mutate the routes to make up the numbers required for the
            # proper population
            self.mutate_routes(debug=debug)

            # if it's time to plot the progress, then do it
            if self.iteration % number_of_iterations_between_plots_required == 0:
                self.plot_progress(debug=debug)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def evaluate_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "evaluate_routes"
            print("Starting", function_name)

        # sort the routes as the distances have already been calculated
        self.routes.sort(key=lambda x: x.distance, reverse=False)

        # save the best distance
        self.distances.append(self.routes[0].distance)

        # range of distances
        try:
            self.range_of_distances = self.routes[-1].distance - \
                self.routes[0].distance
        except:
            you_can_break_here = True

        # create a measure of diversity
        # Quick and dirty is a function of the median, min and max routes
        # diversity = max(max_route - med_route, med_route - min_route) / (max_route - min_route)
        # or...
        # diversity = 1 - min(max_route - med_route, med_route - min_route) / max(max_route - med_route, med_route - min_route)
        # so if they are mostly clustered up one end diversity is lower
        # use low diversity to drive more deaths, more radical procreation and more (and more radical) mutations
        index_of_median = int(self.number_of_cities)
        delta_top = self.routes[index_of_median].distance - \
            self.routes[0].distance
        delta_bottom = self.routes[-1].distance - \
            self.routes[index_of_median].distance
        self.diversity.append(min(delta_top, delta_bottom) /
                              max(delta_top, delta_bottom))

        if self.range_of_distances != 0:

            # store the ranking
            position = 0
            for route in self.routes:

                # save the position
                route.position = position

                # save the fitness (bigger is better)
                # the best route has a fitnes of 1
                # other routes are less
                route.fitness = 1 - (route.distance -
                                     self.routes[0].distance) / self.range_of_distances

                # try alternate route fitness
                # as the position of the shortest route is 0,
                # the fitness of that route will be 1
                # This ensures it will survive
                route.fitness = 1 - position / self.number_of_routes

                # increment the position
                position = position + 1

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def kill_weakest_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "kill_weakest_routes"
            print("Starting", function_name)

        # Generates a random amount of danger for each route
        # If the danger is higher than the fitness, the route will die
        # generate the set of random dangers in one hit
        # This function gives a higher proportion of higher dangers
        # More of the fit ones will die
        # More will die overall
        # this function kills about 75% of the routes
        dangers = 1 - np.random.rand(self.number_of_routes) * \
            np.random.rand(self.number_of_routes)

        diversity_checks = np.random.rand(self.number_of_routes)

        # now check fitness against the dangers
        # kill if it's less
        # by not copying it over to new list
        new_routes = []
        distances_to_check_for_diversity = []
        for route_index, route in enumerate(self.routes):

            # is it fit enough?
            danger = dangers[route_index]
            if danger <= route.fitness:

                # increase the diversity by refusing multiple copies of the same route
                if self.routes[route_index].distance not in distances_to_check_for_diversity:

                    # this route survives!!
                    new_routes.append(self.routes[route_index])

                    # add this distance to diversity checking store of distances
                    distances_to_check_for_diversity.append(
                        self.routes[route_index].distance)

                    # update the provenenace
                    new_routes[-1].provenance.append("Survivor")

        # have I destroyed all the routes!!
        # it really should be impossible as the fittest route
        # has a health of 1
        if len(new_routes) == 0:
            you_can_break_here = True

        # replace the routes
        self.routes = new_routes

        # how many did I kill?
        number_of_routes_killed = self.number_of_routes - len(new_routes)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        return number_of_routes_killed

    def mutate_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "mutate_routes"
            print("Starting", function_name)

        # creates new routes that are mutations of the existing routes
        # a single mutation is achieved by swapping a pair of randomly chosen cites
        # first it choses how many pairs to swap in that route
        # the lower the fitness, the more mutations will be created
        # within that one journey

        # what's the maximum number of mutations per route
        maximum_mutations_per_route = max(2, int(1 * self.number_of_cities))
        minimum_mutatations_per_route = 1

        # generate the random route indices to mutate to get to the correct number of routes
        # using only the routes that survived
        self.number_of_mutations = self.number_of_routes - \
            self.number_survived - self.number_of_children
        indices_to_mutate = np.random.choice(
            self.number_survived, self.number_of_mutations)
        possible_number_of_mutations_for_this_route = range(
            minimum_mutatations_per_route, maximum_mutations_per_route)

        for route_index in indices_to_mutate:

            route = self.routes[route_index]

            # first let's choose an amount of mutations
            # there will be a minimum and a maximum
            number_of_mutations = np.random.choice(
                possible_number_of_mutations_for_this_route)

            # create a copy and put it onto the  end of the list
            if len(self.routes) < self.number_of_routes:

                # put a copy of this one on the end
                self.routes.append(route.mutate_route(
                    number_of_mutations, debug=False))

            else:

                # I already have the amount of routes that I want so get out
                return

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

        # and out of here
        return

    def procreate_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "procreate_routes"
            print("Starting", function_name)

        # create offspring
        #
        # how many children required?
        self.number_of_children = int((self.number_of_routes -
                                       self.number_survived) / 2) - 1

        # randomly choose parents from the fittest survivors
        parents = np.random.choice(
            self.number_survived, self.number_of_children * 2)

        for child_index in range(self.number_of_children):
            parent_1 = self.routes[parents[child_index * 2]]
            parent_2 = self.routes[parents[child_index * 2 + 1]]

            # now create the child and add it to the routes
            child_route = parent_1.procreate_route(parent_2)
            self.routes.append(child_route)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def create_routes(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "create_routes"
            print("Starting", function_name)

        # create the routes
        routes = []
        for route_index in range(self.number_of_routes):

            route = np.random.choice(
                self.number_of_cities, self.number_of_cities, replace=False)

            # generate a name
            name = self.name + " number: " + str(route_index)
            route = Route(self.cities, name)

            # tell it where it came from
            routes.append(route)

        # and save them
        self.routes = routes

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def write_provenance(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "write_provenance"
            print("Starting", function_name)

        # create a filename
        filename_to_use = "__name_" + self.name + \
            "__cities_" + str(self.number_of_cities) +\
            "__routes_" + str(self.number_of_routes) +\
            "__superIterations_" + str(self.number_of_super_iterations) +\
            "__iterations_" + str(self.number_of_iterations) +\
            "__distance_" + str(int(self.routes[0].distance)) +\
            "__type_provenance" +\
            "__ts_" + str(self.start_time_formatted) +\
            ".txt"
        filename_to_use = os.path.join("outputNoGit", filename_to_use)

        # write out the provenance
        # do a comma seperated list
        with open(filename_to_use, 'a') as the_file:
            the_file.write(",".join(self.routes[0].provenance))

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def create_video(self, plots, unique_name, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "create_video"
            print("Starting", function_name)

        # create a filename
        filename_to_use = "__name_" + self.name +\
            "__cities_" + str(self.number_of_cities) +\
            "__routes_" + str(self.number_of_routes) +\
            "__superIterations_" + str(self.number_of_super_iterations) +\
            "__iterations_" + str(self.number_of_iterations) +\
            "__distance_" + str(int(self.routes[0].distance)) +\
            "__uniqueName" + unique_name +\
            "__type_video" +\
            "__ts_" + str(self.start_time_formatted) +\
            ".avi"

        filename_to_use = os.path.join("outputNoGit", filename_to_use)

        # initialize the FourCC, video writer, dimensions of the frame, and
        writer = None
        frame = plots[0]  # for sizing some artefacts

        # check if the writer is None
        if writer is None:
            # store the image dimensions, initialzie the video writer,
            # and construct the zeros array
            (h, w) = frame.shape[:2]
            writer = cv2.VideoWriter(filename_to_use, self.video_parameters["fourcc"], self.video_parameters["frames_per_second"],
                                     (w, h), True)
            zeros = np.zeros((h, w), dtype="uint8")

        # write the plots to the video file
        fade_seconds = 1
        fade_factor = self.video_parameters["frames_per_second"] * fade_seconds

        for plot_index, plot in enumerate(plots):

            if plot_index == 0:

                # fade the first one in from white
                (h, w) = plot.shape[:2]
                white = np.zeros((h, w, 3), dtype="uint8") + 255

                # just show white first
                for factor in range(2 * fade_factor):
                    faded = white * (factor / (2 * fade_factor))
                    writer.write(faded.astype(np.uint8))

                # then fade in the first plot
                # create a fade
                for factor in range(fade_factor):
                    faded = plot * (factor/fade_factor) + \
                        white * (1 - factor / fade_factor)
                    writer.write(faded.astype(np.uint8))

                # then hold the first plot for viewers to take it in
                for _ in range(3 * fade_factor):
                    writer.write(faded.astype(np.uint8))

                continue

            # say what the previous one was so I can fade it out
            plot_previous = plots[plot_index - 1]

            # create a fade
            for factor in range(fade_factor):
                faded = plot * (factor/fade_factor) + \
                    plot_previous * (1 - factor / fade_factor)
                writer.write(faded.astype(np.uint8))

            # now the full
            plot = plot.astype(np.uint8)
            for _ in range(fade_factor):
                writer.write(plot)

        writer.release()

        you_can_break_here = True

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def plot_progress(self, save_images=False, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "plot_progress"
            print("Starting", function_name)

        # Spits out a graph of the progress and the current best route
        # horizontally stacked
        # So that a gif or animation of the development pf the route can be built

        # check how fast I am going by including the
        # iterations per minute
        iterations_per_minute = int(
            self.iteration / ((time.time() - self.start_time) / 60))

        # create the x and y coordinates of the cities
        # for plotting the current best route
        x = []
        y = []
        for city_index in self.routes[0].route:
            x.append(self.cities[city_index][0])
            y.append(self.cities[city_index][1])

        # calculate the plot scale factor by working out
        # how many genepools to stack on top of each other
        # and how tall they can be to fit in the video height
        video_height = self.video_parameters["shape"][0]

        # get the standard plot height
        # get a reference to the current fgure
        standard_plot_height = plt.gcf().bbox.height

        # get the scale factor needed to fit the plots on top of each other
        # but do't scale them up
        scale_factor = self.number_of_super_iterations * \
            standard_plot_height / video_height
        scale_factor = min(1, scale_factor)

        # start a figure
        plt.figure()

        # plot the cities on the chart
        home_city = self.routes[0].route[0]
        last_city = self.routes[0].route[-1]

        # Mark the home and final city on the map
        plt.scatter(x[0], y[0], c="red", s=500)
        plt.scatter(x[-1], y[-1], c="green", s=150)

        # Mark all the intermediate cities on the map
        plt.scatter(x[1:-1],  y[1:-1], c="blue", s=100)

        # mark the route on the map
        plt.plot(x, y, color='k', linestyle='-', linewidth=2)

        # And a title
        plt.title(str(self.number_of_cities) + " City locations and best route so far\n (distance: " +
                  str(int(self.distances[-1])) + ")")

        # nice and clean
        plt.axis('off')

        # save the file
        if (self.iteration == self.number_of_iterations) or (self.iteration == 0):
            filename_to_use = "test"
            filename_to_use = "__name_" + self.name +\
                "__cities_" + str(self.number_of_cities) +\
                "__routes_" + str(self.number_of_routes) + \
                "__superIterations_" + str(self.number_of_super_iterations) +\
                "__iterations_" + str(self.number_of_iterations) +\
                "__distance_" + str(int(self.routes[0].distance)) +\
                "__ipm_" + str(int(iterations_per_minute)) +\
                "__type_keyStage" +\
                "__superIteration_" + str(self.super_iteration_number) +\
                "__iteration_" + str(self.iteration) +\
                "__ts_" + str(self.start_time_formatted)
            plt.savefig(os.path.join('outputNoGit',
                                     filename_to_use + ".png"))

        # turn the figure into a numpy array
        route_figure_as_array = plt_to_numpy_array(plt, scale_factor)

        # finish that one
        plt.close('all')

        # start a new figure
        plt.figure()

        plt.title(self.name)

        # set the axes
        axes = plt.gca()
        x_minimum = 0
        x_maximum = self.number_of_iterations * self.number_of_super_iterations - 1
        y_minimum = 0
        y_maximum = self.distances[0] * 1.1
        axes.set_xlim([x_minimum, x_maximum])
        axes.set_ylim([y_minimum, y_maximum])

        plt.xlabel("Generations")
        plt.ylabel("Route Distance")

        # plot the progress
        plt.plot(self.distances, color='k',
                 linestyle='-', linewidth=2)

        # plot the vertical lines at route leakage points
        for iteration_index in range(self.number_of_iterations, self.number_of_super_iterations * self.number_of_iterations, self.number_of_iterations):

            # only go as far as the itrations already done
            if iteration_index >= len(self.distances):
                break

            plot_this_x = (iteration_index - 0.00001,
                           iteration_index)
            try:
                plot_this_y = (
                    0, self.distances[iteration_index] + 0.02 * self.distances[0])
            except:
                you_can_break_here = True

            plt.plot(plot_this_x, plot_this_y, c="orange")

            plt.annotate('Route \npool \nLeakage', xy=(
                0.5, 0.5), xytext=(iteration_index, 0.025 * self.distances[0] + self.distances[iteration_index]))

        # put a colourful dot on the beginning of the line
        plt.scatter(0, self.distances[-1], c="green", s=200)

        # put a colourful dot at the bottom axis at where we are
        plt.scatter(len(self.distances), 0, c="green", s=200)

        # turn the figure into a numpy array
        progress_figure_as_array = plt_to_numpy_array(plt, scale_factor)

        # put them side by side
        plot_to_save = np.hstack(
            (progress_figure_as_array, route_figure_as_array))

        # save to disk if we need to
        save_images = True
        if save_images == True:
            # save the stacked image
            filename_to_use = "__name_" + self.name +\
                "__cities_" + str(self.number_of_cities) +\
                "__routes_" + str(self.number_of_routes) + \
                "__superIterations_" + str(self.number_of_super_iterations) +\
                "__iterations_" + str(self.number_of_iterations) +\
                "__distance_" + str(int(self.routes[0].distance)) +\
                "__ipm_" + str(int(iterations_per_minute)) +\
                "__type_combined" +\
                "__superIteration_" + str(self.super_iteration_number) +\
                "__iteration_" + str(self.iteration) +\
                "__ts_" + str(self.start_time_formatted)
            cv2.imwrite(os.path.join(
                "plots", filename_to_use + ".png"), plot_to_save)

        # clear out the plot
        plt.close('all')

        # now save a copy of the plot array
        self.plots.append(plot_to_save)

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def plot_cities(self, debug=False, plot_route=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "plot_cities"
            print("Starting", function_name)

        # Spits out a plot of just the cities with no routes on

        # create the x and y coordinates of thecities
        # for plotting the current best route
        x = []
        y = []
        for city in self.cities:
            x.append(city[0])
            y.append(city[1])

        # start a figure
        plt.figure()

        plt.xlabel('Any unit of distance you like')
        plt.ylabel('Any unit of distance you like')

        # plot the cities on the chart
        home_city = self.cities[0]

        # put the home city on with a bigger red dot
        plt.scatter(home_city[0], home_city[1], c="red", s=500)

        # put the rest of the cities on
        plt.scatter(x[1:],  y[1:], c="blue", s=100)

        # add the title
        plt.title(str(self.number_of_cities) + " City locations")

        if plot_route:

            # nice and clean
            plt.axis('off')

            # mark the route on the map
            plt.plot(x, y, color='k', linestyle='-', linewidth=2)

            # Create a meaningful filename
            filename_to_use = "__name_" + self.name +\
                "__cities_" + str(self.number_of_cities) +\
                "__routes_" + str(self.number_of_routes) + \
                "__superIterations_" + str(self.number_of_super_iterations) +\
                "__iterations_" + str(self.number_of_iterations) +\
                "__type_route" +\
                "__ts_" + str(self.start_time_formatted)

        else:

            # Create a meaningful filename
            filename_to_use = "__name_" + self.name +\
                "__cities_" + str(self.number_of_cities) +\
                "__routes_" + str(self.number_of_routes) + \
                "__superIterations_" + str(self.number_of_super_iterations) +\
                "__iterations_" + str(self.number_of_iterations) +\
                "__type_cities" +\
                "__ts_" + str(self.start_time_formatted)

        # save the file
        plt.savefig(os.path.join('outputNoGit',
                                 filename_to_use + ".png"))

        # finish that one
        plt.close('all')

        # timer because it's a long process!!
        if debug:
            print("Leaving",
                  function_name,
                  "and the process took",
                  time.time() - start_time)

    def plot_diversity(self, debug=False):

        if debug:
            # start a timer because it's a long process!!
            start_time, function_name = time.time(), "plot_diversity"
            print("Starting", function_name)

        # Spits out a plot of the diversity

        # create the x and y coordinates of thecities
        # for plotting the current best route
        x = []
        y = []
        for city in self.cities:
            x.append(city[0])
            y.append(city[1])

        # start a figure
        plt.figure()

        # set the axes
        axes = plt.gca()
        x_minimum = 0
        x_maximum = self.number_of_iterations * self.number_of_super_iterations - 1
        y_minimum = 0
        y_maximum = 1.05
        axes.set_xlim([x_minimum, x_maximum])
        axes.set_ylim([y_minimum, y_maximum])

        # plot it
        plt.plot(self.diversity)

        # plot the vertical lines at route leakage points
        for iteration_index in range(self.number_of_iterations, self.number_of_super_iterations * self.number_of_iterations, self.number_of_iterations):
            plot_this_x = (iteration_index - 0.00001,
                           iteration_index)
            plot_this_y = (0, 0.02 + self.diversity[iteration_index])
            plt.plot(plot_this_x, plot_this_y, c="orange")

            plt.annotate('Route \npool \nLeakage', xy=(
                0.5, 0.5), xytext=(iteration_index, 0.025 + self.diversity[iteration_index]))

        # add the title
        plt.title("Diversity of routes in:" + self.name)
        plt.xlabel('Iterations of evolutionary cycle')
        plt.ylabel('Diversity')

        # Create a meaningful filename
        filename_to_use = "__name_" + self.name +\
            "__cities_" + str(self.number_of_cities) +\
            "__routes_" + str(self.number_of_routes) + \
            "__superIterations_" + str(self.number_of_super_iterations) +\
            "__iterations_" + str(self.number_of_iterations) +\
            "__type_diversity" +\
            "__ts_" + str(self.start_time_formatted)

        # save the file
        plt.savefig(os.path.join('outputNoGit',
                                 filename_to_use + ".png"))

        # finish that one
        plt.close('all')

        # timer because it's a long process!!
        if debug:
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
    number_of_cities = 70

    # 400 took 142 seconds
    # 200 took 90  seconds
    number_of_routes = 2000

    # 25 cities needs 90 iterations

    number_of_route_pools = 4
    number_of_super_iterations = 12
    number_of_iterations = 100

    # print out the key variables
    print("number_of_cities =", number_of_cities)
    print("number_of_routes =", number_of_routes)
    print("number_of_super_iterations =", number_of_super_iterations)
    print("number_of_route_pools =", number_of_route_pools)
    print("number_of_iterations =", number_of_iterations)
    #=====================================================================================#
    # first create all the gene pools with the cloned cities in all of them
    route_pools = []
    for route_pool_index in range(number_of_route_pools):

        # generate the name
        name = "route_pool_" + str(route_pool_index)

        # create the route collection
        route_collection = Route_collection(name,
                                            number_of_cities, number_of_routes, number_of_super_iterations, number_of_iterations, debug=debug)

        # copy the cities from the 1st route collection
        # and populate all the routes with thise cities
        if route_pool_index > 0:
            route_collection.set_cities(route_pools[0].cities)

        # now add it to the list
        route_pools.append(route_collection)

        # creata a possible break point
        you_can_break_here = True

    # holder for lowest route found so far
    # it's ok to use any of the routes found so far
    lowest_route_found_so_far = route_pools[0].routes[0].distance

    for super_iteration_index in range(number_of_super_iterations):

        # give a status update
        print("Starting super iteration", super_iteration_index + 1, "of",
              number_of_super_iterations, "at", time.strftime("%Y%m%d-%H%M%S"))

        for route_pool_index in range(number_of_route_pools):

            # give a status update
            print("    Starting route_pool", route_pool_index + 1, "of",
                  number_of_route_pools, "at", time.strftime("%Y%m%d-%H%M%S"))

            # pull the route collection out of the gene pool
            route_collection = route_pools[route_pool_index]

            # now set th esuper_iteration_number
            route_collection.super_iteration_number = super_iteration_index

            # now evolve the routes to find a good one
            route_collection.evolve_routes(debug=debug)

            # get the shortest route found
            lowest_route_found_so_far = min(
                lowest_route_found_so_far, route_collection.distances[-1])

        # right now we've been round all the gene pools, leak
        # the genes of the best routes to all the gene pools
        for route_pool_recipient_index in range(number_of_route_pools):

            # set up the recipient
            recipient = route_pools[route_pool_recipient_index]

            # now round the donors
            for route_pool_donor_index in range(number_of_route_pools):

                # don't donate to yourself
                if route_pool_donor_index == route_pool_recipient_index:
                    continue

                # set up the donor
                donor = route_pools[route_pool_donor_index]

                # now inject onto the end of the recipient gene pool
                recipient.routes[-1 -
                                 route_pool_donor_index] = copy.deepcopy(donor.routes[0])

                # update the provenance to show it's leaked
                recipient.routes[-1 -
                                 route_pool_donor_index].provenance.append("Leaked from " + donor.name)

                print("Leaking and number of iterations is:",
                      len(donor.distances))

        # give a status update
        print("    Ending super iteration, shortest route so far:",
              int(lowest_route_found_so_far))

    # We've done all the super iterations so make the videos
    for route_pool_index in range(number_of_route_pools):

        # set up this route_pool
        route_pool = route_pools[route_pool_index]

        # now save the provenance
        route_pool.write_provenance(debug=debug)

        # now visualise the provenance
        route_pool.routes[0].visualise_provenance()

        # plot the diversity
        route_pool.plot_diversity(debug=debug)

        # plot the final best route
        route_pool.plot_cities(plot_route=True)

        # now make the video
        unique_name = "allSuperIterations"
        route_pool.create_video(route_pool.plots, unique_name, debug=debug)

    # and now make a video stacking all the gene pools on top of each other
    # all the gene pools have the same number of plots
    all_stacked_plots = []

    # loop round the plots and then for each one, get the appropriate one for each gene pool
    number_of_plots = len(route_pools[0].plots)
    for plot_index in range(number_of_plots):

        for route_pool_index in range(number_of_route_pools):

            # we already have the 1st one stacked
            if route_pool_index == 0:
                stacked_plots = route_pools[0].plots[plot_index]

            else:
                stacked_plots = np.vstack((
                    stacked_plots, route_pools[route_pool_index].plots[plot_index]))

        # now append the stacked plots to all the stacked plots
        all_stacked_plots.append(stacked_plots)

    # now we have all the stacked plots, make a video of that
    # now make the video
    unique_name = "allGenePoolsStacked"
    route_pools[0].create_video(all_stacked_plots, unique_name, debug=debug)

    print("Leaving",
          function_name,
          "and the process took",
          time.time() - start_time)

    return return_code


if __name__ == '__main__':

    debug = False

    # just make sure that the random numbers generate
    # consistently for testing purposes
    np.random.seed(1)

    # do the run_tests
    return_code = run_tests(debug=debug)

    # final return code
    print("return_code", return_code)
